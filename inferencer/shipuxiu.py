from typing import Dict, Any, List

from utils import load_pickle, preprocess_text
from inferencer import BaseInferencer

class ShipuxiuInferencer(BaseInferencer):
    def __init__(self,
                 types: List[str],
                 **kwargs) -> None:
        super().__init__(types=types)
        ...

    def load(self,
             file_name: str,
             **kwargs) -> Dict[str, Any]:
        cur_data = load_pickle(file_name)
        try:
            del cur_data['components'][' ']
        except:
            pass
        cur_data = {
            'id': cur_data['id'],
            'title': cur_data['title'],
            'img': cur_data['title_img'],
            'type': cur_data['title_img_type'],
            'description': "",
            'components_nested': {'材料':cur_data['components']},
            'components_flat': cur_data['components'],
            'steps': cur_data['steps'],
        }

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
            cur_data['steps'][i]['description'] = preprocess_text(cur_data['steps'][i]['description'])
        
        return cur_data

