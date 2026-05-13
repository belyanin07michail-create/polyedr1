#!/usr/bin/env -S python3 -B

from time import time
from common.tk_drawer import TkDrawer
from shadow.polyedr import Polyedr


tk = TkDrawer()
try:
    for name in ["ccc", "cube", "box", "king", "cow"]:
        tk.clean()

        print("=============================================================")
        print(f"Начало работы с полиэдром '{name}'")
        start_time = time()

        poly = Polyedr(f"data/{name}.geom")
        tk.draw_circle(poly.c)  # Рисуем круг, масштабированный на коэффициент
        poly.draw(tk)

        delta_time = time() - start_time
        print(f"Изображение полиэдра '{name}' заняло {delta_time} сек.")

        result = poly.calc_special_edges_sum()
        print(f"Сумма длин ребер (оба конца не 'хорошие'): {result:.4f}")

        input("Hit 'Return' to continue -> ")
except (EOFError, KeyboardInterrupt):
    print("\nStop")
    tk.close()
