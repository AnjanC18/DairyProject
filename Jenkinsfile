pipeline {
    agent any

    environment {
        IMAGE_NAME = "dairy-management"
        REPO_URL = "https://github.com/AnjanC18/DairyProject"
        BRANCH_NAME = "main"
    }

    stages {
        stage('Checkout Source Code') {
            steps {
                echo '📥 Cloning repository...'
                git url: "${REPO_URL}", branch: "${BRANCH_NAME}"
            }
        }

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
