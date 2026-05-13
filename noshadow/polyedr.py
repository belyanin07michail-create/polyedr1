from math import pi
from common.r3 import R3
from common.tk_drawer import TkDrawer


class Edge:
    """Ребро полиэдра"""

    # Параметры конструктора: начало и конец ребра (точки в R3)

    def __init__(self, beg, fin):
        self.beg, self.fin = beg, fin


class Facet:
    """Грань полиэдра"""

    # Параметры конструктора: список вершин

    def __init__(self, vertexes):
        self.vertexes = vertexes


class Polyedr:
    """Полиэдр"""

    # Параметры конструктора: файл, задающий полиэдр

    def __init__(self, file):

        # списки вершин, рёбер и граней полиэдра
        self.vertexes, self.edges, self.facets = [], [], []

        # список строк файла
        with open(file) as f:
            for i, line in enumerate(f):
                if i == 0:
                    # обрабатываем первую строку; buf - вспомогательный массив
                    buf = line.split()
                    # коэффициент гомотетии
                    c = float(buf.pop(0))
                    # углы Эйлера, определяющие вращение
                    alpha, beta, gamma = (float(x) * pi / 180.0 for x in buf)
                elif i == 1:
                    # во второй строке число вершин, граней и рёбер полиэдра
                    nv, nf, ne = (int(x) for x in line.split())
                elif i < nv + 2:
                    # задание всех вершин полиэдра
                    x, y, z = (float(x) for x in line.split())
                    p = R3(x, y, z).rz(alpha).ry(beta).rz(gamma) * self.c
                    self.vertexes.append(p)
                else:
                    # вспомогательный массив
                    buf = line.split()
                    # количество вершин очередной грани
                    size = int(buf.pop(0))
                    # массив вершин этой грани
                    vertexes = [self.vertexes[int(n) - 1] for n in buf]
                    # задание рёбер грани
                    for n in range(size):
                        self.edges.append(Edge(vertexes[n - 1], vertexes[n]))
                    # задание самой грани
                    self.facets.append(Facet(vertexes))

    def calc_special_edges_sum(self):
        def is_not_good(p):
            # Проверка попадания в круг, масштабированный на коэффициент c
            return (p.x**2 + p.y**2) <= (self.c ** 2)

        total_length = 0.0
        for e in self.edges:
            if is_not_good(e.beg) and is_not_good(e.fin):
                total_length += e.beg.distance(e.fin)
        return total_length

    # Метод изображения полиэдра
    def draw(self, tk):  # pragma: no cover
        for e in self.edges:
            for f in self.facets:
                e.shadow(f)
            for s in e.gaps:
                tk.draw_line(e.r3(s.beg), e.r3(s.fin))
