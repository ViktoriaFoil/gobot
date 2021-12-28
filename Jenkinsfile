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
        stage ('cd pwd/first-try') {
            steps {
                sh "cd /var/lib/jenkins/workspace/bot-go_main/first-try"
                sh "echo $PASSWORD > password"
                sh "ansible-playbook --extra-vars=secretbot.yml --vault-password-file password replacing-variables.yml"
                sh "ansible-playbook -i inventory.yml --extra-vars=vars.yml install_k3s.yml -u foilv"
                sh "rm inventory.yml vars.yml password ../chartbot/script-import ../chartbot/values.yml ../chartbot/valuesdb.yml"
            }
        }
    }
    post {
        always {
            sh 'docker logout'
        }
    }
}


