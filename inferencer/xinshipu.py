from typing import Dict, Any, List
import re
from utils import load_pickle, preprocess_text, preprocess_strip_begin_numbers
from inferencer import BaseInferencer
import jieba.posseg as pseg

class XinshipuInferencer(BaseInferencer):
    def __init__(self,
                 types: List[str],
                 **kwargs) -> None:
        super().__init__(types=types)
        ...

    def load(self,
             file_name: str,
             **kwargs) -> Dict[str, Any]:
        cur_data = load_pickle(file_name)

        cur_data1 = {}
        try:
            cur_data1['id'] = cur_data['id']
        except Exception as e:
            cur_data1['id'] = ''

        try:
            cur_data1['title'] = cur_data['title']
        except Exception as e:
            cur_data1['title'] = ''

        try:
            cur_data1['img'] = cur_data['title_img']
        except Exception as e:
            cur_data1['img'] = ''

        try:
            cur_data1['type'] = cur_data['title_img_type']
        except Exception as e:
            cur_data1['type'] = ''

        try:
            cur_data1['description'] = cur_data['description']
        except Exception as e:
            cur_data1['description'] = ''

        if cur_data1['description'] is None:
            cur_data1['description'] = ''

        # try:
        #     cur_data1['components_nested'] = {'材料': cur_data['components']}
        # except Exception as e:
        #     cur_data1['components_nested'] = {}
        #
        # for k, v in cur_data1['components_nested'].items():
        #     for l, s in v.items():
        #         if s is None:
        #             cur_data1['components_nested'][k][l] = ''

        cur_data1['components_nested'] = {'材料':{}}
        flag = 0
        quantifier = None

        try:
            for i in cur_data['components']:
                match = re.search(r"\d", i)
                if match:
                    index = match.start()
                    cur_data1['components_nested']['材料'][i[:index]] = i[index:]
                elif '量' in i:
                    index = re.search('量', i).start()
                    cur_data1['components_nested']['材料'][i[:index-1]] = i[index-1:]
                else:
                    words = pseg.cut(i)
                    for word, flag1 in words:
                        if flag1 == 'm':
                            quantifier = word
                            break
                    if quantifier is None:
                        flag = 1
                    else:
                        index = re.search(quantifier, i).start()
                        cur_data1['components_nested']['材料'][i[:index]] = i[index:]
        except Exception as e:
            cur_data1['components_nested'] = {}
            cur_data1['description'] += '     材料：' + ','.join(cur_data['components']) + '\n'
            flag = 0

        if len(cur_data['components']) == 0:
            cur_data1['components_nested'] = {}

        if flag:
            cur_data1['components_nested'] = {}
            cur_data1['description'] += '\n     材料：' + ','.join(cur_data['components']) + '\n'

        cur_data1['components_flat'] = {}

        if len(cur_data['steps']) == 0:
            cur_data1['steps'] = []
        elif len(cur_data['steps']) == 1:
            cur_data1['steps'] = []
            cur_data1['description'] += '     步骤：' + cur_data['steps'][0]['description'] + '\n'
        else:
            try:
                cur_data1['steps'] = cur_data['steps']
            except Exception as e:
                cur_data1['steps'] = []


        try:
            cur_data1['tips'] = cur_data['tips']
        except Exception as e:
            cur_data1['tips'] = ''

        if cur_data1['tips'] is None:
            cur_data1['tips'] = ''

        try:
            cur_data1['comments'] = cur_data['comments']
        except Exception as e:
            cur_data1['comments'] = []

        cur_data = cur_data1

        for i in range(len(cur_data['steps'])):
            step = cur_data['steps'][i]
            step_key = step.keys()
            if 'description' not in step_key:
                cur_data['steps'][i]['description'] = ''
            if 'img' not in step_key:
                cur_data['steps'][i]['img'] = ''

        # NOTE: 完善类型检查
        assert isinstance(cur_data['title'], str)

        def assert_str_or_list_of_str(text):
            assert isinstance(text, str) \
                   or isinstance(text, list) and all(isinstance(i, str) for i in text)

        assert_str_or_list_of_str(cur_data['img'])
        assert_str_or_list_of_str(cur_data['type'])
        assert isinstance(cur_data['description'], str)
        assert isinstance(cur_data['components_nested'], dict) \
               or all(isinstance(value, dict) for value in cur_data['components_nested'].values())
        assert all(isinstance(i, dict) and 'description' in i and 'img' in i for i in cur_data['steps'])

        # 文本预处理
        cur_data['title'] = preprocess_text(cur_data['title'])
        cur_data['description'] = preprocess_text(cur_data['description'])
        for key1, inner_dict in cur_data['components_nested'].items():
            for key2, value in inner_dict.items():
                cur_data['components_nested'][key1][key2] = preprocess_text(value)
        for key in cur_data['components_flat'].keys():
            cur_data['components_flat'][key] = preprocess_text(cur_data['components_flat'][key])
        for i in range(len(cur_data['steps'])):
            cur_data['steps'][i]['description'] = preprocess_text(preprocess_strip_begin_numbers(cur_data['steps'][i]['description']))

        return cur_data