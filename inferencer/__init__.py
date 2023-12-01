from inferencer.base import BaseInferencer
from inferencer.meichichina import MeishiChinaInferencer
from inferencer.daydaycook import DaydaycookInferencer
from inferencer.xiachufang import XiachufangInferencer
from inferencer.xinshipu import XinshipuInferencer

__all__ = [
    'BaseInferencer',
    'MeishiChinaInferencer',
    'DaydaycookInferencer',
    'XiachufangInferencer',
    'XinshipuInferencer'
    ]

EXP_STR2CLASS_NAME = {
    'meishichina': 'MeishiChinaInferencer',
    'daydaycook': 'DaydaycookInferencer',
    'xiachufang': 'XiachufangInferencer',
    'xinshipu': 'XinshipuInferencer'
}
