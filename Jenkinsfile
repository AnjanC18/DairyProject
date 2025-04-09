pipeline {
    agent any

    environment {
        IMAGE_NAME = 'dairy-management'
    }

    stages {
        stage('Checkout Code') {
            steps {
                git 'https://github.com/your-username/your-repo.git'  // Replace with your repo
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'python -m pip install --upgrade pip'
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME .'
            }
        }

        stage('Run Container') {
            steps {
                sh 'docker run -d -p 5000:5000 --name flask_app $IMAGE_NAME'
            }
        }

        stage('Test App') {
            steps {
                echo "You can add integration or health check tests here."
            }
        }
    }

    post {
        always {
            echo 'Cleaning up...'
            sh 'docker rm -f flask_app || true'
        }
    }
}
