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
                dir("first-try/"){
                    sh "echo $PASSWORD > password"
                }
            }
        }
        stage ('ls') {
            steps {
                dir("first-try/"){
                    sh "ls"
                }
            }
        }
        stage ('change files') {
            steps {
                dir("first-try/"){
                    sh "ansible-playbook replacing-variables.yml --vault-password-file password"
                }
            }
        }
        stage ('run playbook') {
            steps {
                dir("first-try/"){
                    sh "ansible-playbook -i inventory.yml install_bot.yml -u foilv"
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


