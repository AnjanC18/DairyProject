pipeline {
    agent any

    environment {
        IMAGE_NAME = 'dairy-management'
        CONTAINER_NAME = 'dairy-app'
        HOST_PORT = '5001'
        CONTAINER_PORT = '5000'
    }

    stages {
        stage('🐳 Build Docker Image') {
            steps {
                echo "Building Docker image: ${IMAGE_NAME}"
                sh "docker build -t ${IMAGE_NAME} ."
            }
        }

        stage('🧼 Stop Previous Container') {
            steps {
                echo "Removing old container if it exists..."
                sh "docker rm -f ${CONTAINER_NAME} || true"
            }
        }

        stage('🚀 Run Docker Container') {
            steps {
                echo "Running container on port ${HOST_PORT}..."
                sh "docker run -d -p ${HOST_PORT}:${CONTAINER_PORT} --name ${CONTAINER_NAME} ${IMAGE_NAME}"
            }
        }
    }

    post {
        always {
            echo '🎯 Pipeline completed.'
        }
    }
}
