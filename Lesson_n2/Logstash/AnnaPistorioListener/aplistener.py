import json

from flask import Flask, request, redirect
from os import path

aplistener = Flask(__name__)

map2emoji = {
    "negative": "😡", 
    "neutral":  "🤨", 
    "positive": "🥰"
}

def write_in_store(json_body):
    with open('./storage/.store', 'a+') as store: 
        store.write(json_body + "\n")


def load_from_store():
    if not path.exists('./storage/.store'): return []
    with open('./storage/.store', 'r+') as store: 
        return [ json.loads(p) for p in store.readlines() ]


@aplistener.route("/send-quote", methods=['GET', 'POST'])
def random_quote():
    data = json.dumps(request.json)
    write_in_store(data)
    return "ok Anna..."
    

@aplistener.route("/read-quotes")
def read_quotes():
    m2e = lambda p: map2emoji.get(p['sentiment']['polarity'], '⚠️')
    p2s = lambda p: { "sentiment": m2e(p), "quote": p['message'] }
    quotes = [ p2s(p) for p in load_from_store() ]
    return aplistener.response_class(
        response=json.dumps(quotes),
        mimetype='application/json'
    )


if __name__ == "__main__":
    aplistener.run(debug=True,
            host='0.0.0.0',
            port=12000)