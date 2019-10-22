import os
import json

### configs start ###
save_dir = 'photos/'

log_file_name = 'downloaded.json'

host = 'http://zhouyc.cc/'

api = host + 'api/printer/task?id=%s'

def save_log(log_list):
    json.dump(log_list, open(log_file_name, 'w'))

def check_existing_files():
    print('Check directory', save_dir)
    if not os.path.exists(save_dir) or not os.path.isfile(log_file_name):
        os.makedirs(save_dir, exist_ok=True)
        log_list = []
        save_log(log_list)
    else:
        log_list = json.load(open(log_file_name, 'r'))

    return log_list

api_finish = host + 'api/printer/update-status?id=%s&status=%d'
