from typing import Dict, Union, Tuple, Optional
from pygame import Surface, draw, BLEND_RGBA_MULT, SRCALPHA
from .const import prepImage, loadImage


class Elemento:

    def __init__(
            self, imgdata: Union[str, Dict[str, Union[str, int]]],
            defaultsize: float, circular: bool, lockable: bool,
            aura: Optional[Tuple[int, int, int]] = None) -> None:
        '''
        imgdata:
            - img o {img, [x], [y], [size]}
            - donde size es: int >= 1 o float = 1 / 2^n
        '''

        self.posx = 0
        self.posy = 0
        self.sizecategory = 1
        self.aura = aura

        if isinstance(imgdata, str):
            image = imgdata
        else:
            self.posx = imgdata.get('x', 0)
            self.posy = imgdata.get('y', 0)
            self.sizecategory = imgdata.get('size', 1)
            image = imgdata.get('img', None)

            if (
                    not isinstance(self.posx, int) or
                    not isinstance(self.posy, int)):
                print(type(self.posx), type(self.posy), self.posx, self.posy)
                raise ValueError(
                    'La posición de los elementos debe estar '
                    'definida por números enteros')
            if not isinstance(self.sizecategory, (int, float)):
                raise ValueError(
                    'La categoria de tamaño debe ser un número')
            if image is None:
                raise ValueError(
                    'Todos los elementos deben tener una '
                    f'imagen asociada {self.__class__.__name__}')

            self.posx *= defaultsize
            self.posy *= defaultsize

        self.basesize = defaultsize
        self.cellsize = self.basesize * self.sizecategory
        self.lockable = lockable
        self.circular = circular
        self.name = image

        self.image: Surface = None
        self.__reloadImage()

    def __reloadImage(self):
        self.image = prepImage(
            loadImage(self.name), self.cellsize, self.circular)

    def resize(self, newbasesize: int):
        self.cellsize = newbasesize * self.sizecategory
        self.posx = self.posx * newbasesize // self.basesize
        self.posy = self.posy * newbasesize // self.basesize
        self.basesize = newbasesize
        self.__reloadImage()

    def biggerCategory(self):
        if self.sizecategory >= 1:
            self.sizecategory += 1
        else:
            self.sizecategory *= 2

        self.cellsize = self.basesize * self.sizecategory
        self.__reloadImage()

    def smallerCategory(self):
        if self.sizecategory < 0.25:
            return

        if self.sizecategory > 1:
            self.sizecategory -= 1
        else:
            self.sizecategory /= 2

        self.cellsize = self.basesize * self.sizecategory
        self.__reloadImage()

    def show(
            self, window: Surface,
            transparency: bool = False,
            backprint: Optional[Tuple[int, int, int]] = None):

        alpha = 128
        if transparency:
            transparent = self.image.copy()
            transparent.fill((255, 255, 255, alpha), None, BLEND_RGBA_MULT)
            img = transparent

        else:
            img = self.image

        x, y = self.posx, self.posy
        if self.sizecategory < 1:
            x += self.cellsize / 2
            y += self.cellsize / 2
        x += 1
        y += 1

        if backprint is not None:
            if transparency:
                transparent = Surface(self.image.get_size(), SRCALPHA)
                transparent.fill((*backprint, alpha), None)
                window.blit(transparent, (x, y))
            else:
                draw.rect(
                    window, backprint, (x, y, self.cellsize, self.cellsize))

        if self.aura is not None and not transparency:
            draw.rect(
                window, self.aura,
                (x, y, self.cellsize, self.cellsize),
                0, round(self.cellsize / 2.5))

        window.blit(img, (x, y))

        return

    def inside(
            self, posOrX: Union[Tuple[float, float], float],
            y: Optional[float] = None
            ) -> bool:

        if y is None:
            x, y = posOrX
        else:
            x = posOrX

        if self.sizecategory < 1:
            portion = (self.basesize - self.cellsize) / 2
            x, y = x - portion, y - portion

        if self.posx > x or x > self.posx + self.cellsize:
            return False

        if self.posy > y or y > self.posy + self.cellsize:
            return False

        return True

    def __str__(self) -> str:
        return f'{self.__class__.__name__}{vars(self)}'

    def __repr__(self) -> str:
        return str(self)

    def data(self) -> Dict[str, Union[str, int]]:
        return {
            'img': self.name,
        } | ({
                'x': int((self.posx * self.sizecategory + 1) // self.cellsize),
                'y': int((self.posy * self.sizecategory + 1) // self.cellsize)
            } if self.posx or self.posy else {}
        ) | ({
            'size': self.sizecategory
            } if self.sizecategory != 1 else {}
        )


class Objeto(Elemento):

    def __init__(
            self, data: Union[str, Dict[str, Union[str, int]]],
            size: float) -> None:
        super().__init__(data, size, False, True)


class Creature(Elemento):

    def getColor(hostile: bool) -> Tuple[int, int, int]:
        return (250, 80, 80) if hostile else (80, 250, 80)

    def __init__(
            self, data: Union[str, Dict[str, Union[str, int]]],
            size: float, hostile: bool) -> None:
        super().__init__(data, size, True, False, Creature.getColor(hostile))


class Aliado(Creature):

    def __init__(
            self, data: Union[str, Dict[str, Union[str, int]]],
            size: float) -> None:
        super().__init__(data, size, False)


class Enemigo(Creature):

    def __init__(
            self, data: Union[str, Dict[str, Union[str, int]]],
            size: float) -> None:
        super().__init__(data, size, True)
