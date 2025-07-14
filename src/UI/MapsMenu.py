from customtkinter import CTkFrame, CTkButton
from AppData import MENU_ICON_FONT, MENU_LABEL_FONT, IMAGE_CORNER_RADIUS
from UI.MapWidget import MapWidget


class MapsMenu(CTkFrame):
    """
    map menu for the 4runner dashboard
    """

    def __init__(self, master, **kwargs):
        """
        Initializes the settings menu frame.
        
        @param master: the parent widget
        @param kwargs: additional keyword arguments for CTkFrame
        """

        super().__init__(master, **kwargs)

        # creates spacer widgets and sets grid layout
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        for col in range(1, 8, 2):
            spacer = CTkButton(self, text="", font=MENU_ICON_FONT, fg_color="transparent", hover=False, height=0)
            spacer.grid(row=1, column=col)
            self.columnconfigure(col + 1, weight=1)

        # places map and back button
        main_menu = CTkButton(self, text="Main Menu", font=MENU_LABEL_FONT, command=lambda: master.change_menu("main"))
        map = MapWidget(self, corner_radius=IMAGE_CORNER_RADIUS)
        main_menu.grid(row=0, column=1, columnspan=7, pady=(10, 0), sticky="new")
        map.grid(row=1, column=1, columnspan=7, sticky="nsew", pady=10)
