import matplotlib.pyplot as plt

# 读取Titanic数据集
labels = ['RF', 'LR', 'NB', 'HALKP', 'CDS']
fmeasure=[[0.37, 0.481, 0.506, 0.654, 0.362, 0.562, 0.428, 0.234],
          [0.24, 0.504, 0.41, 0.635, 0.439, 0.531, 0.284, 0.07],
          [0.306, 0.475, 0.453, 0.294, 0.51, 0.526, 0.428, 0.225],
          [0.429, 0.564, 0.613, 0.675, 0.458, 0.527, 0.61, 0.402],
          [0.436, 0.522, 0.695, 0.696, 0.507, 0.567, 0.662, 0.601]]

gmean = [[0.542, 0.783, 0.529, 0.649, 0.489, 0.564, 0.523, 0.352],
         [0.396, 0.746, 0.493, 0.622, 0.544, 0.35, 0.408, 0.191],
         [0.482, 0.712, 0.509, 0.41, 0.614, 0.548, 0.523, 0.352],
         [0.583, 0.708, 0.622, 0.683, 0.568, 0.494, 0.636, 0.468],
         [0.587, 0.783, 0.55, 0.664, 0.617, 0.6, 0.658, 0.535]]

balance = [[0.52, 0.783, 0.518, 0.642, 0.477, 0.541, 0.493, 0.386],
           [0.408, 0.731, 0.474, 0.618, 0.513, 0.382, 0.414, 0.319],
           [0.472, 0.691, 0.495, 0.417, 0.592, 0.538, 0.498, 0.383],
           [0.552, 0.699, 0.598, 0.667, 0.544, 0.485, 0.636, 0.466],
           [0.555, 0.778, 0.554, 0.663, 0.604, 0.583, 0.655, 0.535]]


# 设置图形的显示风格
plt.style.use('ggplot')

# 设置中文和负号正常显示
# plt.rcParams['font.sans-serif'] = 'Microsoft YaHei'

plt.xticks(fontsize=15, family='Times New Roman')
plt.yticks(fontsize=15, family='Times New Roman')
plt.rcParams['axes.unicode_minus'] = False

# 绘图：整体乘客的年龄箱线图
plt.boxplot(x=balance,  # 指定绘图数据
            labels=labels,
            sym="",
            patch_artist=True,  # 要求用自定义颜色填充盒形图，默认白色填充
            showmeans=True,  # 以点的形式显示均值
            boxprops={'color': 'black', 'facecolor': '#9999ff'},  # 设置箱体属性，填充色和边框色
            #flierprops={'marker': 'o', 'markerfacecolor': 'red', 'color': 'black'},  # 设置异常值属性，点的形状、填充色和边框色
            meanprops={'marker': 'D', 'markerfacecolor': 'indianred'},  # 设置均值点的属性，点的形状、填充色
            medianprops={'linestyle': '--', 'color': 'orange'})  # 设置中位数线的属性，线的类型和颜色
# 设置y轴的范围
plt.ylim(0, 0.8)

# 去除箱线图的上边框与右边框的刻度标签
plt.tick_params(top='off', right='off')
# 显示图形
plt.show()