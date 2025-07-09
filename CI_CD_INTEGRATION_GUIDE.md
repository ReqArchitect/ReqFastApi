# ReqArchitect Validation Framework - CI/CD Integration Guide

This guide provides comprehensive instructions for integrating the validation framework into your CI/CD pipeline with support for GitHub Actions, GitLab CI, and Jenkins.

## 🎯 Overview

The validation framework integrates seamlessly into CI/CD pipelines to:
- Automatically validate all microservices after deployment
- Fail builds on critical service failures (<80% success rate or 500 errors)
- Generate comprehensive reports and artifacts
- Send alerts via Slack/email for failures and regressions
- Support environment-specific configurations

## 📋 Prerequisites

- Docker and Docker Compose installed
- Python 3.8+ with required dependencies
- Access to container registry (if using private images)
- Slack webhook URL (optional, for notifications)
- SMTP credentials (optional, for email alerts)

## 🔧 Environment Variables

### Required for All Platforms

```bash
# JWT Authentication
JWT_SECRET=your-jwt-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# Test Data
TEST_TENANT_ID=test-tenant-123
TEST_USER_ID=test-user-456
TEST_EMAIL=test@example.com
TEST_PASSWORD=testpass123
TEST_ROLE=Admin

# Validation Settings
VALIDATION_RETRY_ATTEMPTS=3
VALIDATION_RETRY_DELAY=2
VALIDATION_TIMEOUT=30
VALIDATION_CHECK_INTERVAL=15
VALIDATION_HISTORY_RETENTION=7

# Environment
VALIDATION_ENV=production
CI_PIPELINE_ID=${CI_PIPELINE_ID}
CI_COMMIT_SHA=${CI_COMMIT_SHA}
CI_BRANCH=${CI_BRANCH}
```

### Optional for Notifications

```bash
# Slack Integration
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL

# Email Integration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
FROM_EMAIL=alerts@yourcompany.com
EMAIL_RECIPIENTS=dev-team@yourcompany.com,ops@yourcompany.com
```

## 🚀 GitHub Actions Integration

### Basic Workflow

```yaml
# .github/workflows/validation.yml
name: ReqArchitect Validation

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '*/15 * * * *'  # Every 15 minutes

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: pip install -r validation_requirements.txt
      
      - name: Start services
        run: |
          docker-compose up -d
          sleep 30
      
      - name: Run validation
        env:
          JWT_SECRET: ${{ secrets.JWT_SECRET }}
          TEST_TENANT_ID: ${{ secrets.TEST_TENANT_ID }}
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
        run: python continuous_validation_framework.py --run-once
      
      - name: Check critical services
        run: python scripts/check_critical_health.py
      
      - name: Generate summary
        run: python scripts/generate_validation_summary.py
      
      - name: Upload artifacts
        uses: actions/upload-artifact@v4
        with:
          name: validation-reports-${{ github.run_number }}
          path: |
            validation_outputs/
            logs/validation/
            validation_summary.md
          retention-days: 30
```

### Advanced Workflow with Parallel Testing

```yaml
# .github/workflows/validation-advanced.yml
name: Advanced Validation

on:
  push:
    branches: [ main, develop ]
  workflow_dispatch:

jobs:
  setup:
    runs-on: ubuntu-latest
    outputs:
      matrix: ${{ steps.set-matrix.outputs.matrix }}
    steps:
      - uses: actions/checkout@v4
      - id: set-matrix
        run: |
          echo "matrix={\"services\":[\"auth_service\",\"gateway_service\",\"ai_modeling_service\"]}" >> $GITHUB_OUTPUT

  validate-services:
    needs: setup
    runs-on: ubuntu-latest
    strategy:
      matrix:
        service: ${{ fromJson(needs.setup.outputs.matrix).services }}
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: pip install -r validation_requirements.txt
      
      - name: Start specific service
        run: |
          docker-compose up -d ${{ matrix.service }}
          sleep 30
      
      - name: Validate service
        env:
          JWT_SECRET: ${{ secrets.JWT_SECRET }}
          VALIDATION_ENV: production
        run: |
          python continuous_validation_framework.py \
            --run-once \
            --config validation_config.json \
            --service ${{ matrix.service }}
      
      - name: Upload service results
        uses: actions/upload-artifact@v4
        with:
          name: ${{ matrix.service }}-validation
          path: validation_outputs/
          retention-days: 7

  aggregate-results:
    needs: [validate-services]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Download all results
        uses: actions/download-artifact@v4
        with:
          path: validation_outputs/
      
      - name: Aggregate and analyze
        run: python scripts/aggregate_results.py
      
      - name: Send notifications
        if: failure()
        run: python scripts/send_email_alert.py
```

