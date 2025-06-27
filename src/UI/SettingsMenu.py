from customtkinter import CTkFrame, CTkLabel, CTkButton
from AppData import ICON_FONT, LABEL_FONT, APPEARANCE_SETTINGS
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
        appearance_text = APPEARANCE_SETTINGS.MODES[APPEARANCE_SETTINGS.mode].ICON
        theme_text = APPEARANCE_SETTINGS.THEMES[APPEARANCE_SETTINGS.theme].ICON
        scale_text = APPEARANCE_SETTINGS.SCALES[APPEARANCE_SETTINGS.scaling].ICON

        # creates the labels for the buttons
        back_label = CTkLabel(self, text="Back", font=LABEL_FONT)
        appearance_label = CTkLabel(self, text="appearance", font=LABEL_FONT)
        theme_label = CTkLabel(self, text="Theme", font=LABEL_FONT)
        scale_label = CTkLabel(self, text="Scale", font=LABEL_FONT)
        back_label.grid(row=0, column=1, sticky="s")
        appearance_label.grid(row=0, column=3, sticky="s")
        theme_label.grid(row=0, column=5, sticky="s")
        scale_label.grid(row=0, column=7, sticky="s")

        # creates the buttons of the menu
        back_button = CTkButton(self, text="↩️", font=ICON_FONT, command=lambda: parent.change_menu("main"))
        appearance_button = CTkButton(self, text=appearance_text, font=ICON_FONT, command=lambda: self.change_appearance(appearance_button))
        theme_button = CTkButton(self, text=theme_text, font=ICON_FONT, command=lambda: self.change_theme(theme_button))
        scale_button = CTkButton(self, text=scale_text, font=ICON_FONT, command=lambda: self.change_scaling(scale_button))
        shell_button = CTkButton(self, text="Open Shell", font=LABEL_FONT, command=self.open_shell)
        back_button.grid(row=1, column=1, sticky="nsew")
        appearance_button.grid(row=1, column=3, sticky="nsew")
        theme_button.grid(row=1, column=5, sticky="nsew")
        scale_button.grid(row=1, column=7, sticky="nsew")
        shell_button.grid(row=2, column=1, columnspan=7, pady=(0, 10), sticky="sew")

        # sets the grid layout
        self.grid_rowconfigure(0, weight=1, uniform="row0")
        self.grid_rowconfigure(2, weight=1, uniform="row0")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(4, weight=1)
        self.grid_columnconfigure(6, weight=1)
        self.grid_columnconfigure(8, weight=1)

    def change_appearance(self, button):
        """
        Changes the appearance of the application.
        
        @param button: the button that was clicked
        """

        current_appearance = APPEARANCE_SETTINGS.mode
        next_appearance = APPEARANCE_SETTINGS.MODES[current_appearance].NEXT
        APPEARANCE_SETTINGS.set_mode(next_appearance)
        button.configure(text=APPEARANCE_SETTINGS.MODES[next_appearance].ICON)
        APPEARANCE_SETTINGS.save()

    def change_theme(self, button):
        """
        Changes the theme of the application.
        
        @param button: the button that was clicked
        """

        current_theme = APPEARANCE_SETTINGS.theme
        next_theme = APPEARANCE_SETTINGS.THEMES[current_theme].NEXT
        APPEARANCE_SETTINGS.set_theme(next_theme, self.winfo_toplevel())
        button.configure(text=APPEARANCE_SETTINGS.THEMES[next_theme].ICON)
        APPEARANCE_SETTINGS.save()

    def change_scaling(self, button):
        """
        Changes the scaling of the application.
        
        @param button: the button that was clicked
        """

        current_scaling = APPEARANCE_SETTINGS.scaling
        next_scaling = APPEARANCE_SETTINGS.SCALES[current_scaling].NEXT
        APPEARANCE_SETTINGS.set_scaling(next_scaling)
        button.configure(text=APPEARANCE_SETTINGS.SCALES[next_scaling].ICON)
        APPEARANCE_SETTINGS.save()

    def open_shell(self):
        """
        kills the display and opens the terminal shell.
        """
        
        self.winfo_toplevel().destroy()
        run(['sudo', 'killall', 'Xorg'])
