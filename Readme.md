
# EncounterManager

A simple visualization and creation tool for TTRPG encounters implemented with Pygame.

Loosely tested on python 3.10.9

_Note: since the last commit, this repository has suffered a almost complete rework which has made the format uncompatible with the last version._

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

## Usage

_Note: the pyw extension makes so that it can be executed without a terminal popping up._

First, install the requirements:
```
python -m pip install -r requirements.txt
```

Then, run the code:
```
python main.py
```

And that's it. The default location for images and encounter files is the directory `~/.encountermanager/`.

From here, you can select a background image for a new encounter or a previously created encounter.


### Commands

A list of available commands.


| Shortcuts | Methods                |
| --------- | ---------------------- |
| B         | change_background      |
| W         | enlarge_window         |
| Ctrl + W  | shrink_window          |
| D         | switch_grid_visibility |
| G         | reduce_grid            |
| Ctrl + G  | enlarge_grid           |
| C         | change_entity_type     |
| T         | change_creature_team   |
| S         | change_creature_status |
| L         | make_entity_larger     |
| Ctrl + L  | make_entity_smaller    |
| H         | bring_home             |
| Ctrl + H  | bring_all_home         |
| A         | create_creature        |
| I         | create_item            |
| Click     | select_entity          |
| Esc       | deselect_entity        |
| Click     | move_entity            |
| Right     | move_entity_right      |
| Left      | move_entity_left       |
| Up        | move_entity_up         |
| Down      | move_entity_down       |
| Del, Supr | destroy_entity         |
| Ctrl + Z  | undo                   |
| Ctrl + Y  | redo                   |


WIP:
- Ctrl + C for copy
- Ctrl + V for paste


## Manual encounter creation and debugging

The encounter files are stored in `.json` format, you can find a couple of examples on the `examples/` directory.
