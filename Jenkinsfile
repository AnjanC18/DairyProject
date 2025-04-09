pipeline {
    agent {
        docker {
            image 'python:3.10'
        }
    }

    stages {
        stage('Clone Repo') {
            steps {
                echo 'Cloning the repo...'
            }
        }
        stage('Install Dependencies') {
            steps {
                echo 'Installing dependencies...'
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Run App') {
            steps {
                echo 'Running the app...'
                sh 'python app.py'
            }
        }
        stage('Test') {
            steps {
                echo 'Running tests...'
                // Add your test command here
            }
        }
    }
}
