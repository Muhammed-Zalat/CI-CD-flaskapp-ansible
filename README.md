# CI-CD-flaskapp-ansible
# CI/CD Pipeline for Flask App using Jenkins, Docker, and Ansible

This project sets up a complete CI/CD pipeline to automate the build, test, and deployment of a Flask web application using Jenkins, Docker, and Ansible.

---

📁 **CI-CD-flaskapp-ansible/**  
│  
├── 📁 **app/**  
│   ├── 📄 app.py  
│   ├── 📄 requirements.txt  
│   └── 📄 Dockerfile  
│  
├── 📁 **ansible/**  
│   ├── 📄 inventory  
│   └── 📄 playbook.yml  
│  
├── 📄 Jenkinsfile  
├── 📄 Dockerfile-jenkins  
├── 📄 README.md  
└── 📄 project-tree  

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
```groovy
stage('Clone Repository') {
    steps {
        git 'https://github.com/Muhammed-Zalat/CI-CD-flaskapp-ansible.git'
    }
}
```
2. **Build Docker Image:** The Flask app is containerized using Docker
```groovy
stage('Build Docker Image') {
    steps {
        dir('app') {
            sh 'docker build -t muhammedzalat/flaskapp:latest .'
        }
    }
}

```
3. **Push Image to Docker Hub:** The image is pushed to your Docker Hub account.
```groovy
   stage('Push to Docker Hub') {
    steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub', passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
            sh 'echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin'
            sh 'docker push muhammedzalat/flaskapp:latest'
        }
    }
}
```
4. **Deploy with Ansible:** The image is pulled and run on the target server using an Ansible playbook.
```groovy
stage('Deploy with Ansible') {
    steps {
        dir('ansible') {
            sh 'ansible-playbook -i inventory playbook.yml'
        }
    }
}
```
---
## 🐳 Buid Jenkins Image
      docker build -t jenkins-docker-ansible .

---

      docker run -d \
        --name jenkins-docker-ansible \
        --restart unless-stopped \
        -p 8080:8080 -p 50000:50000 \
        -v jenkins_home:/var/jenkins_home \
        -v /var/run/docker.sock:/var/run/docker.sock \
        jenkins-docker-ansible
  
  ---
  
## 🛠️ Installing Python Automatically on Target Server
  Ansible typically requires Python to be installed on the target node. To make the deployment work on a fresh target       
  machine with no dependencies, we used the raw module in our playbook to install Python:
```yaml
     tasks:
       - name: Ensure python is installed on the target server
         raw: yum install -y python3
         changed_when: false
```      
  This ensures that Ansible can take full control of the server even if Python is missing, making the setup fully automated and   
  agentless from the start.

## Install Docker on Target Server
  If Docker is not already installed on the target machine, Ansible installs it. This ensures the target server can run       containerized applications:
```yaml
- name: Ensure Docker is installed
   yum:
      name: docker-ce
      state: present
```
## Ensure Docker Service is Running
   If Docker is stopped or failed the ansible start it automatically:
```yaml
- name: Ensure Docker service is running and enabled
  service:
    name: docker
    state: started
    enabled: true
```

## Pull the Docker Image from Docker Hub
Once Docker is ready, Ansible pulls the latest version of your Flask app image from Docker Hub:
```yaml
- name: Pull image from DockerHub
  docker_image:
      name: muhammedzalat/flaskapp
      source: pull
```
## Run the Flask App in a Container
Ansible ensures any previous container is removed, and a new container is launched from the freshly pulled image:
```yaml
- name: Run docker container
   docker_container:
      name: flaskapp
      image: muhammedzalat/flaskapp
        state: started
        recreate: no
        ports:
          - "5000:5000"
```
  ---
  
### ✅ Requirements
- Docker installed on host
- Jenkins running inside a Docker container with access to /var/run/docker.sock
- Ansible installed in Jenkins container or on host
- Docker Hub credentials added in Jenkins (Credentials ID: docker-hub-creds)
- Remote server with Docker installed and accessible by Ansible

### 👨‍💻 **Author**  
**Muhammed Galal Zalat**  
[![GitHub](https://img.shields.io/badge/GitHub-@Muhammed--Zalat-181717?style=flat&logo=github)](https://github.com/Muhammed-Zalat)  
