from flask import Flask, jsonify
import requests
import re
from urllib import parse
from bs4 import BeautifulSoup, Comment, Declaration

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
@app.route('/scraper/<path:url>', methods=['GET'])
def scraper(url):
    try:
        response = requests.get(url).content
        texts = BeautifulSoup(response, 'html.parser').findAll(string=True)
        output = "".join(list(filter(is_article_text, texts)))
    except:
        output= None
    print(output)
    return jsonify({"Output":output})

if __name__ == '__main__':
    app.run()
