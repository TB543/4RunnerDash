from datetime import datetime, timedelta
from customtkinter import CTkFrame, CTkLabel, StringVar
from Dev.TSCTkButton import TSCTkButton


class Calendar(CTkFrame):
    """
    a class to represent a calender date picker
    """

    def __init__(self, master, callback, **kwargs):
        """
        creates the calendar object

        :param master: the master widget to control this one
        :param callback: the function that is called when a date is picked, takes 1 parameter the date string in MM-DD-YYYY format
        """

        # initializes class
        self.callback = callback
        self.month = datetime.now().month
        self.year = datetime.now().year
        super().__init__(master, **kwargs)

        # draws header
        self.header = StringVar(self)
        header = CTkFrame(self)
        TSCTkButton(header, text="◀◀", width=50, font=("Arial", 10), command=lambda: self.draw(self.month, self.year - 1)).pack(side="left", padx=10)
        TSCTkButton(header, text="▶▶", width=50, font=("Arial", 10), command=lambda: self.draw(self.month, self.year + 1)).pack(side="right", padx=10)
        TSCTkButton(header, text="◀", width=50, font=("Arial", 10), command=lambda: self.draw(self.month - 1, self.year)).pack(side="left")
        TSCTkButton(header, text="▶", width=50, font=("Arial", 10), command=lambda: self.draw(self.month + 1, self.year)).pack(side="right")
        CTkLabel(header, textvariable=self.header, font=("Arial", 20, "bold")).pack(side="left", expand=True, pady=10)
        header.pack(side="top", fill="x", padx=5, pady=5)

        # draws body
        self.body = CTkFrame(self)
        for i, day in enumerate(["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]):
            self.body.columnconfigure(i, weight=1)
            self.body.rowconfigure(i, weight=1)
            CTkLabel(self.body, text=day, font=("Arial", 20)).grid(row=0, column=i)
        self.body.pack(fill="both", padx=5, pady=5, expand=True)
        self.draw(self.month, self.year)

    def draw(self, month, year):
        """
        draws the calender UI

        :param month: the month to draw
        :param year: the year to draw
        """

        # month looping
        if month > 12:
            month = 1
            year += 1
        elif month < 1:
            month = 12
            year -= 1

        # sets header
        self.month = month
        self.year = year
        date = datetime(year, month, 1)
        self.header.set(date.strftime("%B %Y"))

        # clears old calendar
        for widget in self.body.winfo_children():
            if type(widget) == TSCTkButton:
                widget.destroy()

        # draws days
        row = 1
        while date.month == month:
            row += 1 if date.weekday() == 6 and date.day != 1 else 0
            btn = TSCTkButton(self.body, text=date.day, font=("Arial", 20), command=lambda d=date.strftime("%m/%d/%Y"): self.callback(d))
            btn.grid(row=row, column=(date.weekday() + 1) % 7, stick="nsew", padx=5, pady=5)
            date += timedelta(days=1)
