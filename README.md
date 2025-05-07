# CI-CD-flaskapp-ansible
# CI/CD Pipeline for Flask App using Jenkins, Docker, and Ansible

This project sets up a complete CI/CD pipeline to automate the build, test, and deployment of a Flask web application using Jenkins, Docker, and Ansible.

---
## 📁 Project Structure
CI-CD-flaskapp-ansible/
├── app/ # Flask application code
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── ansible/ # Ansible playbooks for deployment
│   ├── inventory
│   └── playbook.yml
├── Jenkinsfile # Declarative pipeline definition
├── Dockerfile-jenkins # To custom jenkins image included docker and ansible
├── README.md # Project documentation
└── project-tree # Project Structure

---

## 🔧 Technologies Used

- **Jenkins** (in Docker) for CI/CD orchestration
- **Docker** for containerizing the Flask app
- **Docker Hub** to store and distribute the built image
- **Ansible** to deploy the app on a remote server
- **GitHub** as the source code repository

---

## 🚀 Pipeline Overview

1. **Clone Repository:** Jenkins pulls the latest code from GitHub.
   stage('Clone Repository') {
            steps {
                git 'https://github.com/Muhammed-Zalat/CI-CD-flaskapp-ansible.git'
            }

2. **Build Docker Image:** The Flask app is containerized using Docker.
   stage('Build Docker Image') {
            steps {
                dir('app') {
                    sh 'docker build -t $DOCKER_IMAGE:latest .'
                }
            }
3. **Push Image to Docker Hub:** The image is pushed to your Docker Hub account.
   stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                    sh 'docker push $DOCKER_IMAGE:latest'
                }
            }
        }

4. **Deploy with Ansible:** The image is pulled and run on the target server using an Ansible playbook.
   stage('Deploy with Ansible') {
            steps {
                dir('ansible') {
                    sh 'ansible-playbook -i inventory Playbook.yaml'
                }
            }
        }


## 🐳 Buid Jenkins Image
docker build -t jenkins-docker .

---

docker run -d \
  --name jenkins \
  --restart unless-stopped \
  -p 8080:8080 -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  jenkins-docker
  
  ---
  
## 🛠️ Installing Python Automatically on Target Server
  Ansible typically requires Python to be installed on the managed (target) node. To make the deployment work on a fresh target       
  machine with no dependencies, we used the raw module in our playbook to install Python:
    
  tasks:
    - name: Ensure python is installed on the target server
      raw: yum install -y python3
      changed_when: false
      
  This ensures that Ansible can take full control of the server even if Python is missing, making the setup fully automated and   
  agentless from the start.

  ---
  
✅ Requirements
   Docker installed on host

   Jenkins running inside a Docker container with access to /var/run/docker.sock

   Ansible installed in Jenkins container or on host

   Docker Hub credentials added in Jenkins (Credentials ID: docker-hub-creds)

   Remote server with Docker installed and accessible by Ansible

🧠 Author
  Muhammed Galal Zalat
  GitHub: @Muhammed-Zalat
