import tensorflow as tf

def matmul_plus_bias_with_dropout(x, w, b, p):
    return tf.matmul(tf.nn.dropout(x, keep_prob=p), w) + b

def network(x, p_1, p_2, n_classes=73):
    """
    文字認識のネットワークモデルを定義します。
    :param x: 画像
    :param p_1: ドロップアウト率
    :param p_2: ドロップアウト率
    :return: 最終層の出力
    """

    """
    MNISTネットワークとの変更点
    ・ラベルは73種類あるため、n_classesの値を変更
    ・畳み込みレイヤを1つ追加
    ・画像サイズ(48×48)に合わせて、カーネルサイズとストライド(カーネルの移動間隔)を変更
    """

    # Input: 48x48x3
    # 入力は [batch, in_height, in_width, in_channels] の順で定義する
    x = tf.reshape(x, [-1, 48, 48, 3])
    
    # Conv1: 48x48x3 -> 23x23x15
    # カーネルは [filter_height, filter_width, in_channels, out_channels] の順で定義する
    k = tf.Variable(tf.truncated_normal([4, 4, 3, 15], mean=0.0, stddev=0.1))
    x = tf.nn.conv2d(x, k, strides=[1, 2, 2, 1], padding='VALID')
    # ReLU1
    x = tf.nn.relu(x)

    # Conv2: 23x23x15 -> 11x11x30
    k = tf.Variable(tf.truncated_normal([3, 3, 15, 30], mean=0.0, stddev=0.1))
    x = tf.nn.conv2d(x, k, strides=[1, 2, 2, 1], padding='VALID')
    # ReLU2
    x = tf.nn.relu(x)

    # MaxPool: 11x11x30 -> 5x5x30
    x = tf.nn.max_pool(x, ksize=[1, 3, 3, 1], strides=[1, 2, 2, 1], padding='VALID')
    
    # Flatten: 5x5x30 -> 750
    x = tf.reshape(x, [-1, 750])

    # Dense&Dropout: 750 -> 200
    w = tf.Variable(tf.zeros([750, 200]))
    b = tf.Variable([0.1] * 200)
    x = matmul_plus_bias_with_dropout(x, w, b, p_1)
    # ReLU3
    x = tf.nn.relu(x)

    # Dense&Dropout: 200 -> 73
    w = tf.Variable(tf.zeros([200, n_classes]))
    b = tf.Variable([0.1] * n_classes)
    x = matmul_plus_bias_with_dropout(x, w, b, p_2)
    # Softmax
    y = tf.nn.softmax(x, name='y')

    return y