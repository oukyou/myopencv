import numpy as np
import cv2
import os

from template.models import Templates, Images
from api.models import Transaction

from django.shortcuts import get_object_or_404
from django.conf import settings
from django.contrib import messages

#===========================================
# private method
#===========================================
def handler( transaction ,request):
    # 画像の相対パス
    path = transaction.src_image.path

    # テンプレート画像
    template = get_object_or_404(Templates, pk=transaction.template_id)
    images = template.Images.all().order_by('rank')

    # opencvでテンプレートマッチング
    return opencv(path, images, request)


def resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation = inter)

    # return the resized image
    return resized

def opencv(path, images, request):
    target = cv2.imread(path)
    gray = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)

    # ソート番号
    sort_no = 0
    # 認識結果マップ
    result_map = {}
    sort_map = {}

    # テンプレートソート順番配列
    template_sort = []

    for image in images:
        # テンプレート読み込み
        template_img = cv2.imread(os.path.join(settings.MEDIA_ROOT, str(image.path)))
        template_img = cv2.cvtColor(template_img, cv2.COLOR_BGR2GRAY)

        # テンプレートリサイズ
        template_img = resize(template_img, width=int(template_img.shape[1] * 0.64))
        (tH, tW) = template_img.shape[:2]

        #テンプレート数を数える
        sort_no += 1
        template_sort.append(sort_no)

        found_list = []
        # 元画像を縮小してマーチングする
        for scale in np.linspace(0.2, 1.0, 20)[::-1]:
            # 元画像リサイズ
            resized = resize(gray, width=int(gray.shape[1] * scale))
            r = gray.shape[1] / float(resized.shape[1])

            # 元画像リサイズ後のサイズがテンプレートより小さいの場合処理しない
            if resized.shape[0] < tH or resized.shape[1] < tW:
                break

            # テンプレートマーチング実施
            result = cv2.matchTemplate(resized, template_img, cv2.TM_CCOEFF_NORMED)

            # マーチング結果が８０％以上似てる場合のみ認める
            threshold = 0.8
            loc_tuples = np.where(result >= threshold)
            loc = sorted(zip(*loc_tuples[::-1]), key=lambda x: x[0])
            for pt in loc:
                found = (int(pt[0] * r), int(pt[1] * r), r)
                found_list.append(found)

        # マーチング結果が存在する場合
        if len(found_list) != 0:
            found_list = sorted(found_list, key=lambda x: x[0])
            for index in range(len(found_list)):
                try:
                    (ptX, ptY, ratio) = found_list[index]
                    (ptNextX, _, _) = found_list[index + 1]
                except IndexError:
                    ptNextX = None

                # 最大X軸値を保存する（１テンプレート１回のみ）
                # 同じテンプレートが複数存在する場合、テンプレート順番で保存する
                if ptNextX is None or ((ptNextX - ptX) >= int(tW * ratio / 2)):
                    sort_map[ptX] = (sort_no, ptX, ptY, int(tW * ratio), int(tH * ratio))
                    if str(sort_no) + "_" + str(ptX) not in result_map:
                        result_map[str(sort_no) + "_" + str(ptX)] = (sort_no, ptX, ptY, int(tW * ratio), int(tH * ratio))
        else:
            messages.error(request, "画像名（{0}）のテンプレートがマーチングできません。".format(image.name))
            return False

    # テンプレート数がマーチング結果数と一致しない場合処理しない
    if len(sort_map) != len(template_sort):
        messages.error(request, "テンプレート数と比較用写真にあるテンプレート数と一致していません。")
        return False

    # マーチング結果のX軸値を昇順でソートする
    item_list = sorted(list(result_map.items()), key=lambda x: x[0])
    # テンプレート順をソートする
    sort_list = sorted(list(sort_map.items()), key=lambda x: x[0])

    # マーチング結果を判定する
    match_result = {}
    for index in range(len(item_list)):
        (sort_no, ptX, _, _, _) = item_list[index][1]
        count = sort_no - 1
        ptXTemp = sort_list[count][0]

        # テンプレート順のX軸値がマーチング結果X軸値が同じの場合OK
        if ptX == ptXTemp:
            match_result[sort_no] = ("OK", sort_list[count][1])
        if sort_no not in match_result:
            match_result[sort_no] = ("NG", sort_list[count][1])
        temp_sort_no = sort_no

    # マーチング結果を描画する
    for item in list(match_result.items()):
        (_, ptX, ptY, tW, tH) = item[1][1]
        if item[1][0] == "OK":
            cv2.rectangle(target, (ptX, ptY), (ptX + tW, ptY + tH), (0, 255, 0), 2)
        else:
            cv2.rectangle(target, (ptX, ptY), (ptX + tW, ptY + tH), (0, 0, 255), 2)
            cv2.putText(target, "NG", (ptX, ptY + tH // 2), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)

    # 結果格納パス
    resultPath = os.path.join(os.path.dirname(path), "result", os.path.basename(path))
    cv2.imwrite(resultPath, target);
    return True








