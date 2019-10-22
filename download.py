from urllib.request import urlretrieve, urlopen
import json
import os
import time

from print_file import print_file
from config import *

log_list = check_existing_files()
print(log_list)

def download(task):
    '''
    @ param: task, API 返回的特定的对象

    根据 API 返回的文件 URL, 保存到本地, 等待下游打印功能
    '''
    try:

        # 用 "时间戳 + 原始文件名" 的形式下载到 /photo 文件夹里
        time_stamp = task.get('createdTime')
        origin_name = task.get('name')
        id = task.get('key')
        url = api%id
        name = '%s_%s'%(time_stamp, origin_name)
        path = os.path.join(save_dir, name)

        # 下载文件，返回路径
        print('[Retriving]', url)
        urlretrieve(url, path)
        print('[Download] %s -> %s'%(origin_name, path))
        return path
    except KeyboardInterrupt:
        raise KeyboardInterrupt
    except:
        return False


def fetch_once():
    '''
    获取一次服务器的全部打印任务列表, 与本地的已打印列表做比对
    打印差值文件, 将成功打印的文件录入本地列表, 失败的文件多次重试
    完成后发送请求, 更新 server 端的任务 status
    '''

    def update_status(id, status):
        urlopen(api_finish%(id, status))

    # 调用一次 API，获取全部任务列表
    with urlopen(api%'') as url:
        data = json.loads(url.read().decode())
        tasks = data.get('tasks', None)

        # 啥信息都没 fetch 到，这就诡异了
        if tasks is None:
            return

        # 筛选那些不在本地 log_list 里的任务（by task-id）
        task_to_download = [task for task in tasks if task.get('key') not in log_list]
        # print('Collected %d files'%len(task_to_download))


        # 把新文件先都下载下来，然后打印，更新状态
        for task in task_to_download:
            printed_successfully_flag = False
            name = task.get('name')

            # 下载新文件，如果下载失败返回 False
            new_file_path = download(task)
            if new_file_path:

                # 交给下游任务打印，如果打印失败返回 False
                if print_file(new_file_path):
                    print('[Print] %s'%(name))
                    printed_successfully_flag = True

                # 如果打印失败，给个提示，下次重新 fetch
                else:
                    print('[Error] file not printed   %s'%(name))
            else:
                print('[Error] file not downloaded   %s'%(name))

            # 打印完之后更新状态，保存本地记录
            if printed_successfully_flag:
                update_status(task.get('key'), 2)
                log_list.append(task.get('key'))
            else:
                update_status(task.get('key'), -1)

            save_log(log_list)
            print('-----------------------------')
