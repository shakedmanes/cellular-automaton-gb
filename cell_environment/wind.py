from random import randint, choice

from direction_matrix import DirectionMatrix


class Wind:
    """
    Represent wind capability for specific cell in the world.
    """
    __affect_speed_factor = 5
    __chance_direction_change = 0.25
    __chance_speed_change = 0.15

    def __init__(
            self,
            wind_instance=None,
            direction=None,
            speed=None,
            min_speed_range=0,
            max_speed_range=0,
            possible_direction_list=None
    ):
        if isinstance(wind_instance, Wind):
            self._copy_values(wind_instance)
        else:
            self.__min_speed_range = min_speed_range
            self.__max_speed_range = max_speed_range
            self.__possible_direction_list = possible_direction_list or DirectionMatrix.get_all_directions()
            self.__direction = direction or self.generate_wind_direction()
            self.__speed = speed or self.generate_wind_speed()

    def generate_wind_speed(self):
        """
        Generates random wind speed based on min and max speed range

        :return: Randomized speed in the given range.
        """
        return randint(self.__min_speed_range, self.__max_speed_range)

    def generate_wind_direction(self):
        """
        Generates random wind direction.

        :return: Randomized direction for the wind.
        """
        return choice(self.__possible_direction_list)

    @property
    def direction(self):
        """
        Getter for direction of the wind

        :return: The direction of the wind (function name of DirectionMatrix)
        """
        return self.__direction

    @direction.setter
    def direction(self, new_direction):
        """
        Setter for direction of the wind

        :param new_direction: Function name of DirectionMatrix which represent direction
        """
        self.__direction = new_direction

    @property
    def speed(self):
        """
        Getter for speed of the wind

        :return: Speed number (k/h)
        """
        return self.__speed

    @speed.setter
    def speed(self, new_speed):
        """
        Setter for speed of the wind

        :param new_speed: New speed number (k/h) to set
        """
        self.__speed = new_speed

    @property
    def max_speed_range(self):
        """
        Getter for max speed range for generation of speed of the wind

        :return: Max speed value
        """
        return self.__max_speed_range

    @max_speed_range.setter
    def max_speed_range(self, new_max_speed_range):
        """
        Setter for max speed range for generation of speed of the wind

        :param new_max_speed_range: New max speed number (k/h) to set
        """
        self.__max_speed_range = new_max_speed_range

    @property
    def min_speed_range(self):
        """
        Getter for min speed range for generation of speed of the wind

        :return: Min speed value
        """
        return self.__min_speed_range

    @min_speed_range.setter
    def min_speed_range(self, new_min_speed_range):
        """
        Setter for min speed range for generation of speed of the wind

        :param new_min_speed_range: New min speed number (k/h) to set
        """
        self.__min_speed_range = new_min_speed_range

    def get_affected_locations(self):
        """
        Returns list of affected locations by the wind speed and direction

        :return: List of functions which resolves location affected by the wind.
        """
        # Used for chaining multiple methods
        chainer = lambda func1, func2: lambda *args: func1(*func2(*args))

        # Calculating number of cells need to update
        num_cells_update = self.__speed // Wind.__affect_speed_factor
        curr_affected_loc_func = getattr(DirectionMatrix, self.__direction)
        affected_locations = [curr_affected_loc_func]

        # Iterating each number of cell needed to update so all the location functions will be included
        for _ in range(num_cells_update - 1):
            curr_affected_loc_func = chainer(getattr(DirectionMatrix, self.__direction), curr_affected_loc_func)
            affected_locations.append(curr_affected_loc_func)

        return affected_locations

    def next_generation(self):
        """
        Updates the next generation properties of the wind and return new generation changes

        :return: Dictionary containing the changes needed for the next generation of the wind
        """
        if self.speed > 0:
            return {
                'update_location': getattr(DirectionMatrix, self.__direction),
                'update_affected_locations': self.get_affected_locations()
            }
        return {}

    def set_opposite_direction(self):
        """
        Updates the wind direction to be the opposite from the current direction
        """
        self.direction = DirectionMatrix.get_opposite_direction(self.direction)

    def _copy_values(self, wind_instance):
        """
        Copy values from existing wind instance.

        :param wind_instance: Wind instance to copy from.
        """
        self.__direction = wind_instance.direction
        self.__speed = wind_instance.speed
        self.__min_speed_range = wind_instance.min_speed_range
        self.__max_speed_range = wind_instance.max_speed_range
