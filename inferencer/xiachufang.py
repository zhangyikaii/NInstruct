from typing import Dict, Any, List

from utils import load_pickle, preprocess_text, preprocess_strip_begin_numbers
from inferencer import BaseInferencer


class XiachufangInferencer(BaseInferencer):
    def __init__(self,
                 types: List[str],
                 **kwargs) -> None:
        super().__init__(types=types)
        ...

    def load(self,
             file_name: str,
             **kwargs) -> Dict[str, Any]:
        cur_data = load_pickle(file_name)

        # keys = ['id', 'title', 'img', 'type', 'description', 'components_nested', 'components_flat', 'steps']

        # cur_data = {
        #     'id': cur_data['id'],
        #     'title': cur_data['title'],
        #     'img': cur_data['title_img'],
        #     'type': cur_data['title_img_type'],
        #     'description': cur_data['description'],
        #     'components_nested': {k: {list(i.keys())[0]: list(i.values())[0]} for k in cur_data['components'].keys() for
        #                           i in cur_data['components'][k]},
        #     'components_flat': {list(i.values())[0]: list(i.keys())[0] for i in cur_data['components']['方法']},
        #     'steps': cur_data['steps'],
        # }
        if len(cur_data.keys()) == 1 or '页面不存在' in cur_data['title'] or '你访问得太多了' in cur_data['title']:
            return {}

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

        try:
            cur_data1['components_nested'] = {'材料': cur_data['components']}
        except Exception as e:
            cur_data1['components_nested'] = {}

        for k, v in cur_data1['components_nested'].items():
            for l, s in v.items():
                if s is None:
                    cur_data1['components_nested'][k][l] = ''

        for k, v in cur_data1['components_nested'].copy().items():
            for l, s in v.copy().items():
                if s == '':
                    del cur_data1['components_nested'][k][l]

        cur_data1['components_flat'] = {}

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

