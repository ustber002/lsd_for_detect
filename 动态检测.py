import cv2
import math
import numpy as np
from scipy.cluster.hierarchy import dendrogram, linkage,fcluster

cap = cv2.VideoCapture('video/01.mp4')

while True:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    lsd = cv2.createLineSegmentDetector(0,_scale=1)

    dlines = lsd.detect(gray)
    k = []
    l = []
    theta = []
    ltheta = np.zeros((8))
    suml = np.zeros((8))
    meanl = np.zeros((8))
    image = img
    image2 = img
    for dline in dlines[0]:
        x0 = int(round(dline[0][0]))
        y0 = int(round(dline[0][1]))
        x1 = int(round(dline[0][2]))
        y1 = int(round(dline[0][3]))
        # cv2.line(image, (x0, y0), (x1, y1), 255, 1, cv2.LINE_AA)
        # cv2.circle(image, (x0, y0), 2, (0, 255, 0), -1)
        # cv2.circle(image, (x1, y1), 2, (0, 255, 0), -1)
        k0 = (dline[0][3] - dline[0][1]) / (dline[0][2] - dline[0][0])
        l0 = ((dline[0][2] - dline[0][0]) ** 2 + (dline[0][3] - dline[0][1]) ** 2) ** 0.5
        theta0 = math.degrees(math.atan(k0))


        theta0 = (int(theta0 // 22.5)) * 22.5
        for i in range(0, 8):
            if theta0 == (i - 4) * 22.5:
                ltheta[i] += l0
                suml[i] += 1

                break
            else:
                pass

        k.append(k0)
        l.append(l0)
        theta.append(theta0)
    meanl = ltheta / suml
    where_are_NaNs = np.isnan(meanl)
    meanl[where_are_NaNs] = 0
    print(k)

    print(theta)
    print(l)
    print(meanl)
    print(np.argmax(meanl))
    sum = 0
    jieju = []
    x0list = []
    x1list = []
    y0list = []
    y1list = []
    delta = 0 #判别是否有LSD直线
    for dline in dlines[0]:
        x0 = int(round(dline[0][0]))
        y0 = int(round(dline[0][1]))
        x1 = int(round(dline[0][2]))
        y1 = int(round(dline[0][3]))
        l0 = ((dline[0][2] - dline[0][0]) ** 2 + (dline[0][3] - dline[0][1]) ** 2) ** 0.5
        theta0 = math.degrees(math.atan((dline[0][3] - dline[0][1]) / (dline[0][2] - dline[0][0])))
        # theta0 = int(theta0 * 0.1) * 10

        if theta0 >= (((np.argmax(meanl)) - 4) * 22.5 - 5) and theta0 <= (((np.argmax(meanl)) - 3) * 22.5 + 5) and l0 > 180: #角度筛选和长度筛选
            # if theta0 >= -30 and theta0 <= 0:
            # cv2.line(image, (x0, y0), (x1, y1), 255, 1, cv2.LINE_AA)
            # cv2.circle(image, (x0, y0), 2, (0, 255, 0), -1)
            # cv2.circle(image, (x1, y1), 2, (0, 255, 0), -1)
            sum = sum + 1

            b = int((x0 * y1 - x1 * y0) / (x0 - x1) ) # 直线的截距
            jieju.append(b)
            x0list.append(x0)
            x1list.append(x1)
            y0list.append(y0)
            y1list.append(y1)
            delta = 1
        else:
            pass
    if delta == 1:
        print('sum:', sum)
        print('jieju:', jieju)

        if len(jieju)>1:
            X = [[i] for i in jieju]

        #method是指计算类间距离的方法,比较常用的有3种:
        #single:最近邻,把类与类间距离最近的作为类间距
        #average:平均距离,类与类间所有pairs距离的平均
        #complete:最远邻,把类与类间距离最远的作为类间距
            Z = linkage(X, 'single')
            f = fcluster(Z,10,'distance')
            print(f)
            # fig = plt.figure(figsize=(5, 3))
            # dn = dendrogram(Z)
            # plt.show()





            for i in range (1,f.max()+1):
                xzanshi = []
                yzanshi = []

                for j in range(len(jieju)):
                    if f[j] == i:
                        xzanshi.append(x0list[j])
                        yzanshi.append(y0list[j])
                        xzanshi.append(x1list[j])
                        yzanshi.append(y1list[j])
                print(xzanshi)
                print(yzanshi)
                k = np.polyfit(xzanshi, yzanshi, 1)
                print('k=',k)
                cv2.line(image2, (0, int(k[1])), (1500, int(1500*k[0]+k[1])), 255, 1, cv2.LINE_AA)
        else:
            pass




    cv2.imshow('new', image2)


    if cv2.waitKey(20) == ord('q'):  # 按Q退出
        break

