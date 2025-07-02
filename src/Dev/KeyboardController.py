from customtkinter import CTkButton, CTkSlider, ThemeManager


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
        self.interactables = []
        self.index = -1
        window.bind("<Tab>", lambda event: self.cycle_interactables())
        window.bind("<space>", lambda event: self.space())
        window.bind("<Up>", self.arrows)
        window.bind("<Down>", self.arrows)
        window.bind("<Left>", self.arrows)
        window.bind("<Right>", self.arrows)
        window.focus_force()

    def find_interactables(self, root):
        """
        recursively searches the root for all interactable elements

        @param root: the root element to recursively search
        """

        if (isinstance(root, CTkButton) or isinstance(root, CTkSlider)) and root.cget("fg_color") != "transparent":
            self.interactables.append(root)
        for widget in root.winfo_children():
            self.find_interactables(widget) if widget.winfo_ismapped() else None

    def cycle_interactables(self):
        """
        cycles through the visible interactables each time the user presses tab and makes the visually "focused"
        """

        # loads interactables if needed
        if not self.interactables:
            self.find_interactables(self.window)
            index = -1

        # resets color of previously focused element
        elif isinstance(self.interactables[self.index], CTkButton):
            self.interactables[self.index].configure(fg_color=ThemeManager.theme["CTkButton"]["fg_color"])
        elif isinstance(self.interactables[self.index], CTkSlider):
            self.interactables[self.index].configure(button_color=ThemeManager.theme["CTkSlider"]["button_color"])

        # sets the color of the next selected element
        self.index = (self.index + 1) % len(self.interactables)
        if isinstance(self.interactables[self.index], CTkButton):
            self.interactables[self.index].configure(fg_color=ThemeManager.theme["CTkButton"]["hover_color"])
        elif isinstance(self.interactables[self.index], CTkSlider):
            self.interactables[self.index].configure(button_color=ThemeManager.theme["CTkSlider"]["button_hover_color"])

    def space(self):
        """
        handles when the user presses space: clicks a button if it is focused
        """

        if not self.interactables:
            return
        if isinstance(self.interactables[self.index], CTkButton):
            self.interactables[self.index].invoke()
            self.window.update()
        if not self.interactables[self.index].winfo_ismapped():
            self.interactables[self.index].configure(fg_color=ThemeManager.theme["CTkButton"]["fg_color"])
            self.interactables.clear() 

    def arrows(self, event):
        """
        handles when the user presses the arrow keys: moves a slider if it is focused
        """

        # no slider selected
        if not self.interactables or not isinstance(self.interactables[self.index], CTkSlider):
            return
        
        # gets 5% of value to apply as the delta
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
