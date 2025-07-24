from customtkinter import CTkFrame, CTkButton


class VirtualKeyboard(CTkFrame):
    """
    a class for a virtual keyboard using the 101/104 - ANSI layout 
    where each key that is pressed sends the key to a widget
    """

    # keyboard layout in the following form KEYS[row][column][*0 for normal key*, *1 fir shifted key*]
    KEYS = (
        (('`', '~'), ('1', '!'), ('2', '@'), ('3', '#'), ('4', '$'), ('5', '%'), ('6', '^'), ('7', '&'), ('8', '*'), ('9', '('), ('0', ')'), ('-', '_'), ('=', '+'), ('Back',)),
        (('Tab',), ('q', 'Q'), ('w', 'W'), ('e', 'E'), ('r', 'R'), ('t', 'T'), ('y', 'Y'), ('u', 'U'), ('i', 'I'), ('o', 'O'), ('p', 'P'), ('[', '{'), (']', '}'), ('\\', '|')),
        (('Caps',), ('a', 'A'), ('s', 'S'), ('d', 'D'), ('f', 'F'), ('g', 'G'), ('h', 'H'), ('j', 'J'), ('k', 'K'), ('l', 'L'), (';', ':'), ("'", '"'), ('Enter',)),
        (('Shift',), ('z', 'Z'), ('x', 'X'), ('c', 'C'), ('v', 'V'), ('b', 'B'), ('n', 'N'), ('m', 'M'), (',', '<'), ('.', '>'), ('/', '?'), ('Shift', 'Shift')),
        ((' ',), (' ',), (' ',), ('Space',), (' ', ' '), ('←',), ('→',), (' ', ' '), ('✖',))
    )

    # lists how many columns a given key takes up. default is 4
    COLUMNS = {
        ('Back',): 8,
        ('Tab',): 6,
        ('\\', '|'): 6,
        ('Caps',): 7,
        ('Enter',): 9,
        ('Shift',): 9,
        ('Shift', 'Shift'): 11,
        (' ',): 5,
        ('Space',): 25
    }

    # list of commands for the keys
    COMMANDS = {
        ('Back',): lambda s: lambda: s.entry.delete(s.entry.index("insert") - 1) if s.entry.index("insert") != 0 else None,
        ('Tab',): lambda s: lambda: s.key(('\t', '\t')),
        ('Caps',): lambda s: lambda: s.caps_lock(),
        ('Enter',): lambda s: lambda: s.enter(),
        ('Shift',): lambda s: lambda: s.shift(),
        ('Shift', 'Shift'): lambda s: lambda: s.shift(),
        ('Space',): lambda s: lambda: s.key((' ', ' ')),
        ('←',): lambda s: lambda: s.entry.icursor(s.entry.index("insert") - 1),
        ('→',): lambda s: lambda: s.entry.icursor(s.entry.index("insert") + 1),
        ('✖',): lambda s: lambda: s.exit(),
    }

    def __init__(self, master, entry, callback, **kwargs):
        """
        Initializes the virtual keyboard.
        
        @param master: the parent widget
        @param entry: the CTkEntry widget to send keystrokes to
        @param callback: the function to call when enter is pressed
        @param kwargs: additional keyword arguments for CTkFrame
        """

        # initializes superclass and sets fields
        super().__init__(master, **kwargs)
        self.entry = entry
        self.callback = callback
        self.key_index = 0
        self.caps = False

        # sets grid and configures keyboard to open automatically
        self.entry.bind("<FocusIn>", lambda e: self.place(relx=.5, rely=.5, relwidth=1, relheight=.5, anchor="n"))
        self.entry.bind("<FocusOut>", lambda e: self.place_forget())
        for i in range(60):
            self.columnconfigure(i, weight=1, uniform="key")

        # creates a frame to contain each row
        self.columnconfigure(0, weight=1)
        for row, keys in enumerate(VirtualKeyboard.KEYS):
            self.rowconfigure(row, weight=1)

            # creates buttons
            column = 0
            for key in keys:
                command = VirtualKeyboard.COMMANDS[key](self) if key in VirtualKeyboard.COMMANDS else lambda k=key: self.key(k)
                button = CTkButton(self, text=key[0], font=("Arial", 20), command=command)
                button.metadata = key
                columns = VirtualKeyboard.COLUMNS[key] if key in VirtualKeyboard.COLUMNS else 4
                button.grid(row=row, column=column, columnspan=columns, sticky="nsew", padx=3, pady=3)
                column += columns

                # handles when the button is a spacer
                if key[0] == ' ':
                    button.configure(state="disabled")

    def key(self, key):
        """
        handles when the user presses a key on the virtual keyboard

        @param key: the key that was pressed
        """

        self.entry.insert(self.entry.index("insert"), key[self.key_index])
        self.shift() if (self.key_index == 1 and (not self.caps)) or (self.key_index == 0 and self.caps) else None

    def shift(self):
        """
        handles when the user presses the shift button
        """

        self.key_index = 1 if self.key_index == 0 else 0
        for button in self.winfo_children():
            if len(button.metadata) == 2:
                button.configure(text=button.metadata[self.key_index])

    def caps_lock(self):
        """
        handles when the user presses the caps lock button
        """

        self.caps = False if self.caps else True
        self.shift() if (self.caps and self.key_index == 0) or ((not self.caps) and self.key_index == 1) else None

    def enter(self):
        """
        handles when the user presses the enter key
        """

        self.exit()
        self.callback()

    def exit(self):
        """
        closes the window and unfocuses the entry
        """

        self.place_forget()
        self.master.focus()
