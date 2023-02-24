import tensorflow as tf
import os
from PIL import Image
import numpy as np
import cv2

graph_def = tf.compat.v1.GraphDef()
labels = []

# model.pb ファイルはトレーニング済みのモデル
filename = "./model_export/vegetable_tf/model.pb"

# labels.txt ファイルは分類ラベル
labels_filename = "./model_export/vegetable_tf/labels.txt"

# モデルをプロジェクトにロードする
with tf.io.gfile.GFile(filename, 'rb') as f:
    graph_def.ParseFromString(f.read())
    tf.import_graph_def(graph_def, name='')

with open(labels_filename, 'rt') as lf:
    for l in lf:
        labels.append(l.strip())


def convert_to_opencv(image):
    # RGB -> BGR conversion is performed as well.
    image = image.convert('RGB')
    r,g,b = np.array(image).T
    opencv_image = np.array([b,g,r]).transpose()
    return opencv_image

def crop_center(img,cropx,cropy):
    h, w = img.shape[:2]
    startx = w//2-(cropx//2)
    starty = h//2-(cropy//2)
    return img[starty:starty+cropy, startx:startx+cropx]

def resize_down_to_1600_max_dim(image):
    h, w = image.shape[:2]
    if (h < 1600 and w < 1600):
        return image

    new_size = (1600 * w // h, 1600) if (h > w) else (1600, 1600 * h // w)
    return cv2.resize(image, new_size, interpolation = cv2.INTER_LINEAR)

def resize_to_256_square(image):
    h, w = image.shape[:2]
    return cv2.resize(image, (256, 256), interpolation = cv2.INTER_LINEAR)

def update_orientation(image):
    exif_orientation_tag = 0x0112
    if hasattr(image, '_getexif'):
        exif = image._getexif()
        if (exif != None and exif_orientation_tag in exif):
            orientation = exif.get(exif_orientation_tag, 1)
            # orientation is 1 based, shift to zero based and flip/transpose based on 0-based values
            orientation -= 1
            if orientation >= 4:
                image = image.transpose(Image.TRANSPOSE)
            if orientation == 2 or orientation == 3 or orientation == 6 or orientation == 7:
                image = image.transpose(Image.FLIP_TOP_BOTTOM)
            if orientation == 1 or orientation == 2 or orientation == 5 or orientation == 6:
                image = image.transpose(Image.FLIP_LEFT_RIGHT)
    return image


# テストデータをロードする
#imageFile = "./vegetable/テストデータ/banana/reg0a6xjphd.jpeg"
imageFile = "./vegetable/テストデータ/cabbage/キャベツC-min-770x578.jpg"
image = Image.open(imageFile)

image = update_orientation(image)

image = convert_to_opencv(image)


# 寸法が1600を超える画像を処理する
image = resize_down_to_1600_max_dim(image)


# 中央の最大の正方形を切り取る
h, w = image.shape[:2]
min_dim = min(w,h)
max_square_image = crop_center(image, min_dim, min_dim)


# サイズを 256×256 に縮小する
augmented_image = resize_to_256_square(max_square_image)


# モデルの特定の入力サイズの中心を切り取る
with tf.compat.v1.Session() as sess:
    input_tensor_shape = sess.graph.get_tensor_by_name('Placeholder:0').shape.as_list()
network_input_size = input_tensor_shape[1]

augmented_image = crop_center(augmented_image, network_input_size, network_input_size)


# 推論処理：画像がテンソルとして準備されると、予測のためにモデルを介して送信することができる。
output_layer = 'loss:0'
input_node = 'Placeholder:0'

with tf.compat.v1.Session() as sess:
    try:
        prob_tensor = sess.graph.get_tensor_by_name(output_layer)
        predictions = sess.run(prob_tensor, {input_node: [augmented_image] })
    except KeyError:
        print ("Couldn't find classification output layer: " + output_layer + ".")
        print ("Verify this a model exported from an Object Detection project.")
        exit(-1)


# 結果表示：モデルを介して画像テンソルを実行した場合は、ラベルにマッピングする必要がある。
highest_probability_index = np.argmax(predictions)
print('Classified as: ' + labels[highest_probability_index])
print()

label_index = 0
for p in predictions:
    truncated_probablity = np.float64(np.round(p,8))
    print (labels[label_index], truncated_probablity)
    label_index += 1