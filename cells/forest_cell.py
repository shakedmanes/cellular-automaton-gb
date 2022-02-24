from cells.world_cell import WorldCell
from settings import LogicSettings, CellTypes


class ForestCell(WorldCell):
    """
    Represent an forest cell in the world.
    """
    _cell_type = CellTypes.FOREST

    _temp_earth_cell_factor = 60
    _air_pollution_earth_cell_factor = 0.8
    _air_pollution_neighbors_decrease_factor = -0.03

    def __init__(self, temp=None, air_pollution=None, wind_instance=None, cloud_instance=None):
        super().__init__(
            temp=temp,
            air_pollution=air_pollution,
            wind_instance=wind_instance,
            cloud_instance=cloud_instance
        )

    def next_generation(self):
        """
        Updates the forest cell properties as generation passed.
        Does all the things default world cell does, but including:

        - Each generation, forest cells reduce air pollution in their neighborhood.
        - When the temperature reach temperature factor (or more), forest cells become Earth Cells.
        - When the air pollution reach air pollution factor (or more), forest cells become Earth Cells.

        :return: Object of changes which occurs outside the cell (wind properties and more)
        """
        generation_changes = super().next_generation()

        # Each generation, forest cells reduce air pollution in their neighborhood
        generation_changes['apply_changes_locations'] = {
            'field': 'air_pollution',
            'locations': self._get_all_neighbors_directions(),
            'value': ForestCell._air_pollution_neighbors_decrease_factor
        }

        # If the temperature reach temperature factor (or more), forest cells become Earth Cells
        if self.temp >= ForestCell._temp_earth_cell_factor:
            generation_changes['cell_change'] = CellTypes.EARTH

        # If the air pollution reach air pollution factor (or more), forest cells become Earth Cells
        if self.air_pollution >= ForestCell._air_pollution_earth_cell_factor:
            generation_changes['cell_change'] = CellTypes.EARTH

        return generation_changes
