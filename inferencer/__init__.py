from inferencer.base import BaseInferencer
from inferencer.meichichina import MeishiChinaInferencer

__all__ = [
    'BaseInferencer',
    'MeishiChinaInferencer'
    ]

EXP_STR2CLASS_NAME = {
    'meishichina': 'MeishiChinaInferencer'
}