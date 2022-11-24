# ISSUE_05
Задание: Дана функция, возвращающая текущий год. Дату и время получаем из API-worldclock.
Напишите на неё тесты, проверяющие все сценарии работы.

Установка:
>pip install -U pytest
>pip install pytest-cov

Запуск теста:
>python -m pytest -v what_is_year_now.py

Запуск test coverage:
>python -m pytest -q what_is_year_now.py --cov

Сохранить отчет о покрытии в виде html файла:
>python -m pytest -q what_is_year_now.py --cov . --cov-report html
