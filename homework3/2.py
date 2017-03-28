from abc import ABC, abstractmethod
import csv, json


def csv_load(file: object) -> str:
    reader = csv.reader(file)
    result = ""
    for row in reader:
        result += row[0] + '\n'
    result = result.replace(';', ' ').rstrip()
    return result


def csv_save(s: str, file: object) -> None:
    s = s.split(" ")
    writer = csv.writer(file, delimiter=";", escapechar=None, quoting=csv.QUOTE_NONE, lineterminator='')
    writer.writerow(s)


def json_load(file: object) -> str:
    return '\n'.join(json.load(file)['rows'])


def json_save(s: str, file: object) -> None:
    s = s.split("\n")
    json.dump({'rows': s}, file, separators=(',', ': '))


class AbsConverterFabric(ABC):
    @abstractmethod
    def create_converter(self, _from: str, _to: str) -> object:
        raise NotImplemented


class AbstractConverter(ABC):
    @abstractmethod
    def load(self, file: object) -> str:
        raise NotImplemented

    @abstractmethod
    def save(self, s: str, file: object) -> object:
        raise NotImplemented


class ConverterFabric(AbsConverterFabric):
    def create_converter(self, _from: str, _to: str) -> object:
        if _from == 'json':
            load = json_load
        if _from == 'csv':
            load = csv_load

        if _to == 'json':
            save = json_save
        if _to == 'csv':
            save = csv_save
        return type('Converter', (AbstractConverter,), {'load': load, 'save': save})

fab = ConverterFabric()
converter1 = fab.create_converter('csv', 'json')
converter2 = fab.create_converter('json', 'csv')


with open('csv.txt', 'r') as file:
    result = converter1.load(file)
    print(result)

print()

with open('json.txt', 'w') as file:
    converter1.save(result, file)

with open('json.txt', 'r') as file:
    result = converter2.load(file)
    print(result)

with open('csv.txt', 'w') as file:
    converter2.save(result, file)


# with open('json.txt', 'r') as myfile:
#     string = json_load(myfile)
#
# with open('csv.txt', 'r') as myfile:
#     string = csv_load(myfile)
#
# with open('csv.txt', 'w') as myfile:
#     csv_save(string, myfile)
#
# with open('json.txt', 'w') as myfile:
#     json_save(string, myfile)
