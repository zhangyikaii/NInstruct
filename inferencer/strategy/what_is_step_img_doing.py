import os
from typing import List, Any, Dict

from utils import download_img, make_data_dict, ID_COUNTER, LOGGER, log_failed_img
from configs import IMG_SAVE_PATH

def what_is_step_img_doing(data: Dict[str, Any], **kwargs) -> List[Any]:
    results = []
    for idx, cur_step in enumerate(data['steps']):
        img_file = os.path.join(IMG_SAVE_PATH, f"{data['id']}_{str(ID_COUNTER)}_{what_is_step_img_doing.__name__}_{idx}.jpg")

        if os.path.isfile(img_file):
            LOGGER.warning(f'img has been downloaded in {what_is_step_img_doing.__name__}: [{img_file}]')

        if not download_img(
            cur_step['img'],
            img_file
            ):
            LOGGER.debug(f"img download failed, url: [{cur_step['img']}]")
            log_failed_img(str(ID_COUNTER), cur_step['img'], img_file)
            # continue

        results.append(
            make_data_dict(
                cur_id=str(ID_COUNTER),
                cur_conversations=[
                    f"图：<img>{img_file}</img>，图中在做什么？",
                    f"{cur_step['description']}"
                ]
            )
        )
        ID_COUNTER.increment()
    return results
