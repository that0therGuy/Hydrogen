from axinite import axtools
import websocket, json, queue, time, threading


def create_websocket_api(): 
    ws = websocket.WebSocketApp("ws://localhost:8000/api/simulate",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    _queue = queue.Queue()

    def on_message(ws, message):
        data = json.dumps(message)
        args = axtools.reads(data)

        def callback(result):
            ws.send(result)

        _queue.put((args, callback))

    def on_error(ws, error):
        print(f"Error: {error}")

    def on_close(ws, close_status_code, close_msg):
        print("WebSocket closed")

    def process():
        while True:
            if not _queue.empty():
                args, callback = _queue.get()
                axtools.load(args)
                callback(axtools.saves(args))
                _queue.task_done()
            time.sleep(1)

    threading.Thread(target=process, daemon=True).start()
    threading.Thread(target=ws.run_forever, daemon=True).start()