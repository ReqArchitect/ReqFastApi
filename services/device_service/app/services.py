from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, asc
from typing import List, Optional, Dict, Any
import json
import logging
import redis
from datetime import datetime, timedelta
import uuid

from .models import Device, DeviceLink
from .schemas import DeviceCreate, DeviceUpdate, DeviceLinkCreate, DeviceLinkUpdate
from .config import settings

logger = logging.getLogger(__name__)

class DeviceService:
    def __init__(self, db: Session, redis_client: redis.Redis):
        self.db = db
        self.redis = redis_client

    def create_device(self, device_data: DeviceCreate, tenant_id: str, user_id: str) -> Device:
        """Create a new device."""
        try:
            device = Device(
                tenant_id=tenant_id,
                user_id=user_id,
                **device_data.dict()
            )
            self.db.add(device)
            self.db.commit()
            self.db.refresh(device)
            
            # Emit Redis event
            self._emit_device_event("device.created", device)
            
            logger.info(f"Device created: {device.id}")
            return device
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating device: {e}")
            raise

    def get_device(self, device_id: str, tenant_id: str) -> Optional[Device]:
        """Get device by ID."""
        return self.db.query(Device).filter(
            and_(Device.id == device_id, Device.tenant_id == tenant_id)
        ).first()

    def list_devices(
        self, 
        tenant_id: str, 
        skip: int = 0, 
        limit: int = 100,
        device_type: Optional[str] = None,
        location: Optional[str] = None,
        lifecycle_state: Optional[str] = None,
        manufacturer: Optional[str] = None,
        status: Optional[str] = None,
        compliance_status: Optional[str] = None
    ) -> List[Device]:
        """List devices with filtering."""
        query = self.db.query(Device).filter(Device.tenant_id == tenant_id)
        
        if device_type:
            query = query.filter(Device.device_type == device_type)
        if location:
            query = query.filter(Device.location.contains(location))
        if lifecycle_state:
            query = query.filter(Device.lifecycle_state == lifecycle_state)
        if manufacturer:
            query = query.filter(Device.manufacturer.contains(manufacturer))
        if status:
            query = query.filter(Device.status == status)
        if compliance_status:
            query = query.filter(Device.compliance_status == compliance_status)
        
        return query.offset(skip).limit(limit).all()

    def update_device(self, device_id: str, device_data: DeviceUpdate, tenant_id: str) -> Optional[Device]:
        """Update device."""
        try:
            device = self.get_device(device_id, tenant_id)
            if not device:
                return None
            
            update_data = device_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(device, field, value)
            
            device.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(device)
            
            # Emit Redis event
            self._emit_device_event("device.updated", device)
            
            logger.info(f"Device updated: {device_id}")
            return device
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating device: {e}")
            raise

    def delete_device(self, device_id: str, tenant_id: str) -> bool:
        """Delete device."""
        try:
            device = self.get_device(device_id, tenant_id)
            if not device:
                return False
            
            # Delete associated links first
            self.db.query(DeviceLink).filter(DeviceLink.device_id == device_id).delete()
            
            self.db.delete(device)
            self.db.commit()
            
            # Emit Redis event
            self._emit_device_event("device.deleted", device)
            
            logger.info(f"Device deleted: {device_id}")
            return True
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error deleting device: {e}")
            raise

    def get_device_by_serial(self, serial_number: str, tenant_id: str) -> Optional[Device]:
        """Get device by serial number."""
        return self.db.query(Device).filter(
            and_(Device.serial_number == serial_number, Device.tenant_id == tenant_id)
        ).first()

    def get_device_by_asset_tag(self, asset_tag: str, tenant_id: str) -> Optional[Device]:
        """Get device by asset tag."""
        return self.db.query(Device).filter(
            and_(Device.asset_tag == asset_tag, Device.tenant_id == tenant_id)
        ).first()

    def get_devices_by_type(self, device_type: str, tenant_id: str) -> List[Device]:
        """Get devices by type."""
        return self.db.query(Device).filter(
            and_(Device.device_type == device_type, Device.tenant_id == tenant_id)
        ).all()

    def get_devices_by_location(self, location: str, tenant_id: str) -> List[Device]:
        """Get devices by location."""
        return self.db.query(Device).filter(
            and_(Device.location.contains(location), Device.tenant_id == tenant_id)
        ).all()

    def get_devices_by_manufacturer(self, manufacturer: str, tenant_id: str) -> List[Device]:
        """Get devices by manufacturer."""
        return self.db.query(Device).filter(
            and_(Device.manufacturer.contains(manufacturer), Device.tenant_id == tenant_id)
        ).all()

    def get_active_devices(self, tenant_id: str) -> List[Device]:
        """Get active devices."""
        return self.db.query(Device).filter(
            and_(Device.status == "active", Device.tenant_id == tenant_id)
        ).all()

    def get_critical_devices(self, tenant_id: str) -> List[Device]:
        """Get critical devices."""
        return self.db.query(Device).filter(
            and_(
                Device.security_level == "critical",
                Device.tenant_id == tenant_id
            )
        ).all()

    def get_devices_needing_maintenance(self, tenant_id: str) -> List[Device]:
        """Get devices needing maintenance."""
        today = datetime.utcnow()
        return self.db.query(Device).filter(
            and_(
                Device.next_maintenance <= today,
                Device.tenant_id == tenant_id
            )
        ).all()

    def get_devices_by_compliance_status(self, compliance_status: str, tenant_id: str) -> List[Device]:
        """Get devices by compliance status."""
        return self.db.query(Device).filter(
            and_(Device.compliance_status == compliance_status, Device.tenant_id == tenant_id)
        ).all()

    def get_deployment_map(self, device_id: str, tenant_id: str) -> Dict[str, Any]:
        """Get deployment map for device."""
        device = self.get_device(device_id, tenant_id)
        if not device:
            return {}
        
        # Get linked elements
        links = self.db.query(DeviceLink).filter(DeviceLink.device_id == device_id).all()
        
        deployment_nodes = []
        supported_software = []
        communication_paths = []
        artifacts = []
        
        for link in links:
            if link.linked_element_type == "node":
                deployment_nodes.append({
                    "id": link.linked_element_id,
                    "link_type": link.link_type,
                    "relationship_strength": link.relationship_strength,
                    "dependency_level": link.dependency_level
                })
            elif link.linked_element_type == "system_software":
                supported_software.append({
                    "id": link.linked_element_id,
                    "link_type": link.link_type,
                    "implementation_status": link.implementation_status,
                    "deployment_status": link.deployment_status
                })
            elif link.linked_element_type == "communication_path":
                communication_paths.append({
                    "id": link.linked_element_id,
                    "link_type": link.link_type,
                    "connection_status": link.connection_status,
                    "performance_impact": link.performance_impact
                })
            elif link.linked_element_type == "artifact":
                artifacts.append({
                    "id": link.linked_element_id,
                    "link_type": link.link_type,
                    "deployment_status": link.deployment_status
                })
        
        # Calculate deployment score
        deployment_score = self._calculate_deployment_score(device, links)
        
        # Generate recommendations
        recommendations = self._generate_deployment_recommendations(device, links)
        
        return {
            "device_id": device.id,
            "device_name": device.name,
            "device_type": device.device_type,
            "deployment_nodes": deployment_nodes,
            "supported_software": supported_software,
            "communication_paths": communication_paths,
            "artifacts": artifacts,
            "deployment_score": deployment_score,
            "recommendations": recommendations
        }

    def get_compliance_status(self, device_id: str, tenant_id: str) -> Dict[str, Any]:
        """Get compliance status for device."""
        device = self.get_device(device_id, tenant_id)
        if not device:
            return {}
        
        # Calculate compliance score
        compliance_score = self._calculate_compliance_score(device)
        
        # Get compliance items
        compliance_items = self._get_compliance_items(device)
        non_compliant_items = self._get_non_compliant_items(device)
        
        # Generate recommendations
        recommendations = self._generate_compliance_recommendations(device, compliance_items, non_compliant_items)
        
        return {
            "device_id": device.id,
            "device_name": device.name,
            "compliance_status": device.compliance_status,
            "compliance_score": compliance_score,
            "compliance_items": compliance_items,
            "non_compliant_items": non_compliant_items,
            "recommendations": recommendations,
            "last_audit_date": device.last_inspection_date,
            "next_audit_date": device.next_inspection_date
        }

    def _calculate_deployment_score(self, device: Device, links: List[DeviceLink]) -> float:
        """Calculate deployment score for device."""
        score = 0.0
        total_weight = 0.0
        
        # Base score from device status
        if device.status == "active":
            score += 0.3
        elif device.status == "maintenance":
            score += 0.2
        else:
            score += 0.1
        
        total_weight += 0.3
        
        # Score from links
        for link in links:
            weight = 0.1
            if link.relationship_strength == "strong":
                weight = 0.2
            elif link.relationship_strength == "weak":
                weight = 0.05
            
            if link.implementation_status == "active":
                score += weight * 1.0
            elif link.implementation_status == "pending":
                score += weight * 0.5
            else:
                score += weight * 0.0
            
            total_weight += weight
        
        return score / total_weight if total_weight > 0 else 0.0

    def _calculate_compliance_score(self, device: Device) -> float:
        """Calculate compliance score for device."""
        score = 0.0
        total_items = 0
        
        # Security compliance
        if device.security_level in ["high", "critical"]:
            score += 1.0
        elif device.security_level == "standard":
            score += 0.7
        else:
            score += 0.3
        total_items += 1
        
        # Encryption compliance
        if device.encryption_enabled:
            score += 1.0
        else:
            score += 0.0
        total_items += 1
        
        # Antivirus compliance
        if device.antivirus_installed:
            score += 1.0
        else:
            score += 0.0
        total_items += 1
        
        # Firewall compliance
        if device.firewall_enabled:
            score += 1.0
        else:
            score += 0.0
        total_items += 1
        
        # Maintenance compliance
        if device.next_maintenance and device.next_maintenance > datetime.utcnow():
            score += 1.0
        else:
            score += 0.0
        total_items += 1
        
        return score / total_items if total_items > 0 else 0.0

    def _get_compliance_items(self, device: Device) -> List[Dict[str, Any]]:
        """Get compliant items for device."""
        items = []
        
        if device.security_level in ["high", "critical"]:
            items.append({"type": "security_level", "status": "compliant", "value": device.security_level})
        
        if device.encryption_enabled:
            items.append({"type": "encryption", "status": "compliant", "value": "enabled"})
        
        if device.antivirus_installed:
            items.append({"type": "antivirus", "status": "compliant", "value": "installed"})
        
        if device.firewall_enabled:
            items.append({"type": "firewall", "status": "compliant", "value": "enabled"})
        
        if device.next_maintenance and device.next_maintenance > datetime.utcnow():
            items.append({"type": "maintenance", "status": "compliant", "value": "scheduled"})
        
        return items

    def _get_non_compliant_items(self, device: Device) -> List[Dict[str, Any]]:
        """Get non-compliant items for device."""
        items = []
        
        if device.security_level not in ["high", "critical"]:
            items.append({"type": "security_level", "status": "non_compliant", "value": device.security_level})
        
        if not device.encryption_enabled:
            items.append({"type": "encryption", "status": "non_compliant", "value": "disabled"})
        
        if not device.antivirus_installed:
            items.append({"type": "antivirus", "status": "non_compliant", "value": "not_installed"})
        
        if not device.firewall_enabled:
            items.append({"type": "firewall", "status": "non_compliant", "value": "disabled"})
        
        if not device.next_maintenance or device.next_maintenance <= datetime.utcnow():
            items.append({"type": "maintenance", "status": "non_compliant", "value": "overdue"})
        
        return items

    def _generate_deployment_recommendations(self, device: Device, links: List[DeviceLink]) -> List[str]:
        """Generate deployment recommendations."""
        recommendations = []
        
        if device.status != "active":
            recommendations.append("Consider activating the device for production use")
        
        if not links:
            recommendations.append("Link the device to supporting nodes and software")
        
        weak_links = [link for link in links if link.relationship_strength == "weak"]
        if weak_links:
            recommendations.append("Strengthen relationships with linked elements")
        
        pending_links = [link for link in links if link.implementation_status == "pending"]
        if pending_links:
            recommendations.append("Complete implementation of pending links")
        
        return recommendations

    def _generate_compliance_recommendations(self, device: Device, compliance_items: List[Dict], non_compliant_items: List[Dict]) -> List[str]:
        """Generate compliance recommendations."""
        recommendations = []
        
        if not device.encryption_enabled:
            recommendations.append("Enable encryption for data protection")
        
        if not device.antivirus_installed:
            recommendations.append("Install and configure antivirus software")
        
        if not device.firewall_enabled:
            recommendations.append("Enable and configure firewall rules")
        
        if device.security_level not in ["high", "critical"]:
            recommendations.append("Upgrade security level to high or critical")
        
        if not device.next_maintenance or device.next_maintenance <= datetime.utcnow():
            recommendations.append("Schedule maintenance and inspection")
        
        return recommendations

    def _emit_device_event(self, event_type: str, device: Device):
        """Emit Redis event for device changes."""
        try:
            event_data = {
                "event_type": event_type,
                "device_id": str(device.id),
                "tenant_id": str(device.tenant_id),
                "user_id": str(device.user_id),
                "device_name": device.name,
                "device_type": device.device_type,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            self.redis.publish("device_events", json.dumps(event_data))
            logger.info(f"Emitted device event: {event_type} for device {device.id}")
        except Exception as e:
            logger.error(f"Error emitting device event: {e}")

class DeviceLinkService:
    def __init__(self, db: Session, redis_client: redis.Redis):
        self.db = db
        self.redis = redis_client

    def create_device_link(self, device_id: str, link_data: DeviceLinkCreate, user_id: str) -> DeviceLink:
        """Create a new device link."""
        try:
            link = DeviceLink(
                device_id=device_id,
                created_by=user_id,
                **link_data.dict()
            )
            self.db.add(link)
            self.db.commit()
            self.db.refresh(link)
            
            # Emit Redis event
            self._emit_link_event("device_link.created", link)
            
            logger.info(f"Device link created: {link.id}")
            return link
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating device link: {e}")
            raise

    def get_device_link(self, link_id: str) -> Optional[DeviceLink]:
        """Get device link by ID."""
        return self.db.query(DeviceLink).filter(DeviceLink.id == link_id).first()

    def list_device_links(self, device_id: str) -> List[DeviceLink]:
        """List links for a device."""
        return self.db.query(DeviceLink).filter(DeviceLink.device_id == device_id).all()

    def update_device_link(self, link_id: str, link_data: DeviceLinkUpdate) -> Optional[DeviceLink]:
        """Update device link."""
        try:
            link = self.get_device_link(link_id)
            if not link:
                return None
            
            update_data = link_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(link, field, value)
            
            self.db.commit()
            self.db.refresh(link)
            
            # Emit Redis event
            self._emit_link_event("device_link.updated", link)
            
            logger.info(f"Device link updated: {link_id}")
            return link
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating device link: {e}")
            raise

    def delete_device_link(self, link_id: str) -> bool:
        """Delete device link."""
        try:
            link = self.get_device_link(link_id)
            if not link:
                return False
            
            self.db.delete(link)
            self.db.commit()
            
            # Emit Redis event
            self._emit_link_event("device_link.deleted", link)
            
            logger.info(f"Device link deleted: {link_id}")
            return True
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error deleting device link: {e}")
            raise

    def get_links_by_type(self, device_id: str, link_type: str) -> List[DeviceLink]:
        """Get device links by type."""
        return self.db.query(DeviceLink).filter(
            and_(DeviceLink.device_id == device_id, DeviceLink.link_type == link_type)
        ).all()

    def get_links_by_element_type(self, device_id: str, element_type: str) -> List[DeviceLink]:
        """Get device links by element type."""
        return self.db.query(DeviceLink).filter(
            and_(DeviceLink.device_id == device_id, DeviceLink.linked_element_type == element_type)
        ).all()

    def _emit_link_event(self, event_type: str, link: DeviceLink):
        """Emit Redis event for link changes."""
        try:
            event_data = {
                "event_type": event_type,
                "link_id": str(link.id),
                "device_id": str(link.device_id),
                "linked_element_id": str(link.linked_element_id),
                "linked_element_type": link.linked_element_type,
                "link_type": link.link_type,
                "created_by": str(link.created_by),
                "timestamp": datetime.utcnow().isoformat()
            }
            
            self.redis.publish("device_link_events", json.dumps(event_data))
            logger.info(f"Emitted device link event: {event_type} for link {link.id}")
        except Exception as e:
            logger.error(f"Error emitting device link event: {e}") 