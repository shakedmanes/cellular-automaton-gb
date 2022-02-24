from cells.world_cell import WorldCell
from settings import LogicSettings, CellTypes


class CityCell(WorldCell):
    """
    Represent an city cell in the world.
    """
    _cell_type = CellTypes.CITY

    _temp_earth_cell_factor = 95
    _temp_neighbors_increase_factor = 0.02
    _air_pollution_grow_factor = 0.08

    def __init__(self, temp=None, air_pollution=None, wind_instance=None, cloud_instance=None):
        super().__init__(
            temp=temp,
            air_pollution=air_pollution,
            wind_instance=wind_instance,
            cloud_instance=cloud_instance
        )

    def next_generation(self):
        """
        Updates the city cell properties as generation passed.
        Does all the things default world cell does, but including:

        - When the temperature reach predefined factor, city cells become Earth Cells.
        - Each generation the city cell heats the neighbors cells' temperature by predefined heat factor.
        - Produces air pollution each generation.

        :return: Object of changes which occurs outside the cell (wind properties and more)
        """
        generation_changes = super().next_generation()

        # If the temperature reach predefined celsius factor, city cells become Earth Cells.
        if self.temp >= CityCell._temp_earth_cell_factor:
            generation_changes['cell_change'] = CellTypes.EARTH

        # Each generation, city cells heat temperature in their neighborhood by predefined temperature heat factor
        generation_changes['apply_changes_locations'] = {
            'field': 'air_pollution',
            'locations': self._get_all_neighbors_directions(),
            'value': CityCell._temp_neighbors_increase_factor
        }

        # Produces air pollution each generation.
        self.air_pollution += CityCell._air_pollution_grow_factor

        return generation_changes
