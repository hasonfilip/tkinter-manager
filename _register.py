#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk

class Register:

    def __init__(self,parent) -> None:
        self.main_frame=tk.Frame(parent, borderwidth=1, relief="solid")

    # MENU
        menu=tk.Frame(self.main_frame, borderwidth=1, relief="solid")
        button1 = tk.Button(menu, text="New", command=self.new_button_onclick)
        button2 = tk.Button(menu, text="Sort by...")#, command=self.button2_click)
        button3 = tk.Button(menu, text="Settings")#, command=self.button3_click)
        button4 = tk.Button(menu, text="Button 4")#, command=self.button4_click)

        self.sorting_var = tk.StringVar(value="Name")
        sort_combobox = ttk.Combobox(menu, textvariable=self.sorting_var, values=["Name", "Date", "Priority"], width=8)

        button1.pack(side="left", padx=5, pady=5)
        button2.pack(side="left", padx=5, pady=5)
        button3.pack(side="left", padx=5, pady=5)
        button4.pack(side="left", padx=5, pady=5)
        sort_combobox.pack(side="left", padx=5, pady=5)


    # FRAMES

        menu.pack(side="top", fill="x")

    def new_button_onclick(self):
        new_frame=tk.Frame(self.main_frame, borderwidth=1, relief="solid", height=100, background="green")
        new_frame.pack(side="top", fill="x",padx=5, pady=5)
        new_frame.bind("<Button-1>", self.open_task)

    def open_task(self, event):
        print("done")
        pass
