from customtkinter import CTkFrame, CTkLabel
from Dev.TSCTkButton import TSCTkButton
from AppData import PIN


class PinPad(CTkFrame):
    """
    a class to represent a PinPad widget

    note that this class only supports 1 pin shared across all pin pad instances
    additionally the pin will only need to be entered once per session and will remain unlocked until the next run
    """

    unlocked = False
    active_instances = {}

    def __init__(self, master, callback, *args, **kwargs):
        """
        initialize a PinPad widget

        @param master the master widget
        @param callback the callback function for when pin has been entered successfully
        @param args: the arguments passed to the widget
        @param kwargs: the keyword arguments passed to the widget
        """

        # set class fields
        super().__init__(master, *args, **kwargs)
        self.callback = callback
        self.after_clear = self.after(0, lambda: None)
        self.pin = ""

        # places toplevel widgets
        self.pin_label = CTkLabel(self, text="Enter Pin", font=("Arial", 20))
        close_button = TSCTkButton(self, text="x", width=12, font=("Arial", 20),command=self.place_forget)
        container = CTkFrame(self)
        self.pin_label.grid(row=0, column=0, columnspan=2, sticky="s")
        close_button.grid(row=0, column=1, pady=5, padx=5)
        container.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=2, pady=(20, 2))

        # configures grid layout
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        container.rowconfigure(0, weight=1)
        container.rowconfigure(1, weight=1)
        container.rowconfigure(2, weight=1)
        container.rowconfigure(3, weight=1)
        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, weight=1)
        container.columnconfigure(2, weight=1)

        # places buttons
        for i in range(1, 10):
            button = TSCTkButton(container, text=i, width=12, font=("Arial", 20), command=lambda d=i: self.select_digit(d))
            button.grid(row=(i - 1) // 3, column=(i - 1) % 3, sticky="nsew", padx=7, pady=7)
        button = TSCTkButton(container, text=0, width=12, font=("Arial", 20), command=lambda: self.select_digit(0))
        button.grid(row=3, column=1, sticky="nsew", padx=7, pady=7)

    def select_digit(self, digit):
        """
        handles when the user selects a digit

        @param digit: the digit to select
        """

        # updates UI
        self.after_cancel(self.after_clear)
        self.pin += str(digit)
        self.pin_label.configure(text=" * " * len(self.pin))

        # handles when pin is correct
        if self.pin == str(PIN):
            PinPad.unlocked = True
            self.after(250, lambda: [instance.place_forget() for instance in PinPad.active_instances.values()])
            self.after(250, self.callback)

        # handles when pin is incorrect
        elif len(self.pin) == len(str(PIN)):
            self.pin = ""
            self.after_clear = self.after(250, lambda: self.pin_label.configure(text="Incorrect"))

    def place(self, **kwargs):
        """
        overrides the place method to ensure only 1 pinpad is active per menu and previously entered pin is cleared

        @param kwargs: the arguments passed to the widget
        """

        # resets pin
        self.pin = ""
        self.pin_label.configure(text="Enter Pin")

        # removes old pinpad
        if instance := PinPad.active_instances.get(self.master):
            instance.place_forget()
        PinPad.active_instances[self.master] = self
        super().place(**kwargs)
