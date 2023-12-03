import os
from typing import List, Any, Dict
import random

from utils import download_img, make_data_dict, ID_COUNTER, LOGGER, log_failed_img
from configs import IMG_SAVE_PATH

def what_are_step_imgs_doing(
    data: Dict[str, Any],
    what_are_step_num_imgs: int = 3,
    what_are_step_num_iters: int = 1,
    **kwargs) -> List[Any]:
    results = []
    if len(data['steps']) == 0:
        return results

    for _ in range(what_are_step_num_iters):
        cur_sampled = random.sample(range(len(data['steps'])), what_are_step_num_imgs)
        img_file_list = []
        for img_idx in cur_sampled:
            cur_step = data['steps'][img_idx]
            img_file = os.path.join(IMG_SAVE_PATH, f"{data['id']}_{str(ID_COUNTER)}_{what_are_step_imgs_doing.__name__}_{img_idx}.jpg")

            if os.path.isfile(img_file):
                LOGGER.warning(f'img has been downloaded in {what_are_step_num_imgs.__name__}: [{img_file}]')

            if not download_img(
                cur_step['img'],
                img_file
                ):
                LOGGER.debug(f"img download failed, url: [{cur_step['img']}]")
                log_failed_img(str(ID_COUNTER), cur_step['img'], img_file)
                # continue

            img_file_list.append(img_file)
        if len(img_file_list) != len(cur_sampled):
            continue

        results.append(
            make_data_dict(
                cur_id=str(ID_COUNTER),
                cur_conversations=[
                    '，'.join([f"({cur_idx + 1}) <img>{cur_img_file}</img>" for cur_idx, cur_img_file in enumerate(img_file_list)])
                        + f"，这些图中在做什么？",
                    ''.join([f"图 ({cur_idx + 1})：{data['steps'][img_idx]['description']}" for cur_idx, img_idx in enumerate(cur_sampled)]) + '。'
                ]
            )
        )
        ID_COUNTER.increment()
    return results
