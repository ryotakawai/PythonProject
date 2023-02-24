from PIL import Image
from pathlib import Path
import pandas as pd


# データセットクラスを定義
class Dataset():

    def __init__(self, images, labels):
        self._images = images
        self._labels = labels
        
    @property
    def images(self):
        return self._images
    
    @property
    def labels(self):
        return self._labels


# CSVファイルから画像とラベルを読み込む
def load_data(dataset_root, csv_file, one_hot=False):
    images = list()
    labels = list()
    if not isinstance(dataset_root, Path):
        dataset_root = Path(dataset_root)
    if not isinstance(csv_file, Path):
        csv_file = Path(csv_file)
    df = pd.read_csv(csv_file)

    hexcodes = sorted(df['hexcode'].unique().tolist())

    for row in df.itertuples():
        image_path = dataset_root / row.hexcode / row.filename
        image = Image.open(image_path).convert('RGB')
        images.append(image)
        labels.append(hexcodes.index(row.hexcode))
    return images, labels

