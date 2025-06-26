import customtkinter as ctk
from subprocess import run

app = ctk.CTk()

screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
app.geometry(f"{screen_width}x{screen_height}+0+0")

b = ctk.CTkButton(app, text="cmd", command=lambda: run(['sudo', 'pkill', 'Xorg']))
b2 = ctk.CTkButton(app, text="close", command=lambda: exit(0))
b.pack()
b2.pack()

app.mainloop()