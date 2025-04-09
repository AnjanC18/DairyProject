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

        stage('Run Flask App in Foreground') {
            steps {
                echo '🚀 Running Flask app — output below will look just like VS Code...'
                sh 'docker run --rm -p 5000:5000 $IMAGE_NAME'
            }
        }
    }

    post {
        always {
            echo '✅ Build finished. Visit http://localhost:5000 while it’s running.'
        }
    }
}
