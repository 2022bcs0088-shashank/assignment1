pipeline {
    agent any
    environment {
        DOCKER_USER = "2022bcs0088shashank"
        REPO_NAME = "assignment-1"
        BUILD_VER = "${env.BUILD_NUMBER}"
    }
    stages {
        // --- STAGE 1: DEVOPS VERSION ---
        stage('Stage1: Unit Testing') {
            steps {
                script {
                    sh "pip3 install -r stage1-devops/requirements.txt --break-system-packages"
                    sh "export PYTHONPATH=\${WORKSPACE}/stage1-devops && pytest stage1-devops/tests/"
                }
            }
        }
        stage('Stage1: Build & Push (Logic-Based)') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', 'docker-hub-credentials') {
                        def logicApp = docker.build("${DOCKER_USER}/${REPO_NAME}:logicbased-${BUILD_VER}", "-f stage1-devops/Dockerfile stage1-devops/")
                        logicApp.push()
                        logicApp.push("logicbased-latest")
                    }
                }
            }
        }

        // --- STAGE 2: ML VERSION ---
        stage('Stage2: Train & Evaluate ML') {
            steps {
                script {
                    sh "pip3 install -r stage2-ml/requirements.txt --break-system-packages"
                    
                    sh "python3 stage2-ml/app/train.py"
                    
                    def results = readJSON file: 'stage2-ml/app/output/metrics.json'
                    echo "F1-Score: ${results.f1_score}"
                    echo "ROC-AUC: ${results.roc_auc}"
                }
            }
        }
        stage('Stage2: Build & Push (ML-Based)') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', 'docker-hub-credentials') {
                        def mlApp = docker.build("${DOCKER_USER}/${REPO_NAME}:mlbased-${BUILD_VER}", "-f stage2-ml/Dockerfile stage2-ml/")
                        mlApp.push()
                        mlApp.push("mlbased-latest")
                    }
                }
            }
        }
    }
    post {
        always {
            archiveArtifacts artifacts: 'stage2-ml/app/models/*.pkl, stage2-ml/app/output/*.json', fingerprint: true
        }
    }
}