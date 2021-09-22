import cv2
import numpy as np
import numpy
import matplotlib.pyplot as plt
from PIL import Image
from scipy.spatial.distance import pdist

def calculate(image1, image2):
    # 灰度直方图算法
    # 计算单通道的直方图的相似值
    hist1 = cv2.calcHist([image1], [0], None, [256], [0.0, 255.0])
    hist2 = cv2.calcHist([image2], [0], None, [256], [0.0, 255.0])
    # 计算直方图的重合度
    degree = 0
    for i in range(len(hist1)):
        if hist1[i] != hist2[i]:
            degree = degree + (1 - abs(hist1[i] - hist2[i]) / max(hist1[i], hist2[i]))
        else:
            degree = degree + 1
    degree = degree / len(hist1)
    return degree


def cosine(image1, image2):
    X = np.vstack([image1, image2])
    return pdist(X, 'cosine')[0]


def rest(img,zongshu):
    xx = 0
    yy = 0
    js = 0#计数
    bkzb = []#选框坐标
    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 将图片变为灰度图
    ret, thresh = cv2.threshold(imgray, 127, 255, cv2.THRESH_BINARY_INV)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_TC89_L1)  # 获取边缘的两个数值
    # 闭运算使图像显示更清楚
    kernel = np.ones((5, 5), np.uint8)
    first = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    # cv2.imshow('imageshow', first )  #显示返回值image，其实与输入参数的thresh原图没啥区别
    # 待处理的主图像
    img = cv2.drawContours(first, contours, -1, (225, 225, 0), 2)  # img为三通道才能显示轮廓
    # cv2.imshow('dierge', img )
    # 外接矩形绘制
    # 第一次循环用于筛选
    for c in contours:
        if cv2.contourArea(c) > 1500 and cv2.contourArea(c) < 5000:
            (x, y, w, h) = cv2.boundingRect(c)
            bkzb.append([x, y, w, h, 1])
            # img = cv2.drawContours(img, contours, -1, (225, 225, 0), 5)  # img为三通道才能显示轮廓
            img = cv2.drawContours(img, [c], -1, (255, 255, 255), 1)
            js = js + 1
            zongshu.append(js)
    for i in range(0, js):
        for j in range(0, js):
            if bkzb[j][4] == 0:
                continue
            x1 = bkzb[i][2]
            y1 = bkzb[i][3]
            if x1 / y1 > 1.5 or y1 / x1 > 1.5:
                bkzb[i][4] = 0
            # 第一部分
            if bkzb[i][0] + bkzb[i][2] <= bkzb[j][0] + bkzb[j][2] and bkzb[i][1] + bkzb[i][3] <= bkzb[j][1] + bkzb[j][
                3] and bkzb[j][0] <= bkzb[i][0] + bkzb[i][2] and bkzb[j][1] <= bkzb[i][1] + bkzb[i][3]:
                if bkzb[i][0] > bkzb[j][0] and bkzb[i][1] < bkzb[j][1]:
                    bkzb[i][0] = bkzb[j][0]
                    bkzb[i][3] = bkzb[j][3] - bkzb[i][1] + bkzb[j][1]
                    bkzb[j][4] = 0
                elif bkzb[i][0] < bkzb[j][0] and bkzb[i][1] < bkzb[j][1]:
                    bkzb[i][2] = bkzb[j][2] - bkzb[i][0] + bkzb[j][0]
                    bkzb[i][3] = bkzb[j][3] - bkzb[i][1] + bkzb[j][1]
                    bkzb[j][4] = 0
                elif bkzb[i][0] < bkzb[j][0] and bkzb[i][1] > bkzb[j][1]:
                    bkzb[i][1] = bkzb[j][1]
                    bkzb[i][2] = bkzb[j][2] - bkzb[i][0] + bkzb[j][0]
                    bkzb[j][4] = 0
                elif bkzb[i][0] > bkzb[j][0] and bkzb[i][1] > bkzb[j][1]:
                    bkzb[i][4] = 0
                    break
    # 第二部分
    # 进行筛选
    img1 = ''
    for i in range(0, js):
        if bkzb[i][4] == 0:
            continue
        img1 = cv2.rectangle(img, (bkzb[i][0], bkzb[i][1]), (bkzb[i][0] + bkzb[i][2], bkzb[i][1] + bkzb[i][3]),
                             (0, 0, 255), 1)
    # cv2.imshow('drawimg2', img1)
    # 测试部分
    if len(img1) != 0:
        res = cv2.resize(img1, (0, 0), fx=0.2, fy=0.2)
    # cv2.imshow('drawimg1',res)
    return bkzb

def cv_imread(file_path):#读取中文路径方法
    cv_img = cv2.imdecode(np.fromfile(file_path,dtype=np.uint8),-1)
    return cv_img

def test(imageSrc1,imageSrc2):
    image = cv_imread(imageSrc1)  # 输入图像
    img = cv_imread(imageSrc2)  # 第二个图像
    js = 0#计数重置
    zongshu = []
    zs = 0#总数重置
    bkzb1 = rest(img,zongshu)
    changdu1 = len(zongshu)
    zongshu = []
    bkzb2 = rest(image,zongshu)
    changdu2 = len(zongshu)
    # 测试部分
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    img1 = thresh
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    img2 = thresh
    # 把图进行裁剪
    zs = 0#总数
    xs = 0#相似数
    cw = 0#错误数
    xt = 0#相同数
    ccq = 0#循环结束判断条件
    zh = 0#总和
    for i in range(0, changdu1):
        x1 = bkzb1[i][0]
        x2 = bkzb1[i][1]
        y1 = bkzb1[i][2]
        y2 = bkzb1[i][3]
        img11 = img1[x2:x2 + y2, x1:x1 + y1]
        for j in range(0, changdu2):
            if bkzb1[i][4] == 0:
                continue
            x3 = bkzb2[j][0]
            x4 = bkzb2[j][1]
            y3 = bkzb2[j][2]
            y4 = bkzb2[j][3]
            img22 = img2[x4:x4 + y4, x3:x3 + y3]
            # 测试部分
            image1 = img11
            image2 = img22
            w1, h1 = image1.shape
            w2, h2 = image2.shape
            if w1 < w2:
                w = w1
            else:
                w = w2
            if h1 < h2:
                h = h1
            else:
                h = h2
            image1 = cv2.resize(image1, (h, w))
            image2 = cv2.resize(image2, (h, w))
            image1 = np.asarray(image1).flatten()
            image2 = np.asarray(image2).flatten()
            zh = zh + cosine(image1, image2)
            zh = zh / 2
            if cosine(image1, image2) < 0.05:
                xs = xs + 1
                zs = 0

                xsd = calculate(image1, image2)
                if xsd > 0.13:
                    xt = xt + 1
            if cosine(image1, image2) == 0:
                back = '相似度为：100%'
                ccq = 1
                break
        if ccq == 1:
            break
    if (xs == 0):
        back = '相似度为:0%'
    else:
        back = '相似度为：' + str(xt / xs * 100) + '%'
    # 返回判断值
    return back
#test("2.png","2.png")
cv2.waitKey(0)
cv2.destroyAllWindows()
