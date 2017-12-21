__author__ = 'sss'
import cv2

# 加载摄像头
cam = VideoCapture(0)   # 0 -> 摄像头序号，如果有两个三个四个摄像头，要调用哪一个数字往上加嘛
# 抓拍十张小图片
for x in range(0, 9):
    s, img = cam.read()
    if s:
        imwrite("o-" + str(x) + ".jpg", img)