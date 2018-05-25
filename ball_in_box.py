import numpy as np
import math
import random
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

LENGTH = 13  # 长方形的长
WIDTH = 5  # 长方形的宽
DOTS_NUM = 10  # 障碍点个数
CENTER_NUM = 3  # 圆心个数
dots_x = []  # 障碍点横坐标
dots_y = []  # 障碍点纵坐标
dots = []  # 障碍点

circle = []  # 圆
cir_fig = []  # 圆的图形
center_x = []  # 圆心横坐标
center_y = []  # 圆心纵坐标
radii = []  # 圆的半径
axis_x = np.linspace(0, LENGTH, LENGTH * 10)  # 对长[0,LENGTH]间隔取LENGTH*10个点
axis_y = np.linspace(0, WIDTH, WIDTH * 10)  # 对宽[0,WIDTH]间隔取WIDTH*10个点
# 圆心
centers = [(x, y) for x in axis_x
           for y in axis_y]

# 随机生成障碍点
for i in range(DOTS_NUM):
    dots_x.append(random.uniform(0, LENGTH))
    dots_y.append(random.uniform(0, WIDTH))
    dots.append((dots_x[i], dots_y[i]))


# print(dots)

# 计算圆心与障碍点间的距离
def distance(x, y, a, b):
    return math.sqrt((x - a) * (x - a) + (y - b) * (y - b))


dis_min = []  # 存每个圆心到障碍点/边界距离中的最小值
center_tem = []  # 存每个圆心的坐标
for x, y in centers:  # 遍历每个圆心
    dis = []  # 圆心到障碍点/边界的距离
    for a, b in dots:  # 遍历每个障碍点
        dis.append(distance(x, y, a, b))  # 求当前圆心到每个障碍点的距离
    dis = dis + [x, y, LENGTH - x, WIDTH - y]  # 加上圆心到边界的距离
    # print(dis)
    dis_min.append(min(dis))  # 取当前圆心到障碍点/边界距离中的最小值，作为当前圆心对应的半径
    # print(dis_min)
    center_tem.append((x, y))  # 记录下当前圆心的坐标
    # print(center_tem)

indices = np.argsort(dis_min)[-CENTER_NUM:]  # 取dis_min中前CENTER_NUM大元素的索引

for i in indices:
    center = center_tem[i]
    center_x.append(center[0])
    center_y.append(center[1])
    radii.append(dis_min[i])

colors = ['blue', 'yellow', 'pink']
for i in range(len(radii)):  # 遍历前CENTER_NUM个圆
    circle.append((center_x[i], center_y[i], radii[i]))
    cir_fig.append(Circle(xy=(center_x[i], center_y[i]), radius=radii[i], facecolor=colors[i], alpha=0.5))

fig = plt.figure()
ax = fig.add_subplot(111)  # 将画布分割为1行1列，取第1块
ax.set_aspect(1)  # 坐标轴单位为1
ax.plot(dots_x, dots_y, 'gx')  # 画障碍点
ax.plot(center_x, center_y, 'ro')  # 画圆心
ax.axis([0, LENGTH, 0, WIDTH])
for i in range(len(radii)):
    ax.add_patch(cir_fig[i])  # 画圆
plt.show()
