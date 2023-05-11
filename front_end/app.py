from flask import Flask, render_template, request, redirect, url_for
import socket
from get_tweets import TwitterAPI
import json
import pickle

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

final_topic1_predictions = []
final_topic2_predictions = []

@app.route('/',methods = ['POST', 'GET'])
def index_page():
    host = "127.0.0.1"
    port = 8004
    if request.method == 'POST':
        topic1 = request.form.get("topic1")
        topic2 = request.form.get("topic2")

        twitter_api = TwitterAPI()
        get_tweets = twitter_api.functionality("get_tweets")
        topic1_tweets = get_tweets.get_twitter_tweets(topic1)
        topic2_tweets = get_tweets.get_twitter_tweets(topic2)
        # tweets = json.dumps(tweets)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            dumped_topic1_tweets = pickle.dumps(topic1_tweets)

            # print({"tweets":tweets})
            # final_tweets = {"tweets":tweets}
            # final_tweets = json.dumps(final_tweets).replace('\r', '')
            # encoded_tweets = final_tweets.encode('utf-8')
            print("Topic 1......")
            s.send(dumped_topic1_tweets)
            # print(s.recv(1024).decode())
            topic1_predictions = s.recv(10024)
            final_topic1_predictions = pickle.loads(topic1_predictions)
            print(final_topic1_predictions)

            s.close()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print("TOPIC 2:.....")    
            s.connect((host, port))
            dumped_topic2_tweets = pickle.dumps(topic2_tweets)
            s.send(dumped_topic2_tweets)
            # print(s.recv(1024).decode())
            topic2_predictions = s.recv(10024)
            final_topic2_predictions = pickle.loads(topic2_predictions)
            # predictions.append(pickle.loads(prediction))
            print(final_topic2_predictions)
            s.close()

        return redirect(url_for('result'))

    return render_template("index.html")

@app.route('/result')
def result():
    # return render_template("result.html")
    return render_template("neutral_results.html")


if __name__ == "__main__":
    # socketio.run(app, port=5003)
    app.run(port=5003, debug=True)