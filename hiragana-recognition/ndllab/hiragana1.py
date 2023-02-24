from PIL import Image
from pathlib import Path
import pandas as pd


# データセットクラスを定義
class Dataset():

    def __init__(self, images, labels):
        self._images = images
        
    @property
    def images(self):
        return self._images


# CSVファイルから画像を読み込む
def load_data(dataset_root, csv_file, one_hot=False):
    images = list()
    if not isinstance(dataset_root, Path):
        dataset_root = Path(dataset_root)
    if not isinstance(csv_file, Path):
        csv_file = Path(csv_file)
    df = pd.read_csv(csv_file)
            
    for row in df.itertuples():
        # 画像ファイルをカラー画像(RGB)として読み込む
        image_path = dataset_root / row.hexcode / row.filename
        image = Image.open(image_path).convert('RGB')
        images.append(image)
    return images

