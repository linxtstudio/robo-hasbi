from flask import Flask

app = Flask('robi')

@app.route('/')
def home():
    return "I'm alive"

def exposed_api():
  app.run(host='0.0.0.0',port=8080)