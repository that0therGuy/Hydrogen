from flask import Flask, request, jsonify
from backend import __version__
import queue, threading, time, json, hashlib
from axinite import axtools

def create_api(app: Flask): 
    @app.route('/api', methods=['GET'])
    def api():
        return jsonify({'version': __version__})
    
    _queue = queue.Queue()
    _results = {}

    @app.route('/api/simulate', methods=['POST'])
    def simulate():
        data = request.get_json()
        template = json.dumps(data)
        args = axtools.reads(template)
        id = hashlib.sha256(template.encode()).hexdigest()
        _queue.put((id, args))
        return jsonify({"status": "in-queue", "id": id})
    
    @app.route('/api/simulation/<id>', methods=['GET'])
    def simulation(id):
        if id in _queue.queue:
            return jsonify({"status": "in-queue"})
        elif id in _results:
            return jsonify({"status": "done", "result": _results[id]})
        else:
            return jsonify({"status": "not-found"})
        
    def process():
        while True:
            if not _queue.empty():
                id, args = _queue.get()
                axtools.load(args)
                _results[id] = axtools.saves(args)
                _queue.task_done()
            time.sleep(1)
    
    threading.Thread(target=process, daemon=True).start()