from typing import Dict, Any, List

from utils import load_pickle, preprocess_text
from inferencer import BaseInferencer

class MeishiJieInferencer(BaseInferencer):
    def __init__(self,
                 types: List[str],
                 **kwargs) -> None:
        super().__init__(types=types)
        ...

    def load(self,
             file_name: str,
             **kwargs) -> Dict[str, Any]:
        cur_data = load_pickle(file_name)
        ii = list(cur_data['components'].keys())
        ii.remove('方法')
        cur_data = {
            'id': cur_data['id'],
            'title': cur_data['title'],
            'img': cur_data['title_img'],
            'type': cur_data['title_img_type'],
            'description': cur_data['description'],
            'components_nested': {k: {list(i.keys())[0]: list(i.values())[0]} for k in ii for
                                  i in cur_data['components'][k]},
            'components_flat': {'工艺':str(i) for i in cur_data['components']['方法']},
            'steps': cur_data['steps'],
        }
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
            cur_data['steps'][i]['description'] = preprocess_text(cur_data['steps'][i]['description'])

        return cur_data


