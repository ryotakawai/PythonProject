import numpy as np
from imblearn.over_sampling import RandomOverSampler
from ndllab.hiragana6 import Dataset


class OverSampler():

    class OverSampledDataset(Dataset):
        pass

    def __init__(self):
        self.sampler = RandomOverSampler(sampling_strategy='not majority')

    def resample_from_dataset(self, dataset):
        """
        不均衡データに対してオーバーサンプリングを適用し、均衡データにします。
        """
        image_shape = dataset.images.shape
        label_shape = dataset.labels.shape

        # リサンプリングを行う
        # 事前にX, yの入力サイズに合わせて、データを変形する
        X = np.reshape(dataset.images, (image_shape[0], -1))
        if len(label_shape) == 2:
            y = np.argmax(dataset.labels, axis=1)
        else:
            y = dataset.labels
        self.sampler.fit_resample(X, y)

        # リサンプリングの結果を用いて、データセットを再生成する
        idx = self.sampler.sample_indices_
        return self.OverSampledDataset(dataset.images[idx], dataset.labels[idx])
