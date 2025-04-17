import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from flask import Flask, request, jsonify
from flask_cors import CORS
# TF-IDF vectorizer

data = pd.read_csv('../data/fake_or_real_news.csv')
data['fake'] = data['label'].apply(lambda x:0 if x == 'REAL' else 1)
data = data.drop('label', axis=1)
x, y = data['title'], data['fake']
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
vectorizer = TfidfVectorizer(stop_words='english', max_df=0.7)
x_train_vectorized = vectorizer.fit_transform(x_train)
x_test_vectorized = vectorizer.transform(x_test)
clf = LinearSVC()
clf.fit(x_train_vectorized, y_train)
clf.score(x_train_vectorized, y_train)
def predict_news_type(text):
    vectorized_text = vectorizer.transform([text])
    value = clf.predict(vectorized_text)   
    return "Real" if value == 0 else "Fake"

app = Flask(__name__)
CORS(app)
@app.route('/check', methods=['POST'])
def check():    
    try:
        request_data = request.get_json()
        if not request_data or 'text' not in request_data:
            return jsonify({"error": "Missing 'text' field in JSON payload"}), 400
        text_to_check = request_data['text']
        if not isinstance(text_to_check, str) or not text_to_check.strip():
             return jsonify({"error": "'text' field must be a non-empty string"}), 400
        prediction = predict_news_type(text_to_check)
        print(prediction)
        return jsonify({'prediction': prediction})

    except Exception as e:
        print(f"Error processing request: {e}")
        return jsonify({"error": "An internal server error occurred"}), 500
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)