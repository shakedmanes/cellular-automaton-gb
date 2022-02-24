from csv import reader
from random import randint, sample

from settings import LogicSettings, CellTypes
from cells.cell_factory import CellFactory
from cell_environment.wind import Wind
from cell_environment.cloud import Cloud
from direction_matrix import DirectionMatrix


class CellularAutomaton:
    """
    Represent the cellular automaton logic behind the world.
    """

    __environment_dist_min = 10
    __environment_dist_max = 15
    __cell_data_delimiter = ';'
    __wind_dist_map = [
        {25: (0, 0)},
        {60: (5, 10)},
        {10: (10, 15)},
        {5: (16, 20)}
    ]

    def __init__(self, world_file_path=LogicSettings.WORLD_FILE_PATH):
        self.__environment_dist = CellularAutomaton.generate_environment_dist()
        self.__generation = 0
        self.__read_world_file(world_file_path)

    @property
    def generation(self):
        """
        Getter for current generation of the world

        :return: Generation number
        """
        return self.__generation

    @property
    def world_grid(self):
        """
        Getter for world grid containing all the cells of the world

        :return: World grid matrix
        """
        return self.__world_grid

    def next_generation(self):
        """
        Updates the whole world cells, wind and clouds as generation passed.

        """
        # Update the generation counter
        self.__generation += 1

        # Copy the world grid to apply inline cell generation transitions
        copy_world_grid = list(self.__world_grid)

        # Contains the new wind locations by the movement of each wind
        new_wind_locations = []

        # Generation changes list, containing the changes needed for the cell or its environment
        generation_changes = []

        # Apply inline cell generation transitions
        for row_index in range(len(copy_world_grid)):
            for col_index in range(len(copy_world_grid[row_index])):
                cell_next_generation_changes = copy_world_grid[row_index][col_index].next_generation()

                # If the generation changes actually contains exterior changes
                if len(cell_next_generation_changes) > 0:
                    generation_changes.append(
                        {(row_index, col_index): copy_world_grid[row_index][col_index].next_generation()}
                    )

        # Apply generation changes on the cells
        for generation_change_obj in generation_changes:
            (row_index, col_index) = list(generation_change_obj.keys())[0]

            # Applying the generation change
            self.apply_generation_change(
                (row_index, col_index),
                generation_change_obj[(row_index, col_index)],
                copy_world_grid
            )

        # Set the new world grid as result of the generation changes
        self.__world_grid = copy_world_grid

    def apply_generation_change(self, cell_location, generation_change, curr_generation_cells):
        """
        Applies current generation changes to current given generation cells

        :param cell_location: The location of the cell the generation change belongs to
        :param generation_change: Object of generation change for a given location
        :param curr_generation_cells: List of current generation cells
        """
        (cell_row, cell_col) = cell_location
        curr_cell_instance = curr_generation_cells[cell_row][cell_col]

        # Iterate over the keys which defined the types of generation changes need to perform
        for generation_change_key in generation_change.keys():

            # Deal with generation changes in the environment objects (wind and cloud)
            if generation_change_key == 'environment':
                changes_obj = generation_change[generation_change_key]
                wind_instance = changes_obj['wind_instance']
                cloud_instance = changes_obj['cloud_instance']
                update_location_func = changes_obj.get('update_location', None)
                update_affected_locations = changes_obj.get('update_affected_locations', None)
                air_pollution_passed = changes_obj['air_pollution_passed']

                # If the wind need to move to other location
                if update_location_func:
                    # Removing the wind instance from the current cell if it the same wind as
                    # the wind moved now
                    if curr_cell_instance.wind == wind_instance:
                        curr_cell_instance.wind = None

                    # Removing the cloud instance from the current cell if it the same cloud as
                    # the wind moved the cloud with it now
                    if curr_cell_instance.cloud == cloud_instance:
                        curr_cell_instance.cloud = cloud_instance

                    # Calculate the next cell location of the moving wind
                    (wind_next_row, wind_next_col) = update_location_func(cell_row, cell_col)

                    # If the next location is not valid, need to opposite the direction of the wind
                    if not self.is_valid_location((wind_next_row, wind_next_col)):
                        wind_instance.set_opposite_direction()
                        (wind_next_row, wind_next_col) = \
                            getattr(DirectionMatrix, wind_instance.direction)(cell_row, cell_col)

                    # Set the wind at the new location
                    curr_generation_cells[wind_next_row][wind_next_col].wind = wind_instance

                # If the wind affected other locations with air pollution
                if update_affected_locations:

                    # Update the affected locations by the air pollution passed with the wind
                    for affected_location_func in update_affected_locations:
                        (curr_affect_row, curr_affect_col) = affected_location_func(cell_row, cell_col)

                        # Update only if the location is valid
                        if self.is_valid_location((curr_affect_row, curr_affect_col)):
                            curr_generation_cells[curr_affect_row][curr_affect_col].air_pollution += air_pollution_passed

            # Deal with cell type change
            if generation_change_key == 'cell_change':
                new_cell_type = generation_change[generation_change_key]
                curr_generation_cells[cell_row][cell_col] = \
                    CellFactory.change_cell_type(curr_cell_instance, new_cell_type)

            # Deal with area generation changes in results of the current cell
            if generation_change_key == 'apply_changes_locations':
                changes_obj = generation_change[generation_change_key]
                field = changes_obj['field']
                value = changes_obj['value']

                # Apply the property change in each of the given locations
                for location_funcs in changes_obj['locations']:
                    (curr_row, curr_col) = location_funcs(cell_row, cell_col)

                    # Apply only if it valid location of cell
                    if self.is_valid_location((curr_row, curr_col)):
                        setattr(
                            curr_generation_cells[curr_row][curr_col],
                            field,
                            getattr(curr_generation_cells[curr_row][curr_col], field) + value
                        )

    @staticmethod
    def generate_environment_dist():
        """
        Generates the environment distribution across the world

        :return: Distribution for environment properties across the world
        """
        return randint(CellularAutomaton.__environment_dist_min, CellularAutomaton.__environment_dist_max)

    def is_valid_location(self, location):
        """
        Checks if the location is valid (in the world grid)

        :param location: (row, col) location in the world grid
        :return: True if the location is valid and in the world grid, Otherwise False
        """
        (row, col) = location
        return (0 <= row < len(self.__world_grid)) and (0 <= col < len(self.__world_grid[0]))

    def generate_distribution_list(self):
        """
        Generates the distribution list of environments properties in the location across the world

        :return: List of locations which will have environments properties
        """
        # Calculate the number of elements needed
        num_env_elements = int((self.__environment_dist / 100) * (LogicSettings.NUM_CELLS ** 2))

        # Take a sample from all the possible locations in the grid
        return sample(
            [(i, j) for i in range(LogicSettings.NUM_CELLS) for j in range(LogicSettings.NUM_CELLS)],
            num_env_elements
        )

    def generate_wind_speed_dist(self, location_list):
        """
        Generates the wind speed distribution across the wind instances locations
        by the predefined wind speed distribution

        :param location_list: List of locations for the wind instances
        :return: Dictionary of the locations as keys and temperature for each location as value
        """
        dist_wind_speed = {}
        curr_location_list = location_list

        # For each distribution, calculate number of locations to extract
        for wind_dist_obj in self.__wind_dist_map:
            percentage, speed_range = list(wind_dist_obj.items())[0]
            num_to_select = int((percentage / 100) * len(location_list))

            selected_locations = sample(
                curr_location_list,
                len(curr_location_list) if num_to_select > len(curr_location_list) else num_to_select
            )

            dist_wind_speed = {**dist_wind_speed, **{loc: speed_range for loc in selected_locations}}

            curr_location_list = list(set(curr_location_list) - set(selected_locations))

        # If there's some leftovers, append them as first speed range selection
        if len(curr_location_list) > 0:
            speed_range = list(self.__wind_dist_map[0].values())[0]
            dist_wind_speed = {**dist_wind_speed, **{loc: speed_range for loc in curr_location_list}}

        return dist_wind_speed

    def __read_world_file(self, world_file_path):
        """
        Reads world file and loads the world grid

        :param world_file_path: Path to world file.
        """
        self.__world_grid = []

        dist_list = self.generate_distribution_list()
        wind_dist_list = self.generate_wind_speed_dist(dist_list)

        with open(world_file_path, 'r') as world_file:
            world_csv = reader(world_file, delimiter=',')
            curr_cell_row = []

            curr_row = 0
            curr_col = 0

            for row in world_csv:
                for cell in row:
                    cell_data = CellularAutomaton.__extract_cell_data(cell)

                    # If the cell in the distribution list, he need to be created with wind and cloud
                    # Otherwise, without them.
                    if (curr_row, curr_col) in dist_list:

                        # Extract the wind speed range for the cell
                        min_speed_range, max_speed_range = wind_dist_list[(curr_row, curr_col)]

                        # Extract the possible directions for the wind to generate
                        possible_wind_directions = DirectionMatrix.get_possible_direction_from_location(
                            location=(curr_row, curr_col),
                            border_size=LogicSettings.NUM_CELLS
                        )

                        # Creates the cell with the wind and cloud properties
                        curr_cell_row.append(
                            CellFactory.create_cell(
                                *cell_data,
                                wind_instance=Wind(
                                    min_speed_range=min_speed_range,
                                    max_speed_range=max_speed_range,
                                    possible_direction_list=possible_wind_directions
                                ),
                                cloud_instance=Cloud()
                            )
                        )

                    else:
                        curr_cell_row.append(CellFactory.create_cell(*cell_data))

                    curr_col += 1

                self.__world_grid.append(curr_cell_row)

                curr_cell_row = []
                curr_row += 1
                curr_col = 0

    @classmethod
    def __extract_cell_data(cls, cell):
        """
        Extracts single cell data from world file.

        :param cell: Formatted cell data from the world file.
        :return: List of extracted cell data values.
        """
        cell_data = cell.split(cls.__cell_data_delimiter)
        parsed_cell_data = [CellTypes(int(cell_data[0]))]

        for cell_data_val in cell_data[1:]:
            parsed_cell_data.append(int(cell_data_val))

        return parsed_cell_data

