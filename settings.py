from enum import Enum
from os.path import abspath


class CellTypes(Enum):
    EARTH = 0
    SEA = 1
    CITY = 2
    ICEBERG = 3
    FOREST = 4


class AppSettings:
    """
    Contains configurations values for the automaton (GUI)
    """

    # App settings

    APP_TITLE = 'Global Warming Automaton'

    APP_FRAME = {
        'WIDTH': 1700,
        'HEIGHT': 1400
    }

    CELL_SIZE = {
        'WIDTH': 35,
        'HEIGHT': 35
    }

    NUM_CELLS = 30

    CANVAS = {
        'WIDTH': CELL_SIZE.get('WIDTH') * (NUM_CELLS + 5),  # Take padding of 5 cells
        'HEIGHT': CELL_SIZE.get('HEIGHT') * NUM_CELLS
    }

    CELL_INFO_DIALOG = {
        'WIDTH': 100,
        'HEIGHT': 100,
    }

    CELL_CUBE = {
        CellTypes.EARTH: {
            'COLOR': 'brown'
        },
        CellTypes.SEA: {
            'COLOR': 'blue'
        },
        CellTypes.CITY: {
            'COLOR': 'yellow'
        },
        CellTypes.ICEBERG: {
            'COLOR': 'white'
        },
        CellTypes.FOREST: {
            'COLOR': 'green'
        }
    }


class LogicSettings:
    """
    Contains configurations values for the automaton (GUI)
    """
    WORLD_FILE_PATH = f'{abspath("")}/world.csv'

    NUM_CELLS = AppSettings.NUM_CELLS

    TEMP = {
        CellTypes.EARTH: {
            'START': 20,
            'END': 28
        },
        CellTypes.SEA: {
            'START': 16,
            'END': 24
        },
        CellTypes.CITY: {
            'START': 20,
            'END': 28
        },
        CellTypes.ICEBERG: {
            'START': -24,
            'END': -10
        },
        CellTypes.FOREST: {
            'START': 18,
            'END': 26
        }
    }
