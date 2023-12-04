from openai import OpenAI
import os
from typing import List, Any, Dict
import random
import json
from utils import download_img, make_data_dict, ID_COUNTER, LOGGER
from configs import IMG_SAVE_PATH
import openai
import os
os.environ["OPENAI_API_KEY"] = "sk-"
client = OpenAI()
# openai.api_key = "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"
prompt0 = "请基于数据描述和一些示例任务，设计更多任务，并以一个字典返回，包括指令、输入和输出字段。数据描述：菜名：DIY腌糖蒜，描述：腌好的糖蒜鲜而不辣，酸甜可口，最重要的一点是用这种方法腌的糖蒜吃过后嘴里不会有蒜味！去除了你吃蒜后怕口中有大蒜味的后顾之忧。主要步骤：(1) 准备好新鲜的大蒜。(2) 将鲜蒜去须茎，剥去外皮，放在清水中泡3天（每天换2到3次水，以去掉蒜的异味）。主要材料：主料新鲜大蒜200g、醋500ml，辅料水200ml。注意事项：注意要及时端离火口，静置放凉。示例任务：{'指令': '请回答菜品的主要原材料', '输入': '腌糖蒜', '输出': '主料新鲜大蒜200g、醋500ml，辅料水200ml。'}{'指令': '请回答制作菜品时的注意事项', '输入': '腌制糖蒜'， '输出': '注意要及时端离火口，静置放凉。'}"
# response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}])
# response = response["choices"][0]["message"]["content"]
tr = "{'指令': '请回答菜品的主要原材料', '输入': '腌糖蒜', '输出': '主料新鲜大蒜200g、醋500ml，辅料水200ml。'}{'指令': '请回答制作菜品时的注意事项', '输入': '腌制糖蒜'， '输出': '注意要及时端离火口，静置放凉。'}"
tr = json.load(tr)
print(tr['指令'])
def gpt_generation(
    data: Dict[str, Any],
    **kwargs) -> List[Any]:
    results = []
    if len(data['steps']) == 0:
        return results
    if len(data['components'].keys()) == 0:
        return results
    prompt = [f'数据描述:菜名：{data["title"]}，'+f'描述：{data["description"]}'
              +'主要步骤:'+''.join([f" ({i + 1}){data['steps'][i]['description']}" for i in range(len(data['steps']))])
              +'主要材料:'+'，'.join([f"{i}"+'、'.join([f"{list(data['components'][i][j].keys())[0]}{list(data['components'][i][j].values())[0]}" for j in range(len(data['components'][i]))]) for i in list(data['components'].keys())])
              ]
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "system", "content":prompt0},{"role": "user", "content": prompt}])
    response = response["choices"][0]["message"]["content"]
    response = json.load(response)
    results.append(
        make_data_dict(
            cur_id=str(ID_COUNTER),
            cur_conversations=[
               response['指令']+response['输入'],
               response['输出']
            ]
        )
    )
    ID_COUNTER.increment()
    return results