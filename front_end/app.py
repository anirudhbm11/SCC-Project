from flask import Flask, render_template, request, redirect, url_for
from get_tweets import TwitterAPI
from training.inference import MLModel

app = Flask(__name__)

final_topic1_predictions = {}
final_topic2_predictions = {}

models = MLModel()
model = models.select_model("BertSent")
bert_model = model.get_model()

@app.route('/',methods = ['POST', 'GET'])
def index_page():
    '''
    Getting the topic from the front end and redirecting it to the results page
    '''
    host = "127.0.0.1"
    port = 8004
    global final_topic1_predictions
    global final_topic2_predictions
    if request.method == 'POST':
        topic1 = "#"+request.form.get("topic1")
        topic2 = "#"+request.form.get("topic2")

        twitter_api = TwitterAPI()
        get_tweets = twitter_api.functionality("get_tweets")
        topic1_tweets = get_tweets.get_twitter_tweets(topic1, topic2)
        topic2_tweets = get_tweets.get_twitter_tweets(topic2, topic1)

        predictions_helper = twitter_api.functionality("prediction_helper")
        final_topic1_predictions = predictions_helper.get_predictions(topic1_tweets, model, bert_model)
        final_topic2_predictions = predictions_helper.get_predictions(topic2_tweets, model, bert_model)

        return redirect(url_for('result'))

    return render_template("index.html")

@app.route('/result')
def result():
    result = {"topic1": final_topic1_predictions, "topic2":final_topic2_predictions}
    print(result)
    return render_template("result.html", result=result)


if __name__ == "__main__":
    app.run(port=5003, debug=True)