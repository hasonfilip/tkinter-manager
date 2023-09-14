import tkinter as tk
from math import *

class Cli:
    def __init__(self, parent) -> None:
        self.cli_frame = tk.Frame(parent)
        self.cli_label = tk.Label(self.cli_frame, text="Python command line", width=18, height=2, borderwidth=1, relief="solid")
        self.cli_input = tk.Entry(self.cli_frame, bg="black", fg="#1fff00",insertbackground="#1fff00")
        self.cli_output = tk.Entry(self.cli_frame, bg="black", fg="#1fff00")
        self.cli_label.pack(side="top", pady=5)
        self.cli_input.pack(side="top", fill="x", expand=False)
        self.cli_input.bind("<Return>", self.update_cli_output)
        self.cli_output.pack(side="top", fill="x", expand=False)
        self.cli_frame.pack(side="bottom", fill="both", expand=True)
    
    def update_cli_output(self, event):
        self.cli_output.delete(0, "end")
        x = self.cli_input.get()
        try:
            y=eval(x)
        except Exception as e:
            y=f"Error: {e}"
        try:
            self.cli_output.insert(0, y)
        except:
            self.cli_output.insert(0, "")
        self.cli_input.delete(0, "end")




