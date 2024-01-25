from flask import Flask, jsonify
import requests
import re
from bs4 import BeautifulSoup, Comment, Declaration
import time

def is_article_text(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element)):
        return False
    elif type(element) is Comment or type(element) is Declaration:
        return False
    elif len(str(element)) < 200:
        return False
    return True

app = Flask(__name__)
@app.route('/article/<path:url>', methods=['GET'])
def converter(url):
    start=time.time()
    try:
        response = requests.get(url).content
        texts = BeautifulSoup(response, 'html.parser').findAll(string=True)
        output = "".join(list(filter(is_article_text, texts)))
    except:
        output= None

    headers = {
        # 'Content-Type': 'application/json',
        'Authorization': f"Bearer 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",}
    json_data = {
        'model': 'gpt-3.5-turbo',
        'messages': [{'role': 'user','content': output+"\n\n Convert this news article into a Hindi Bollywood song and display the song in the Devanagri Script. Do not display any comments or any comments, in any case."}]}

    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=json_data)
    return response.json()['choices'][0]['message']['content']

if __name__ == '__main__':
    app.run()
