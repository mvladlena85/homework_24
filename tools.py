import re
from typing import Dict, List, Tuple, Optional, Generator, Set, Iterator, Any


def dict_to_list(data: Dict[Optional[Any], str]) -> List[Tuple[str, str]]:
    """
        перевод формата даных из dict вида:
            {
                "file_name": "apache_logs.txt",
                "cmd1": "filter",
                "value1": "POST",
                "cmd2": "map",
                "value2": "0"
            }
        в более удобный формат для итерирования [(cmd, value)]:
            [("filter", "POST"), ("map", "0")]
    """
    i = 1
    res_list = []
    while True:
        try:
            param = data['cmd' + str(i)]
            value = data['value' + str(i)]
            res_list.append((param, value))
            i += 1
        except KeyError:
            break
    return res_list


def file_gen(file_path: str) -> Generator:
    """
        Генератор для считывания данных с файла
    """
    with open(file_path, encoding='utf-8', mode='r') as f:
        for line in f:
            yield line


def filter_data(value: str, data: Iterator[str]) -> Iterator[str]:
    """
        Фильтрация данных по параметру value
    """
    return filter(lambda v: value in v, data)


def map_data(value: str, data: Iterator[str]) -> Iterator[str]:
    """
        Отображение данных колонки под номером 'value'
    """
    return map(lambda v: v.split(" ")[int(value)], data)


def unique(data: Iterator[str]) -> Iterator[str]:
    """
        Оставляет только уникальные значения
    """
    return iter(set(data))


def sort_data(value: str, data: Iterator[str]) -> Iterator[str]:
    """
        Сортировка данных по параметру value: "asc/desc"
    """
    return iter(sorted(data, reverse=True if value == "desc" else False))


def limit(value: str, data: Iterator[str]) -> Iterator[str]:
    """
        Выводит только указанное в value количество записей
    """
    result = []
    try:
        for i in range(int(value)):
            result.append(next(data))
    except StopIteration:
        pass
    return iter(result)


def regex(value: str, data: Iterator[str]) -> Iterator[str]:
    """
        Фильтрация строк по регулярному выражению value
    """
    reg_ex = re.compile(value)
    result = []
    try:
        while True:
            line = next(data)
            m = reg_ex.search(line)
            if m is not None:
                result.append(line)
    except StopIteration:
        pass
    return iter(result)


def query(cmd: str, value: str, data: Iterator[str]) -> Iterator[str]:
    """
        Выбор запроса cmd: ["filter", "map", "unique", "sort", "limit"]
    """
    if cmd == "regex":
        return regex(value, data)
    if cmd == "filter":
        return filter_data(value, data)
    if cmd == "map":
        return map_data(value, data)
    if cmd == "unique":
        return unique(data)
    if cmd == "sort":
        return sort_data(value, data)
    if cmd == "limit":
        return limit(value, data)
    return data
