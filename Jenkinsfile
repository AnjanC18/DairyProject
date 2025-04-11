pipeline {
    agent any

    environment {
        IMAGE_NAME = "dairy-management"
        CONTAINER_NAME = "dairy-management-container"
        APP_PORT = "5000"
    }

    stages {
        stage('Clone Repository') {
            steps {
                echo '📥 Cloning repository...'
                git url: 'https://github.com/AnjanC18/DairyProject', branch: 'main'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo '🔨 Building Docker image...'
                sh 'docker build -t $IMAGE_NAME .'
            }
        }

        stage('Stop Previous Container') {
            steps {
                echo '🧹 Cleaning up old containers...'
                sh """
                docker stop $CONTAINER_NAME || true
                docker rm $CONTAINER_NAME || true
                """
            }
        }

        stage('Run Docker Container') {
            steps {
                echo '🚀 Running Docker container...'
                sh """
                docker run -d --name $CONTAINER_NAME -p $APP_PORT:5000 $IMAGE_NAME
                """
            }
        }
    }

    post {
        success {
            echo "✅ Build successful! App is running at http://localhost:$APP_PORT"
        }
        failure {
            echo "❌ Build failed. Check the console output for errors."
        }
    }
}
