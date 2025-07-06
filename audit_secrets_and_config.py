#!/usr/bin/env python3
"""
Secrets and Configuration Audit Script
Audits .env files for security issues and validates configuration hygiene
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Any
import hashlib
import secrets

class SecretsAuditor:
    """Audit secrets and configuration for security issues"""
    
    def __init__(self):
        self.project_root = Path(".")
        self.issues = []
        self.warnings = []
        self.recommendations = []
        
        # Common sensitive patterns
        self.sensitive_patterns = [
            r'password\s*=\s*["\']?[^"\'\s]+["\']?',
            r'secret\s*=\s*["\']?[^"\'\s]+["\']?',
            r'key\s*=\s*["\']?[^"\'\s]+["\']?',
            r'token\s*=\s*["\']?[^"\'\s]+["\']?',
            r'api_key\s*=\s*["\']?[^"\'\s]+["\']?',
            r'private_key\s*=\s*["\']?[^"\'\s]+["\']?',
            r'jwt_secret\s*=\s*["\']?[^"\'\s]+["\']?',
            r'secret_key\s*=\s*["\']?[^"\'\s]+["\']?',
        ]
        
        # Default/placeholder values
        self.default_values = [
            'your-super-secret-jwt-key-change-this-in-production',
            'your-super-secret-key-change-this-in-production',
            'your-openai-api-key-here',
            'your-stripe-secret-key',
            'your-stripe-publishable-key',
            'your-email@gmail.com',
            'your-app-password',
            'username',
            'password',
            'localhost',
            '5432',
            'database_name',
            'REPLACE_ME',
            'change-this-in-production'
        ]

    def scan_for_env_files(self) -> List[Path]:
        """Find all .env files in the project"""
        env_files = []
        
        # Look for .env files in project root and service directories
        for env_file in self.project_root.rglob(".env*"):
            if env_file.is_file() and not env_file.name.startswith('.env.example'):
                env_files.append(env_file)
        
        return env_files

    def audit_env_file(self, env_file: Path) -> Dict[str, Any]:
        """Audit a single .env file for security issues"""
        print(f"🔍 Auditing {env_file}...")
        
        audit_result = {
            "file": str(env_file),
            "issues": [],
            "warnings": [],
            "sensitive_vars": [],
            "default_values": [],
            "recommendations": []
        }
        
        try:
            with open(env_file, 'r') as f:
                content = f.read()
                lines = content.split('\n')
            
            for line_num, line in enumerate(lines, 1):
                line = line.strip()
                
                # Skip comments and empty lines
                if line.startswith('#') or not line:
                    continue
                
                # Check for sensitive patterns
                for pattern in self.sensitive_patterns:
                    if re.search(pattern, line, re.IGNORECASE):
                        audit_result["sensitive_vars"].append({
                            "line": line_num,
                            "content": line,
                            "pattern": pattern
                        })
                
                # Check for default/placeholder values
                for default_val in self.default_values:
                    if default_val in line:
                        audit_result["default_values"].append({
                            "line": line_num,
                            "content": line,
                            "default_value": default_val
                        })
                
                # Check for hardcoded credentials
                if '=' in line:
                    key, value = line.split('=', 1)
                    value = value.strip().strip('"\'')
                    
                    # Check for obvious credentials
                    if any(cred in key.lower() for cred in ['password', 'secret', 'key', 'token']):
                        if value and value not in self.default_values:
                            audit_result["warnings"].append({
                                "line": line_num,
                                "message": f"Potential hardcoded credential: {key}",
                                "content": line
                            })
        
        except Exception as e:
            audit_result["issues"].append(f"Error reading file: {e}")
        
        return audit_result

    def validate_env_example(self) -> Dict[str, Any]:
        """Validate env.example against best practices"""
        print("📋 Validating env.example...")
        
        validation_result = {
            "file": "env.example",
            "issues": [],
            "warnings": [],
            "recommendations": []
        }
        
        env_example = self.project_root / "env.example"
        
        if not env_example.exists():
            validation_result["issues"].append("env.example file not found")
            return validation_result
        
        try:
            with open(env_example, 'r') as f:
                content = f.read()
            
            # Check for proper documentation
            if not content.startswith('#'):
                validation_result["warnings"].append("env.example should start with documentation")
            
            # Check for required sections
            required_sections = [
                "COMMON CONFIGURATION",
                "PRODUCTION OVERRIDES"
            ]
            
            for section in required_sections:
                if section not in content:
                    validation_result["recommendations"].append(f"Add {section} section")
            
            # Check for proper placeholder values
            if "your-super-secret-jwt-key-change-this-in-production" not in content:
                validation_result["warnings"].append("JWT secret placeholder not found")
            
            # Check for environment-specific configurations
            if "ENVIRONMENT=" not in content:
                validation_result["recommendations"].append("Add ENVIRONMENT variable")
            
            if "DEBUG=" not in content:
                validation_result["recommendations"].append("Add DEBUG variable")
        
        except Exception as e:
            validation_result["issues"].append(f"Error reading env.example: {e}")
        
        return validation_result

    def generate_secure_secrets(self) -> Dict[str, str]:
        """Generate secure secrets for production use"""
        print("🔐 Generating secure secrets...")
        
        secrets_dict = {
            "JWT_SECRET": secrets.token_urlsafe(64),
            "SECRET_KEY": secrets.token_urlsafe(64),
            "DATABASE_PASSWORD": secrets.token_urlsafe(32),
            "REDIS_PASSWORD": secrets.token_urlsafe(32),
            "STRIPE_SECRET_KEY": "sk_test_" + secrets.token_hex(24),
            "OPENAI_API_KEY": "sk-" + secrets.token_hex(48),
            "SMTP_PASSWORD": secrets.token_urlsafe(24)
        }
        
        return secrets_dict

    def create_vault_integration_example(self) -> str:
        """Create example Vault integration configuration"""
        vault_config = """
