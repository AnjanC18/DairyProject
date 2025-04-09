pipeline {
    agent any

    environment {
        IMAGE_NAME = "dairy-management"
    }

    stages {
        stage('Build Docker Image') {
            steps {
                echo '🔨 Building Docker image...'
                sh 'docker build -t $IMAGE_NAME .'
            }
        }

        stage('Run App and Show Output') {
            steps {
                echo '🚀 Running app in foreground (Flask output will be shown below)...'
                sh 'docker run --rm -p 5000:5000 $IMAGE_NAME'
            }
        }
    }

    post {
        always {
            echo '✅ Pipeline finished. Visit http://localhost:5000 to view your app if it’s still running.'
        }
    }
}
