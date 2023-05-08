import socket
import time
import json
from training.inference import MLModel
from get_tweets import Prediction
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
            
            data = conn.recv(1024).decode()

            tweet = json.loads(data)

            predictions_helper = Prediction()
            predictions = predictions_helper.get_predictions(tweet, model, bert_model)

            print(predictions)

            conn.send(pickle.dumps(predictions))


            



