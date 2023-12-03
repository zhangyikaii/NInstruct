import os
import re
import pickle
import json
import importlib
import ast
import time
import argparse
from argparse import ArgumentParser
import openai

from configs import JSON_SAVE_PATH, OPEN_AI_KEY, IMG_DOWNLOAD_FAILED_LOGS

class Counter:
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1

    def __str__(self):
        return f'{self.count:010d}'

class GPT:
    def __init__(self):
        self.client = openai.OpenAI(api_key=OPEN_AI_KEY)

    def answer(self, question):
        completion = self.client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": question}])

        return completion.choices[0].message.content


ID_COUNTER = Counter()

import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s [%(levelname)s]: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='logs/running.log',
                    filemode='w')

LOGGER = logging.getLogger('ginstruct')

def load_pickle(file_name):
    with open(file_name, 'rb') as f:
        return pickle.load(f)

def save_pickle(file_name, data):
    with open(file_name, 'wb') as f:
        pickle.dump(data, f, protocol=pickle.DEFAULT_PROTOCOL)

def preprocess_text(text: str = ''):
    assert isinstance(text, str)
    # text = re.sub(r'^\d+\s*', '', text) # 去除开头的数字
    text = text.strip()
    text = re.sub(r'^[.,;?”’:。，]+', '', text)  # 去除开头的标点符号
    text = re.sub(r'\[(\w+)R\]', r'[\1]', text) # [赞R] 替换为 [赞]
    text = re.sub(r'@\S+\s*', '', text) # 删除 @ 之后的信息
    text = text.strip()
    return text

def remove_non_chinese_digits(text):
    # 使用正则表达式匹配非数字和非中文字符并替换为空格
    cleaned_text = re.sub(r'[^\u4e00-\u9fff0-9]', '', text)
    return cleaned_text

def download_img(url: str, dest_file: str):
    if not os.path.isfile(dest_file):
        max_attempts = 10
        time_limit = 180 # in 3min
        start_time = time.time()

        for attempt in range(1, max_attempts + 1):
            try:
                wget.download(url, dest_file)
                return True
            except Exception as e:
                LOGGER.debug(f"Attempt {attempt} failed: {e}")
                if time.time() - start_time >= time_limit:
                    LOGGER.debug("Download timed out.")
                    break
                continue

        LOGGER.debug("Download failed after multiple attempts.")
        return False
    return True

def log_failed_img(data_id: str, url: str, dest_file: str):
    with open(IMG_DOWNLOAD_FAILED_LOGS, 'a') as f:
        f.write(f'{data_id},{url},{dest_file}\n')

def get_class_from_module(module_name, class_name):
    try:
        module = importlib.import_module(module_name)
        return getattr(module, class_name)
    except ModuleNotFoundError:
        return None

def make_data_dict(cur_id, cur_conversations):
    return {
        "id": cur_id,
        "conversations": [
            {
                "from": "user" if i % 2 == 0 else "assistant",
                "value": cur_conversations[i]
            } for i in range(len(cur_conversations))
        ]}

def save_results(data, data_id2file_name) -> None:
    # try:
    #     with open(os.path.join(JSON_SAVE_PATH,'data.json')) as f:
    #         existing_data = json.load(f)
    # except FileNotFoundError:
    #     existing_data = []
    # existing_data.append(data)
    # 如果要实现追加，把下面的data改成existing_data，并消除上面六行的注释即可。
    with open(os.path.join(JSON_SAVE_PATH, 'data.json'), 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
    # 如果要实现追加，把w修改成a模式即可。
    with open(os.path.join(JSON_SAVE_PATH, 'map.csv'), 'w', encoding='utf-8') as csv_file:
        csv_file.write("data_id,file_name\n")
        for key, value in data_id2file_name.items():
            csv_file.write(f"{key},{value}\n")

def parse_dict_arg(arg_str):
    try:
        parsed_dict = ast.literal_eval(arg_str)
        if not isinstance(parsed_dict, dict):
            raise ValueError("Input is not in a valid dictionary format.")
        return parsed_dict
    except (SyntaxError, ValueError):
        raise argparse.ArgumentTypeError("Unable to parse the input as a valid dictionary.")

def get_command_line_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--exp', type=str, default='meishichina')
    parser.add_argument('--infer', nargs='*', default=None, required=True)
    parser.add_argument("--fit-kwargs", type=parse_dict_arg, default={}, help="Provide a dictionary-like argument")

    args, _ = parser.parse_known_args()
    parser = ArgumentParser(parents=[parser], add_help=False)

    return args, parser

import pprint
_utils_pp = pprint.PrettyPrinter()
def pprint(x):
    _utils_pp.pprint(x)
