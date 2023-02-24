"""
事前に学習済みの Haar Cascades という検出器を使って、顔や目、笑顔といったものを検出する
CascadeClassifier()を使って検出器を読み込む

下のリンクからカスケード分類器は入手できる
https://github.com/opencv/opencv/tree/master/data/haarcascades

"""

"""
<<エラー発生時の処理>>
AttributeError: partially initialized module 'cv2' has no attribute 'gapi_wip_gst_GStreamerPipeline' (most likely due to a circular import)
    $ pip install "opencv-python-headless<4.3"
    
"""

# OpenCV をインポート
import cv2

face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')

def detect_face(img):

    # 読み込んだ顔の画像をまずcopy()で複製する
    face_img = img.copy()

    # detectMultiScale()を使って顔検出を行う
    face_rects = face_cascade.detectMultiScale(face_img)

    """
    その結果をfor文を使って座標と幅と高さをそれぞれタプルとして取り出し、
    rectangle()を使って顔画像に四角形を描いていく。
    画像を渡し、2点の座標、色、線の太さを指定していく。
        cv2.rectangle(img, pt1, pt2, color, thickness, lineType, shift)
            img(Ndarray型) : 対象の画像データ
            pt1((int型, int型)) : 長方形の左上頂点の座標
            pt2((int型, int型)) : 長方形の右下頂点の座標
            color((int型, int型, int型)) : 線の色RGB
            thickness(int型) : 線の太さ
            lineType : 線を描画するアルゴリズム　※デフォルトは「cv2.LINE_8」
            shift(int型) : 小数点以下を表すビッド数
    """
    for (x,y,w,h) in face_rects:
        cv2.rectangle(face_img, (x,y), (x+w,y+h), (0,255,0), 10)

    return face_img


"""
カメラと接続してオブジェクトを生成
カメラが1台だけ接続された環境なのでデフォルトの0と指定
"""
cap = cv2.VideoCapture(0)

# OpenCVのカメラの設定値を取得
camera_parameter = ['CAP_PROP_FRAME_WIDTH',
 'CAP_PROP_FRAME_HEIGHT',
 'CAP_PROP_FOURCC',
 'CAP_PROP_BRIGHTNESS',
 'CAP_PROP_CONTRAST',
 'CAP_PROP_SATURATION',
 'CAP_PROP_HUE',
 'CAP_PROP_GAIN',
 'CAP_PROP_EXPOSURE',]

for x in range(9):
     print(camera_parameter[x], '=', cap.get(x))


# 取得画像の解像度を変更
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)

while True:

    # retで読み込みの可否(true or false)、frameで映像パラメータを取得
    ret, frame = cap.read(0)

    # 映像パラメータframeをdetect_face()を使って顔検出を行う
    frame = detect_face(frame)

    # 表示　※第1引数はタイトル
    cv2.imshow('Video Face Detection', frame)

    """
    1ミリ秒キーイベントを待ち、[esc]キーが押されたらbreakして終了させる
    27 という数字はASCII制御文字列で[esc]キーを意味する
    """
    if cv2.waitKey(1) & 0xFF == 27:
        break

# release()でデバイスを解放して終了させる
cap.release()
# destroyAllWindows()でウィンドウを破棄して操作を終了させる
cv2.destroyAllWindows()