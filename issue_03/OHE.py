from typing import List, Tuple
import unittest


class TestFitTransform(unittest.TestCase):
    """класс тестирует функцию fit_transform"""

    def test_diff_cities(self):
        """сравнение результата функции с ожидаемым результатом"""
        actual_trans_cities = fit_transform(['Moscow', 'New York',
                                            'Moscow', 'London'])
        expected_trans_cities = [
            ('Moscow', [0, 0, 1]),
            ('New York', [0, 1, 0]),
            ('Moscow', [0, 0, 1]),
            ('London', [1, 0, 0]),
        ]
        self.assertEqual(actual_trans_cities, expected_trans_cities)

    def test_all_equal_cat(self):
        """сравнение результата функции с ожидаемым результатом,
        когда задается одна категория"""
        actual_trans_cities = fit_transform(['Moscow', 'Moscow', 'Moscow'])
        expected_trans_cities = [
            ('Moscow', [1]),
            ('Moscow', [1]),
            ('Moscow', [1])
        ]
        self.assertEqual(actual_trans_cities, expected_trans_cities)

    def test_order_matters(self):
        """тест проверяет, имеет ли значение порядок заданных
        категорий: сравнивает с теми же категориями в другом порядке"""
        actual_trans_words = fit_transform(['I', 'love', 'python'])
        expected_trans_words = [
            ('I', [0, 1, 0]),
            ('love', [0, 0, 1]),
            ('python', [1, 0, 0]),
        ]
        self.assertNotEqual(actual_trans_words, expected_trans_words)

    def test_empty_args(self):
        """проверка на исключение, когда аргументы
        не были переданы в fit_transform"""
        with self.assertRaises(TypeError):
            fit_transform()


def fit_transform(*args: str) -> List[Tuple[str, List[int]]]:
    """
    fit_transform(iterable)
    fit_transform(arg1, arg2, *args)
    """
    if len(args) == 0:
        raise TypeError('expected at least 1 arguments, got 0')

    categories = args if isinstance(args[0], str) else list(args[0])
    uniq_categories = set(categories)
    bin_format = f'{{0:0{len(uniq_categories)}b}}'

    seen_categories = dict()
    transformed_rows = []

    for cat in categories:
        bin_view_cat = (int(b) for b in
                        bin_format.format(1 << len(seen_categories)))
        seen_categories.setdefault(cat, list(bin_view_cat))
        transformed_rows.append((cat, seen_categories[cat]))

    return transformed_rows


if __name__ == '__main__':
    print(fit_transform(['Moscow']))
