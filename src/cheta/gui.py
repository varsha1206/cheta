import tkinter as tk

def open_gui():
    root = tk.Tk()
    root.title("Cheta - Live Sports")
    root.geometry("300x150")

    btn_cricket = tk.Button(root, text="Cricket", width=15)
    btn_football = tk.Button(root, text="Football", width=15)

    btn_cricket.pack(pady=10)
    btn_football.pack(pady=10)

    root.mainloop()
