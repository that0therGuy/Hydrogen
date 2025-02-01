from flask import Flask, send_file

def create_pages(app: Flask):
    @app.route('/')
    def index():
        return send_file('static/index.html')
    
    