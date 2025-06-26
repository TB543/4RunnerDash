from customtkinter import CTkFrame, CTkLabel, CTkButton
from AppData import ICON_FONT, LABEL_FONT
from subprocess import run

class SettingsMenu(CTkFrame):
    """
    Settings menu for the 4Runner Dash application.
    """

    def __init__(self, parent, fg_color=None, **kwargs):
        """
        Initializes the settings menu frame.
        
        @param parent: the parent widget
        @param fg_color: the foreground color of the frame
        @param kwargs: additional keyword arguments for CTkFrame
        """

        super().__init__(parent, fg_color=fg_color, **kwargs)

        # creates the labels for the buttons
        appearance_label = CTkLabel(self, text="Appearance", font=LABEL_FONT)
        theme_label = CTkLabel(self, text="Theme", font=LABEL_FONT)
        scale_label = CTkLabel(self, text="Scale", font=LABEL_FONT)
        appearance_label.grid(row=0, column=1, sticky="s")
        theme_label.grid(row=0, column=3, sticky="s")
        scale_label.grid(row=0, column=5, sticky="s")

        # creates the buttons of the menu
        appearance_button = CTkButton(self, text="", font=ICON_FONT)
        theme_button = CTkButton(self, text="", font=ICON_FONT)
        scale_button = CTkButton(self, text="", font=ICON_FONT)
        shell_button = CTkButton(self, text="Open Shell", font=LABEL_FONT, command=self.open_shell)
        appearance_button.grid(row=1, column=1, sticky="nsew")
        theme_button.grid(row=1, column=3, sticky="nsew")
        scale_button.grid(row=1, column=5, sticky="nsew")
        shell_button.grid(row=3, column=0, columnspan=7, padx=10, pady=10, sticky="sew")

        # sets the grid layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(4, weight=1)
        self.grid_columnconfigure(6, weight=1)

    def open_shell(self):
        """
        kills the display and opens the terminal shell.
        """
        
        self.winfo_toplevel().destroy()
        run(['sudo', 'killall', 'Xorg'])
