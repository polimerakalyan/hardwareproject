pipeline {
    agent any

    stages {
        stage('Clone') {
            steps {
                git branch: 'master', url: 'https://github.com/polimerakalyan/hardwareproject.git'
            }
        }

    stages {
        stage('Build') {
            steps {
                sh 'docker build -t django-app .'
            }
        }

        stage('Stop Old Container') {
            steps {
                sh 'docker rm -f django-app || true'
            }
        }

        stage('Run Container') {
            steps {
                sh 'docker run -d --network app-network -p 8000:8000 --name django-app django-app'
            }
        }
    }
}  

