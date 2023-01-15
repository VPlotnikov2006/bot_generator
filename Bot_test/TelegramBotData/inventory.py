adjacency_list = []


class Inventory:
    node = 0
    size = 0
    visit_req = []
    inventory_req = []

    def __init__(self):
        self.__used = [0] * self.node
        self.__inventory = [0] * self.size

    @classmethod
    def set_visit_req(
        cls,
        v: "Вершина, для которой задается требование",
        u: "Вершина, которую необходимо посетить",
    ):
        """Задает требование для посещения вершины"""
        if max(v, u) >= cls.node:
            raise IndexError("Такой вершины нет")
        cls.visit_req[v].append(u)

    @classmethod
    def set_inventory_req(
        cls,
        v: "Вершина, для которой задается требование",
        i: "Индекс предмета, который должен быть у игрока",
    ):
        """Задает требование для посещения вершины"""
        if v >= cls.node:
            raise IndexError("Такой вершины нет")
        if i >= cls.size:
            raise IndexError("Такого предмета нет")
        cls.inventory_req[v].append(i)

    def visit_add(self, v: "Индекс вершины"):
        """Добавляет вершину v в список посещенных"""
        if v >= self.node:
            raise IndexError("Такой вершины нет")
        self.__used[v] += 1

    def visit_check(self, v: "Индекс начальной вершины", u: "Индекс конечной вершины"):
        """Проверка на возможность пройти по ребру v->u учитывая посещенные вершины"""
        if u not in adjacency_list[v]:
            return False
        for i in self.visit_req[u]:
            if not self.__used[i]:
                return False
        return True

    def visit_get(self, v: "Индекс вершины"):
        """Количество посешений вершины v"""
        if v >= self.node:
            raise IndexError("Такой вершины нет")
        return self.__used[v]

    def visit_get_all(self):
        """Список посещенности всех вершин"""
        return self.__used.copy()

    def inventory_add(self, i: "Индекс предмета в инвенторе"):
        """Добавление предмета с индексом i в инвентарь"""
        if i >= self.size:
            raise IndexError("Такого предмета нет")
        self.__inventory[i] += 1

    def inventory_check(
        self, v: "Индекс начальной вершины", u: "Индекс конечной вершины"
    ):
        """Проверка на возможность пройти по ребру v->u учитывая предметы инвенторя"""
        if u not in adjacency_list[v]:
            return False
        if not len(self.inventory_req[u]):
            return True
        for i in self.inventory_req[u]:
            if not self.__inventory[i]:
                return False
        return True

    def inventory_get(self, i: "Индекс предмета в инвенторе"):
        """Количество предметов с индексом i"""
        if i >= self.size:
            raise IndexError("Такого предмета нет")
        return self.__inventory[i]

    def inventory_get_all(self):
        """Инвентарь игрока"""
        return self.__inventory.copy()

    def check(self, v: "Индекс начальной вершины", u: "Индекс конечной вершины"):
        """Проверка на возможность пройти по ребру v->u"""
        return self.visit_check(v, u) and self.inventory_check(v, u)
