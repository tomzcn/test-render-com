from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    f=open('1.txt','w')
    f.write('1')
    f.close()
    f=open('1.txt','r')
    f.read()
    f.close()
    return 'Hello, World!'
