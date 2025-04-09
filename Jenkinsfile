pipeline {
    agent any

    environment {
        IMAGE_NAME = "dairy-management"
    }

    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/AnjanC18/DairyProject.git' // replace with your repo if needed
            }
        }

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

        stage('Test Health Check') {
            steps {
                sh 'curl --retry 5 --retry-connrefused http://localhost:5000'
            }
        }
    }

    post {
        always {
            echo 'Cleaning up containers...'
            sh 'docker rm -f dairy-app || true'
        }
    }
}
