from random import randint

from settings import LogicSettings
from direction_matrix import DirectionMatrix


class WorldCell:
    """
    Represent an abstraction for cell in the world.
    """
    _cell_type = None
    _air_pollution_heat_bound = 0.60
    _air_pollution_cool_bound = 0.25
    _air_pollution_heat_temp_factor = 0.35
    _air_pollution_cool_temp_factor = -0.05
    _wind_air_pollution_percentage_factor = 0.35
    _cloud_rain_temp_cool_factor = -1.5
    _cloud_rain_air_pollution_drop_percentage_factor = -0.25

    def __init__(self, temp=None, air_pollution=None, wind_instance=None, cloud_instance=None):
        """
        Creates a cell in the world which have the following properties:

        :param temp: Temperature of the cell, If none given it will be determined by the cell logic.
        :param air_pollution: The percentage of air pollution in the cell, If none given it will be determined by the cell logic.
        """
        self._temp = temp or self._random_temp()
        self._air_pollution = air_pollution or 0
        self._wind_instance = wind_instance
        self._cloud_instance = cloud_instance

    @property
    def type(self):
        if self._cell_type is not None:
            return self._cell_type

        raise AssertionError('Abstract cell type determined, need to override the world cell class.')

    @property
    def temp(self):
        """
        Getter for temp property.

        :return: Temperature value.
        """
        return self._temp

    @temp.setter
    def temp(self, new_temp):
        """
        Setter for temp property.

        :param new_temp: New temp value.
        """
        if new_temp > 150:
            self._temp = 150
        elif new_temp < -50:
            self._temp = -50
        else:
            self._temp = new_temp

    @property
    def air_pollution(self):
        """
        Getter for air pollution property.

        :return: Air pollution value.
        """
        return self._air_pollution

    @air_pollution.setter
    def air_pollution(self, new_air_pollution):
        """
        Setter for temp property.

        :param new_air_pollution: New air pollution value.
        """
        if new_air_pollution > 1:
            self._air_pollution = 1
        elif new_air_pollution < 0:
            self._air_pollution = 0
        else:
            self._air_pollution = new_air_pollution

    @property
    def wind(self):
        """
        Getter for wind property.

        :return: Wind instance of the cell.
        """
        return self._wind_instance

    @wind.setter
    def wind(self, new_wind):
        """
        Setter for wind property.

        :param new_wind: New wind instance value.
        """
        self._wind_instance = new_wind

    @property
    def cloud(self):
        """
        Getter for cloud property.

        :return: Cloud instance of the cell.
        """
        return self._cloud_instance

    @cloud.setter
    def cloud(self, new_cloud):
        """
        Setter for cloud property.

        :param new_cloud: New cloud instance value.
        """
        self._cloud_instance = new_cloud

    def next_generation(self):
        """
        Updates the world cell properties as generation passed.
        As defaults:

        - If cloud rains - temperature drops by rain factor and air pollution drops by rain air pollution drop factor.
        - If air pollution above heat bound - temperature grows by heat factor.
        - If air pollution below cool bound - temperature drops by cool factor.

        :return: Object of changes which occurs outside the cell (wind properties and more)
        """

        generation_changes = {}

        # If cloud exists, update the properties of the cell accordingly
        if self.cloud is not None:
            if self.cloud.should_rain():
                self.temp += WorldCell._cloud_rain_temp_cool_factor
                self.air_pollution += self.air_pollution * WorldCell._cloud_rain_air_pollution_drop_percentage_factor

            # Continue in the next generation of the cloud
            self.cloud.next_generation()

        # If wind exists, update the properties of the cell accordingly
        if self.wind is not None:
            generation_changes['environment'] = {
                **self.wind.next_generation(),
                'wind_instance': self.wind,
                'cloud_instance': self.cloud,
                'air_pollution_passed': self.air_pollution * WorldCell._wind_air_pollution_percentage_factor
            }

        # If the air pollution is below the cooling bound, the cell can be cooled
        if self.air_pollution <= WorldCell._air_pollution_cool_bound:
            self.temp += WorldCell._air_pollution_cool_temp_factor

        # If the air pollution is above the heating bound, the cell can be heated
        if self.air_pollution >= WorldCell._air_pollution_heat_bound:
            self.temp += WorldCell._air_pollution_heat_temp_factor

        return generation_changes

    def _random_temp(self):
        """
        Generates random temperature for the cell by its temp rules corresponding to its type.

        :return: Temperature for the cell
        """
        if self._cell_type is not None:
            return randint(
                LogicSettings.TEMP.get(self._cell_type).get('START'),
                LogicSettings.TEMP.get(self._cell_type).get('END')
            )

        return 0

    def _get_all_neighbors_directions(self):
        """
        Returns all the possible neighbors directions (Basically all directions possible)

        :return: List of functions to calculate directions to neighbors
        """
        return [getattr(DirectionMatrix, direction) for direction in DirectionMatrix.get_all_directions()]
