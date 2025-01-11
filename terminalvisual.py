
from guitools.loader import paramsFromFile, DEFAULT_PARAMS
from visual import loop

import argparse


def getParser():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-f', '--file',
        help='Fichero de configuracion .config o .json',
        default=None)

    parser.add_argument(
        '-mw', '--maxwidth', help='Maxima anchura de la ventana',
        default=DEFAULT_PARAMS['maxw'], type=int)
    parser.add_argument(
        '-mh', '--maxheight', help='Maxima altura de la ventana',
        default=DEFAULT_PARAMS['maxh'], type=int)

    parser.add_argument(
        '-c', '--mincells', help='Minimo numero de celdas en un lado',
        default=DEFAULT_PARAMS['mincells'], type=int)

    parser.add_argument(
        '-bg', '--background', help='Fichero de fondo',
        default=DEFAULT_PARAMS['background'])

    parser.add_argument(
        '-obj', '--object', help='Fichero de imagen de objeto',
        default=DEFAULT_PARAMS['object'],
        action="extend", nargs="+", type=str)

    parser.add_argument(
        '-p', '--player', help='Fichero de imagen de jugador',
        default=DEFAULT_PARAMS['player'],
        action="extend", nargs="+", type=str)

    parser.add_argument(
        '-m', '--mob', help='Fichero de imagen de mob',
        default=DEFAULT_PARAMS['mob'],
        action="extend", nargs="+", type=str)

    parser.add_argument(
        '-fi', '--fullimage',
        help='Hacer que salga la imagen de fondo sin cortar',
        default=False, action='store_true')

    return parser


if __name__ == '__main__':
    parser = getParser()
    args = parser.parse_args()

    if args.file is not None:
        try:
            params = paramsFromFile(args.file)
        except ValueError as e:
            print(e)
            exit()
    else:
        params = (
            (args.maxwidth, args.maxheight), args.mincells,
            args.background, args.object, args.player, args.mob,
            args.fullimage)

    print('Parametros:', *params)
    try:
        loop(*params)
    except ValueError as e:
        print(e)
        exit()
