pipeline {
    agent { label 'linux' }
    environment {
        DOCKERHUB_CREDENTIALS = credentials('login-dockerhub')
    }
    
    stages {
        stage ('build') {
            steps {
                sh 'docker build -t foilv/tournament_go:jenkins1 .' 
            }
        }
        stage ('login') {
            steps {
                sh echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin
            }
        }
        stage ('push') {
            steps {
                sh 'docker push foilv/tournament_go:jenkins1'
            }
        }
    }
    post {
        always {
            sh 'docker logout'
        }
    }
}


