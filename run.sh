source activate zykycy
python main.py --exp daydaycook --infer how_to_sort_step_imgs what_are_components_flat what_are_components_nested what_are_step_imgs_doing what_is_dish what_is_step_img_doing --fit-kwargs "{'how_to_sort_num_iters': 2, 'what_are_step_num_iters': 2, 'what_are_components_nested_skipped_keys': ['方法']}"
