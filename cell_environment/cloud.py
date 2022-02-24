from random import randint


class Cloud:
    """
    Represent cloud capability for specific cell in the world.
    """
    __max_precipitation = 100
    __precipitation_grow_factor = 10

    def __init__(self, cloud_instance=None, precipitation=None):
        if isinstance(cloud_instance, Cloud):
            self._copy_values(cloud_instance)
        else:
            self.__precipitation = precipitation or Cloud.generate_precipitation()

    @property
    def precipitation(self):
        """
        Getter for precipitation of the cloud

        :return: Precipitation percentage
        """
        return self.__precipitation

    @precipitation.setter
    def precipitation(self, new_precipitation):
        """
        Setter for precipitation of the cloud

        :param new_precipitation: Precipitation percentage to set
        """
        self.__precipitation = new_precipitation

    @staticmethod
    def generate_precipitation():
        """
        Generate random precipitation value

        :return: Random generated precipitation percentage
        """
        return randint(0, Cloud.__max_precipitation)

    def should_rain(self):
        """
        Returns if the cloud should rain right now.

        :return: True if the cloud should rain right now, Otherwise false.
        """
        return self.__precipitation == Cloud.__max_precipitation

    def next_generation(self):
        """
        Updates the cloud properties as generation passed.
        Each generation the precipitation of the grow by 10%.
        If the precipitation was 100% in the last generation, it resets to 0%.
        """
        if self.__precipitation >= Cloud.__max_precipitation:
            self.__precipitation = 0
        else:
            self.__precipitation += Cloud.__precipitation_grow_factor

    def _copy_values(self, cloud_instance):
        """
        Copy values from existing cloud instance.

        :param cloud_instance: Cloud instance to copy from.
        """
        self.__precipitation = cloud_instance.precipitation
