from pathlib import Path

DATA_PATHS = {
    'meishichina': f'data',
    'daydaycook' : f'data/daydaycook',
    'douguo': f'douguo_data'
}

IMG_SAVE_PATH = 'results/imgs'
Path(IMG_SAVE_PATH).mkdir(parents=True, exist_ok=True)

JSON_SAVE_PATH = 'results'
