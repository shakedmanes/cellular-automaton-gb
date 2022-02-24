from random import choice


class DirectionMatrix:
    """
    Direction matrix for calculating all directions within the matrix
    """

    __all_directions = [
        'up',
        'down',
        'right',
        'left',
        'up_right',
        'up_left',
        'down_right',
        'down_left'
    ]

    __opposite_directions = {
        'up': 'down',
        'down': 'up',
        'right': 'left',
        'left': 'right',
        'up_right': 'down_left',
        'up_left': 'down_right',
        'down_right': 'up_left',
        'down_left': 'up_right'
    }

    @classmethod
    def get_all_directions(cls):
        """
        Gather all directions functions within the class

        :return: List of possible directions in the class
        """
        return cls.__all_directions

    @classmethod
    def get_opposite_direction(cls, direction):
        """
        Returns the opposite direction for a given direction

        :param direction: Direction to get opposite direction to
        :return: Opposite direction
        """
        return cls.__opposite_directions[direction]

    @classmethod
    def get_possible_direction_from_location(cls, location, border_size):
        """
        Returns all the possible directions from a given location

        :param location: Location to move from
        :param border_size: The border size bounds
        :return: List of possible directions from the given location
        """
        curr_possible_directions = set(cls.get_all_directions())
        location_row, location_col = location

        # If the location on the first row, means we can't move up, so all the up directions are removed
        if location_row == 0:
            curr_possible_directions -= {'up', 'up_left', 'up_right'}

        # If the location on the first column, means we can't move left, so all the left directions are removed
        if location_col == 0:
            curr_possible_directions -= {'left', 'up_left', 'down_left'}

        # If the location is on the border size row
        # means we can't move down, so all the down directions are removed
        if location_row == border_size - 1:
            curr_possible_directions -= {'down', 'down_left', 'down_right'}

        # If the location is on the border size column
        # means we can't move right, so all the right directions are removed
        if location_col == border_size - 1:
            curr_possible_directions -= {'right', 'up_right', 'down_right'}

        return list(curr_possible_directions)

    @staticmethod
    def up(row, col):
        return row - 1, col

    @staticmethod
    def down(row, col):
        return row + 1, col

    @staticmethod
    def right(row, col):
        return row, col - 1

    @staticmethod
    def left(row, col):
        return row, col + 1

    @classmethod
    def up_right(cls, row, col):
        location = cls.up(row, col)
        return cls.right(location[0], location[1])

    @classmethod
    def up_left(cls, row, col):
        location = cls.up(row, col)
        return cls.left(location[0], location[1])

    @classmethod
    def down_right(cls, row, col):
        location = cls.down(row, col)
        return cls.right(location[0], location[1])

    @classmethod
    def down_left(cls, row, col):
        location = cls.down(row, col)
        return cls.left(location[0], location[1])
