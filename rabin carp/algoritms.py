import random
import time
import unittest

import generator_govna
import naive as nv


class RabinKarpTest(unittest.TestCase):
    """Тесты для метода Рабина-Карпа"""

    def func(self, text, patt):
        return nv.rabinus_karpus(text, patt)

    def setUp(self):
        """Инициализация"""
        self.text1 = 'axaxaxax'
        self.pattern1 = 'xax'
        self.text2 = 'bababab'
        self.pattern2 = 'bab'

    def test_return_type(self):
        """Проверка того, что функция возвращает список"""
        self.assertIsInstance(
            self.func(self.text1, "x"), list,
            msg="Функция должна возвращать список"
        )

    def test_returns_empty(self):
        """Проверка того, что функция, когда следует, возвращает пустой список"""
        self.assertEqual(
            [], self.func(self.text1, "z"),
            msg="Функция должна возвращать пустой список, если нет вхождений"
        )
        self.assertEqual(
            [], self.func("", self.pattern1),
            msg="Функция должна возвращать пустой список, если текст пустой"
        )
        self.assertEqual(
            [], self.func("", ""),
            msg="Функция должна возвращать пустой список, если текст пустой, даже если образец пустой"
        )

    def test_finds(self):
        """Проверка того, что функция ищет все вхождения непустых образцов"""
        self.assertEqual(
            [1, 3, 5], self.func(self.text1, self.pattern1),
            msg="Функция должна искать все вхождения"
        )
        self.assertEqual(
            [0, 2, 4], self.func(self.text2, self.pattern2),
            msg="Функция должна искать все вхождения"
        )

    def test_finds_all_empties(self):
        """Проверка того, что функция ищет все вхождения пустого образца"""
        self.assertEqual(
            list(range(len(self.text1))), self.func(self.text1, ""),
            msg="Пустая строка должна находиться везде"
        )


# сравнения по скорости рабина карпа и простого перебора
random.seed(time.time())
dlina_str = random.randrange(100, 100000)
dlina_pat = random.randrange(1, int(dlina_str / 4))
st = generator_govna.generate_shit_right_now(dlina_stroki=dlina_str, dlina_pattern=dlina_pat)
tic = time.perf_counter()
x = nv.brute_force(st[0], st[1])
toc = time.perf_counter()
print(f"Вычисление 1 заняло {toc - tic:0.4f} секунд")
tic = time.perf_counter()
y = nv.rabinus_karpus(st[0], st[1])
toc = time.perf_counter()
print(f"Вычисление 2 заняло {toc - tic:0.4f} секунд")
if x != y:
    print("алгоритм наелся и спит(ошибка)")
# на конец для приличия тесты пройдем
unittest.main()
