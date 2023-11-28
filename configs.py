from pathlib import Path

DATA_PATHS = {
    'meishichina': f'data',
}

IMG_SAVE_PATH = 'results/imgs'
Path(IMG_SAVE_PATH).mkdir(parents=True, exist_ok=True)

JSON_SAVE_PATH = 'results'
