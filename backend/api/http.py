from flask import Flask, request, jsonify
from backend import __version__
import queue, threading, time, json
from axinite import axtools

def create_http_api(app: Flask): 
    @app.route('/api', methods=['GET'])
    def api():
        return jsonify({'version': __version__})
    
    _queue = queue.Queue()

    @app.route('/api/simulate', methods=['POST'])
    def simulate():
        data = request.get_json()
        args = axtools.reads(json.dumps(data))

        def callback(result):
            return jsonify(result)

        _queue.put((args, callback))
        return jsonify({"status": "processing"})

    def process():
        while True:
            if not _queue.empty():
                args, callback = _queue.get()
                axtools.load(args)
                result = axtools.saves(args)
                callback(result)
                _queue.task_done()
            time.sleep(1)

    threading.Thread(target=process, daemon=True).start()