## 🔧 GitLab CI Integration

### Basic Pipeline

```yaml
# .gitlab-ci.yml
stages:
  - validate

variables:
  DOCKER_DRIVER: overlay2
  DOCKER_TLS_CERTDIR: "/certs"

validation:
  stage: validate
  image: python:3.11
  services:
    - docker:dind
  before_script:
    - apt-get update && apt-get install -y docker-compose
    - pip install -r validation_requirements.txt
    - mkdir -p logs/validation
  script:
    - docker-compose up -d
    - sleep 30
    - |
      python continuous_validation_framework.py \
        --run-once \
        --config validation_config.json
    - python scripts/check_critical_health.py
    - python scripts/generate_validation_summary.py
  after_script:
    - docker-compose down
  artifacts:
    name: "validation-reports-$CI_PIPELINE_ID"
    paths:
      - validation_outputs/
      - logs/validation/
      - validation_summary.md
    expire_in: 30 days
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == "main"
    - if: $CI_PIPELINE_SOURCE == "schedule"
```

### Advanced Pipeline with Multiple Environments

```yaml
# .gitlab-ci.yml (Advanced)
stages:
  - validate
  - deploy
  - post-deploy-validate

variables:
  DOCKER_DRIVER: overlay2
  DOCKER_TLS_CERTDIR: "/certs"

validation:
  stage: validate
  image: python:3.11
  services:
    - docker:dind
  before_script:
    - apt-get update && apt-get install -y docker-compose
    - pip install -r validation_requirements.txt
  script:
    - docker-compose up -d
    - sleep 30
    - python continuous_validation_framework.py --run-once
    - python scripts/check_critical_health.py
  artifacts:
    paths:
      - validation_outputs/
    expire_in: 1 week
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"

deploy-staging:
  stage: deploy
  image: alpine:latest
  script:
    - echo "Deploying to staging..."
    - sleep 10
  environment:
    name: staging
    url: https://staging.reqarchitect.com
  rules:
    - if: $CI_COMMIT_BRANCH == "develop"

post-deploy-validation:
  stage: post-deploy-validate
  image: python:3.11
  services:
    - docker:dind
  before_script:
    - apt-get update && apt-get install -y docker-compose
    - pip install -r validation_requirements.txt
  script:
    - docker-compose -f docker-compose.staging.yml up -d
    - sleep 30
    - |
      python continuous_validation_framework.py \
        --run-once \
        --config validation_config_staging.json
    - python scripts/check_critical_health.py
  artifacts:
    paths:
      - validation_outputs/
    expire_in: 1 week
  environment:
    name: staging
    url: https://staging.reqarchitect.com
  rules:
    - if: $CI_COMMIT_BRANCH == "develop"
```

## 🔧 Jenkins Integration

### Declarative Pipeline

