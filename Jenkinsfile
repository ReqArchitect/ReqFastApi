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
                    // Install Python dependencies
                    sh '''
                        python -m pip install --upgrade pip
                        pip install -r validation_requirements.txt
                    '''
                    
                    // Create validation logs directory
                    sh 'mkdir -p logs/validation'
                }
            }
        }
        
        stage('Start Services') {
            steps {
                script {
                    // Start ReqArchitect services
                    sh 'docker-compose up -d'
                    
                    // Wait for services to be ready
                    sh 'sleep 30'
                    
                    // Verify services are running
                    sh 'docker-compose ps'
                }
            }
        }
        
        stage('Run Validation') {
            steps {
                script {
                    // Run validation framework
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
                    // Check critical services health
                    sh 'python scripts/check_critical_health.py'
                    
                    // Store the exit code
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
                    // Generate validation summary
                    sh 'python scripts/generate_validation_summary.py'
                    
                    // Archive validation reports
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
                    // Send email alerts
                    sh 'python scripts/send_email_alert.py'
                    
                    // Send Slack notification
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
                    // Stop services
                    sh 'docker-compose down'
                    
                    // Clean up Docker resources
                    sh 'docker system prune -f'
                }
            }
        }
    }
    
    post {
        always {
            script {
                // Publish validation results
                publishHTML([
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: 'validation_outputs',
                    reportFiles: 'validation_report_*.html',
                    reportName: 'Validation Report'
                ])
                
                // Archive logs
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