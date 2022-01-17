#! /usr/bin/env python3

import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title = "prova"

myText = tk.StringVar()
entryBox = tk.Entry(root, textvariable=myText)
entryBox.grid(row=0, column=0, sticky=["n", "w"])
button = tk.Button(root, text="Ok", command=root.destroy)
button.grid(row=0, column=1, sticky=["e", "s"])

root.mainloop()

print(f"Text: {myText.get()}")
