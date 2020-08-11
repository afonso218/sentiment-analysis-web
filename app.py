from __future__ import print_function
from flask import Flask , jsonify, render_template
from textblob import TextBlob
import sys

app = Flask(__name__)

def log(text):
    print(str(text), file=sys.stderr)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/api/sentiment/<message>')
def sentiment(message):
    
    
    language = TextBlob(message).detect_language()
        
    if language != 'en':
        text = TextBlob(str(TextBlob(message).translate(from_lang=language, to='en')))
    else:
        text = TextBlob(message)
    
    log(text)
    response = {'polarity' : text.polarity , 'subjectivity' : text.subjectivity, 'language' : language.upper(), 'translate' : str(text)}

    return jsonify(response)

@app.route('/api/nouns/<message>')
def nouns(message):
    
    if TextBlob(message).detect_language() == 'en':
        response = {'nouns' : TextBlob(message).noun_phrases}
    else:
        response = {'nouns' : ''}

    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)
