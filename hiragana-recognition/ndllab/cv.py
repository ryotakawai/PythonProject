from ndllab.hiragana6 import HiraganaDataset, Dataset
import sklearn.model_selection
import numpy as np


class KFold():

    def __init__(self, one_hot=False, cv=5):
        self._train = None
        self._val = None
        self._test = None
        self._one_hot = one_hot
        self.cv = 5
        self.baseset = HiraganaDataset(one_hot=self._one_hot, validation_size=0)
        self.n_classes = self.baseset.n_classes

    def next_train_val(self):
        """
        トレーニングセットとバリデーションセットの組を返すイテレータです。
        """
        base_images = self.baseset.train.images
        base_labels = self.baseset.train.labels
        # basesetはシャッフルされていないことに注意
        for train_index, val_index in sklearn.model_selection.KFold(n_splits=self.cv, shuffle=True).split(base_images):
            train_images = base_images[train_index]
            train_labels = base_labels[train_index]
            val_images = base_images[val_index]
            val_labels = base_labels[val_index]
            yield Dataset(train_images, train_labels), Dataset(val_images, val_labels)
    
    @property
    def test(self):
        """
        テストセットを返します。
        """
        return self.baseset.test
