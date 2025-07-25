from customtkinter import CTkButton


class CTkButtonFixed(CTkButton):
    """
    sometimes customtkinter has a glitch where the label is shorter than it needs to be
    to fit the text. This results in a render glitch where the text is cut off at the top.
    This class gives the text some extra padding to the top
    """

    def _draw(self, no_color_updates=False):
        """
        changes the draw method to add extra padding to the text label

        @param no_color_updates: used in the super class
        """

        super()._draw(no_color_updates)
        if self._text_label:
            self._text_label.configure(pady=30)
    
    def _create_grid(self):
        """
        changes the create grid method to adjust the position of the text label
        """

        super()._create_grid()
        self.configure(height=self._font[1] + 20)
        self._text_label.place(relx=.5, rely=.5, y=15, anchor="center")
    