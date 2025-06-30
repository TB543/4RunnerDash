from customtkinter import CTkButton, CTkSlider, ThemeManager


class UIControls:
    """
    a class to add keyboard controls to the UI. useful for development/debugging
    tab to cycle between interactable elements
    space to click focused button
    arrow keys to move focused slider
    """

    window = None
    interactables = []
    index = -1

    @classmethod
    def add(cls, window):
        """
        adds UI controls to the root

        @param window: the root window to add UI controls to
        """

        cls.window = window
        window.bind("<Tab>", lambda event: cls.cycle_interactables())
        window.bind("<space>", lambda event: cls.space())
        window.bind("<Up>", cls.arrows)
        window.bind("<Down>", cls.arrows)
        window.bind("<Left>", cls.arrows)
        window.bind("<Right>", cls.arrows)
        window.focus_force()

    @classmethod
    def find_interactables(cls, root):
        """
        recursively searches the root for all interactable elements

        @param root: the root element to recursively search
        """

        if (isinstance(root, CTkButton) or isinstance(root, CTkSlider)) and root.cget("fg_color") != "transparent":
            cls.interactables.append(root)
        for widget in root.winfo_children():
            cls.find_interactables(widget) if widget.winfo_ismapped() else None

    @classmethod
    def cycle_interactables(cls):
        """
        cycles through the visible interactables each time the user presses tab and makes the visually "focused"
        """

        # loads interactables if needed
        if not cls.interactables:
            cls.find_interactables(cls.window)
            index = -1

        # resets color of previously focused element
        elif isinstance(cls.interactables[cls.index], CTkButton):
            cls.interactables[cls.index].configure(fg_color=ThemeManager.theme["CTkButton"]["fg_color"])
        elif isinstance(cls.interactables[cls.index], CTkSlider):
            cls.interactables[cls.index].configure(button_color=ThemeManager.theme["CTkSlider"]["button_color"])

        # sets the color of the next selected element
        cls.index = (cls.index + 1) % len(cls.interactables)
        if isinstance(cls.interactables[cls.index], CTkButton):
            cls.interactables[cls.index].configure(fg_color=ThemeManager.theme["CTkButton"]["hover_color"])
        elif isinstance(cls.interactables[cls.index], CTkSlider):
            cls.interactables[cls.index].configure(button_color=ThemeManager.theme["CTkSlider"]["button_hover_color"])

    @classmethod
    def space(cls):
        """
        handles when the user presses space: clicks a button if it is focused
        """

        if cls.index == -1:
            return
        if isinstance(cls.interactables[cls.index], CTkButton):
            cls.interactables[cls.index].configure(fg_color=ThemeManager.theme["CTkButton"]["fg_color"])
            cls.interactables[cls.index].invoke()
            cls.interactables.clear()

    @classmethod
    def arrows(cls, event):
        """
        handles when the user presses the arrow keys: moves a slider if it is focused
        """

        # no slider selected
        if not isinstance(cls.interactables[cls.index], CTkSlider):
            return
        
        # gets 5% of value to apply as the delta
        min_val = cls.interactables[cls.index].cget("from_") 
        max_val = cls.interactables[cls.index].cget("to") 
        current = cls.interactables[cls.index].get()
        delta = (max_val - min_val) * 0.05
        
        # vertical slider
        if cls.interactables[cls.index].cget("orientation") == "vertical":
            if event.keysym == "Up":
                cls.interactables[cls.index].set(current + delta)
            elif event.keysym == "Down":
                cls.interactables[cls.index].set(current - delta)

        # horizontal slider
        else:
            if event.keysym == "Left":
                cls.interactables[cls.index].set(current - delta)
            elif event.keysym == "Right":
                cls.interactables[cls.index].set(current + delta)
