from authentication import Authentication
import json
import requests
from training.inference import MLModel
import pprint

class TwitterAPI:
    def __init__(self) -> None:
        pass

    def functionality(self, task):
        if task == "get_tweets":
            return GetTweets()
        else:
            raise NotImplementedError

class GetTweets():
    def get_twitter_tweets(self, query, language="en",numpages=1):
        auth = Authentication()
        bearer_token = auth.authentication_type("bearer")
        next_page = 0
        tweets = []

        query_params = {'query':query + " lang:en -is:retweet",'tweet.fields':"created_at,lang"}

        for i in range(numpages):
            if i == 0:
                response = requests.get("https://api.twitter.com/2/tweets/search/recent",params=query_params,headers=bearer_token)
                # print(response)
            else:
                query_params["next_token"] = next_page
                response = requests.get("https://api.twitter.com/2/tweets/search/recent",params=query_params,headers=bearer_token)

            response = response.json()
            next_page = response["meta"]["next_token"]
            data = response["data"]
            for j, row in enumerate(data):
                # print(str(j)+": " + row["text"])
                # print("\n")
                tweets.append(row)

        return tweets


class Prediction:
    def get_sentiment(self, tweet, model, bert_model): 
        text_prediction = {}
        prediction_and_score = model.predict(bert_model, tweet)
        prediction = prediction_and_score[0]
        if(prediction == "LABEL_2"):
            text_prediction["label"] = "positive"
        elif prediction == "LABEL_1":
            text_prediction["label"] = "negative"
        else:
            text_prediction["label"] = "neutral"
        return (text_prediction, prediction_and_score)

    def get_predictions(self, tweets, model, bert_model):
        predictions = {}
        predictions["text_predictions"] = []
        # for tweet in tweets:
        text_prediction = self.get_sentiment(tweets["text"], model, bert_model)
        predictions["text_predictions"].append({"text": tweets["text"], "prediction":text_prediction[0], "score": text_prediction[1]})

        return predictions


if __name__ == "__main__":
    twitter_api = TwitterAPI()
    get_tweets = twitter_api.functionality("get_tweets")
    tweets = get_tweets.get_twitter_tweets("biden")

    models = MLModel()
    model = models.select_model("BertSent")
    bert_model = model.get_model()

    predictions_helper = Prediction()
    predictions = predictions_helper.get_predictions(tweets, model, bert_model)

    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(predictions)

