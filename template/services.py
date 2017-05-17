import numpy as np
import cv2
import os

from template.models import Templates, Images
from api.models import Transaction

from django.shortcuts import get_object_or_404

def handler(imagepath, templates):
    """
    :param imagepath: 
    :param templates: 
    :return: 
    """

    # 結果格納パス
    resultImage = os.path.join(os.path.dirname(imagepath), "result", os.path.basename(imagepath))
    # 結果格納フォルダー
    folder = os.path.dirname(resultImage);
    if not os.path.isdir(folder):
        # 存在しない場合、新規に作る
        os.mkdir(folder)


    # load the image image, convert it to grayscale, and detect edges
    template = cv2.imread(imagepath)
    # grayscale
    template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    # detect edges
    template = cv2.Canny(template, 50, 200)

    print("result image path : " + resultImage)
    cv2.imwrite(resultImage, template);



# 画像の相対パス
imagename = "transaction/cod_mw3.jpg";

# ROOT PATH
rootPath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 画像の絶対パス
imagepath = os.path.join(rootPath, "data", imagename)

id = 9

template = get_object_or_404(Templates, pk=id)
images = template.Images.all().order_by('rank')

items = []
for image in images:
    items.append(image.path)


print(items)
handler(imagepath, [])













