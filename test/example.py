# def mouseMoveEvent(self, event):
#     self.circle = Cell(event.pos().x(), event.pos().y(), 50)
    # self.update()
    # self.show()

# def mousePressEvent(self, event):
#     self.circle = Cell(event.pos().x(), event.pos().y(), 50)
#     self.update()
#     self.show()
#     x = -(event.pos().x() - self.resource.x)
#     y = -(event.pos().y() - self.resource.y)
#     v = organism.calc([x, y], self.circle.w, self.circle.b)
#     # self.circle = Cell(self.circle.x + int(int(v[0])), self.circle.y + int(v[1]), 50)
#     self.b = (event.pos().x(), event.pos().y())
#     self.e = (self.circle.x + int(int(v[0])), self.circle.y+ int(v[1]))
#     self.update()
#     self.show()





# random.seed(10, version = 2)
#
#
# # матрица весов первого слоя
# w1 = np.array([[random.uniform(-1, 1) for i in range(9)] for j in range(4)])
#
# # веса второго слоя
# w2 = np.array([[random.uniform(-1, 1) for i in range(4)] for j in range(4)])
#
# w3 = np.array([[random.uniform(-1, 1) for i in range(4)] for j in range(2)])
# # веса смещения первого и второго слоев
# b1 = np.array([random.uniform(-1, 1) for i in range(4)])
# b2 = np.array([random.uniform(-1, 1) for i in range(4)])
# b3 = np.array([random.uniform(-1, 1) for i in range(2)])
#
# w = [w1, w2, w3]  # массив матриц весов
# b = [b1, b2, b3]  # массив весов смещения
#
# # Произвольный входной вектор x
# x = [0.19438, 6, 1, 1, 1, 1, 1, 8 ]
#
