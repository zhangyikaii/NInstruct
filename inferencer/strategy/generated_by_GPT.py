import os
from typing import List, Any, Dict

from utils import download_img, make_data_dict, ID_COUNTER, LOGGER, GPT, remove_non_chinese_digits, log_failed_img
from configs import IMG_SAVE_PATH, RAW_PROMPT
import re

def generated_by_GPT(data: Dict[str, Any], **kwargs) -> List[Any]:
    results = []
    img_file = os.path.join(IMG_SAVE_PATH, f"{data['id']}_{str(ID_COUNTER)}_{generated_by_GPT.__name__}.jpg")

    if os.path.isfile(img_file):
        LOGGER.warning(f'img has been downloaded in {generated_by_GPT.__name__}: [{img_file}]')

    if not download_img(
        data['img'],
        img_file
        ):
        LOGGER.debug(f"img download failed, url: [{data['img']}]")
        log_failed_img(str(ID_COUNTER), data['img'], img_file)
        # return results

    keys = data.keys()
    prompt = ''

    for i in keys:
        if i == 'title':
            prompt += '标题：\n' + data[i] + '\n'
        if i == 'description':
            prompt += '描述：\n' + data[i] + '\n'
        if i == 'tips':
            if data[i]:
                prompt += '诀窍：\n' + data[i] + '\n'
        if i == 'components_nested':
            if data[i]:
                for k, v in data[i].items():
                    prompt += k + '：\n'
                    for l, s in v.items():
                        prompt += l + s + ','
                    prompt += '\n'
        if i == 'components_flat':
            if data[i]:
                for k, v in data[i].items():
                    prompt += k + '：' + 'v'
                    prompt += '\n'
        if i == 'steps':
            if data[i]:
                prompt += '步骤：\n'
                for j in data[i]:
                    prompt += j['description'] + '\n'
        if i == 'comments':
            if data[i]:
                prompt += '评论：\n'
                for j in data[i]:
                    for k in j:
                        prompt += k + '        '
                    prompt += '\n'


    gpt = GPT()
    response = gpt.answer(RAW_PROMPT + '\n' + prompt)

    response = response.split()

    non_chinese_digits_response = []

    for i in range(len(response)):
        non_chinese_digits_response.append(remove_non_chinese_digits(response[i]))

    split_response = []
    for item in non_chinese_digits_response:
        if '输入' in item or '输出' in item or '指令' in item:
            index = re.search('输入', item)
            if index is None:
                index = re.search('输出', item)
            if index is None:
                index = re.search('指令', item)
            index = index.start()
            split_response.append(item[:index + 2])
            try:
                split_response.append(item[index + 2:])
            except Exception as e:
                pass
        else:
            split_response.append(item)

    final_response = [item for item in split_response if item.strip() != ""]

    for i in range(len(final_response)):
        if '指令' in final_response[i]:
            results.append(
                make_data_dict(
                    cur_id=str(ID_COUNTER),
                    cur_conversations=[
                     '图：' + '<img>' + img_file + '</img>'+',' + final_response[i + 1],
                        final_response[i + 5]
                    ]
                )
            )
            ID_COUNTER.increment()
    # results.append(
    #     make_data_dict(
    #         cur_id=str(ID_COUNTER),
    #         cur_conversations=[
    #             f"图：<img>{img_file}</img>，图中这道菜叫什么名字？",
    #             f"{data['title']}"
    #         ]
    #     )
    # )
    # ID_COUNTER.increment()

    return results