```groovy
// Jenkinsfile
pipeline {
    agent any
    
    environment {
        PYTHON_VERSION = '3.11'
        DOCKER_COMPOSE_VERSION = '2.20.0'
    }
    
    stages {
        stage('Setup') {
            steps {
                script {
                    sh '''
                        python -m pip install --upgrade pip
                        pip install -r validation_requirements.txt
                    '''
                    sh 'mkdir -p logs/validation'
                }
            }
        }
        
        stage('Start Services') {
            steps {
                script {
                    sh 'docker-compose up -d'
                    sh 'sleep 30'
                    sh 'docker-compose ps'
                }
            }
        }
        
        stage('Run Validation') {
            steps {
                script {
                    sh '''
                        python continuous_validation_framework.py \
                            --run-once \
                            --config validation_config.json
                    '''
                }
            }
        }
        
        stage('Check Critical Services') {
            steps {
                script {
                    sh 'python scripts/check_critical_health.py'
                    
                    env.CRITICAL_SERVICES_HEALTHY = sh(
                        script: 'python scripts/check_critical_health.py; echo $?',
                        returnStdout: true
                    ).trim()
                }
            }
        }
        
        stage('Generate Summary') {
            steps {
                script {
                    sh 'python scripts/generate_validation_summary.py'
                    
                    archiveArtifacts(
                        artifacts: 'validation_outputs/*,logs/validation/*,validation_summary.md',
                        fingerprint: true
                    )
                }
            }
        }
        
        stage('Send Alerts') {
            when {
                anyOf {
                    expression { env.CRITICAL_SERVICES_HEALTHY == '1' }
                    expression { currentBuild.result == 'FAILURE' }
                }
            }
            steps {
                script {
                    sh 'python scripts/send_email_alert.py'
                    
                    if (env.SLACK_WEBHOOK_URL) {
                        slackSend(
                            channel: '#reqarchitect-alerts',
                            color: 'danger',
                            message: "ReqArchitect validation failed in build ${env.BUILD_NUMBER}"
                        )
                    }
                }
            }
        }
        
        stage('Cleanup') {
            always {
                script {
                    sh 'docker-compose down'
                    sh 'docker system prune -f'
                }
            }
        }
    }
    
    post {
        always {
            script {
                publishHTML([
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: 'validation_outputs',
                    reportFiles: 'validation_report_*.html',
                    reportName: 'Validation Report'
                ])
                
                archiveArtifacts(
                    artifacts: 'validation_framework.log',
                    allowEmptyArchive: true
                )
            }
        }
        
        success {
            script {
                if (env.SLACK_WEBHOOK_URL) {
                    slackSend(
                        channel: '#reqarchitect-alerts',
                        color: 'good',
                        message: "ReqArchitect validation passed in build ${env.BUILD_NUMBER}"
                    )
                }
            }
        }
        
        failure {
            script {
                if (env.SLACK_WEBHOOK_URL) {
                    slackSend(
                        channel: '#reqarchitect-alerts',
                        color: 'danger',
                        message: "ReqArchitect validation failed in build ${env.BUILD_NUMBER}"
                    )
                }
            }
        }
    }
}
```

### Scripted Pipeline

```groovy
// Jenkinsfile (Scripted)
node {
    def pythonVersion = '3.11'
    def dockerComposeVersion = '2.20.0'
    
    stage('Setup') {
        sh '''
            python -m pip install --upgrade pip
            pip install -r validation_requirements.txt
            mkdir -p logs/validation
        '''
    }
    
    stage('Start Services') {
        sh '''
            docker-compose up -d
            sleep 30
            docker-compose ps
        '''
    }
    
    stage('Run Validation') {
        sh '''
            python continuous_validation_framework.py \
                --run-once \
                --config validation_config.json
        '''
    }
    
    stage('Check Critical Services') {
        def criticalHealthy = sh(
            script: 'python scripts/check_critical_health.py; echo $?',
            returnStdout: true
        ).trim()
        
        env.CRITICAL_SERVICES_HEALTHY = criticalHealthy
    }
    
    stage('Generate Summary') {
        sh 'python scripts/generate_validation_summary.py'
        
        archiveArtifacts(
            artifacts: 'validation_outputs/*,logs/validation/*,validation_summary.md',
            fingerprint: true
        )
    }
    
    stage('Send Alerts') {
        if (env.CRITICAL_SERVICES_HEALTHY == '1' || currentBuild.result == 'FAILURE') {
            sh 'python scripts/send_email_alert.py'
            
            if (env.SLACK_WEBHOOK_URL) {
                slackSend(
                    channel: '#reqarchitect-alerts',
                    color: 'danger',
                    message: "ReqArchitect validation failed in build ${env.BUILD_NUMBER}"
                )
            }
        }
    }
    
    stage('Cleanup') {
        sh '''
            docker-compose down
            docker system prune -f
        '''
    }
    
    // Post-build actions
    if (currentBuild.result == 'SUCCESS') {
        if (env.SLACK_WEBHOOK_URL) {
            slackSend(
                channel: '#reqarchitect-alerts',
                color: 'good',
                message: "ReqArchitect validation passed in build ${env.BUILD_NUMBER}"
            )
        }
    }
}
```

