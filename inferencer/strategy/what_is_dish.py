import os
from typing import List, Any, Dict

from utils import download_img, make_data_dict, ID_COUNTER, LOGGER, log_failed_img
from configs import IMG_SAVE_PATH

def what_is_dish(data: Dict[str, Any], **kwargs) -> List[Any]:
    results = []
    img_file = os.path.join(IMG_SAVE_PATH, f"{data['id']}_{str(ID_COUNTER)}_{what_is_dish.__name__}.jpg")

    if os.path.isfile(img_file):
        LOGGER.warning(f'img has been downloaded in {what_is_dish.__name__}: [{img_file}]')

    if not download_img(
        data['img'],
        img_file
        ):
        LOGGER.debug(f"img download failed, url: [{data['img']}]")
        log_failed_img(str(ID_COUNTER), data['img'], img_file)
        # return results

    results.append(
        make_data_dict(
            cur_id=str(ID_COUNTER),
            cur_conversations=[
                f"图：<img>{img_file}</img>，图中这道菜叫什么名字？",
                f"{data['title']}"
            ]
        )
    )
    ID_COUNTER.increment()

    return results
