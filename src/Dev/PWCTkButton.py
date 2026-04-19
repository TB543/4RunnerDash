from Dev.TSCTkButton import TSCTkButton
from Dev.CTkButtonFixed import CTkButtonFixed
from UI.Widgets.PinPad import PinPad
from AppData import SECURITY_LEVEL


class PWCTkButton(TSCTkButton):
    """
    a class for a password protected button that requires a pin to complete its functionality

    note that this program only supports 1 pin shared across all password protected buttons
    additionally the pin will only need to be entered once per session and will remain unlocked until the next run
    """

    def __init__(self, master, pinpad_master, security_level, *args, **kwargs):
        """
        creates the button

        @param master: the master widget for the button
        @param pinpad_master: the master widget for the pin pad overlay for the button
        @param security_level: the security level of the button
        @param args: additional arguments
        @param kwargs: additional keyword arguments
        """

        command = kwargs.get("command", lambda: None)
        pinpad = PinPad(pinpad_master, command, border_width=2)
        kwargs["command"] = lambda: command() if PinPad.unlocked or security_level > SECURITY_LEVEL else pinpad.place(relx=.5, rely=.5, relwidth=.4, relheight=.9, anchor="center")
        super().__init__(master, *args, **kwargs)
        self.after(0, pinpad.lift)


class PWCTkButtonFixed(PWCTkButton, CTkButtonFixed):
    """
    a password protected button that includes the logic for fixing the render bug for larger buttons
    """
