pipeline {
    agent any
    environment {
        DOCKER_USER = "2022bcs0088shashank"
        REPO_NAME = "assignment-1"
        IMAGE_TAG = "${env.BUILD_NUMBER}" 
        FULL_IMAGE_NAME = "${DOCKER_USER}/${REPO_NAME}"
    }
    stages {
        stage('Stage1: Unit Testing') {
            steps {
                script {
                    sh "pip3 install -r stage1-devops/requirements.txt --break-system-packages"
                    sh "export PYTHONPATH=\${WORKSPACE}/stage1-devops && pytest stage1-devops/tests/"                }
            }
        }
        stage('Stage1: Build & Push Versioned Image') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', 'docker-hub-credentials') {
                        def app = docker.build("${FULL_IMAGE_NAME}:${IMAGE_TAG}", "-f stage1-devops/Dockerfile stage1-devops/")
                        
                        app.push()
                        
                        app.push("latest")
                    }
                }
            }
        }
    }
}