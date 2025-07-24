from customtkinter import CTkButton, CTkSlider, ThemeManager, CTkRadioButton, CTkEntry, CTkScrollableFrame


class KeyboardController:
    """
    a class to add keyboard controls to the UI. useful for development/debugging
    tab to cycle between interactable elements
    space to click focused button
    arrow keys to move focused slider
    """

    def __init__(self, window):
        """
        adds UI controls to the root

        @param window: the root window to add UI controls to
        """

        self.window = window
        self.window.update()
        self.interactables = []
        self.find_interactables(self.window)
        self.index = -1
        self.window.bind("<Tab>", lambda event: self.cycle_interactables())
        self.window.bind("<space>", lambda event: self.space())
        self.window.bind("<Up>", self.arrows)
        self.window.bind("<Down>", self.arrows)
        self.window.bind("<Left>", self.arrows)
        self.window.bind("<Right>", self.arrows)
        self.window.focus_force()

    def find_interactables(self, root):
        """
        recursively searches the root for all interactable elements

        @param root: the root element to recursively search
        """

        if ((isinstance(root, CTkButton) and root.cget("state") == "normal") or isinstance(root, CTkSlider) or isinstance(root, CTkRadioButton) or isinstance(root, CTkEntry) or isinstance(root, CTkScrollableFrame)) and root.cget("fg_color") != "transparent":
            self.interactables.append(root)
        for widget in root.winfo_children():
            self.find_interactables(widget) if widget.winfo_ismapped() else None

    def cycle_interactables(self):
        """
        cycles through the visible interactables each time the user presses tab and makes the visually "focused"
        """

        # resets color of previously focused element
        if isinstance(self.interactables[self.index], CTkButton):
            self.interactables[self.index].configure(fg_color=ThemeManager.theme["CTkButton"]["fg_color"])
        elif isinstance(self.interactables[self.index], CTkSlider):
            self.interactables[self.index].configure(button_color=ThemeManager.theme["CTkSlider"]["button_color"])
        elif isinstance(self.interactables[self.index], CTkRadioButton):
            self.interactables[self.index].configure(border_color=ThemeManager.theme["CTkRadioButton"]["border_color"])
        elif isinstance(self.interactables[self.index], CTkEntry):
            self.interactables[self.index].configure(takefocus=0)
            self.window.after(0, lambda: self.window.focus())
        elif isinstance(self.interactables[self.index], CTkScrollableFrame):
            self.interactables[self.index]._scrollbar.configure(button_color=ThemeManager.theme["CTkScrollbar"]["button_color"])

        # sets the color of the next selected element
        self.index = (self.index + 1) % len(self.interactables)
        if isinstance(self.interactables[self.index], CTkButton):
            self.interactables[self.index].configure(fg_color=ThemeManager.theme["CTkButton"]["hover_color"])
        elif isinstance(self.interactables[self.index], CTkSlider):
            self.interactables[self.index].configure(button_color=ThemeManager.theme["CTkSlider"]["button_hover_color"])
        elif isinstance(self.interactables[self.index], CTkRadioButton):
            self.interactables[self.index].configure(border_color=ThemeManager.theme["CTkRadioButton"]["hover_color"])
        elif isinstance(self.interactables[self.index], CTkEntry):
            self.interactables[self.index].configure(takefocus=1)
        elif isinstance(self.interactables[self.index], CTkScrollableFrame):
            self.interactables[self.index]._scrollbar.configure(button_color=ThemeManager.theme["CTkScrollbar"]["button_hover_color"])

    def space(self):
        """
        handles when the user presses space: clicks a button if it is focused
        """

        # handles when no widget is focused
        if self.index == -1:
            return

        # clicks the button
        interactable = self.interactables[self.index]
        if isinstance(interactable, CTkButton) or isinstance(interactable, CTkRadioButton):
            interactable.invoke()
            self.window.update()
            self.interactables.clear()
            self.find_interactables(self.window)
        
        # handles menu change
        if not interactable.winfo_ismapped():
            interactable.configure(fg_color=ThemeManager.theme["CTkButton"]["fg_color"])
            self.index = -1

    def arrows(self, event):
        """
        handles when the user presses the arrow keys: moves a slider if it is focused

        @param event: the event that triggered the arrow key press
        """

        # no slider selected
        if self.index == -1:
            return
        
        # gets 5% of value to apply as the delta for slider
        if isinstance(self.interactables[self.index], CTkSlider):
            min_val = self.interactables[self.index].cget("from_") 
            max_val = self.interactables[self.index].cget("to") 
            current = self.interactables[self.index].get()
            delta = (max_val - min_val) * 0.05
            
            # vertical slider
            if self.interactables[self.index].cget("orientation") == "vertical":
                if event.keysym == "Up":
                    self.interactables[self.index].set(current + delta)
                elif event.keysym == "Down":
                    self.interactables[self.index].set(current - delta)

            # horizontal slider
            else:
                if event.keysym == "Left":
                    self.interactables[self.index].set(current - delta)
                elif event.keysym == "Right":
                    self.interactables[self.index].set(current + delta)

        # shifts the frame by 5%
        elif isinstance(self.interactables[self.index], CTkScrollableFrame):
            pos = self.interactables[self.index]._parent_canvas.yview()[0]
            if event.keysym == "Up":
                self.interactables[self.index]._parent_canvas.yview_moveto(max(pos - 0.05, 0))
            elif event.keysym == "Down":
                self.interactables[self.index]._parent_canvas.yview_moveto(min(pos + 0.05, 1))
