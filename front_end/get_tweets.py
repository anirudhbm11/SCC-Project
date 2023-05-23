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
    def get_twitter_tweets(self, topic1, topic2, language="en",numpages=2):
        auth = Authentication()
        bearer_token = auth.authentication_type("bearer")
        next_page = 0
        tweets = []
        i = numpages

        query_params = {'query':topic1 + " lang:en -is:retweet" + " -" + topic2 + " -" + topic2[1:],'tweet.fields':"created_at,lang,entities"}
        print(query_params)

        while i != 0:
            if i == numpages:
                response = requests.get("https://api.twitter.com/2/tweets/search/recent",params=query_params,headers=bearer_token)
                # print(response)
            else:
                query_params["next_token"] = next_page
                response = requests.get("https://api.twitter.com/2/tweets/search/recent",params=query_params,headers=bearer_token)
            response = response.json()
            if "next_token" in response["meta"].keys():
                next_page = response["meta"]["next_token"]
            else:
                next_page = None
            data = response["data"]
            for j, row in enumerate(data):
                # print(str(j)+": " + row["text"])
                # print("\n")
                tweets.append(row)
            i -= 1

            if next_page == None:
                break

        return tweets


class Prediction:
    def get_sentiment(self, tweet, model, bert_model): 
        text_prediction = {}
        prediction_and_score = model.predict(tweet, bert_model)
        prediction = prediction_and_score
        if(prediction == "LABEL_2"):
            text_prediction["label"] = "positive"
        elif prediction == "LABEL_1":
            text_prediction["label"] = "neutral"
        else:
            text_prediction["label"] = "negative"
        return (text_prediction, prediction_and_score)

    def get_predictions(self, tweets, model, bert_model):
        '''
        Getting hashtags and sentiment scores for all tweets
        '''
        predictions = {}
        predictions["text_predictions"] = []
        all_hashtags = dict()
        positiveTweets = 0
        negativeTweets = 0
        neutralTweets = 0
        count = 0
        tweets_created_date = {}
        for tweet in tweets:
            date = tweet["created_at"].split("T")[0]
            if date in tweets_created_date:
                tweets_created_date[date] += 1
            else:
                tweets_created_date[date] = 1
            if "entities" in tweet.keys():
                if "hashtags" in tweet["entities"].keys():
                    hashtags = tweet["entities"]["hashtags"]
                    for hashtag in hashtags:
                        tag = hashtag["tag"].lower()
                        if tag in all_hashtags:
                            all_hashtags[tag] += 1
                        else:
                            all_hashtags[tag] = 1
            text_prediction = self.get_sentiment(tweet["text"],  model, bert_model)
            if text_prediction[0]["label"] == "positive":
                positiveTweets += 1
            elif text_prediction[0]["label"] == "negative":
                negativeTweets += 1
            else:
                neutralTweets += 1
            if count <= 50:
                predictions["text_predictions"].append({"text": tweet["text"], "prediction":text_prediction[0]})
            count += 1

        sorted_hashtags = dict(sorted(all_hashtags.items(), key=lambda x: x[1], reverse=True)[:50])

        sorted_tweets_created_date = dict(sorted(tweets_created_date.items(), key=lambda x: x[0]))

        predictions["aggregate"] = {}
        predictions["aggregate"]["hashtags"] = sorted_hashtags
        predictions["aggregate"]["positiveTweets"] = positiveTweets
        predictions["aggregate"]["negativeTweets"] = negativeTweets
        predictions["aggregate"]["neutralTweets"] = neutralTweets
        predictions["aggregate"]["tweets_created_date"] = sorted_tweets_created_date

        return predictions


if __name__ == "__main__":
    twitter_api = TwitterAPI()
    get_tweets = twitter_api.functionality("get_tweets")
    tweets = get_tweets.get_twitter_tweets("#biden", "#trump")
    # tweets = ["One of them and testing it"]

    models = MLModel()
    model = models.select_model("BertSent")
    bert_model = model.get_model()

    predictions_helper = twitter_api.functionality("prediction_helper")
    predictions = predictions_helper.get_predictions(tweets, model, bert_model)

    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(predictions)

