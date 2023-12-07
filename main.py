import re
import os
import glob
import json
from tqdm import tqdm
from pathlib import Path
from typing import List
from utils import download_img, get_class_from_module, save_results, get_command_line_parser, pprint, ID_COUNTER
from inferencer import EXP_STR2CLASS_NAME
import configs
from configs import DATA_PATHS

class GenerateInstances():
    def __init__(self,
                 exp_str: str,
                 infer_strs: List[str]) -> None:
        configs.JSON_SAVE_PATH = os.path.join(configs.JSON_SAVE_PATH, exp_str)
        Path(configs.JSON_SAVE_PATH).mkdir(parents=True, exist_ok=True)

        cur_data_json_file = os.path.join(configs.JSON_SAVE_PATH, 'data.json')
        ID_COUNTER.set_str(exp_str)
        if os.path.isfile(cur_data_json_file):
            with open(cur_data_json_file, 'r', encoding='utf-8') as json_file:
                loaded_data = json.load(json_file)
            if len(loaded_data) != 0:
                ID_COUNTER.config(ID_COUNTER.str2int(loaded_data[-1]['id']))
        self.exp_str = exp_str
        self.infer_strs = infer_strs
        inferencer_class = get_class_from_module('inferencer', EXP_STR2CLASS_NAME[exp_str])
        assert inferencer_class is not None, 'Inferencer class import failed.'
        self.inferencer = inferencer_class(types=infer_strs)

    def run(self, **fit_kwargs) -> None:
        results, results_data_id2file_name = [], {}
        files = glob.glob(os.path.join(DATA_PATHS[self.exp_str], "*.pkl"))
        for pkl_file in tqdm(files):
            cur = self.inferencer.load(pkl_file)
            if not len(cur):
                continue

            cur = self.inferencer.fit(cur, **fit_kwargs)

            results_data_id2file_name.update({i['id']: pkl_file for i in cur})
            results.extend(cur)

        save_results(results, results_data_id2file_name)

def main():
    args, _ = get_command_line_parser()
    pprint(vars(args))
    generator = GenerateInstances(
        exp_str=args.exp,
        infer_strs=args.infer
        )
    generator.run(**args.fit_kwargs)

if __name__ == '__main__':
    main()
