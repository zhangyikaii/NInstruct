from typing import Dict, Any, List, Tuple, Optional

from inferencer.strategy import STRATEGIES

class BaseInferencer():
    def __init__(self,
                 types: List[str]) -> None:
        self.inference_funcs = {
            i: STRATEGIES[i] for i in types
            }

    def load(self,
             file_name: str,
             **kwargs) -> Dict[str, Any]:
        raise NotImplementedError("Subclass must implement the 'load' method")

    def fit(self,
            data: Dict[str, Any],
            **kwargs) -> List[Any]:
        results = []
        for cur_stra in self.inference_funcs.keys():
            results.extend(self.inference_funcs[cur_stra](data, **kwargs))
        return results