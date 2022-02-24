from cells.world_cell import WorldCell
from settings import LogicSettings, CellTypes


class SeaCell(WorldCell):
    """
    Represent a sea cell in the world.
    """
    _cell_type = CellTypes.SEA

    _temp_earth_cell_factor = 100
    _temp_iceberg_cell_factor = -1

    def __init__(self, temp=None, air_pollution=None, wind_instance=None, cloud_instance=None):
        super().__init__(
            temp=temp,
            air_pollution=air_pollution,
            wind_instance=wind_instance,
            cloud_instance=cloud_instance
        )

    def next_generation(self):
        """
        Updates the sea cell properties as generation passed.
        Does all the things default world cell does, but including:

        - When the temperature reach 100 celsius (or more), sea cells become Earth Cells.
        - When the temperature reach -1 celsius (or less), sea cells become Iceberg Cells.

        :return: Object of changes which occurs outside the cell (wind properties and more)
        """
        generation_changes = super().next_generation()

        # If the temperature reach 100 celsius (or more), sea cells become Earth Cells
        if self.temp >= SeaCell._temp_earth_cell_factor:
            generation_changes['cell_change'] = CellTypes.EARTH

        # If the temperature reach -1 celsius (or less), sea cells become Iceberg Cells
        if self.temp <= SeaCell._temp_iceberg_cell_factor:
            generation_changes['cell_change'] = CellTypes.ICEBERG

        return generation_changes
