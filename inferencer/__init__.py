from inferencer.base import BaseInferencer
from inferencer.meishichina import MeishiChinaInferencer
from inferencer.daydaycook import DaydaycookInferencer
from inferencer.douguo import DouGuoInferencer
from inferencer.xiachufang import XiachufangInferencer
from inferencer.xinshipu import XinshipuInferencer
from inferencer.meishijie import MeishiJieInferencer
from inferencer.shipuxiu import ShipuxiuInferencer

__all__ = [
    'BaseInferencer',
    'MeishiChinaInferencer',
    'DaydaycookInferencer',
    'DouGuoInferencer',
    'XiachufangInferencer',
    'XinshipuInferencer',
    'MeishiJieInferencer',
    'ShipuxiuInferencer'
    ]

EXP_STR2CLASS_NAME = {
    'meishichina': 'MeishiChinaInferencer',
    'daydaycook': 'DaydaycookInferencer',
    'douguo':'DouGuoInferencer',
    'xiachufang': 'XiachufangInferencer',
    'xinshipu': 'XinshipuInferencer',
    'meishijie': 'MeishiJieInferencer',
    'shipuxiu': 'ShipuxiuInferencer'
}
