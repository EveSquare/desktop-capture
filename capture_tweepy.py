import json, config #標準のjsonモジュールとconfig.pyの読み込み
from requests_oauthlib import OAuth1Session #OAuthのライブラリの読み込み
import tweepy
from PIL import ImageGrab
import sys
import numpy as np
import cv2
from matplotlib import pyplot as plt

# full screen
ImageGrab.grab().save("desk_capture.png")

# 先ほど取得した各種キーを代入する
CK="6eppxEHZgA6oBgLmwdMUnjOq8"
CS="dbpeIZwcFDcip6TP5HRp8Z9tf8A8mWXVLAogD7S9Gx3Jd5mMWf"
AT="1084114248874156032-CTx91Gp4yz21oTsDs3vhLzyrYr3eyS"
AS="VxIqOf9ityUzfUFaGkhfCzh1J7e9rdmqJvyfrhqljtMPd"

# Twitterオブジェクトの生成
auth = tweepy.OAuthHandler(CK, CS)
auth.set_access_token(AT, AS)
api = tweepy.API(auth)

print( "KOKONO >> ", end="")
str = input()
# グローーバル変数
drawing = False
complete_region = False
ix, iy, width, height = -1, -1, 0, 0
box = [ix, iy, width, height]


# マウスコールバック関数
def my_mouse_callback(event, x, y, flags, param):
    global ix, iy, width, height, box, drawing, complete_region

    if event == cv2.EVENT_MOUSEMOVE:  # マウスが動いた時
        if (drawing == True):
            width = x - ix
            height = y - iy

    elif event == cv2.EVENT_LBUTTONDOWN:  # マウス左押された時
        drawing = True

        ix = x
        iy = y
        width = 0
        height = 0

    elif event == cv2.EVENT_LBUTTONUP:  # マウス左離された時
        drawing = False
        complete_region = True

        if (width < 0):
            ix += width
            width *= -1
        if (height < 0):
            iy += height
            height *= -1

    box = [ix, iy, width, height]  # 切り取り範囲格納


# メイン関数
def main():
    global ix, iy, width, height, box, drawing, complete_region

    source_window = "draw_rectangle"
    roi_window = "region_of_image"

    img = cv2.imread('desk_capture.png')  # 画像の読み込み
    temp = img.copy()  # 画像コピー

    cv2.namedWindow(source_window)
    cv2.setMouseCallback(source_window, my_mouse_callback)

    while (1):
        cv2.imshow(source_window, temp)

        if (drawing):  # 左クリック押されてたら
            temp = img.copy()  # 画像コピー
            cv2.rectangle(temp, (ix, iy), (ix + width, iy + height), (0, 255, 0), 2)  # 矩形を描画

        if (complete_region):  # 矩形の選択が終了したら
            complete_region = False

            roi = img[iy:iy + height, ix:ix + width]  # 元画像から選択範囲を切り取り
            cv2.imshow(roi_window, roi)  # 切り取り画像表示

            # ヒストグラム作成
            color = ('b', 'g', 'r')
            for i, col in enumerate(color):
                histr = cv2.calcHist([roi], [i], None, [256], [0, 256])
                plt.plot(histr, color=col)
                plt.xlim([0, 256])

        # キー操作
        k = cv2.waitKey(1) & 0xFF
        if k == 27:  # esc押されたら終了
            break
        elif k == ord('s'):  # 's'押されたら画像を保存
            cv2.imwrite('roi.png', roi);
            api.update_with_media(status=str, filename='roi.png')
            break


    cv2.destroyAllWindows()



if __name__ == "__main__":
    main()


print('Done!')