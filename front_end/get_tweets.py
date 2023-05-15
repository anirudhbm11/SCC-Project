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
        elif task == "prediction_helper":
            return Prediction()
        else:
            raise NotImplementedError

class GetTweets():
    def get_twitter_tweets(self, query, language="en",numpages=1):
        auth = Authentication()
        bearer_token = auth.authentication_type("bearer")
        next_page = 0
        tweets = []

        query_params = {'query':query + " lang:en -is:retweet",'tweet.fields':"created_at,lang,entities"}

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
        prediction_and_score = model.predict(tweet, bert_model)
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
        all_hashtags = dict()
        positiveTweets = 0
        negativeTweets = 0
        neutralTweets = 0
        count = 0
        for tweet in tweets:
            if count == 1:
                break
            if "hashtags" in tweet["entities"].keys():
                hashtags = tweet["entities"]["hashtags"]
                for hashtag in hashtags:
                    tag = hashtag["tag"]
                    if tag in all_hashtags:
                        all_hashtags[tag] += 1
                    else:
                        all_hashtags[tag] = 1
            text_prediction = self.get_sentiment(tweet["text"],  model, bert_model)
            if text_prediction[0] == "positive":
                positiveTweets += 1
            elif text_prediction[0] == "negative":
                negativeTweets += 1
            else:
                neutralTweets += 1
            predictions["text_predictions"].append({"text": tweet["text"], "prediction":text_prediction[0]})
            count += 1

        sorted_hashtags = dict(sorted(all_hashtags.items(), key=lambda x: x[1], reverse=True))
        print(sorted_hashtags)

        predictions["aggregate"] = {}
        predictions["aggregate"]["hashtags"] = sorted_hashtags
        predictions["aggregate"]["positiveTweets"] = positiveTweets
        predictions["aggregate"]["negativeTweets"] = negativeTweets
        predictions["aggregate"]["neutralTweets"] = neutralTweets

        return predictions


if __name__ == "__main__":
    twitter_api = TwitterAPI()
    get_tweets = twitter_api.functionality("get_tweets")
    tweets = get_tweets.get_twitter_tweets("#biden")
    # tweets = ["One of them and testing it"]

    # print(tweets)

    models = MLModel()
    model = models.select_model("BertSent")
    bert_model = model.get_model()

    predictions_helper = twitter_api.functionality("prediction_helper")
    predictions = predictions_helper.get_predictions(tweets, model, bert_model)

    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(predictions)

