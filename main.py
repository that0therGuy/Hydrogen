from flask import Flask, url_for, send_file
from backend import get_env_var

app = Flask(__name__)

@app.route('/')
def index():
    return send_file('static/index.html')

if __name__ == '__main__':
    app.run(port=get_env_var('PORT') | 8080)