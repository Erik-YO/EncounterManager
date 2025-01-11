
# EncounterManager

A simple visualization and creation tool for TTRPG encounters implemented with Pygame.

Tested on python 3.10.9

## Features

It supports:
- 3 kinds of movable elements
  - Players (green outer ring)
  - Enemies (red outer ring)
  - Objects
- Adjustable grid: cell size and object placement
- Adjustable sizes for entities
  - Quarter of a cell
  - Half a cell
  - 1 cell
  - 2 cells
  - ...
- Static background image



# Use

_Note: the pyw extension makes so that it can be executed without a terminal popping up._
That's it, the rest can 

## For creation

```
python creator.pyw
```


## For terminal input instead

This is mostly for testing purposes. It only supports visualization.

```
python310 terminalvisual.py -bg imgs/backgrounds/barco.jpg -mw 600 -mh 800 -c 11 -obj "imgs/tripulacion/Lepto Silgoy.jpg" imgs/tripulacion/sailor.jpg imgs/tripulacion/sailor.jpg -p imgs/Mokba.png imgs/Isaias.jpg -m imgs/Noah.jpg
```

```
python310 terminalvisual.py -fi -bg imgs/backgrounds/bg1.jpg -mw 1400 -mh 800 -c 13 -p imgs/p1.png imgs/p2.jpg imgs/p3.jpg -m imgs/mobs/e1.png imgs/mobs/e2.png
```

```
python310 terminalvisual.py -bg imgs/backgrounds/bg2.jpg -mw 700 -mh 700 -c 10 -p imgs/p1.jpg -m imgs/mobs/e1.png
```

Using a configuration file:

```
python310 terminalvisual.py -f encounters/barco.json
python310 terminalvisual.py -f encounters/forest.config
```

barco.config
```
maxw = 600
maxh = 800
mincells = 11
background = imgs/backgrounds/barco.jpg

object = imgs/tripulacion/Lepto Silgoy.jpg
object = imgs/tripulacion/sailor.jpg
object = imgs/tripulacion/sailor.jpg

player = imgs/Mokba.png
player = imgs/Isaias.jpg

mob = imgs/Noah.jpg
mob = imgs/bichos/shadow.jpg

fullImage = false
```

barco.json
```
{
    "maxw": 600,
    "maxh": 800,
    "mincells": 11,
    "background": "imgs/backgrounds/barco.jpg",
    "object": [
        "imgs/tripulacion/Lepto Silgoy.jpg",
        "imgs/tripulacion/sailor.jpg",
        "imgs/tripulacion/sailor.jpg"
    ],
    "player": [
        "imgs/Mokba.png",
        "imgs/Isaias.jpg"
    ],
    "mob": [
        "imgs/Noah.jpg"
    ],
    "fullImage": false
}
```

noah.json
```
{
    "maxw": 700,
    "maxh": 700,
    "mincells": 10,
    "background": "imgs/backgrounds/bg_noah.png",
    "player": [
        {
            "img": "imgs/Noah.jpg",
            "x": 4,
            "y": 8
        }
    ],
    "mob": [
        {
            "img": "imgs/bichos/shadow.jpg",
            "x": 4,
            "y": 1
        }
    ]
}
```


