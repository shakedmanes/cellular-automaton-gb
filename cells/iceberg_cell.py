from cells.world_cell import WorldCell
from settings import LogicSettings, CellTypes


class IcebergCell(WorldCell):
    """
    Represent an iceberg cell in the world.
    """
    _cell_type = CellTypes.ICEBERG

    _temp_sea_cell_factor = 0
    _temp_neighbors_decrease_factor = -0.025

    def __init__(self, temp=None, air_pollution=None, wind_instance=None, cloud_instance=None):
        super().__init__(
            temp=temp,
            air_pollution=air_pollution,
            wind_instance=wind_instance,
            cloud_instance=cloud_instance
        )

    def next_generation(self):
        """
        Updates the iceberg cell properties as generation passed.
        Does all the things default world cell does, but including:

        - When the temperature reach 0 (or more) celsius, iceberg cells become Sea Cells.
        - Each generation, iceberg cells cools temperature in their neighborhood by temperature factor.

        :return: Object of changes which occurs outside the cell (wind properties and more)
        """
        generation_changes = super().next_generation()

        # If the temperature reach 0 (or more) celsius, iceberg cells become Sea Cells
        if self.temp >= IcebergCell._temp_sea_cell_factor:
            generation_changes['cell_change'] = CellTypes.SEA

        # Iceberg cells cools temperature in their neighborhood by temperature factor
        generation_changes['apply_changes_locations'] = {
            'field': 'temp',
            'locations': self._get_all_neighbors_directions(),
            'value': IcebergCell._temp_neighbors_decrease_factor
        }

        return generation_changes
