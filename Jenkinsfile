pipeline {
    agent any
    environment {
        DOCKERHUB_CREDENTIALS = credentials('login-dockerhub')
        SECRETPASS = credentials('pass')
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
    
        stage ('echo pass') {
            steps {
                sh "touch first-try/password | echo $PASSWORD > first-try/password"
            }
        }
        stage ('change files') {
            steps {
                sh "ansible-playbook first-try/replacing-variables.yml --vault-password-file first-try/password"
                }
            }
        }
        stage ('run playbook') {
            steps {
                sh "ansible-playbook -i first-try/inventory.yml first-try/install_bot.yml -u foilv"
            }
        }
        stage ('remove files') {
            steps {
                sh "rm first-try/inventory.yml first-try/vars.yml first-try/password chartbot/script-import chartbot/values.yml chartbot/valuesdb.yml"
            }
        }
    }
    post {
        always {
            sh 'docker logout'
        }
    }
}


