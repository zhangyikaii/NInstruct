import re
import os
import glob
import json
from pathlib import Path
from typing import List
from utils import download_img, get_class_from_module, save_results, get_command_line_parser, pprint
from inferencer import EXP_STR2CLASS_NAME
from configs import DATA_PATHS

class GenerateInstances():
    def __init__(self,
                 exp_str: str,
                 infer_strs: List[str]) -> None:
        self.exp_str = exp_str
        self.infer_strs = infer_strs
        inferencer_class = get_class_from_module('inferencer', EXP_STR2CLASS_NAME[exp_str])
        assert inferencer_class is not None, 'Inferencer class import failed.'
        self.inferencer = inferencer_class(types=infer_strs)

    def run(self, **fit_kwargs) -> None:
        results, results_data_id2file_name = [], {}
        files = glob.glob(os.path.join(DATA_PATHS[self.exp_str], "*.pkl"))
        for pkl_file in files:
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
