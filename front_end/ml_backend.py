import socket
import time
import json
from training.inference import MLModel
from get_tweets import TwitterAPI
import pickle

hostname = "127.0.0.1"
port = 8004

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    s.bind((hostname,port))
    s.listen()

    models = MLModel()
    model = models.select_model("BertSent")
    bert_model = model.get_model()
    
    while True:
        conn, addr = s.accept()

        print("Connection accepted..........")

        with conn:
            print("Connection accepted from " + str(addr))
            
            # data = b""
            # while True:
            chunk = conn.recv(10024)
            #     if not chunk:
            #         break
            #     data += chunk

            # tweets_decoded = data.decode('utf-8')
            # tweets = json.loads(tweets_decoded)["tweets"]
            tweets = pickle.loads(chunk)
            # data = conn.recv(1024)
            # tweets = json.loads(data.decode())["tweets"]

            print(tweets)

            twitter_api = TwitterAPI()
            predictions_helper = twitter_api.functionality("prediction_helper")
            predictions = predictions_helper.get_predictions(tweets, model, bert_model)


            conn.send(pickle.dumps(predictions))


            



