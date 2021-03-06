pipeline {
    agent any
    environment {
        DOCKERHUB_CREDENTIALS = credentials('login-dockerhub')
        SECRETPASS = credentials('pass')
        KUBECONFIG = credentials('kubectl_config')
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
       
        stage ('echo kubeconfig') {
            steps {
                dir('first-try/'){
                    sh "echo $KUBECONFIG | base64 -d > kubeconfig | chmod 0600 kubeconfig"
                }
            }
        }

        stage ('echo pass') {
            steps {
                dir('first-try/'){
                    sh "echo $SECRETPASS > password"
                }
            }
        }

        stage ('ls') {
            steps {
                sh "ls first-try/"
            }
        }
        stage ('install role') {
            steps {
                sh "ansible-galaxy install geerlingguy.docker"
            }
        }
        stage ('install collection') {
            steps {
                sh "ansible-galaxy collection install kubernetes.core"
            }
        }
        
        stage ('change files') {
            steps {
                dir('first-try'){
                    sh "ansible-playbook replacing-variables.yml --vault-password-file password"
                }
            }
        }
    
        stage ('run playbook') {
            steps {
                dir('first-try/'){
                    sh "ansible-playbook -vvvv install_bot.yml"
                }
            }
        }
        stage ('remove files') {
            steps {
                dir('first-try/'){
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