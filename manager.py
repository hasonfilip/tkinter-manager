#!/usr/bin/env python3

""" 
TODO název
Autor: Filip Hasoň
zápočtový program
letní semestr 2022/23
Předmět: NPRG031 Programování 2
"""
import tkinter as tk
from tkinter import ttk
import datetime # for _calendar.py
from _calendar import Calendar
from _register import Register



def main(): 
    root=tk.Tk()#screenName="okno")
    calendar = Calendar(root)
    register = Register(root)
    
    register.main_frame.pack(side="left", fill="both", expand=True)
    calendar.main_frame.pack(side="right", fill="both", expand=True)
    root.state('zoomed') 
    root.title('Manager')
    """"
    # Configure column weight for relative width
    root.grid_columnconfigure(0, weight=1)

    # frames,colrs = [0,0,0],["red","green","blue"]
    
    # for i in range(3):
    #     frames[i]=tk.Frame(root, width=200, height=100, bg=colrs[i])
    #     frames[i].grid(row=i, column=0, pady=(10,0), padx=10, sticky="ew")


    def button1_click():
        print("Button 1 clicked!")

    def button2_click():
        print("Button 2 clicked!")



    # Create the first frame
    frame1 = tk.Frame(root, width=200, height=100, borderwidth=2, relief=tk.RAISED)
    frame1.grid(row=1, column=0, pady=10, padx=10, sticky="ew")

    # Create the first button
    button1 = tk.Button(frame1, text="Button 1", command=button1_click)
    button1.pack(side="right", padx=5, pady=5)

    # Create the second button
    button2 = tk.Button(frame1, text="Button 2", command=button2_click)
    button2.pack(side="right", padx=5, pady=5)

    # Create the second frame
    frame2 = tk.Frame(root, width=200, height=100, bg="blue")
    frame2.grid(row=2, column=0, pady=10, padx=10, sticky="ew")

    # Create the third frame
    frame3 = tk.Frame(root, width=200, height=100, bg="green")
    frame3.grid(row=3, column=0, pady=10, padx=10, sticky="ew")


   # print(type(frame1))



    # first = tk.Canvas(root,background="green",height=root.winfo_height()+10,width=root.winfo_width()+10 )
    # first.pack()
    # button = tk.Button(root, text='Stop', width=25, command=root.destroy)

    # button.pack()

    def button_clicked():
        print("Button clicked!")
"""
    root.mainloop()


if __name__ == '__main__':
    main()