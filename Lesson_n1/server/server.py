from flask import Flask, request, redirect
import base64

app = Flask(__name__)

def log_to_file(message: str, ip: str):
    with open(f'logs/api.log', 'a+') as logfile:
        logfile.write(f'{ip}\t{message}\n')


@app.route("/log", methods=['GET'])
def log():
    query = request.args.to_dict()
    messg = query.get('message', 'not specified.')
    log_to_file(messg, request.remote_addr)
    print('api called.')    
    return 'successfully logged.'


@app.route("/", methods=['GET'])
def home():
    return 'My logs server home-page.'


if __name__ == "__main__":

    app.run(debug=True,
            host='0.0.0.0',
            port=5000)