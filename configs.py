from pathlib import Path

DATA_PATHS = {
    'meishichina': f'data/meishichina',
    'daydaycook': f'data/daydaycook',
    'douguo': f'data/douguo',
    'xiachufang': f'data/xiachufang',
    'xinshipu': f'data/xinshipu'
}

IMG_SAVE_PATH = 'results/imgs'
Path(IMG_SAVE_PATH).mkdir(parents=True, exist_ok=True)

JSON_SAVE_PATH = 'results'
