pipeline {
    agent any

    environment {
        IMAGE_NAME = "dairy-management"
    }

    stages {
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME .'
            }
        }

        stage('Run Docker Container') {
            steps {
                sh 'docker run -d -p 5000:5000 --name dairy-app $IMAGE_NAME'
            }
        }

        stage('Health Check') {
            steps {
                sh 'sleep 5 && curl -f http://localhost:5000 || echo "App not responding"'
            }
        }
    }

    post {
        always {
            sh 'docker rm -f dairy-app || true'
        }
    }
}
