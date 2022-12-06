import urllib.request
import json

import pytest
import io
from unittest.mock import patch


API_URL = 'http://worldclockapi.com/api/json/utc/now'

YMD_SEP = '-'
YMD_SEP_INDEX = 4
YMD_YEAR_SLICE = slice(None, YMD_SEP_INDEX)

DMY_SEP = '.'
DMY_SEP_INDEX = 5
DMY_YEAR_SLICE = slice(DMY_SEP_INDEX + 1, DMY_SEP_INDEX + 5)


def test_dot_in_time():
    """Проверяет, что верно работает с датой с '.' """
    date = io.StringIO('{"currentDateTime": "01.05.2022"}')
    with patch('urllib.request.urlopen') as response:
        response.return_value = date
        assert what_is_year_now() == 2022


def test_dash_in_time():
    """Проверяет, что верно работает с датой с '-' """
    date = io.StringIO('{"currentDateTime": "2022-01-05"}')
    with patch('urllib.request.urlopen') as response:
        response.return_value = date
        assert what_is_year_now() == 2022


def test_wrong_format():
    """Проверяет на ошибку при неверном формате даты"""
    date = io.StringIO('{"currentDateTime": "2022:01:05"}')
    with patch('urllib.request.urlopen') as response:
        response.return_value = date
        with pytest.raises(ValueError):
            what_is_year_now()


def test_wrong_length():
    """Проверяет на ошибку при вводе неполной даты,
    либо знаков меньше ожидаемого количества"""
    date = io.StringIO('{"currentDateTime": "2022"}')
    with patch('urllib.request.urlopen') as response:
        response.return_value = date
        with pytest.raises(IndexError):
            what_is_year_now()


def what_is_year_now() -> int:
    """
    Получает текущее время из API-worldclock и
    извлекает из поля 'currentDateTime' год
    Предположим, что currentDateTime может быть в двух форматах:
      * YYYY-MM-DD - 2019-03-01
      * DD.MM.YYYY - 01.03.2019
    """
    with urllib.request.urlopen(API_URL) as resp:
        resp_json = json.load(resp)

    datetime_str = resp_json['currentDateTime']
    if datetime_str[YMD_SEP_INDEX] == YMD_SEP:
        year_str = datetime_str[YMD_YEAR_SLICE]
    elif datetime_str[DMY_SEP_INDEX] == DMY_SEP:
        year_str = datetime_str[DMY_YEAR_SLICE]
    else:
        raise ValueError('Invalid format')

    return int(year_str)
