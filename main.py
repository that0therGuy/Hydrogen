from flask import Flask, url_for, send_file
from backend import *

app = Flask(__name__)

create_pages(app)
create_http_api(app)
create_websocket_api()

if __name__ == '__main__':
    app.run(port=get_env_var('PORT') | 8080)