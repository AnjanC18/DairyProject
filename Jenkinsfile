pipeline {
    agent any

    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/AnjanaGowdaC/DairyManagment.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    dockerImage = docker.build("dairy-management")
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                script {
                    // Run the container in detached mode (-d)
                    sh 'docker run -d -p 5000:5000 dairy-management'
                }
            }
        }
    }
}