# HashiCorp Vault Integration Example
# Add this to your deployment configuration

apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
type: Opaque
data:
  JWT_SECRET: <base64-encoded-jwt-secret>
  SECRET_KEY: <base64-encoded-secret-key>
  DATABASE_PASSWORD: <base64-encoded-db-password>
  REDIS_PASSWORD: <base64-encoded-redis-password>
  STRIPE_SECRET_KEY: <base64-encoded-stripe-key>
  OPENAI_API_KEY: <base64-encoded-openai-key>
  SMTP_PASSWORD: <base64-encoded-smtp-password>
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-deployment
spec:
  template:
    spec:
      containers:
      - name: app
        envFrom:
        - secretRef:
            name: app-secrets
        env:
        - name: DATABASE_URL
          value: "postgresql://user:$(DATABASE_PASSWORD)@db:5432/app"
        - name: REDIS_URL
          value: "redis://:$(REDIS_PASSWORD)@redis:6379/0"
"""
        return vault_config

    def create_helm_secrets_example(self) -> str:
        """Create example Helm secrets configuration"""
        helm_config = """
# Helm Secrets Example
# Create a values-secrets.yaml file (add to .gitignore)

secrets:
  jwt_secret: "your-super-secret-jwt-key-change-this-in-production"
  secret_key: "your-super-secret-key-change-this-in-production"
  database_password: "your-database-password"
  redis_password: "your-redis-password"
  stripe_secret_key: "your-stripe-secret-key"
  openai_api_key: "your-openai-api-key"
  smtp_password: "your-smtp-password"

# In your deployment template:
env:
- name: JWT_SECRET
  valueFrom:
    secretKeyRef:
      name: {{ .Release.Name }}-secrets
      key: jwt_secret
- name: SECRET_KEY
  valueFrom:
    secretKeyRef:
      name: {{ .Release.Name }}-secrets
      key: secret_key
