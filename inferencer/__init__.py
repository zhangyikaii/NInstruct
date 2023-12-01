from inferencer.base import BaseInferencer
from inferencer.meichichina import MeishiChinaInferencer
from inferencer.daydaycook import DaydaycookInferencer

__all__ = [
    'BaseInferencer',
    'MeishiChinaInferencer',
    'DaydaycookInferencer',
    ]

EXP_STR2CLASS_NAME = {
    'meishichina': 'MeishiChinaInferencer',
    'daydaycook': 'DaydaycookInferencer',
}
