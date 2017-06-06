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
    result = opencv(path, images, request)
    return result


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
    result = True
    all_diff = False
    target = cv2.imread(path)
    print(target)

    gray = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)

    # ソート番号
    sort_no = 0
    # 認識結果マップ
    result_map = {}
    sort_map = {}

    # テンプレートソート順番配列
    template_sort = []

    image_name_list = []
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
            addItem = False
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
                    if str(sort_no) + "_" + str(ptX) not in result_map.keys():
                        addItem = True
                        result_map[str(sort_no) + "_" + str(ptX)] = (
                        sort_no, ptX, ptY, int(tW * ratio), int(tH * ratio))
            if not addItem:
                result_map[str(sort_no) + "_None"] = (sort_no, None, None, int(tW / 0.64), int(tH / 0.64))
        else:
            result_map[str(sort_no) + "_None"] = (sort_no, None, None, int(tW / 0.64), int(tH / 0.64))
            image_name_list.append(image.name)

    if len(image_name_list) > 0 and len(image_name_list) < len(template_sort):
        if request:
            messages.error(request, "画像名（{0}）のテンプレートがマーチングできません。".format(','.join(image_name_list)))
        result = False
    elif len(image_name_list) == len(template_sort):
        if request:
            messages.error(request, "テンプレートと全く異なる画像でマーチングできません。")
        result = False
        all_diff=True
    else:
        result = True

    # テンプレート数がマーチング結果数と一致しない場合処理しない
    #if len(sort_map) != len(template_sort):
    #    messages.error(request, "テンプレート数と比較用写真にあるテンプレート数と一致していません。")
    #    return False

    # マーチング結果のX軸値を昇順でソートする
    item_list = sorted(list(result_map.items()), key=lambda x: x[1][0])
    # テンプレート順をソートする
    sort_list = sorted(list(sort_map.items()), key=lambda x: x[0])
    # マーチング結果を判定する
    match_result = {}
    noneCount = 0
    for index in range(len(item_list)):
        (sort_no, ptX, _, w, h) = item_list[index][1]
        if ptX is not None:
            try:
                count = sort_no - noneCount - 1
                ptXTemp = sort_list[count][0]
                # テンプレート順のX軸値がマーチング結果X軸値が同じの場合OK
                if ptX == ptXTemp:
                    match_result[sort_no] = ("OK", sort_list[count][1])
                if sort_no not in match_result:
                    match_result[sort_no] = ("NG", sort_list[count][1])
            except IndexError:
                match_result[sort_no] = ("NG", (sort_no, None, None, w, h))
        else:
            noneCount += 1
            match_result[sort_no] = ("NG", item_list[index][1])

    if not all_diff:
        # マーチング結果を描画する
        nonePtX = nonePtY = None
        loopCount = 0
        hasNoFrist = False
        for item in list(match_result.items()):
            (_, ptX, ptY, tW, tH) = item[1][1]
            if hasNoFrist and ptX is not None:
                cv2.line(target, (ptX, ptY - 20), (ptX, ptY + tH + 20), (0, 0, 255), 2)
                cv2.putText(target, " Image ", (ptX - 60, ptY - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)
                cv2.putText(target, " Missing ", (ptX - 60, ptY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)
                hasNoFrist = False

            if item[1][0] == "OK":
                cv2.rectangle(target, (ptX, ptY), (ptX + tW, ptY + tH), (0, 255, 0), 2)
                nonePtX = ptX + tW
                nonePtY = ptY + tH
            else:
                if ptX is not None:
                    cv2.rectangle(target, (ptX, ptY), (ptX + tW, ptY + tH), (0, 0, 255), 2)
                    cv2.putText(target, "NG", (ptX, ptY + tH // 2), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)
                    nonePtX = ptX + tW
                    nonePtY = ptY + tH
                else:
                    if nonePtX is not None:
                        cv2.line(target, (nonePtX, nonePtY - tH - 20), (nonePtX, nonePtY + 20), (0, 0, 255), 2)
                        cv2.putText(target, " Image ", (nonePtX, nonePtY + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255),
                                    1)
                        cv2.putText(target, " Missing", (nonePtX, nonePtY + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255),
                                    1)
                    else:
                        hasNoFrist = True
    else:
        (tH, tW) = target.shape[:2]
        cv2.rectangle(target, (5, 5), (tW-5, tH-5), (0, 0, 255), 2)
        cv2.putText(target, "Can not matching the image!", (tW//2-200, tH//2), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255),
                    1)
    # 結果格納パス
    resultPath = os.path.join(os.path.dirname(path), "result", os.path.basename(path))

    if resultPath[-4:].lower() == '.png':
        # cv2.IMWRITE_PNG_COMPRESSION，从0到9,压缩级别越高，图像尺寸越小。默认级别为3
        cv2.imwrite(resultPath, target, [int(cv2.IMWRITE_PNG_COMPRESSION), 9]);
    else:
        # 对于JPEG，其表示的是图像的质量，用0-100的整数表示
        cv2.imwrite(resultPath, target, [int(cv2.IMWRITE_JPEG_QUALITY), 40]);

    return result

#===========================================
# private method
#===========================================
def handler_surf( transaction ,request):
    # 画像の相対パス
    path = transaction.src_image.path

    # テンプレート画像
    template = get_object_or_404(Templates, pk=transaction.template_id)
    images = template.Images.all().order_by('rank')

    # opencvでSURF特徴量マッチング
    result = opencv_surf(path, images, request)
    return result

#物体が存在するかどうか
def already_exist(xMin,yMin,xMax,yMax,sortMap):
    exist = False
    for item in sortMap.items():
        minPoint=item[1][1]
        maxPoint=item[1][2]

        if (xMax<=maxPoint[0] and xMax>=(minPoint[0] + (maxPoint[0] -minPoint[0]) // 2)) or (xMin<=(minPoint[0] + (maxPoint[0] -minPoint[0]) // 2) and xMin>=minPoint[0]) or (xMin>=minPoint[0] and xMax<=maxPoint[0]) or (xMin<=minPoint[0] and xMax>=maxPoint[0]) :
            exist= True
            break

    return exist

#特徴量マッチング実施
def exec_matching(targeImg, tempImg, sortMap, resultMap, sort_no, xRatio=0):
    sift = surf = cv2.xfeatures2d.SURF_create()

    kp1, des1 = sift.detectAndCompute(tempImg, None)
    kp2, des2 = sift.detectAndCompute(targeImg, None)

    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)

    flann = cv2.FlannBasedMatcher(index_params, search_params)
    if des1 is not None and des2 is not None:
        matches = flann.knnMatch(des1, des2, k=2)

        # store all the good matches as per Lowe's ratio test.
        good = []
        for m, n in matches:
            if m.distance < 0.7 * n.distance:
                good.append(m)

        if len(good) >= 10:
            src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
            dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

            M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
            h, w = tempImg.shape[:2]
            pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
            dst = cv2.perspectiveTransform(pts, M)

            x_list = sorted(np.int32(dst), key=lambda x: x[0][0])
            y_list = sorted(np.int32(dst), key=lambda x: x[0][1])

            xMin = x_list[0][0][0]
            yMin = y_list[0][0][1]
            xMax = x_list[-1][0][0]
            yMax = y_list[-1][0][1]

            cv2.rectangle(targeImg, (xMin, yMin), (xMax, yMax), (255, 0, 0), 2)
            if xMin >= 0 and yMin >= 0 and xMax >= 0 and yMax >= 0:
                if xMin + xRatio not in sortMap.keys() and not already_exist(xMin + xRatio, yMin, xMax + xRatio, yMax,
                                                                             sortMap):
                    sortMap[xMin + xRatio] = (sort_no, (xMin + xRatio, yMin), (xMax + xRatio, yMax))
                    resultMap[str(sort_no) + "_" + str(xMin + xRatio)] = (
                    sort_no, (xMin + xRatio, yMin), (xMax + xRatio, yMax))
                else:
                    h, w = targeImg.shape[:2]
                    xRatio += int(xMax * 0.8)
                    exec_matching(targeImg[0:h, int(xMax * 0.8):w], tempImg, sortMap, resultMap, sort_no,
                                  xRatio)
            else:
                resultMap[str(sort_no) + "_None"] = (sort_no, (None, None), (None, None))
        else:
            resultMap[str(sort_no) + "_None"] = (sort_no, (None, None), (None, None))
    else:
        resultMap[str(sort_no) + "_None"] = (sort_no, (None, None), (None, None))

def opencv_surf(path, images, request):
    result = True
    target = cv2.imread(path)
    image_gray = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)

    # ソート番号
    sort_no = 0
    # 認識結果マップ
    result_map = {}
    sort_map = {}

    # テンプレートソート順番配列
    template_sort = []

    image_name_list = []
    for image in images:
        # テンプレート読み込み
        template_img = cv2.imread(os.path.join(settings.MEDIA_ROOT, str(image.path)))
        template_img = cv2.cvtColor(template_img, cv2.COLOR_BGR2GRAY)

        sort_no += 1
        template_sort.append(sort_no)
        exec_matching(image_gray, template_img, sort_map, result_map, sort_no)

    # テンプレート数がマーチング結果数と一致しない場合処理しない
    #if len(sort_map) != len(template_sort):
    #    messages.error(request, "テンプレート数と比較用写真にあるテンプレート数と一致していません。")
    #    return False

    # マーチング結果のX軸値を昇順でソートする
    item_list = sorted(list(result_map.items()), key=lambda x: x[1][0])
    # テンプレート順をソートする
    sort_list = sorted(list(sort_map.items()), key=lambda x: x[0])
    # マーチング結果を判定する
    match_result = {}
    noneCount = 0
    for index in range(len(item_list)):
        (sort_no, (ptX, _), _) = item_list[index][1]
        if ptX is not None:
            try:
                count = sort_no - noneCount - 1
                ptXTemp = sort_list[count][0]
                # テンプレート順のX軸値がマーチング結果X軸値が同じの場合OK
                if ptX == ptXTemp:
                    match_result[sort_no] = ("OK", sort_list[count][1])
                if sort_no not in match_result:
                    match_result[sort_no] = ("NG", sort_list[count][1])
            except IndexError:
                match_result[sort_no] = ("NG", (sort_no, None, None))
        else:
            noneCount += 1
            match_result[sort_no] = ("NG", item_list[index][1])
    if noneCount != len(template_sort):
        # マーチング結果を描画する
        nonePtX = nonePtY = None
        loopCount = 0
        hasNoFrist = False
        h, w = target.shape[:2]
        for item in list(match_result.items()):
            loopCount+=1
            (sort_no, (ptX, ptY), (ptMaxX, ptMaxY)) = item[1][1]
            if hasNoFrist and ptX is not None:
                cv2.line(target, (ptX - 2, 5), (ptX - 2, h - 5), (0, 0, 255), 2)
                cv2.putText(target, " Image ", (ptX - 60, ptY - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)
                cv2.putText(target, " Missing ", (ptX - 60, ptY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)
                hasNoFrist = False

            if item[1][0] == "OK":
                cv2.rectangle(target, (ptX, ptY), (ptMaxX, ptMaxY), (0, 255, 0), 2)
                cv2.putText(target, str(sort_no)+"-"+str(loopCount), (ptX + 10, ptY-5), cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                            (0, 255, 0), 2)
                nonePtX = ptMaxX
                nonePtY = ptMaxY
            else:
                if ptX is not None:
                    cv2.rectangle(target, (ptX, ptY), (ptMaxX, ptMaxY), (0, 0, 255), 2)
                    cv2.putText(target, "NG", (ptX+5, ptY+(ptMaxY-ptY)//2), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)
                    cv2.putText(target, str(sort_no) + "-" + str(loopCount), (ptX + 10, ptY - 5),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                                (0, 0, 255), 2)
                    nonePtX = ptMaxX
                    nonePtY = ptMaxY
                else:
                    if nonePtX is not None:
                        cv2.line(target, (nonePtX + 2, 5), (nonePtX + 2, h - 5), (0, 0, 255), 2)
                        cv2.putText(target, " Image ", (nonePtX, nonePtY + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255),
                                    1)
                        cv2.putText(target, " Missing", (nonePtX, nonePtY + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255),
                                    1)
                    else:
                        hasNoFrist = True
    else:
        (tH, tW) = target.shape[:2]
        cv2.rectangle(target, (5, 5), (tW - 5, tH - 5), (0, 0, 255), 2)
        cv2.putText(target, "Can not matching the image!", (tW // 2 - 200, tH // 2), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255),1)
    # 結果格納パス
    resultPath = os.path.join(os.path.dirname(path), "result", os.path.basename(path))

    if resultPath[-4:].lower() == '.png':
        # cv2.IMWRITE_PNG_COMPRESSION，从0到9,压缩级别越高，图像尺寸越小。默认级别为3
        cv2.imwrite(resultPath, target, [int(cv2.IMWRITE_PNG_COMPRESSION), 4]);
    else:
        # 对于JPEG，其表示的是图像的质量，用0-100的整数表示
        cv2.imwrite(resultPath, target, [int(cv2.IMWRITE_JPEG_QUALITY), 80]);

    return result