"""
        return helm_config

    def run_complete_audit(self) -> Dict[str, Any]:
        """Run complete secrets and configuration audit"""
        print("🔍 Starting Secrets and Configuration Audit")
        print("=" * 60)
        
        audit_results = {
            "env_files": [],
            "env_example_validation": {},
            "secure_secrets": {},
            "vault_integration": "",
            "helm_secrets": "",
            "summary": {
                "total_issues": 0,
                "total_warnings": 0,
                "total_recommendations": 0
            }
        }
        
        # Scan for .env files
        env_files = self.scan_for_env_files()
        print(f"📁 Found {len(env_files)} .env files")
        
        # Audit each .env file
        for env_file in env_files:
            audit_result = self.audit_env_file(env_file)
            audit_results["env_files"].append(audit_result)
            
            audit_results["summary"]["total_issues"] += len(audit_result["issues"])
            audit_results["summary"]["total_warnings"] += len(audit_result["warnings"])
            audit_results["summary"]["total_recommendations"] += len(audit_result["recommendations"])
        
        # Validate env.example
        audit_results["env_example_validation"] = self.validate_env_example()
        
        # Generate secure secrets
        audit_results["secure_secrets"] = self.generate_secure_secrets()
        
        # Create integration examples
        audit_results["vault_integration"] = self.create_vault_integration_example()
        audit_results["helm_secrets"] = self.create_helm_secrets_example()
        
        # Print summary
        self.print_audit_summary(audit_results)
        
        return audit_results

    def print_audit_summary(self, results: Dict[str, Any]):
        """Print audit summary"""
        print("\n" + "=" * 60)
        print("📊 AUDIT SUMMARY")
        print("=" * 60)
        
        summary = results["summary"]
        print(f"🔍 Total Issues: {summary['total_issues']}")
        print(f"⚠️  Total Warnings: {summary['total_warnings']}")
        print(f"💡 Total Recommendations: {summary['total_recommendations']}")
        
        # Print issues by file
        for env_audit in results["env_files"]:
            if env_audit["issues"] or env_audit["warnings"]:
                print(f"\n📄 {env_audit['file']}:")
                
                for issue in env_audit["issues"]:
                    print(f"  ❌ {issue}")
                
                for warning in env_audit["warnings"]:
                    print(f"  ⚠️  {warning}")
                
                for rec in env_audit["recommendations"]:
                    print(f"  💡 {rec}")
        
        # Print recommendations
        if summary["total_issues"] > 0:
            print("\n🚨 CRITICAL: Fix security issues before production deployment!")
        
        if summary["total_warnings"] > 0:
            print("\n⚠️  WARNING: Review warnings for potential security issues")
        
        print("\n🔐 SECURE SECRETS GENERATED:")
        for key, value in results["secure_secrets"].items():
            print(f"  {key}: {value[:20]}...")
        
        print("\n📋 Next Steps:")
        print("1. Replace default/placeholder values with secure secrets")
        print("2. Implement Vault or Kubernetes secrets management")
        print("3. Remove any hardcoded credentials from .env files")
        print("4. Use environment-specific configurations")
        print("5. Implement secret rotation policies")

def main():
    """Main function to run the audit"""
    auditor = SecretsAuditor()
    results = auditor.run_complete_audit()
    
    # Save results to file
    with open("secrets_audit_results.json", "w") as f:
        json.dump(results, f, indent=2, default=str)
    
    # Save secure secrets to file (for reference)
    with open("secure_secrets_example.env", "w") as f:
        f.write("# Secure Secrets Example - DO NOT USE IN PRODUCTION\n")
        f.write("# These are examples of properly formatted secrets\n\n")
        for key, value in results["secure_secrets"].items():
            f.write(f"{key}={value}\n")
    
    # Save Vault integration example
    with open("vault_integration_example.yaml", "w") as f:
        f.write(results["vault_integration"])
    
    # Save Helm secrets example
    with open("helm_secrets_example.yaml", "w") as f:
        f.write(results["helm_secrets"])
    
    print(f"\n📄 Audit results saved to:")
    print("  - secrets_audit_results.json")
    print("  - secure_secrets_example.env")
    print("  - vault_integration_example.yaml")
    print("  - helm_secrets_example.yaml")
    
    return results

if __name__ == "__main__":
    main() 