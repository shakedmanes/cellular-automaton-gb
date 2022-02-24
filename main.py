from tkinter import Tk, ttk, Canvas, StringVar, Toplevel, Scrollbar, VERTICAL, NS

from cellular_automaton import CellularAutomaton
from settings import AppSettings, LogicSettings


class AutomatonGUIRunner:
    """
    Controls the automaton and run the GUI interface which attached to the
    main logic of the automaton
    """
    __automaton = CellularAutomaton(LogicSettings.WORLD_FILE_PATH)

    def __init__(self):
        self.__initialize_screen_elements()
        self.__draw_cells()
        self.__attach_spacebar_listener()

    def __initialize_screen_elements(self):
        """
        Initializes the screen elements in the automaton
        """
        self.__app = Tk()
        self.__app.title(AppSettings.APP_TITLE)

        # Creating the world grid to display the cells of the world
        self.__world_frame = ttk.Frame(
            self.__app,
            width=AppSettings.APP_FRAME.get('WIDTH'),
            height=AppSettings.APP_FRAME.get('HEIGHT'),
        )
        self.__world_frame.grid(column=0, row=0)
        self.__app.columnconfigure(0, weight=1)
        self.__app.rowconfigure(0, weight=1)

        self.__generation_label_text = StringVar()
        self.__generation_label_text.set(f'Generation: {self.__automaton.generation}')

        ttk.Label(
            self.__world_frame,
            textvariable=self.__generation_label_text,
            font=('Helvetica', 18, 'bold')
        ).grid(column=0, row=0)
        ttk.Label(
            self.__world_frame,
            text='Press "Spacebar" to pass a generation',
            font=('Helvetica', 18)
        ).grid(column=len(AppSettings.CELL_CUBE.keys()), row=0)

        cell_type_label = ttk.Label(
            self.__world_frame,
            font=('Helvetica', 18),
            text="Cell Type"
        )
        cell_type_label.grid(column=0, row=1)

        cell_color_label = ttk.Label(
            self.__world_frame,
            font=('Helvetica', 18),
            text='Color'
        )
        cell_color_label.grid(column=0, row=2)

        curr_column = 1

        for cell_name, cell_color in AppSettings.CELL_CUBE.items():
            curr_cell_type_label = ttk.Label(
                self.__world_frame,
                font=('Helvetica', 16),
                text=cell_name
            )
            curr_cell_type_label.grid(column=curr_column, row=1)

            curr_cell_color_label = ttk.Label(
                self.__world_frame,
                font=('Helvetica', 32),
                text='■',
                foreground=cell_color.get('COLOR')
            )
            curr_cell_color_label.grid(column=curr_column, row=2)

            curr_column += 1

        self.__world_canvas = Canvas(
            self.__world_frame,
            width=AppSettings.CANVAS.get('WIDTH'),
            height=AppSettings.CANVAS.get('HEIGHT')
        )
        self.__world_canvas.configure(borderwidth=0, highlightthickness=0)
        self.__world_canvas.grid(column=0, row=4, columnspan=len(AppSettings.CELL_CUBE.keys()) + 1)

        self.__scroll_bar_vertical = Scrollbar(self.__world_frame, orient=VERTICAL, command=self.__world_canvas.yview, background='black')
        self.__scroll_bar_vertical.grid(column=len(AppSettings.CELL_CUBE.keys()) + 2, row=3, rowspan=2, sticky=NS)
        self.__world_canvas.configure(yscrollcommand=self.__scroll_bar_vertical.set)

        # Configure canvas height to allow scrollbar to scroll
        canvas_width, canvas_height = \
            int((AppSettings.CANVAS.get('WIDTH') / AppSettings.CELL_SIZE.get('WIDTH')) * AppSettings.NUM_CELLS), \
            int((AppSettings.CANVAS.get('HEIGHT') / AppSettings.CELL_SIZE.get('HEIGHT')) * (AppSettings.NUM_CELLS - 1))
        self.__world_canvas.configure(
            scrollregion=(0, 0, AppSettings.CANVAS.get('WIDTH'), AppSettings.CANVAS.get('HEIGHT')),
            width=canvas_width,
            height=canvas_height
        )

    def __draw_cells(self):
        """
        Draws the cells grid with all the visibility properties for each cell (In each generation)
        """
        self.__world_canvas.delete('all')

        cell_start_x_pos = 0
        cell_start_y_pos = 0

        for row_index in range(len(self.__automaton.world_grid)):
            for col_index in range(len(self.__automaton.world_grid[row_index])):
                # Cell tag is used for extracting fast cell location from the matrix by unique tag
                cell_tag = AutomatonGUIRunner.__construct_cell_tag_from_location(row_index, col_index)

                # Draw actual cell colored rectangle
                self.__world_canvas.create_rectangle(
                    cell_start_x_pos,
                    cell_start_y_pos,
                    cell_start_x_pos + AppSettings.CELL_SIZE.get('WIDTH'),
                    cell_start_y_pos + AppSettings.CELL_SIZE.get('HEIGHT'),
                    fill=
                    AppSettings.CELL_CUBE
                    .get(self.__automaton.world_grid[row_index][col_index].type)
                    .get('COLOR'),
                    outline='black',
                    tags=cell_tag
                )

                # Include temperature indicator inside the rectangle
                self.__world_canvas.create_text(
                    cell_start_x_pos + AppSettings.CELL_SIZE.get('WIDTH') / 2,
                    cell_start_y_pos + AppSettings.CELL_SIZE.get('HEIGHT') / 2,
                    text='{:.1f}'.format(self.__automaton.world_grid[row_index][col_index].temp),
                    tags=cell_tag
                )

                # If cell contains wind, draw a circle inside it to indicate it
                if self.__automaton.world_grid[row_index][col_index].wind is not None:
                    self.__world_canvas.create_oval(
                        cell_start_x_pos + (AppSettings.CELL_SIZE.get('WIDTH') / 2) - 15,
                        cell_start_y_pos + (AppSettings.CELL_SIZE.get('HEIGHT') / 2) - 15,
                        cell_start_x_pos + (AppSettings.CELL_SIZE.get('WIDTH') / 2) + 15,
                        cell_start_y_pos + (AppSettings.CELL_SIZE.get('HEIGHT') / 2) + 15,
                    )

                # Attach click to show information modal about cell
                self.__attach_cell_click_listener(cell_tag)

                cell_start_x_pos += AppSettings.CELL_SIZE.get('WIDTH')

            cell_start_x_pos = 0
            cell_start_y_pos += AppSettings.CELL_SIZE.get('HEIGHT')

    def __attach_spacebar_listener(self):
        """
        Attaches the spacebar key to calculate the next generation of the automaton
        """
        self.__app.bind_all('<space>', lambda e: self.__next_generation())

    def __attach_cell_click_listener(self, cell_tag):
        """
        Attaches click event to all cells in the grid to show the information of a clicked cell.

        :param cell_tag: The cell location tag to attach click to
        """
        self.__world_canvas.tag_bind(cell_tag, '<ButtonRelease-1>', lambda e: self.__show_cell_info(cell_tag))

    def __next_generation(self):
        """
        Calculates the next generation and draws the cells again for the new generation
        """
        self.__automaton.next_generation()
        self.__generation_label_text.set(f'Generation: {self.__automaton.generation}')
        self.__draw_cells()

    def __show_cell_info(self, cell_tag):
        """
        Display a information box for the cell clicked

        :param cell_tag: The cell tag location clicked
        """
        # Extract cell location from cell tag
        row_index, col_index = AutomatonGUIRunner.__extract_cell_location_from_tag(cell_tag)

        # Grab cell instance from automaton
        cell_instance = self.__automaton.world_grid[row_index][col_index]

        # Create the cell info dialog
        dlg = Toplevel(self.__app)
        dlg.minsize(AppSettings.CELL_INFO_DIALOG.get('WIDTH'), AppSettings.CELL_INFO_DIALOG.get('HEIGHT'))
        dlg.wm_title('Cell Info')

        # Show basic information about the cell instance
        ttk.Label(
            dlg,
            text=f'Location: (row={row_index},column={col_index})'
        ).grid()
        ttk.Label(
            dlg,
            text=f'Type: {cell_instance.type}'
        ).grid()
        ttk.Label(
            dlg,
            text=f'Temp: {cell_instance.temp}'
        ).grid()
        ttk.Label(
            dlg,
            text=f'Air Pollution: {cell_instance.air_pollution * 100}%'
        ).grid()

        # If cell has wind, show the information necessary for it
        if cell_instance.wind is not None:
            ttk.Label(
                dlg,
                text=f'Wind Speed: {cell_instance.wind.speed} k/h'
            ).grid()
            ttk.Label(
                dlg,
                text=f'Wind Direction: {cell_instance.wind.direction}'
            ).grid()
        else:
            ttk.Label(
                dlg,
                text='Wind: None.'
            ).grid()

        # If cell has cloud, show the information necessary for it
        if cell_instance.cloud is not None:
            ttk.Label(
                dlg,
                text=f'Cloud: {cell_instance.cloud.precipitation}% Precipitation'
            ).grid()
        else:
            ttk.Label(
                dlg,
                text='Cloud: None.'
            ).grid()

        # When close dialog button is clicked, close the dialog
        dlg.protocol("WM_DELETE_WINDOW", dlg.destroy)

        # Set dialog window to be related to main window
        dlg.transient(self.__app)

        # Wait until the dialog is visible
        dlg.wait_visibility()

        # Don't do nothing until a response is received from the dialog
        dlg.wait_window()

    @staticmethod
    def __construct_cell_tag_from_location(row_index, col_index):
        """
        Constructs a cell tag from cell location

        :param row_index: The row index of the cell
        :param col_index: The column index of the cell
        :return: Cell tag location which is a string of row_index-col_index
        """
        return f'{row_index}-{col_index}'

    @staticmethod
    def __extract_cell_location_from_tag(cell_tag):
        """
        Extracts given cell tag location to actual location

        :param cell_tag: Cell tag location string
        :return: List of the cell location which the first value is the row and the second is the column
        """
        return [int(ax) for ax in cell_tag.split('-')]

    def run(self):
        """
        Runs the automaton
        """
        self.__app.mainloop()


if __name__ == '__main__':
    automaton_runner = AutomatonGUIRunner()
    automaton_runner.run()
