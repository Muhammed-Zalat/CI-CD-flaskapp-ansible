from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "Zalat sends his regards from a Dockerized Flask App using Jenkins + Ansible!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
