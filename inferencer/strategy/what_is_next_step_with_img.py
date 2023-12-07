import os
from typing import List, Any, Dict
import random

from utils import download_img, make_data_dict, ID_COUNTER, LOGGER, log_failed_img, log_img
from configs import IMG_SAVE_PATH


def what_is_next_step_with_img(data: Dict[str, Any], what_is_next_step_num_iters: int = 1, **kwargs) -> List[Any]:
    results = []
    if len(data['steps']) == 0:
        return results

    cur_steps = random.sample(
        list(range(len(data['steps']) - 1)),
        min(what_is_next_step_num_iters, len(data['steps']) - 1)
        )
    for i in cur_steps:
        cur_step = data['steps'][i]
        next_step = data['steps'][i + 1]

        img_file_name = log_img(cur_step['img'])
        img_file = os.path.join(IMG_SAVE_PATH, img_file_name)

        # if os.path.isfile(img_file):
        #     LOGGER.warning(
        #         f'img has been downloaded in {what_is_next_step_with_img.__name__}: [{img_file}]'
        #     )

        # if not download_img(cur_step['img'], img_file):
        #     LOGGER.debug(f"img download failed, url: [{cur_step['img']}]")
        #     log_failed_img(str(ID_COUNTER), cur_step['img'], img_file)

        results.append(
            make_data_dict(
                cur_id=str(ID_COUNTER),
                cur_conversations=[
                    #    response['指令'],
                    #    response['输入'],
                    #    response['输出']
                    f'在做菜品{data["title"]}时，完成<img>{img_file}</img>后，下一步是什么？对应的图片是什么？',
                    f'下一步是{next_step["description"]}，对应的图片是<img>{img_file}</img>'
                ]))
        ID_COUNTER.increment()
    return results
