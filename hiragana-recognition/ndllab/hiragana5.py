from PIL import Image
from pathlib import Path
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np


class Dataset():

    def __init__(self, images, labels):
        self._images = images
        self._labels = labels

    def next_batch(self, batch_size, shuffle=True):
        size = self._labels.shape[0]
        permutation = np.arange(size)
        if shuffle:
            permutation = np.random.permutation(permutation)
        for i in range(0, size, batch_size):
            batch = permutation[i:i+batch_size]
            yield self._images[batch], self._labels[batch] 
        
    @property
    def images(self):
        return self._images

    @property
    def labels(self):
        return self._labels


# データセットクラスを定義
class HiraganaDataset():

    def _load_data(self, dataset_root, csv_file, one_hot=False):
        images = list()
        labels = list()
        if not isinstance(dataset_root, Path):
            dataset_root = Path(dataset_root)
        if not isinstance(csv_file, Path):
            csv_file = Path(csv_file)
        df = pd.read_csv(csv_file)

        self._hexcodes = sorted(df['hexcode'].unique().tolist())

        for row in df.itertuples():
            image_path = dataset_root / row.hexcode / row.filename
            image = Image.open(image_path).convert('RGB')
            images.append(image)
            labels.append(self._hexcodes.index(row.hexcode))
        images = np.stack(images)
        labels = np.array(labels, dtype=np.uint8)
        if one_hot:
            labels = np.eye(len(self._hexcodes))[labels]
        return images, labels
    
    def get_hexcode(self, label):
        return self._hexcodes[label]
    
    def get_character(self, label):
        return chr(int(self.get_hexcode(label)[1:], 16))

    def __init__(self, one_hot=False, validation_size=0.2):
        """
        平仮名データセットを生成します。
        :param one_hot: ラベルをone-hot表現で生成する場合True
        :param validation_size: バリデーションセットの割合
        """
        self._train = None
        self._val = None
        self._test = None
        self._one_hot = one_hot
        self._validation_size = validation_size
        self.n_classes = 73
    
    @property
    def train(self):
        if self._train is None and self._val is None:
            train_val_images, train_val_labels = self._load_data(
                dataset_root="./hiragana73",
                csv_file="./hiragana73_train.csv",
                one_hot=self._one_hot)
            train_images, val_images, train_labels, val_labels = train_test_split(
                train_val_images, train_val_labels, test_size=self._validation_size)
            self._train = Dataset(train_images, train_labels)
            self._val = Dataset(val_images, val_labels)
        return self._train

    @property
    def val(self):
        if self._train is None and self._val is None:
            self.train()
        return self._val
    
    @property
    def test(self):
        if self._test is None:
            test_images, test_labels = self._load_data(
                dataset_root="./hiragana73",
                csv_file="./hiragana73_test.csv",
                one_hot=self._one_hot)
            self._test = Dataset(test_images, test_labels)
        return self._test
