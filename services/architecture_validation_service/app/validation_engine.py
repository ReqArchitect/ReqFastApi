import logging
import time
import httpx
from typing import List, Dict, Any, Optional, Set
from datetime import datetime, timedelta
from app.schemas import (
    ValidationContext, ValidationResult, ValidationIssueCreate, 
    ArchitectureElement, TracePath, IssueType, Severity
)
from app.models import ValidationRule, ValidationException
from sqlalchemy.orm import Session
import json
import redis
import os

logger = logging.getLogger(__name__)

class ValidationEngine:
    """Core validation engine for architecture model validation"""
    
    def __init__(self, db: Session, redis_client: redis.Redis):
        self.db = db
        self.redis = redis_client
        self.microservice_urls = {
            "goal": "http://goal_service:8080",
            "capability": "http://capability_service:8080",
            "business_function": "http://business_function_service:8080",
            "business_process": "http://business_process_service:8080",
            "business_role": "http://business_role_service:8080",
            "application_function": "http://application_function_service:8080",
            "application_service": "http://applicationservice_service:8080",
            "requirement": "http://requirement_service:8080",
            "constraint": "http://constraint_service:8080",
            "driver": "http://driver_service:8080",
            "assessment": "http://assessment_service:8080",
            "workpackage": "http://workpackage_service:8080",
            "gap": "http://gap_service:8080",
            "plateau": "http://plateau_service:8080"
        }
    
    async def run_validation_cycle(self, context: ValidationContext) -> List[ValidationResult]:
        """Run a complete validation cycle for a tenant"""
        logger.info(f"Starting validation cycle {context.validation_cycle_id} for tenant {context.tenant_id}")
        
        start_time = time.time()
        results = []
        
        try:
            # Get active validation rules
            rules = self.db.query(ValidationRule).filter(ValidationRule.is_active == True).all()
            
            # Get active exceptions for this tenant
            exceptions = self.db.query(ValidationException).filter(
                ValidationException.tenant_id == context.tenant_id,
                ValidationException.is_active == True
            ).all()
            
            # Create exception lookup
            exception_lookup = {(ex.entity_type, ex.entity_id, ex.rule_id) for ex in exceptions}
            
            # Run each rule
            for rule in rules:
                try:
                    result = await self._execute_rule(rule, context, exception_lookup)
                    results.append(result)
                except Exception as e:
                    logger.error(f"Error executing rule {rule.name}: {e}")
                    results.append(ValidationResult(
                        rule_id=rule.id,
                        rule_name=rule.name,
                        passed=False,
                        issues_found=[],
                        execution_time_ms=0,
                        metadata={"error": str(e)}
                    ))
            
            # Calculate overall metrics
            total_issues = sum(len(result.issues_found) for result in results)
            execution_time = (time.time() - start_time) * 1000
            
            logger.info(f"Validation cycle completed: {len(results)} rules, {total_issues} issues, {execution_time:.2f}ms")
            
            # Emit Redis event
            self._emit_validation_completed_event(context, total_issues, execution_time)
            
            return results
            
        except Exception as e:
            logger.error(f"Validation cycle failed: {e}")
            raise
    
    async def _execute_rule(self, rule: ValidationRule, context: ValidationContext, exceptions: Set) -> ValidationResult:
        """Execute a single validation rule"""
        start_time = time.time()
        issues = []
        
        try:
            if rule.rule_type == "traceability":
                issues = await self._validate_traceability(rule, context, exceptions)
            elif rule.rule_type == "completeness":
                issues = await self._validate_completeness(rule, context, exceptions)
            elif rule.rule_type == "alignment":
                issues = await self._validate_alignment(rule, context, exceptions)
            else:
                logger.warning(f"Unknown rule type: {rule.rule_type}")
        
        except Exception as e:
            logger.error(f"Error executing rule {rule.name}: {e}")
            issues = [ValidationIssueCreate(
                tenant_id=context.tenant_id,
                entity_type="system",
                entity_id="validation_engine",
                issue_type=IssueType.BROKEN_TRACEABILITY,
                severity=Severity.HIGH,
                description=f"Rule execution failed: {str(e)}",
                recommended_fix="Check rule configuration and service connectivity"
            )]
        
        execution_time = (time.time() - start_time) * 1000
        
        return ValidationResult(
            rule_id=rule.id,
            rule_name=rule.name,
            passed=len(issues) == 0,
            issues_found=issues,
            execution_time_ms=execution_time
        )
    
    async def _validate_traceability(self, rule: ValidationRule, context: ValidationContext, exceptions: Set) -> List[ValidationIssueCreate]:
        """Validate traceability paths between elements"""
        issues = []
        
        try:
            # Parse rule logic (JSON format)
            rule_config = json.loads(rule.rule_logic)
            source_type = rule_config.get("source_type")
            target_type = rule_config.get("target_type")
            relationship_type = rule_config.get("relationship_type")
            min_connections = rule_config.get("min_connections", 1)
            
            # Get elements from source and target services
            source_elements = await self._get_elements(source_type, context.tenant_id)
            target_elements = await self._get_elements(target_type, context.tenant_id)
            
            # Check traceability paths
            for source_element in source_elements:
                connections = await self._find_connections(
                    source_element["id"], 
                    target_type, 
                    relationship_type, 
                    context.tenant_id
                )
                
                if len(connections) < min_connections:
                    # Check if this is an exception
                    exception_key = (source_type, source_element["id"], rule.id)
                    if exception_key not in exceptions:
                        issues.append(ValidationIssueCreate(
                            tenant_id=context.tenant_id,
                            entity_type=source_type,
                            entity_id=source_element["id"],
                            issue_type=IssueType.MISSING_LINK,
                            severity=Severity(rule.severity),
                            description=f"{source_element['name']} ({source_type}) has insufficient connections to {target_type}",
                            recommended_fix=f"Create {relationship_type} relationship to at least {min_connections} {target_type} element(s)",
                            metadata={
                                "source_element": source_element,
                                "expected_connections": min_connections,
                                "actual_connections": len(connections),
                                "relationship_type": relationship_type
                            }
                        ))
        
        except Exception as e:
            logger.error(f"Error in traceability validation: {e}")
            issues.append(ValidationIssueCreate(
                tenant_id=context.tenant_id,
                entity_type="system",
                entity_id="validation_engine",
                issue_type=IssueType.BROKEN_TRACEABILITY,
                severity=Severity.HIGH,
                description=f"Traceability validation failed: {str(e)}",
                recommended_fix="Check service connectivity and rule configuration"
            ))
        
        return issues
    
    async def _validate_completeness(self, rule: ValidationRule, context: ValidationContext, exceptions: Set) -> List[ValidationIssueCreate]:
        """Validate completeness of architecture elements"""
        issues = []
        
        try:
            rule_config = json.loads(rule.rule_logic)
            element_type = rule_config.get("element_type")
            required_fields = rule_config.get("required_fields", [])
            min_count = rule_config.get("min_count", 1)
            
            # Get elements of the specified type
            elements = await self._get_elements(element_type, context.tenant_id)
            
            # Check minimum count
            if len(elements) < min_count:
                issues.append(ValidationIssueCreate(
                    tenant_id=context.tenant_id,
                    entity_type=element_type,
                    entity_id="count_check",
                    issue_type=IssueType.MISSING_LINK,
                    severity=Severity(rule.severity),
                    description=f"Insufficient {element_type} elements: {len(elements)} found, {min_count} required",
                    recommended_fix=f"Create at least {min_count} {element_type} element(s)",
                    metadata={
                        "actual_count": len(elements),
                        "required_count": min_count,
                        "element_type": element_type
                    }
                ))
            
            # Check required fields for each element
            for element in elements:
                missing_fields = []
                for field in required_fields:
                    if field not in element or not element[field]:
                        missing_fields.append(field)
                
                if missing_fields:
                    issues.append(ValidationIssueCreate(
                        tenant_id=context.tenant_id,
                        entity_type=element_type,
                        entity_id=element["id"],
                        issue_type=IssueType.INVALID_ENUM,
                        severity=Severity(rule.severity),
                        description=f"{element.get('name', 'Unknown')} ({element_type}) missing required fields: {', '.join(missing_fields)}",
                        recommended_fix=f"Complete the missing fields: {', '.join(missing_fields)}",
                        metadata={
                            "element": element,
                            "missing_fields": missing_fields,
                            "required_fields": required_fields
                        }
                    ))
        
        except Exception as e:
            logger.error(f"Error in completeness validation: {e}")
            issues.append(ValidationIssueCreate(
                tenant_id=context.tenant_id,
                entity_type="system",
                entity_id="validation_engine",
                issue_type=IssueType.BROKEN_TRACEABILITY,
                severity=Severity.HIGH,
                description=f"Completeness validation failed: {str(e)}",
                recommended_fix="Check service connectivity and rule configuration"
            ))
        
        return issues
    
    async def _validate_alignment(self, rule: ValidationRule, context: ValidationContext, exceptions: Set) -> List[ValidationIssueCreate]:
        """Validate alignment between different layers"""
        issues = []
        
        try:
            rule_config = json.loads(rule.rule_logic)
            source_layer = rule_config.get("source_layer")
            target_layer = rule_config.get("target_layer")
            alignment_criteria = rule_config.get("alignment_criteria", {})
            
            # Get elements from both layers
            source_elements = await self._get_elements_by_layer(source_layer, context.tenant_id)
            target_elements = await self._get_elements_by_layer(target_layer, context.tenant_id)
            
            # Check alignment based on criteria
            for source_element in source_elements:
                aligned_elements = await self._find_aligned_elements(
                    source_element, target_elements, alignment_criteria, context.tenant_id
                )
                
                if not aligned_elements:
                    issues.append(ValidationIssueCreate(
                        tenant_id=context.tenant_id,
                        entity_type=source_element.get("type", "unknown"),
                        entity_id=source_element["id"],
                        issue_type=IssueType.BROKEN_TRACEABILITY,
                        severity=Severity(rule.severity),
                        description=f"{source_element.get('name', 'Unknown')} ({source_layer}) lacks alignment with {target_layer}",
                        recommended_fix=f"Create alignment relationships with {target_layer} elements",
                        metadata={
                            "source_element": source_element,
                            "source_layer": source_layer,
                            "target_layer": target_layer,
                            "alignment_criteria": alignment_criteria
                        }
                    ))
        
        except Exception as e:
            logger.error(f"Error in alignment validation: {e}")
            issues.append(ValidationIssueCreate(
                tenant_id=context.tenant_id,
                entity_type="system",
                entity_id="validation_engine",
                issue_type=IssueType.BROKEN_TRACEABILITY,
                severity=Severity.HIGH,
                description=f"Alignment validation failed: {str(e)}",
                recommended_fix="Check service connectivity and rule configuration"
            ))
        
        return issues
    
    async def _get_elements(self, element_type: str, tenant_id: str) -> List[Dict[str, Any]]:
        """Get elements of a specific type from the appropriate service"""
        if element_type not in self.microservice_urls:
            logger.warning(f"No service URL found for element type: {element_type}")
            return []
        
        try:
            url = f"{self.microservice_urls[element_type]}/{element_type}"
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url, headers={"X-Tenant-ID": tenant_id})
                if response.status_code == 200:
                    return response.json()
                else:
                    logger.error(f"Failed to get {element_type} elements: {response.status_code}")
                    return []
        except Exception as e:
            logger.error(f"Error getting {element_type} elements: {e}")
            return []
    
    async def _get_elements_by_layer(self, layer: str, tenant_id: str) -> List[Dict[str, Any]]:
        """Get elements by layer across all services"""
        layer_mapping = {
            "Motivation": ["goal", "driver", "constraint", "requirement"],
            "Business": ["business_function", "business_process", "business_role"],
            "Application": ["application_function", "application_service"],
            "Technology": ["node", "device", "systemsoftware"],
            "Implementation": ["workpackage", "gap", "plateau"]
        }
        
        all_elements = []
        element_types = layer_mapping.get(layer, [])
        
        for element_type in element_types:
            elements = await self._get_elements(element_type, tenant_id)
            for element in elements:
                element["layer"] = layer
                element["type"] = element_type
            all_elements.extend(elements)
        
        return all_elements
    
    async def _find_connections(self, source_id: str, target_type: str, relationship_type: str, tenant_id: str) -> List[Dict[str, Any]]:
        """Find connections from a source element to target elements"""
        connections = []
        
        # This would typically query the relationship/link services
        # For now, we'll simulate by checking if the target service has any elements
        target_elements = await self._get_elements(target_type, tenant_id)
        
        # In a real implementation, you would query the relationship service
        # to find actual connections between elements
        for element in target_elements:
            # Simulate connection check
            connections.append({
                "target_id": element["id"],
                "target_name": element.get("name", "Unknown"),
                "relationship_type": relationship_type
            })
        
        return connections
    
    async def _find_aligned_elements(self, source_element: Dict[str, Any], target_elements: List[Dict[str, Any]], 
                                   criteria: Dict[str, Any], tenant_id: str) -> List[Dict[str, Any]]:
        """Find elements aligned with the source element based on criteria"""
        aligned = []
        
        # Simple alignment check based on name similarity or other criteria
        source_name = source_element.get("name", "").lower()
        
        for target_element in target_elements:
            target_name = target_element.get("name", "").lower()
            
            # Check for name similarity or other alignment criteria
            if source_name in target_name or target_name in source_name:
                aligned.append(target_element)
        
        return aligned
    
    def _emit_validation_completed_event(self, context: ValidationContext, total_issues: int, execution_time: float):
        """Emit Redis event for validation completion"""
        try:
            event_data = {
                "validation_cycle_id": context.validation_cycle_id,
                "tenant_id": context.tenant_id,
                "user_id": context.user_id,
                "total_issues": total_issues,
                "execution_time_ms": execution_time,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            self.redis.publish("validation.completed", json.dumps(event_data))
            logger.info(f"Emitted validation.completed event for cycle {context.validation_cycle_id}")
            
        except Exception as e:
            logger.error(f"Failed to emit validation.completed event: {e}")
    
    def _emit_issue_detected_event(self, issue: ValidationIssueCreate):
        """Emit Redis event for issue detection"""
        try:
            event_data = {
                "issue_id": str(issue.entity_id),  # Will be replaced with actual issue ID
                "tenant_id": issue.tenant_id,
                "entity_type": issue.entity_type,
                "entity_id": issue.entity_id,
                "issue_type": issue.issue_type.value,
                "severity": issue.severity.value,
                "description": issue.description,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            self.redis.publish("validation.issue_detected", json.dumps(event_data))
            logger.info(f"Emitted validation.issue_detected event for {issue.entity_type}:{issue.entity_id}")
            
        except Exception as e:
            logger.error(f"Failed to emit validation.issue_detected event: {e}") 