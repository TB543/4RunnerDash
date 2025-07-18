from customtkinter import CTkFrame, CTkButton
from AppData import MENU_ICON_FONT, MENU_LABEL_FONT


class OBDMenu(CTkFrame):
    """
    OBD scanner menu for the 4runner dashboard
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

        main_menu = CTkButton(self, text="Main Menu", font=MENU_LABEL_FONT, command=lambda: master.change_menu("main"))
        main_menu.grid(row=0, column=1, columnspan=7, pady=(10, 0), sticky="new")
