import time

from download import fetch_once

if __name__ == "__main__":
    '''
    五秒轮询一次，冲冲冲
    '''
    while True:
        fetch_once()

        # fetch from server every 5 sec.
        time.sleep(5)