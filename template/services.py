import numpy as np
import cv2
import os

from template.models import Templates, Images
from api.models import Transaction

from django.shortcuts import get_object_or_404

#===========================================
# private method
#===========================================
def handler( transaction ):
    # 画像の相対パス
    path = transaction.src_image.path

    # テンプレート画像
    template = get_object_or_404(Templates, pk=transaction.template_id)
    images = []
    for image in template.Images.all().order_by('rank'):
        images.append(image.path.file)

    # opencvでテンプレートマッチング
    opencv(path, images);


def opencv(path, images):
    print("path: " + path)
    print("images: " + str(path))

    # load the image image, convert it to grayscale, and detect edges
    template = cv2.imread(path)
    # grayscale
    template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    # detect edges
    template = cv2.Canny(template, 50, 200)

    # 結果格納パス
    resultPath = os.path.join(os.path.dirname(path), "result", os.path.basename(path))
    cv2.imwrite(resultPath, template);

    return True








