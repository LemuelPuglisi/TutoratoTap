import requests
import time 

SERVER_HOSTNAME='http://logs-server:5000/log'

def remote_log(msg: str):
    query = { 'message': msg }
    try:
        resp = requests.get(url=SERVER_HOSTNAME, params=query)
    except:
        return 500
    return resp.status_code


def log():
    t = 0
    while True: 
        t += 1
        msg = f'time: {t} \t log sent.' 
        status_code = remote_log(msg)
        print(f'http status code: {status_code}')
        time.sleep(1)


if __name__ == '__main__': log()