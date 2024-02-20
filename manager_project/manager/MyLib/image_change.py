import cv2
import numpy as np
import os
from rembg import remove
from tqdm import tqdm
import base64

#画像のリサイズ
def resize(image,target_size=(256, 256)):
    return cv2.resize(image, target_size)

#グレースケール
def gray(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#二値化
def binary(image):
    _, binary_image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return binary_image

#ノイズ除去
def filter(image):
    return cv2.medianBlur(image, 5)


def contours_remove(image):
    # 連結成分を見つける
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(image, connectivity=8)

    # 面積が特定の閾値未満の連結成分を削除する
    min_area_threshold = 500  # この閾値を調整してください

    for label in range(1, num_labels):  # 0は背景なのでスキップします
        area = stats[label, cv2.CC_STAT_AREA]
        if area < min_area_threshold:
            image[labels == label] = 0  # 連結成分を削除
    
    return image

def contours(image):
    #輪郭検出 （cv2.ChAIN_APPROX_SIMPLE）
    contours, _ = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    filtered_contours = []
    for contour in contours:
        if cv2.contourArea(contour) > 200:  # 面積が一定値以上の輪郭のみを考慮
            filtered_contours.append(contour)

    #輪郭の描画
    cv2.drawContours(image, filtered_contours, -1, (0, 255, 0), 4, cv2.LINE_AA)

    return image

def remove_background(image):
    return remove(image)

def encoding(image):
    _, img_encoded = cv2.imencode('.jpg', image)
    # Base64エンコード
    img_str = base64.b64encode(img_encoded).decode()
    return img_str


#指定のフォルダ下にあるファイルのパスを取得
def get_all_file_names(folder_path):
    file_names = []
    for foldername, subfolders, filenames in os.walk(folder_path):
        for filename in filenames:
            file_names.append(os.path.join(foldername, filename))
    
    for filename in os.listdir(folder_path):
        new_path = os.path.join(folder_path,filename)
        if os.path.isfile(new_path):
            file_names.append(new_path)
    
    return file_names

#複数の画像を読み込む
def read_images(image_name_list):
    image_list = []
    for image_name in image_name_list:
        image = cv2.imread(image_name)
        image_list.append(image)
    return image_list


class ImageChange():
    #画像データを直接受け取る
    def __init__(self,image_list):

        self.job_list = []
        self.files = image_list
        
    def add(self,func):
        self.job_list.append(func)

    def get(self):
        file_list = []
        for image in tqdm(self.files, desc="Processing", unit="item"):
            for func in self.job_list:
                image = func(image=image)
            file_list.append(image)
        self.job_list = []
        
        return file_list
    
class ImageReadChange():
    #画像のパスのリストを受け取る
    def __init__(self,image_names):

        self.job_list = []
        self.files = read_images(image_names)
    
class ImageChangeOne(ImageChange):

    def __init__(self,image_path):
        self.job_list = []
        self.image = cv2.imread(image_path)

    def get(self):
        for func in self.job_list:
            self.image = func(image=self.image)
        self.job_list = []
        
        return self.image
    
class ByteImageChangeOne(ImageChangeOne):

    def __init__(self,img_array):
        self.job_list = []
        nparr = np.frombuffer(img_array, np.uint8)
        self.image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)#1はカラー画像