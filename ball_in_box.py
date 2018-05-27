import numpy as np
import math
import random
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

LENGTH = 13  # 长方形的长
WIDTH = 5  # 长方形的宽
BLOCKERS_NUM = 10  # 默认障碍点个数
CIRCLE_NUM = 3  # 圆的个数
BLOCKERS_X = []  # 随机障碍点横坐标
BLOCKERS_Y = []  # 随机障碍点纵坐标
BLOCKERS = []  # 随机障碍点

# 随机生成默认障碍点
for block in range(BLOCKERS_NUM):
    BLOCKERS_X.append(random.uniform(0, LENGTH))
    BLOCKERS_Y.append(random.uniform(0, WIDTH))
    BLOCKERS.append((BLOCKERS_X[block], BLOCKERS_Y[block]))


# 计算圆心与障碍点间的距离
def distance(x, y, a, b):
    return math.sqrt((x - a) * (x - a) + (y - b) * (y - b))


def ball_in_box(m=CIRCLE_NUM, blockers=BLOCKERS):
    """
    m是圆的个数，默认为CIRCLE_NUM；
    n是障碍点的个数，默认为BLOCKERS_NUM；
    blockers是装障碍点的列表，每个障碍点为(a,b)的元组，a、b分别为障碍点的横纵坐标，默认为BLOCKERS(随机生成)
    """
    circle = []  # 圆
    cir_fig = []  # 圆的图形
    center_x = []  # 圆心横坐标
    center_y = []  # 圆心纵坐标
    radii = []  # 圆的半径
    axis_x = np.linspace(0, LENGTH, LENGTH * 10)  # 对长[0,LENGTH]间隔取LENGTH*10个点
    axis_y = np.linspace(0, WIDTH, WIDTH * 10)  # 对宽[0,WIDTH]间隔取WIDTH*10个点
    centers = [(x, y) for x in axis_x
               for y in axis_y]  # 圆心

    blockers_x = []  # 障碍点横坐标
    blockers_y = []  # 障碍点纵坐标

    # 获得障碍点的横纵坐标
    for i in range(len(blockers)):
        blockers_x.append(blockers[i][0])
        blockers_y.append(blockers[i][1])

    # 一开始没有计算圆与圆的情况，这里得到的是dis_min中装满了对应圆的半径
    center_tem = []  # 存已经确定的最大圆
    for i in range(1, m + 1):
        dis_min = []  # 存每个圆心到障碍点/边界距离中的最小值
        for x, y in centers:  # 遍历每个圆心
            dis = []  # 圆心到障碍点/边界的距离
            for a, b in blockers:  # 遍历每个障碍点
                dis.append(distance(x, y, a, b))  # 求当前圆心到每个障碍点的距离
            dis = dis + [x, y, LENGTH - x, WIDTH - y]  # 加上圆心到边界的距离
            if center_tem:  # 如果已经有圆存在
                for a, b in center_tem:  # 遍历每个已经存在的圆
                    i = 0  # radii中的半径和center_tem中的圆是一一对应的，这里图方便弄了个索引i
                    dis.append(distance(x, y, a, b) - radii[i])  # 到每个已经存在的圆的距离
                    i = i + 1
            dis_min.append(min(dis))  # 取当前圆心到障碍点/边界距离中的最小值，作为当前圆心对应的半径

        indices = np.argsort(dis_min)[-1:]  # 取dis_min中最大圆的索引，一次只画一个圆

        # indices是索引数组，所以取indices[0]得到整数索引
        center_x.append(centers[indices[0]][0])
        center_y.append(centers[indices[0]][1])
        radii.append(dis_min[indices[0]])
        center_tem.append(centers[indices[0]])  # 新得到的最大圆
        centers.pop(indices[0])  # 画出的圆就不继续遍历了

    colors = ['blue', 'yellow', 'pink', 'chartreuse', 'darkviolet', 'crimson']
    for i in range(len(radii)):  # 遍历前CIRCLE_NUM个圆
        circle.append((center_x[i], center_y[i], radii[i]))
        cir_fig.append(Circle(xy=(center_x[i], center_y[i]), radius=radii[i], facecolor=colors[i], alpha=0.5))

    fig = plt.figure()
    ax = fig.add_subplot(111)  # 将画布分割为1行1列，取第1块
    ax.set_aspect(1)  # 坐标轴单位为1
    ax.plot(blockers_x, blockers_y, 'gx')  # 画障碍点
    ax.plot(center_x, center_y, 'ro')  # 画圆心
    ax.axis([0, LENGTH, 0, WIDTH])
    for i in range(len(radii)):
        ax.add_patch(cir_fig[i])  # 画圆
    plt.show()

    return circle  # 返回圆心坐标与半径


# test:

print(ball_in_box(m=6))
