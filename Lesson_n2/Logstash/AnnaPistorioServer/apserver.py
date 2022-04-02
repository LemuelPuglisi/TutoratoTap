import random

from flask import Flask, request, redirect, json

apserver = Flask(__name__)

# Tipiche frasi che sentirai da Anna, ma in inglese. 
ap_quotes = [
    'This course sucks',                # dove per corso si intende un generico corso frequentato da Anna
    'This professor sucks',             # dove per professore si intende un generico professore che respira accanto ad Anna
    'This freshman sucks',              # dove per matric- No dai qui Anna ha ragione. 
    'Yes you can have a cigarette',     # a volte Anna si tramuta in un dispenser di cartine-filtrini-tabacco
    'I really love engineers'           # Da informatico, mi dissocio fortemente. 
]

@apserver.route("/random-quote")
def random_quote():
    quote = random.choice(ap_quotes)    
    return apserver.response_class(
        response=json.dumps({ "message": quote }),
        mimetype='application/json'
    )

if __name__ == "__main__":
    apserver.run(debug=True,
            host='0.0.0.0',
            port=5000)