## 🔧 Local Development Integration

### Docker Compose with Validation

```yaml
# docker-compose.validation.yml
version: '3.8'

services:
  # ... existing services ...
  
  validation-runner:
    image: python:3.11
    volumes:
      - .:/app
      - /var/run/docker.sock:/var/run/docker.sock
    working_dir: /app
    environment:
      - JWT_SECRET=supersecret
      - TEST_TENANT_ID=test-tenant-123
      - VALIDATION_ENV=development
    depends_on:
      - gateway_service
      - auth_service
      - ai_modeling_service
    command: |
      sh -c "
        pip install -r validation_requirements.txt &&
        sleep 30 &&
        python continuous_validation_framework.py --run-once &&
        python scripts/generate_validation_summary.py
      "
```

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "Running ReqArchitect validation..."

# Start services
docker-compose up -d

# Wait for services
sleep 30

# Run validation
python continuous_validation_framework.py --run-once

# Check critical services
python scripts/check_critical_health.py

# Stop services
docker-compose down

echo "Validation complete!"
```

## 📊 Monitoring and Alerting

### Slack Integration

```python
# scripts/slack_alert.py
import os
import requests
import json

def send_slack_alert(message, color="good"):
    webhook_url = os.getenv('SLACK_WEBHOOK_URL')
    if not webhook_url:
        return
    
    payload = {
        "attachments": [
            {
                "color": color,
                "title": "ReqArchitect Validation Alert",
                "text": message,
                "fields": [
                    {
                        "title": "Environment",
                        "value": os.getenv('VALIDATION_ENV', 'unknown'),
                        "short": True
                    },
                    {
                        "title": "Pipeline",
                        "value": os.getenv('CI_PIPELINE_ID', 'local'),
                        "short": True
                    }
                ]
            }
        ]
    }
    
    requests.post(webhook_url, json=payload)
```

### Email Integration

```python
# scripts/email_alert.py
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email_alert(subject, body):
    smtp_server = os.getenv('SMTP_SERVER')
    smtp_port = int(os.getenv('SMTP_PORT', '587'))
    smtp_username = os.getenv('SMTP_USERNAME')
    smtp_password = os.getenv('SMTP_PASSWORD')
    from_email = os.getenv('FROM_EMAIL', smtp_username)
    to_emails = os.getenv('EMAIL_RECIPIENTS', '').split(',')
    
    if not all([smtp_server, smtp_username, smtp_password, to_emails]):
        return
    
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = ', '.join(to_emails)
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_username, smtp_password)
    server.send_message(msg)
    server.quit()
```

## 🔧 Best Practices

### 1. Environment-Specific Configuration

```bash
# Development
VALIDATION_ENV=development
VALIDATION_CHECK_INTERVAL=5
VALIDATION_HISTORY_RETENTION=3

# Staging
VALIDATION_ENV=staging
VALIDATION_CHECK_INTERVAL=10
VALIDATION_HISTORY_RETENTION=7

