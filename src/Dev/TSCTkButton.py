from customtkinter import CTkButton


class TSCTkButton(CTkButton):
    """
    a modified CTkButton class for a touch screen. When the user clicks on 
    the touch screen, the mouse hovers over the spot they clicked making the
    CTkButtons appear to be always focused until the user clicks elsewhere.
    This class makes it so the button is only focused while it is being clicked
    """

    def __init__(self, *args, **kwargs):
        """
        creates the CTkButton

        @param args: the arguments to be passed to the super class
        @param kwargs: the key word arguments to be passed to the super class
        """

        super().__init__(*args, **kwargs)
        self._canvas.unbind("<Enter>")
        self._canvas.unbind("<Leave>")
        self._canvas.bind("<ButtonRelease-1>", self._on_leave)
        self._text_label.unbind("<Enter>") if self._text_label is not None else None
        self._text_label.unbind("<Leave>") if self._text_label is not None else None
        self._text_label.bind("<ButtonRelease-1>", self._on_leave) if self._text_label is not None else None
        self._image_label.unbind("<Enter>") if self._image_label is not None else None
        self._image_label.unbind("<Leave>") if self._image_label is not None else None
        self._image_label.bind("<ButtonRelease-1>", self._on_leave) if self._image_label is not None else None
        self.bind("<Unmap>", self._on_leave)

    def _clicked(self, event=None):
        """
        overrides the clicked command to only perform the function and set the color
        to hover color

        @param event: the click event - not used
        """

        if self._state != "disabled":
            self._on_enter()
            if self._command is not None:
                self._command()
