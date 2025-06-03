pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "muhammedzalat/flaskapp"
    }

    stages {
        stage('Clean Workspace') {
            steps {
                cleanWs()
            }
        }

        stage('Clone Repository') {
            steps {
                git 'https://github.com/Muhammed-Zalat/CI-CD-flaskapp-ansible.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                dir('app') {
                    sh 'docker rmi muhammedzalat/flaskapp:latest || true'
                    sh 'docker build --no-cache -t $DOCKER_IMAGE:latest .'
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                    sh 'docker push $DOCKER_IMAGE:latest'
                }
            }
        }

        stage('Deploy with Ansible') {
            steps {
                //sshagent(credentials: ['ansible-ssh-key']) {
                    dir('ansible') {
                        sh '''
                            ANSIBLE_HOST_KEY_CHECKING=False \
                            ansible-playbook -i inventory.ini Playbook.yaml -vvv
                        '''
                    }
                }
            }
        }
    }
}
