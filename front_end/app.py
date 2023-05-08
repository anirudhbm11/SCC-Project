from flask import Flask, render_template, request, redirect, url_for
import socket
from flask_socketio import SocketIO
from threading import Lock
from get_tweets import TwitterAPI
import json
import pickle

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app,cors_allowed_origins='*')

predictions = []

thread = None
thread_lock = Lock()

@app.route('/',methods = ['POST', 'GET'])
def index_page():
    host = "127.0.0.1"
    port = 8004
    if request.method == 'POST':
        topic = request.form.get("topic")

        twitter_api = TwitterAPI()
        get_tweets = twitter_api.functionality("get_tweets")
        tweets = get_tweets.get_twitter_tweets(topic)

        for tweet in tweets:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((host, port))
                tweet = json.dumps(tweet).encode('utf-8')
                s.send(tweet)

                # print(s.recv(1024).decode())

                prediction = s.recv(1024)
                predictions.append(pickle.loads(prediction))

        return redirect(url_for('result'))

    return render_template("index.html")

# def background_thread():
#     print("Generating random sensor values")
#     while True:
#         dummy_sensor_value = round(random() * 100, 3)
#         socketio.emit('sending_message', {'value': dummy_sensor_value, "date": "today"})
#         # socketio.sleep(1)

@socketio.on('connect')
def connect():
    print('Client connected')

    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(sending_message)

@socketio.on('disconnect')
def disconnect():
    print('Client disconnected')

def sending_message():
    for prediction in predictions:
        predictions_final = prediction["text_predictions"][0]
        text_prediction = {"text":predictions_final["text"], "pred":predictions_final["score"][0]}
        socketio.emit('sending_message',text_prediction)
        socketio.emit('sending_prediction', str(prediction))
        socketio.sleep(1)

@app.route('/result')
def result():
    return render_template("result.html")
    # return render_template("neutral_results.html")


if __name__ == "__main__":
    socketio.run(app, port=5003)