import os
from typing import List, Any, Dict

from utils import download_img, make_data_dict, ID_COUNTER, LOGGER, log_failed_img, log_img
from configs import IMG_SAVE_PATH

def what_is_dish(data: Dict[str, Any], what_is_dish_num_imgs: int = 2, **kwargs) -> List[Any]:
    results = []

    cur_data_img = [data['img']] if isinstance(data['img'], str) else data['img']
    cur_data_img = cur_data_img[:what_is_dish_num_imgs]
    cur_data_img_files = []
    for idx, cur_img in enumerate(cur_data_img):
        img_file_name = log_img(cur_img)
        img_file = os.path.join(IMG_SAVE_PATH, img_file_name)

        cur_data_img_files.append(img_file)
        # if not download_img(
        #     cur_img,
        #     img_file
        #     ):
        #     LOGGER.debug(f"img download failed, url: [{data['img']}]")
        #     log_failed_img(str(ID_COUNTER), data['img'], img_file)
        #     # return results

    results.append(
        make_data_dict(
            cur_id=str(ID_COUNTER),
            cur_conversations=[
                f"图：" + '，'.join([f"<img>{cur_img_file}</img>" for cur_img_file in cur_data_img_files]) + "，图中这道菜叫什么名字？",
                f"{data['title']}"
            ]
        )
    )
    ID_COUNTER.increment()

    return results