# Production
VALIDATION_ENV=production
VALIDATION_CHECK_INTERVAL=15
VALIDATION_HISTORY_RETENTION=30
```

### 2. Critical Service Monitoring

```python
# scripts/critical_services.py
CRITICAL_SERVICES = [
    "auth_service",
    "gateway_service", 
    "ai_modeling_service"
]

def check_critical_services():
    for service in CRITICAL_SERVICES:
        health = get_service_health(service)
        if health['success_rate'] < 80.0:
            fail_build(f"Critical service {service} below 80% success rate")
        if health['error_500_count'] > 0:
            fail_build(f"Critical service {service} has 500 errors")
```

### 3. Regression Detection

```python
# scripts/regression_detector.py
def detect_regressions(current_results, baseline_results):
    regressions = []
    
    for service in current_results:
        current_success = current_results[service]['success_rate']
        baseline_success = baseline_results[service]['success_rate']
        
        if current_success < baseline_success - 10:  # 10% threshold
            regressions.append({
                'service': service,
                'current': current_success,
                'baseline': baseline_success,
                'degradation': baseline_success - current_success
            })
    
    return regressions
```

### 4. Artifact Management

```bash
# Clean up old artifacts
find validation_outputs/ -name "validation_*" -mtime +7 -delete
find logs/validation/ -name "*.log" -mtime +30 -delete
```

## 🚨 Troubleshooting

### Common Issues

1. **Services not starting**
   ```bash
   # Check Docker Compose
   docker-compose ps
   docker-compose logs
   
   # Check resource usage
   docker stats
   ```

2. **Validation timeouts**
   ```bash
   # Increase timeout
   export VALIDATION_TIMEOUT=60
   
   # Check service health
   curl -f http://localhost:8080/health
   ```

3. **Authentication failures**
   ```bash
   # Verify JWT configuration
   echo $JWT_SECRET
   echo $JWT_ALGORITHM
   
   # Test token generation
   python -c "import jwt; print(jwt.encode({'test': 'data'}, '$JWT_SECRET', algorithm='HS256'))"
   ```

4. **CI/CD pipeline failures**
   ```bash
   # Check environment variables
   env | grep VALIDATION
   env | grep JWT
   
   # Run validation locally
   python continuous_validation_framework.py --run-once
   ```

### Debug Mode

```bash
# Enable debug logging
export VALIDATION_DEBUG=true
export PYTHONPATH=.

# Run with verbose output
python continuous_validation_framework.py --run-once --verbose
```

## 📈 Metrics and Reporting

### Success Metrics

- **Overall Success Rate**: Target >90%
- **Critical Services**: Target >95%
- **Response Time**: Target <500ms average
- **Error Rate**: Target <5%
- **Uptime**: Target >99.9%

### Failure Thresholds

- **Critical Services**: Fail if <80% success or any 500 errors
- **Non-Critical Services**: Warn if <70% success
- **Response Time**: Warn if >2s average
- **Authentication**: Fail on any 401 errors

### Reporting Schedule

- **Real-time**: Immediate alerts for critical failures
- **Hourly**: Summary reports for non-critical issues
- **Daily**: Comprehensive health reports
- **Weekly**: Trend analysis and recommendations

## 🔄 Continuous Improvement

### Automated Remediation

```python
# scripts/auto_remediation.py
def auto_remediate_service(service_name):
    if service_name == "auth_service":
        restart_auth_service()
        clear_auth_cache()
    elif service_name == "gateway_service":
        restart_gateway_service()
        reload_config()
    elif service_name == "ai_modeling_service":
        restart_ai_service()
        clear_model_cache()
```

### Performance Optimization

```python
# scripts/performance_optimizer.py
def optimize_validation_performance():
    # Parallel validation
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(validate_service, service) 
                  for service in services]
        results = [future.result() for future in futures]
    
    # Caching
    cache_validation_results(results)
    
    # Incremental validation
    validate_only_changed_services()
```

This comprehensive integration guide ensures your validation framework works seamlessly across all major CI/CD platforms while providing robust monitoring, alerting, and reporting capabilities. 