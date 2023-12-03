import os
from typing import List, Any, Dict
import random

from utils import download_img, make_data_dict, ID_COUNTER, LOGGER, log_failed_img
from configs import IMG_SAVE_PATH

def how_to_sort_step_imgs(
    data: Dict[str, Any],
    how_to_sort_num_sorted_imgs: int = 3,
    how_to_sort_num_iters: int = 1,
    **kwargs) -> List[Any]:
    results = []
    if len(data['steps']) == 0:
        return results
    for _ in range(how_to_sort_num_iters):
        cur_sampled = random.sample(range(len(data['steps'])), how_to_sort_num_sorted_imgs)
        img_file_list = []
        for img_idx in cur_sampled:
            cur_step = data['steps'][img_idx]
            img_file = os.path.join(IMG_SAVE_PATH, f"{data['id']}_{str(ID_COUNTER)}_{how_to_sort_step_imgs.__name__}_{img_idx}.jpg")

            if os.path.isfile(img_file):
                LOGGER.warning(f'img has been downloaded in {how_to_sort_step_imgs.__name__}: [{img_file}]')

            if not download_img(cur_step['img'], img_file):
                LOGGER.debug(f"img download failed, url: [{cur_step['img']}]")
                log_failed_img(str(ID_COUNTER), cur_step['img'], img_file)
                # continue

            img_file_list.append(img_file)
        if len(img_file_list) != len(cur_sampled):
            continue

        sorted_sampled_indices = sorted(range(len(cur_sampled)), key=lambda i: cur_sampled[i])
        results.append(
            make_data_dict(
                cur_id=str(ID_COUNTER),
                cur_conversations=[
                    '，'.join([f"({cur_idx + 1}) <img>{cur_img_file}</img>" for cur_idx, cur_img_file in enumerate(img_file_list)])
                        + f"，请理解图片中的制作步骤，并按顺序排序：",
                    "按照步骤排序如下：" + '，'.join([f"({cur_idx + 1})" for cur_idx in sorted_sampled_indices]) + '。'
                ]
            )
        )
        ID_COUNTER.increment()
    return results
