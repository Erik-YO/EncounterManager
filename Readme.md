
# Ejemplos de uso

## Por terminal


```
python310 main.py -bg imgs/backgrounds/barco.jpg -mw 600 -mh 800 -c 11 -obj "imgs/tripulacion/Lepto Silgoy.jpg" imgs/tripulacion/sailor.jpg imgs/tripulacion/sailor.jpg -p imgs/Mokba.png imgs/Isaias.jpg -m imgs/Noah.jpg
```

```
python310 main.py -fi -bg imgs/backgrounds/forest.jpg -mw 1400 -mh 800 -c 13 -p imgs/Mokba.png imgs/Isaias.jpg imgs/Noah.jpg -m "imgs/bichos/Battleforce Angel.png" "imgs/bichos/Astral Blight.png"
```

```
python310 main.py -bg imgs/backgrounds/bg_noah.jpg -mw 700 -mh 700 -c 10 -p imgs/Noah.jpg -m imgs/bichos/shadow.png
```

## Por fichero de configuracion

```
python310 main.py -f encounters/barco.json
python310 main.py -f encounters/forest.config
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


