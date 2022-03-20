import time 

def log():
    """ Python dummy logger example. 
    """
    t = 0
    while True: 
        print(f'time: {t} \t log sent.')
        t += 1
        time.sleep(1)

if __name__ == '__main__': log()