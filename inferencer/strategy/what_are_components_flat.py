import os
from typing import List, Any, Dict

from utils import download_img, make_data_dict, ID_COUNTER, LOGGER, log_failed_img
from configs import IMG_SAVE_PATH

def what_are_components_flat(
    data: Dict[str, Any],
    what_are_components_flat_skipped_keys: List[str] = [],
    **kwargs) -> List[Any]:
    results = []
    img_file = os.path.join(IMG_SAVE_PATH, f"{data['id']}_{str(ID_COUNTER)}_{what_are_components_flat.__name__}.jpg")

    if os.path.isfile(img_file):
        LOGGER.warning(f'img has been downloaded in {what_are_components_flat.__name__}: [{img_file}]')

    if not download_img(
        data['img'],
        img_file
        ):
        LOGGER.debug(f"img download failed, url: [{data['img']}]")
        log_failed_img(str(ID_COUNTER), data['img'], img_file)
        # return results

    for first_component in data['components_flat'].keys():
        if first_component in what_are_components_flat_skipped_keys:
            continue
        results.append(
            make_data_dict(
                cur_id=str(ID_COUNTER),
                cur_conversations=[
                    f"图：<img>{img_file}</img>，图中这道菜的{first_component}怎么样？",
                    f"{data['components_flat'][first_component]}。"
                ]
            )
        )
        ID_COUNTER.increment()

    return results
