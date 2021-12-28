pipeline {
    agent any
    environment {
        DOCKERHUB_CREDENTIALS = credentials('login-dockerhub')
        PASSWORD = credentials('pass')
    }
    
    stages {
        stage ('build') {
            steps {
                sh 'docker build -t foilv/tournaments_go:latest .' 
            }
        }
        stage ('login') {
            steps {
                sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
            }
        }
        stage ('push') {
            steps {
                sh 'docker push foilv/tournaments_go:latest'
            }
        }
        stage ('ls') {
            steps {
                sh "pwd"
            }
        }
    }
    post {
        always {
            sh 'docker logout'
        }
    }
}


