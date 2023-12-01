from inferencer.base import BaseInferencer
from inferencer.meichichina import MeishiChinaInferencer
from inferencer.douguo import DouGuoInferencer

__all__ = [
    'BaseInferencer',
    'MeishiChinaInferencer',
    'DouGuoInferencer'
    ]

EXP_STR2CLASS_NAME = {
    'meishichina': 'MeishiChinaInferencer',
    'douguo':'DouGuoInferencer'
}