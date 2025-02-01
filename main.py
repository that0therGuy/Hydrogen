from flask import Flask, url_for, send_file
from backend import *

app = Flask(__name__)

create_pages(app)
create_api(app)

if __name__ == '__main__':
    print(f"Starting server on port {get_env_var('PORT') or 8080}...")
    app.run(port=get_env_var('PORT') or 8080)