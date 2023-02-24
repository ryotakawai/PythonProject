from PIL import Image
from pathlib import Path
import pandas as pd
import numpy as np

# 前回まで作成したデータセットクラスDatasetを用いて、
# データセットを操作するためのデータセットクラスを定義
class HiraganaDataset():

    class Dataset():

        def __init__(self, images, labels):
            self._images = images
            self._labels = labels
        
        # -----------------------------------------------------------------------------
        # トレーニング時にバッチ学習を実施できるようにするための補助機能を作成する。
        # データセットからバッチ単位でデータを取り出すためのイテレータを実装する。
        # このイテレータはデータセット全体を一巡するまで、画像とラベルの組を返し続ける。
        # -----------------------------------------------------------------------------
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


    def load_data(self, dataset_root, csv_file, one_hot=False):
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
        images = np.stack(images)
        labels = np.array(labels, dtype=np.uint8)
        if one_hot:
            labels = np.eye(len(hexcodes))[labels]
        return images, labels
    
    
    def __init__(self, one_hot=False):
        train_images, train_labels = self.load_data(
            dataset_root="./hiragana73",
            csv_file="./hiragana73_train.csv",
            one_hot=one_hot)
        test_images, test_labels = self.load_data(
            dataset_root="./hiragana73",
            csv_file="./hiragana73_test.csv",
            one_hot=one_hot)
        self.train = self.Dataset(train_images, train_labels)
        self.test = self.Dataset(test_images, test_labels)
        self.n_classes = 73

