
from settings import LogicSettings, CellTypes
from cells.world_cell import WorldCell
from cells.earth_cell import EarthCell
from cells.sea_cell import SeaCell
from cells.city_cell import CityCell
from cells.iceberg_cell import IcebergCell
from cells.forest_cell import ForestCell


class CellFactory:

    @classmethod
    def create_cell(cls, cell_type, cell_temp=None, cell_air_pollution=None, wind_instance=None, cloud_instance=None):
        """
        Creates cell by given type and attaching it wind and cloud instances

        :param cell_type: Cell type to create
        :param cell_temp: Temperature of the cell to create
        :param cell_air_pollution: Air pollution of the cell to create
        :param wind_instance: Instance of wind object
        :param cloud_instance: Instance of cloud object
        :return: New cell of the given type
        """
        return cls.__create_cell_with_values(
            cell_temp=cell_temp,
            cell_air_pollution=cell_air_pollution,
            cell_type=cell_type,
            cell_instance=None,
            wind_instance=wind_instance,
            cloud_instance=cloud_instance
        )

    @classmethod
    def change_cell_type(cls, curr_cell_instance, cell_type):
        """
        Changes existing cell type to given cell type

        :param curr_cell_instance: Current cell instance which will change type
        :param cell_type: The cell type to change to
        :return: New cell instance with the same properties as the previous but in the given type
        """
        return cls.__create_cell_with_values(cell_type=cell_type, cell_instance=curr_cell_instance)

    @staticmethod
    def __create_cell_with_values(cell_type, cell_temp=None, cell_air_pollution=None, cell_instance=None, wind_instance=None, cloud_instance=None):
        """
        Internal create cell function which handles both copying existing cell instance and creating brand new cell

        :param cell_type: The type of the cell to create
        :param cell_temp: The temperature of the cell to create
        :param cell_air_pollution: The air pollution of the cell to create
        :param cell_instance: Existing cell instance or None if needed brand new cell
        :param wind_instance: Wind instance to copy to the new cell
        :param cloud_instance: Cloud instance to copy to the new cell
        :return: New cell of the given type
        """
        temp = cell_temp
        air_pollution = cell_air_pollution
        applying_wind_instance = wind_instance
        applying_cloud_instance = cloud_instance

        # Checking if the cell is actual world cell
        if isinstance(cell_instance, WorldCell):
            temp = cell_instance.temp
            air_pollution = cell_instance.air_pollution
            applying_wind_instance = cell_instance.wind
            applying_cloud_instance = cell_instance.cloud

        if cell_type == CellTypes.EARTH:
            return EarthCell(
                temp=temp,
                air_pollution=air_pollution,
                wind_instance=applying_wind_instance,
                cloud_instance=applying_cloud_instance
            )
        elif cell_type == CellTypes.SEA:
            return SeaCell(
                temp=temp,
                air_pollution=air_pollution,
                wind_instance=applying_wind_instance,
                cloud_instance=applying_cloud_instance
            )
        elif cell_type == CellTypes.CITY:
            return CityCell(
                temp=temp,
                air_pollution=air_pollution,
                wind_instance=applying_wind_instance,
                cloud_instance=applying_cloud_instance
            )
        elif cell_type == CellTypes.ICEBERG:
            return IcebergCell(
                temp=temp,
                air_pollution=air_pollution,
                wind_instance=applying_wind_instance,
                cloud_instance=applying_cloud_instance
            )
        elif cell_type == CellTypes.FOREST:
            return ForestCell(
                temp=temp,
                air_pollution=air_pollution,
                wind_instance=applying_wind_instance,
                cloud_instance=applying_cloud_instance
            )
        else:
            raise TypeError('Bad cell type given.')

