import numpy as np
import random

random.seed(10, version = 2)


# матрица весов первого слоя
w1 = np.array([[random.uniform(-1, 1) for i in range(2)] for j in range(4)])

# веса второго слоя
w2 = np.array([[random.uniform(-1, 1) for i in range(4)] for j in range(4)])

w3 = np.array([[random.uniform(-1, 1) for i in range(4)] for j in range(2)])
# веса смещения первого и второго слоев
b1 = np.array([random.uniform(-1, 1) for i in range(4)])
b2 = np.array([random.uniform(-1, 1) for i in range(4)])
b3 = np.array([random.uniform(-1, 1) for i in range(2)])

w = [w1, w2, w3]  # массив матриц весов
b = [b1, b2, b3]  # массив весов смещения

# Произвольный входной вектор x
x = [0.19438, 6]

# сигмоидальная функция
def norm(x):
    return np.sin(x)


def feed_forward_calc(n_layers, x, w, b):  # (кол-во слоёв, входной веткор, массив весов, массив весов смещений)
    node_in = x
    h = node_in
    for l in range(n_layers-1):
        node_in = h
        z = w[l].dot(node_in) + b[l]
        h = norm(z)
    return h


def calc(x, w, b):
    return feed_forward_calc(4, x, w, b)


def reproduce(w1, w2, b1, b2, r):
    w = (w1 + w2)/2
    b = (b1 + b2)/2
    mutations_w = [[random.uniform(-1, 1)*r for i in range(w.shape[1])] for j in range(w.shape[0])]
    mutations_b = [random.uniform(-1, 1)*r for i in range(b.shape[0])]
    return (w+mutations_w, b+mutations_b)


if __name__ == '__main__':
    print(reproduce(w1, w1, b1, b1, 0.1))
