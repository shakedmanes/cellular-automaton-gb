from cells.world_cell import WorldCell
from settings import LogicSettings, CellTypes


class EarthCell(WorldCell):
    """
    Represent an earth cell in the world.
    """
    _cell_type = CellTypes.EARTH

    _air_pollution_forest_cell_factor = 0.05

    def __init__(self, temp=None, air_pollution=None, wind_instance=None, cloud_instance=None):
        super().__init__(
            temp=temp,
            air_pollution=air_pollution,
            wind_instance=wind_instance,
            cloud_instance=cloud_instance
        )

    def next_generation(self):
        """
        Updates the earth cell properties as generation passed.
        Does all the things default world cell does, but including:

        - When there's rain with less than air pollution factor, earth cells become Forest Cells.

        :return: Object of changes which occurs outside the cell (wind properties and more)
        """
        # If there's rain with less than air pollution factor, earth cells become Forest Cells
        should_become_forest = \
            self.cloud is not None and \
            self.cloud.should_rain() and \
            self.air_pollution <= EarthCell._air_pollution_forest_cell_factor

        generation_changes = {
            **super().next_generation(),
            **({'cell_change': CellTypes.FOREST} if should_become_forest else {}),
        }

        return generation_changes
