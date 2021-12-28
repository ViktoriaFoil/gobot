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
        stage ('change files') {
            steps {
                dir("first-try/"){
                    sh "echo $SECRETPASS | ansible-playbook --extra-vars=secretbot.yml --ask-vault-pass replacing-variables.yml"
                }
            }
        }
        stage ('run playbook') {
            steps {
                dir("first-try/"){
                    sh "ansible-playbook -i inventory.yml --extra-vars=vars.yml install_k3s.yml -u foilv"
                }
            }
        }
        stage ('remove files') {
            steps {
                dir("first-try/"){
                    sh "rm inventory.yml vars.yml password ../chartbot/script-import ../chartbot/values.yml ../chartbot/valuesdb.yml"
                }
            }
        }
    }
    post {
        always {
            sh 'docker logout'
        }
    }
}


