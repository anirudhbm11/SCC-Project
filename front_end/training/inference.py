from joblib import load
from abc import abstractmethod, ABC
import re
import nltk 
import numpy as np
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from sklearn.linear_model import LogisticRegression
import tensorflow as tf
from transformers import AutoTokenizer
from transformers import BertForSequenceClassification, TFAutoModelForSequenceClassification

class MLmodelTasks(ABC):
    @abstractmethod
    def predict(self, data):
        pass

    def clean_data(self, text, stem=False):
         # Lower Case
        text = "".join([w.lower() for w in text])
        
        # Remove http links
        text = re.sub(r'http\S+', '', text)
        
        # Remove punctuations
        punc = '''!()-[]{};:'"\,<>./?@$%^&*_~“”…’’#'''
    #     text = re.sub(r'[^\w\s]', '', text)
        text = "".join([c for c in text if c not in punc])
        
        # Remove stopwords
        lemmatizer = WordNetLemmatizer()
        text_tokens = text.split()
        filtered_sentence = " ".join([lemmatizer.lemmatize(w) for w in text_tokens if not w.lower() in stopwords.words('english') and len(w) > 1])
        
        return filtered_sentence

class LogisticRegression(MLmodelTasks):
    def predict(self, text):
        # model = self.getModel()
        text = self.clean_data(text)
        vectorizer = load("training/tfidf_vectorizer.joblib")
        x_test  = vectorizer.transform([text])

        return model.predict(x_test[0])

    def getModel(self):
        model = load("training/logistic_soc.joblib")
        return model

class BertModel(MLmodelTasks):
    '''
    Calling the saved model and using it for inference
    '''
    def predict(self,text):
        # model = self.get_model()
        text = self.clean_data(text)
        tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")
        x_test = tokenizer([text], padding=True, truncation=True,max_length=80,return_tensors="pt")
        outputs = model(**x_test).logits

        predicted_class_id = outputs.argmax().item()
        predicted_label = model.config.id2label[predicted_class_id]

        return predicted_label

    def get_model(self):
        model = BertForSequenceClassification.from_pretrained('training/bert_soc',num_labels = 2,output_attentions = False,output_hidden_states = False)
        return model

class MLModel:
    def select_model(self, model_name):
        if model_name == "logistic_regression":
            return LogisticRegression()
        elif model_name == "Bert":
            return BertModel()


if __name__ == "__main__":
    models = MLModel()
    model = models.select_model("Bert")
    bert_model = model.get_model()
    print(model.predict(["This is bad. Really bad"], bert_model))
        
