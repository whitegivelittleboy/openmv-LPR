import cv2
import numpy as np
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

def computeSafeRegion(shape, bounding_rect):
    top = bounding_rect[1]  # y
    bottom = bounding_rect[1] + bounding_rect[3]  # y +  h
    left = bounding_rect[0]  # x
    right = bounding_rect[0] + bounding_rect[2]  # x +  w
    min_top = 0
    max_bottom = shape[0]
    min_left = 0
    max_right = shape[1]
    if top < min_top:
        top = min_top
    if left < min_left:
        left = min_left
    if bottom > max_bottom:
        bottom = max_bottom
    if right > max_right:
        right = max_right
    return [left, top, right - left, bottom - top]


def cropImage(image, rect):
    x, y, w, h = computeSafeRegion(image.shape, rect)
    return image[y:y + h, x:x + w]


def detectPlateRough(image_gray, resize_h=720, en_scale=1.08, top_bottom_padding_rate=0.05):
    if top_bottom_padding_rate > 0.2:
        print("error:top_bottom_padding_rate > 0.2:", top_bottom_padding_rate)
        exit(1)
    height = image_gray.shape[0]
    padding = int(height * top_bottom_padding_rate)
    scale = image_gray.shape[1] / float(image_gray.shape[0])
    image = cv2.resize(image_gray, (int(scale * resize_h), resize_h))
    image_color_cropped = image[padding:resize_h - padding, 0:image_gray.shape[1]]
    image_gray = cv2.cvtColor(image_color_cropped, cv2.COLOR_RGB2GRAY)
    watches = watch_cascade.detectMultiScale(image_gray, en_scale, 2, minSize=(36, 9), maxSize=(36 * 40, 9 * 40))
    print("检测到车牌数:"+str(len(watches)))
    cropped_images = []
    for (x, y, w, h) in watches:
        x -= w * 0.14
        w += w * 0.28
        y -= h * 0.15
        h += h * 0.3
        cropped = cropImage(image_color_cropped, (int(x), int(y), int(w), int(h)))
        cropped_images.append([cropped, [x, y + padding, w, h]])
    return cropped_images

# def finemappingVertical(self,rect):
#     rect[2] -= rect[2] * (1 - res_raw[1] + res_raw[0])
#     rect[0] += res[0]


# 输入原始图像，rect是框位置，框选函数
def drawRectBox(image,rect):
    cv2.rectangle(image, (int(rect[0]), int(rect[1])), (int(rect[0] + rect[2]), int(rect[1] + rect[3])), (0,0, 255), 2,cv2.LINE_AA)
    # 文本位置
    # cv2.rectangle(image, (int(rect[0]-1), int(rect[1])-16), (int(rect[0] + 115), int(rect[1])), (0, 0, 255), -1,
    #               cv2.LINE_AA)
    img = Image.fromarray(image)
    imagex = np.array(img)
    return imagex


if __name__ == '__main__':
    watch_cascade = cv2.CascadeClassifier("cascade.xml")

    image = cv2.imread("cyt.jpg")
    images = detectPlateRough(image, image.shape[0],top_bottom_padding_rate=0.1)
    if images:
        rect = images[0][1]
        imagess = drawRectBox(image, rect)
        cv2.imshow('image', imagess)
        cv2.waitKey(0)
    else:
        print("无车牌")
