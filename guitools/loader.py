
from typing import Tuple, List, Union
from os.path import isfile
from json import load


maxW = 'maxw'
maxH = 'maxh'
minNCells = 'mincells'
background = 'background'
objects = 'object'
players = 'player'
mobs = 'mob'
fullImage = 'fullimage'


DEFAULT_PARAMS = {
    maxW: 600,
    maxH: 400,
    minNCells: 10,
    background: None,
    objects: [],
    players: [],
    mobs: [],
    fullImage: False,
}


def paramsFromFile(
        filename: str) -> Tuple[
            Tuple[int, int], int, Union[None, str],
            List[str], List[str], List[str], bool]:

    if filename.endswith('.json'):
        return paramsFromJson(filename)

    return paramsFromConfig(filename)


def paramsFromJson(
        filename: str) -> Tuple[
            Tuple[int, int], int, Union[None, str],
            List[str], List[str], List[str], bool]:

    data = DEFAULT_PARAMS.copy()

    with open(filename, 'r') as f:
        file = load(f)

    data.update(file)

    config = (
        (data[maxW], data[maxH]), data[minNCells], data[background],
        data[objects], data[players], data[mobs], data[fullImage]
    )

    return config


def paramsFromConfig(
        filename: str
        ) -> Tuple[
            Tuple[int, int], int, Union[None, str],
            List[str], List[str], List[str], bool]:

    data = DEFAULT_PARAMS.copy()

    with open(filename, 'r') as file:
        lines = file.readlines()

    for idx, line in enumerate(lines, 1):

        if '#' in line:
            line = line[:line.index('#')]

        line = line.strip()

        if not len(line):
            continue

        key, value, *rest = line.split('=')
        if len(rest):
            raise ValueError(
                f'Error en fichero de configuracion "{filename}", linea {idx}')

        key, value = key.strip().lower(), value.strip()

        if key == maxW:
            try:
                data[key] = int(value)
            except ValueError:
                raise ValueError(
                    f'Valor invalido en linea {idx} {key}:{value}')

        elif key == maxH:
            try:
                data[key] = int(value)
            except ValueError:
                raise ValueError(
                    f'Valor invalido en linea {idx} {key}:{value}')

        elif key == minNCells:
            try:
                data[key] = int(value)
            except ValueError:
                raise ValueError(
                    f'Valor invalido en linea {idx} {key}:{value}')

        elif key == background:
            if not isfile(value):
                raise ValueError(
                    f'El fichero de fondo "{value}" no existe')
            data[key] = value

        elif key == objects:
            if not isfile(value):
                raise ValueError(
                    f'El fichero de objeto "{value}" no existe')

            data[key].append(value)
        elif key == players:
            if not isfile(value):
                raise ValueError(
                    f'El fichero de objeto "{value}" no existe')

            data[key].append(value)
        elif key == mobs:
            if not isfile(value):
                raise ValueError(
                    f'El fichero de objeto "{value}" no existe')

            data[key].append(value)
        elif key == fullImage:
            value = value.lower()
            if value == 'true':
                value = True
            elif value == 'false':
                value = False
            else:
                raise ValueError(
                    'Esperado valor booleano en parametro '
                    f'"{key}", obtenido {value}')

            data[key] = value
        else:
            print(f'Parametro invalido en linea {idx} "{key}" -> "{line}"')

    config = (
        (data[maxW], data[maxH]), data[minNCells], data[background],
        data[objects], data[players], data[mobs], data[fullImage]
    )

    return config
