from . import image_change as ic
from django.conf import settings

import numpy as np
from keras.models import load_model
import math

def ImageEncoding(byte_image_data):
    Image = ic.ByteImageChangeOne(byte_image_data)
    Image.add(ic.resize)
    Image.add(ic.remove_background)
    Image.add(ic.encoding)
    return Image.get()

def number_to_japanese(num):
    num_array = [int(digit) for digit in str(num)]
    # 日本語の数字表記
    japanese_big_units = ["", "万", "億", "兆"]

    length = len(num_array)
    kugiri = math.floor(length/4)+1
    add_cnt = 0

    for i in range(kugiri):
        index = length+add_cnt - (i*4+add_cnt)
        num_array.insert(index, japanese_big_units[i])
        add_cnt += 1
    return ''.join(map(str, num_array))

def Predict(byte_image_data):

    # モデルを読み込む
    model = load_model(settings.TRAINED_MODELS_PATH)
    label = [settings.WEEK_SCORE,settings.NORMAL_SCORE,settings.STRONG_SCORE]#['week', 'normal', 'strong']

    image = ic.ByteImageChangeOne(byte_image_data)
    image.add(ic.remove_background)
    image.add(ic.resize)
    image.add(ic.gray)

    image_data = image.get()

    # 予測
    image_data = np.expand_dims(image_data, axis=0) 
    pred = model.predict(image_data, batch_size=1, verbose=0)

    score = np.max(pred)
    pred_label = label[np.argmax(pred[0])]

    return math.floor(score * pred_label)
