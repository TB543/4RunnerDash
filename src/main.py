import customtkinter as ctk

app = ctk.CTk()

screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
app.geometry(f"{screen_width}x{screen_height}+0+0")

b = ctk.CTkButton(app, command=lambda: print("test"))
b.pack()

app.mainloop()