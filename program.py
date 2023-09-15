#!/usr/bin/env python3

""" 
Tkinter manager
Autor: Filip Hasoň
zápočtový program
letní semestr 2022/23
Předmět: NPRG031 Programování 2
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from modules.cli import Cli
import datetime
import json
import platform
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

months = ["Leden", "Únor", "Březen", "Duben", "Květen", "Červen",
          "Červenec", "Srpen", "Září", "Říjen", "Listopad", "Prosinec"]
days = ["Po", "Út", "St", "Čt", "Pá", "So", "Ne"]

buttons = []
number_of_top_buttons = 0
number_of_mid_buttons = 0
number_of_bot_buttons = 0
first_day = 0
last_day = 0
basic_button_color = "white"
scroll_flag = True

today = int(str(datetime.datetime.now().year)+str(datetime.datetime.now().month).zfill(2)+str(datetime.datetime.now().day).zfill(2))

def main():
    global basic_button_color
    root=tk.Tk()
    root.title('Manager')
    if platform.system() == "Linux":
        root.attributes('-zoomed', True)
    elif platform.system() == "Windows":
        root.state('zoomed')
    
    register = Register(root)
    register.main_frame.pack(side="left", fill="both", expand=True)

    calendar = Calendar(root, register)
    calendar.main_frame.pack(side="right", fill="y", expand=False, padx=10, pady=10)

    basic_button_color = calendar.top_buttons[0].cget("bg")

    cli = Cli(calendar.main_frame)
    cli.cli_frame.pack(side="bottom", fill="both", expand=True)

    register.main_frame.update()
    register.load_tasks()
    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(register.tasks, root))

    root.bind("<Control-n>", lambda event: register.create_new_task())
    root.bind("<Configure>", lambda event: register.sort_tasks())
    root.bind("<Control-s>", lambda event: on_closing(register.tasks, root, False))

    root.mainloop()


def on_closing(tasks:list, root, close=True):
    """Saves tasks and optionally closes the window"""
    list = []
    for task in tasks:
        list.append([task.creation_date, task.deadline, task.title, task.urgency, task.notes])
    json_save(list, "tasks.json")
    if close:
        root.destroy()

def json_save(data, filename):
    """Saves data to a json file"""
    try:
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print(f"An error occurred while saving to {filename}: {e}")    

def json_load(filename): # is called in register.load_tasks()
    """Loads data from a json file"""
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError or json.decoder.JSONDecodeError:
        print(f"File not found. Returning an empty dictionary.")        
        return {}
    except Exception as e:
        print(f"An error occurred while loading from {filename}: {e}")
        return {}

class Task:
    def __init__(self, canvas, creation_date, deadline, title="Title", urgency=0, notes="", order=0, delete_image=None, edit_image=None, delete_callback=None):
        
        self.canvas_parent = canvas
        self.creation_date = creation_date
        self.deadline = deadline
        self.title = title
        self.urgency = urgency
        self.notes = notes
        self.window_id = 0
        self.order = order
        self.delete_callback = delete_callback
        self.frame_height = 100        

        self.edit_image = edit_image
        self.delete_image = delete_image

        self.frame = tk.Frame(self.canvas_parent, borderwidth=1, relief="solid", height=self.frame_height)
        self.frame.pack_propagate(0) 

        self.left_frame = ttk.Frame(self.frame, borderwidth=1, relief="solid", height=100)
        self.left_frame.pack(side="left", padx=5, pady=5)

        self.title_label = tk.Label(self.left_frame, text=self.title, font=("Arial", 10))
        self.title_label.pack(side="left", padx=5, pady=5)
        self.title_label.bind("<Button-1>", self.open_task)
        
        self.edit_button = tk.Button(self.left_frame, image=self.edit_image, width=16, height=16, command=lambda: self.edit_title())
        self.edit_button.pack(side="right", padx=5, pady=5)



        mid_frame = tk.Frame(self.frame)
        mid_frame.pack(side="left", padx=5, pady=5, fill="both", expand=True)

        self.content_sample = tk.Text(mid_frame, height=4, width=30, wrap="word", font=("Arial", 10))
        self.content_sample.insert(tk.END, self.notes)
        self.content_sample.configure(state="disabled")
        self.content_sample.bind("<Button-1>", self.open_task)
        self.content_sample.pack(side="top", padx=5, pady=5, fill="x", expand=True)
        

        self.delete = None
        delete_button = tk.Button(self.frame, image=self.delete_image,width=16,height=16, command=lambda: self.delete())
        delete_button.pack(side="right", padx=(0,5), pady=5)



        right_frame = tk.Frame(self.frame, borderwidth=1, relief="solid")
        right_frame.pack(side="right", padx=5, pady=5)



        priority_options = [0,1,2,3]

        priority_label=tk.Label(right_frame, text="Priority", width=12, height=1)
        priority_label.grid(row=0, column=0, padx=0, pady=5)    

        prio_combobox = ttk.Combobox(right_frame, width=2, state="readonly")
        prio_combobox["values"] = priority_options
        prio_combobox.current(self.urgency)
        prio_combobox.bind("<<ComboboxSelected>>", lambda event: self.change_priority(prio_combobox.get()))
        prio_combobox.grid(row=0, column=1, padx=0, pady=5)


        deadline_frame = tk.Frame(right_frame)
        deadline_frame.grid(row=1, column=1, padx=0, pady=5)

        deadline_label=tk.Label(right_frame, text="Deadline:", width=12, height=1)
        deadline_label.grid(row=1, column=0, padx=0, pady=5)     
        
        self.deadline_day = ttk.Entry(deadline_frame, width=2, justify="center")
        self.deadline_day.insert(0, str(self.deadline)[6:8])
        self.deadline_day.bind("<FocusIn>", lambda event: self.deadline_day.select_range(0, tk.END))
        self.deadline_day.bind("<KeyRelease>", self.change_deadline)
        self.deadline_day.bind("<Return>", lambda event: deadline_frame.focus_set())
        self.deadline_day.pack(side="left", padx=0, pady=5)

        self.deadline_month = ttk.Entry(deadline_frame, width=2, justify="center")
        self.deadline_month.insert(0, str(self.deadline)[4:6])
        self.deadline_month.bind("<FocusIn>", lambda event: self.deadline_month.select_range(0, tk.END))
        self.deadline_month.bind("<KeyRelease>", self.change_deadline)
        self.deadline_month.bind("<Return>", lambda event: deadline_frame.focus_set())
        self.deadline_month.pack(side="left", padx=0, pady=5)

        self.deadline_year = ttk.Entry(deadline_frame, width=4, justify="center")
        self.deadline_year.insert(0, str(self.deadline)[0:4])
        self.deadline_year.bind("<FocusIn>", lambda event: self.deadline_year.select_range(0, tk.END))
        self.deadline_year.bind("<KeyRelease>", self.change_deadline)
        self.deadline_year.bind("<Return>", lambda event: deadline_frame.focus_set())
        self.deadline_year.pack(side="left", padx=(0,5), pady=5)

        self.config_day_button()

    def open_task(self, event=None):
        """Opens a task in a new window"""
        global scroll_flag
        scroll_flag = False
        self.task_window=tk.Toplevel()
        self.task_window.title(self.title)
        self.task_window.geometry("600x400")
        self.task_window.protocol("WM_DELETE_WINDOW", self.close_task)

        self.headline = ttk.Label(self.task_window, text=self.title, font=("Helvetica", 14))
        self.headline.bind("<Button-1>", self.edit_title_within)
        self.headline.pack(side="top", padx=5, pady=(20,0))

        
        self.notes_text = tk.Text(self.task_window,wrap="word", font=("Arial", 10))
        notes_scrollbar = tk.Scrollbar(self.task_window, command=self.notes_text.yview)
        self.notes_text.configure(yscrollcommand=notes_scrollbar.set)
        notes_scrollbar.pack(side="right", fill="y")
        self.notes_text.insert(tk.END, self.notes)
        self.notes_text.pack(side="top", padx=20, pady=20, fill="both", expand=True)

    def close_task(self):
        """Closes the task window"""
        global scroll_flag
        scroll_flag = True
        self.notes = self.notes_text.get("1.0", tk.END)        
        self.task_window.destroy()
        self.task_window = None
        self.content_sample.configure(state="normal")
        self.content_sample.delete("1.0", tk.END)
        self.content_sample.insert(tk.END, self.notes)
        self.content_sample.configure(state="disabled")


    def edit_title_within(self, event=None):
        self.headline.pack_forget()
        self.notes_text.pack_forget()
        self.headline_entry = tk.Entry(self.task_window, justify="center", font=("Helvetica", 14))
        self.headline_entry.insert(0, self.title)
        self.headline_entry.bind("<Return>", self.save_title_within)
        self.headline_entry.bind("<FocusIn>", lambda event: self.headline_entry.select_range(0, tk.END))
        self.headline_entry.focus_set()
        self.headline_entry.pack(side="top", padx=5, pady=(20,0))
        self.notes_text.pack(side="top", padx=20, pady=20, fill="both", expand=True)

    def save_title_within(self, event=None):
        self.notes_text.pack_forget()
        self.title = self.headline_entry.get()
        self.title_label.config(text=self.title)
        self.headline.config(text=self.headline_entry.get())
        self.headline_entry.destroy()
        self.headline.pack(side="top", padx=5, pady=(20,0))
        self.notes_text.pack(side="top", padx=20, pady=20, fill="both", expand=True)
        self.unconfig_day_button()
        self.config_day_button()

    def edit_title(self, event=None):
        self.title_label.pack_forget()
        self.edit_button.pack_forget()

        self.title_entry = tk.Entry(self.left_frame, width=12)
        self.title_entry.insert(0, self.title)        
        self.title_entry.bind("<Return>", self.save_title)
        self.title_entry.bind("<FocusIn>", lambda event: self.title_entry.select_range(0, tk.END))
        self.title_entry.focus_set()
        self.title_entry.pack(side="left", padx=5, pady=5)

        self.save_button = tk.Button(self.left_frame, text="OK", command=lambda: self.save_title(None))
        self.save_button.pack(side="right", padx=5, pady=5)

    def save_title(self, event=None):
        self.title = self.title_entry.get()
        self.title_label.config(text=self.title)
        self.title_entry.destroy()
        self.save_button.destroy()
        self.title_label.pack(side="left", padx=5, pady=5)
        self.edit_button.pack(side="right", padx=5, pady=5)
        self.unconfig_day_button()
        self.config_day_button()

    def change_priority(self, priority):
        self.urgency = int(priority)
        self.unconfig_day_button()
        self.config_day_button()

    def change_deadline(self, event):
        year = self.deadline_year.get()
        month = self.deadline_month.get()
        day = self.deadline_day.get()
        try:
            is_valid_date(year, month, day)
        except InvalidDateException:
            return
        
        self.unconfig_day_button()
        self.deadline = int(self.deadline_year.get()+self.deadline_month.get().zfill(2)+self.deadline_day.get().zfill(2))
        self.config_day_button()
        

    def adjust_date(self, date): # date format is int(yyyymmdd), thus if we want to get the index of the button in the list of buttons 
                                 # using this number, we need to subtract redundance and add the number of buttons in the previous months
        if date>=100 and date<=130:
            date = date - 100 + number_of_top_buttons
        elif date>=200 and date<=230:
            date = date - 200 + number_of_top_buttons + number_of_mid_buttons
        elif date>=8900 and date<=8930:
            date = date - 8900 + number_of_top_buttons
        elif date>=9000 and date<=9030:
            date = date - 9000 + number_of_top_buttons + number_of_mid_buttons
        return date

    def config_day_button(self, shift=0, stop=100):
        """Configures the button of the day the task is on"""
        colors = ["white", "yellow", "orange", "red"] 
        global buttons, first_day, last_day     

        if self.deadline>=first_day and self.deadline<=last_day:
            date = self.adjust_date(self.deadline-first_day)
            if date>=shift and date<=stop:
                buttons[date].config(bg=colors[self.urgency], command=lambda: self.open_task())
                ToolTip.create_tool_tip(buttons[date], self.title)

    def unconfig_day_button(self):
        """Unconfigures the button of the day the task is on"""
        global buttons, first_day, last_day, basic_button_color

        if self.deadline>=first_day and self.deadline<=last_day:
            date = self.adjust_date(self.deadline-first_day)
            buttons[date].config(bg=basic_button_color, command=lambda: None)
            buttons[date].unbind("<Enter>")
            buttons[date].unbind("<Leave>")


class InvalidDateException(Exception):
    pass

def is_valid_date(year, month, day):
    try:
        year = int(year)
        month = int(month)
        day = int(day)
    except ValueError:
        raise InvalidDateException("Year, month and day must be integers")

    if month < 1 or month > 12:
        raise InvalidDateException("Month must be 1-12")

    if day < 1 or day > 31: 
        raise InvalidDateException("Day must be 1-31")

class Register:
    global today
    def __init__(self, parent):

        self.main_frame=tk.Frame(parent, borderwidth=1, relief="solid")        

        self.current_year=datetime.datetime.now().year
        self.current_month=datetime.datetime.now().month  # 1-12
        self.current_day=datetime.datetime.now().day      # 1-31

        self.delete_image = tk.PhotoImage(file="icons/delete.png")  
        self.edit_image = tk.PhotoImage(file="icons/edit.png")

        # MENU

        menu=tk.Frame(self.main_frame, borderwidth=1, relief="solid")
        menu.pack(side="top", fill="x")

        self.new_task_button = tk.Button(menu, text="New task", command=lambda: self.create_new_task())
        self.new_task_button.pack(side="left", padx=5, pady=5)

        self.sort_combobox = ttk.Combobox(menu, width=12, state="readonly")
        self.sort_combobox["values"] = ["Creation date", "Deadline", "Priority", "Title"]
        self.sort_combobox.current(0)
        self.sort_combobox.bind("<<ComboboxSelected>>", lambda event: self.sort_tasks())
        self.sort_combobox.pack(side="right", padx=5, pady=5)

        sort_label = tk.Label(menu, text="Sort by")
        sort_label.pack(side="right", padx=0, pady=5)

        # TASKS

        self.tasks = []

        self.scrollbar = tk.Scrollbar(self.main_frame, orient="vertical") 
        self.tasks_canvas = tk.Canvas(self.main_frame, yscrollcommand=self.scrollbar.set)
        self.tasks_canvas.bind("<Configure>", lambda event: self.tasks_canvas.configure(scrollregion=self.tasks_canvas.bbox("all")))
        self.tasks_canvas.bind_all("<MouseWheel>", lambda event: self.on_mousewheel(event))
        self.tasks_canvas.pack(side="left", fill="both", expand=True)
         
        self.scrollbar.config(command=self.tasks_canvas.yview)
        self.scrollbar.pack(side="right", fill="y")

    def on_mousewheel(self, event):
        """Scrolls the canvas with the mouse wheel"""
        global scroll_flag
        if self.scrollbar.get() != (0.0, 1.0) and scroll_flag:
            if platform.system() == "Linux":
                self.tasks_canvas.yview_scroll(-1*(event.delta), "units")
            elif platform.system() == "Windows":
                self.tasks_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def load_tasks(self):
        """Loads tasks from a json file and creates them again"""
        list = json_load("tasks.json")
        for task in list:
            self.create_new_task(task[0], task[1], task[2], task[3], task[4], self.delete)
        self.tasks_canvas.configure(scrollregion=self.tasks_canvas.bbox("all"))
        
    def create_new_task(self, creation_day=today, deadline=today, title="Title", urgency=0, content="", delete_callback=None):
        """Creates a new task, places it on the canvas and adds it to the list of tasks"""
        new_task = Task(self.tasks_canvas, creation_day, deadline, title, urgency, content, len(self.tasks), self.delete_image, self.edit_image, delete_callback)
        new_task.delete = lambda: self.delete(new_task)
        self.place(new_task)
        self.tasks.append(new_task)
        self.tasks_canvas.configure(scrollregion=self.tasks_canvas.bbox("all"))
        self.sort_tasks()

    def place(self, task:Task):
        """Places a task on the canvas"""
        task.delete = lambda: self.delete(task)
        task.window_id = self.tasks_canvas.create_window(10, 12+(task.frame_height+10)*task.order, window = task.frame, anchor = "nw", width = self.tasks_canvas.winfo_width()-20)

    def remove(self, task:Task):
        """Removes a task from the canvas"""
        self.tasks_canvas.delete(task.window_id)

    def delete(self, task:Task):
        """Deletes a task"""
        if messagebox.askokcancel('Confirmation','Are you sure you want to delete this task?'):
            task.unconfig_day_button()
            self.remove(task) # remove window with frame from canvas
            task.frame.destroy() # destroy frame
            self.tasks.remove(task) # remove from list

            self.sort_tasks()            
            self.tasks_canvas.configure(scrollregion=self.tasks_canvas.bbox("all")) # update scrollregion

    def sort_tasks(self):
        """Sorts tasks according to the selected option"""
        for task in self.tasks:
            self.remove(task)

        sort_by = self.sort_combobox.get()
        if sort_by == "Creation date":
            self.tasks.sort(key=lambda x: x.creation_date)
        elif sort_by == "Deadline":
            self.tasks.sort(key=lambda x: x.deadline)
        elif sort_by == "Priority":
            self.tasks.sort(key=lambda x: x.urgency, reverse=True)
        elif sort_by == "Title":
            self.tasks.sort(key=lambda x: x.title)

        for i, task in enumerate(self.tasks):
            task.order = i
            self.place(task)

        self.tasks_canvas.configure(scrollregion=self.tasks_canvas.bbox("all"))
        self.tasks_canvas.update_idletasks()

    def update(self, shift=0, stop=100):
        for task in self.tasks:
            task.config_day_button(shift, stop)


class Calendar:
    def __init__(self, parent, register=None):
        global buttons, number_of_top_buttons, number_of_mid_buttons, number_of_bot_buttons, first_day, last_day

        self.register = register

        self.main_frame=tk.Frame(parent)

        self.up_image = tk.PhotoImage(file="icons/arrow_up.png")
        self.down_image = tk.PhotoImage(file="icons/arrow_down.png")

        main_label=tk.Label(self.main_frame, text="Kalendář", width=12, height=2, border=1, relief="solid")
        main_label.pack(side="top")

        current_year=datetime.datetime.now().year
        current_month=datetime.datetime.now().month  # 1-12

        year_addition_in_one_month=0  # number of years to add to the year of the middle month
        year_addition_in_two_months=0 # number of years to add to the year of the bottom month        
        if current_month>=11:
            if current_month==12:
                year_addition_in_one_month=1
            year_addition_in_two_months=1

        self.year_for_top=current_year  # years of corresponding months shown on the calendar
        self.month_for_top=current_month
        self.year_for_mid=current_year + year_addition_in_one_month
        self.month_for_mid=((current_month)%12)+1
        self.year_for_bot=current_year + year_addition_in_two_months
        self.month_for_bot=((current_month+1)%12)+1

        first_day = 100*self.month_for_top+10000*self.year_for_top+1
        last_day = 100*self.month_for_bot+10000*self.year_for_bot+32

        up_button=tk.Button(self.main_frame, image=self.up_image, width=32, height=16, command=self.scroll_up)
        up_button.pack(side="top", pady=(5,0))

        self.calendar_frame=tk.Frame(self.main_frame)
        self.calendar_frame.pack(side="top")

        down_button=tk.Button(self.main_frame, image=self.down_image, width=32, height=16, command=self.scroll_down)
        down_button.pack(side="top", pady=(5,0))

        self.top_month_frame=tk.Frame(self.calendar_frame)
        self.top_month_frame.pack(side="top")

        self.mid_month_frame=tk.Frame(self.calendar_frame)
        self.mid_month_frame.pack(side="top")

        self.bot_month_frame=tk.Frame(self.calendar_frame)
        self.bot_month_frame.pack(side="top")

        self.top_buttons=self.make_month(self.top_month_frame,current_year,current_month)
        self.mid_buttons=self.make_month(self.mid_month_frame,current_year+year_addition_in_one_month,((current_month)%12)+1)
        self.bot_buttons=self.make_month(self.bot_month_frame,current_year+year_addition_in_two_months,((current_month+1)%12)+1)

        buttons = self.top_buttons + self.mid_buttons + self.bot_buttons
        number_of_top_buttons = len(self.top_buttons)
        number_of_mid_buttons = len(self.mid_buttons)
        number_of_bot_buttons = len(self.bot_buttons)


    def make_month(self, parent:tk.Frame, year:int, month:int) -> list:
        """Creates a month with buttons for each day and returns a list of those buttons"""
        global months, days
        label = tk.Label(parent, text=months[month-1]+" "+str(year), width=11, height=1, border=1, relief="solid")
        label.pack(side="top", padx=0, pady=5)

        labels_frame=tk.Frame(parent, borderwidth=1, relief="solid")
        labels_frame.pack(side="top", padx=0, pady=0)

        days_frame=tk.Frame(parent, borderwidth=1, relief="solid")        
        days_frame.pack(side="top", padx=0, pady=0)

        for i in range(7):
            label = tk.Label(labels_frame, text=days[i], width=2, height=1)
            label.grid(row=0, column=i, padx=2, pady=0)

        day_buttons = []
        first_day_of_month = datetime.datetime(year, month, 1).weekday() # 0-6

        if month==2:
            if (year%4 == 0) and ((year%100 != 0) or (year%400 == 0)):
                number_of_days=29
            else:
                number_of_days=28
        elif (month<8 and (month%2) == 1) or (month>=8 and (month%2) == 0):
            number_of_days=31
        else:
            number_of_days=30       

        today_is_in_this_month = False
        if datetime.datetime.now().year == year and datetime.datetime.now().month == month:
            today_is_in_this_month = True

        for i in range(number_of_days):            
            day_number=first_day_of_month+i
            day_button = tk.Button(days_frame, text=str(i+1), width=2, height=1)      
            day_button.grid(row=2+(day_number//7), column=day_number%7, padx=0, pady=0) 

            day_buttons.append(day_button)

        if today_is_in_this_month:
            day_buttons[datetime.datetime.now().day-1].config(foreground="#0D01EB")

        return day_buttons       

    
    def scroll_down(self) -> None:  
        """Scrolls the calendar down by one month"""
        global first_day, last_day, buttons, number_of_top_buttons, number_of_mid_buttons, number_of_bot_buttons
        if self.month_for_top==12:
            self.year_for_top+=1
            first_day+=10000
        else: first_day+=100
        if self.month_for_mid==12:
            self.year_for_mid+=1
        if self.month_for_bot==12:
            self.year_for_bot+=1
            last_day+=10000
        else: last_day+=100

        self.month_for_top = ((self.month_for_top)%12)+1
        self.month_for_mid=((self.month_for_mid)%12)+1
        self.month_for_bot=((self.month_for_bot)%12)+1

        self.top_month_frame.destroy()
        self.top_month_frame=tk.Frame(self.calendar_frame)
        self.top_month_frame=self.mid_month_frame
        self.top_buttons=self.mid_buttons
        self.mid_month_frame=self.bot_month_frame
        self.mid_buttons=self.bot_buttons
        self.bot_month_frame=tk.Frame(self.calendar_frame)       
        self.bot_buttons=self.make_month(self.bot_month_frame,self.year_for_bot,self.month_for_bot)
        self.top_month_frame.pack(side="top", padx=0, pady=0)
        self.mid_month_frame.pack(side="top", padx=0, pady=0)
        self.bot_month_frame.pack(side="top", padx=0, pady=0)

        buttons = self.top_buttons + self.mid_buttons + self.bot_buttons
        number_of_top_buttons = len(self.top_buttons)
        number_of_mid_buttons = len(self.mid_buttons)
        number_of_bot_buttons = len(self.bot_buttons)    

        self.register.update(number_of_bot_buttons)

    def scroll_up(self) -> None:
        """Scrolls the calendar up by one month"""
        global first_day, last_day, buttons, number_of_top_buttons, number_of_mid_buttons, number_of_bot_buttons
        self.top_month_frame.pack_forget() # for some reason packing must be forgotten here, unlike in scrollDown()
        self.mid_month_frame.pack_forget()

        self.month_for_top=((self.month_for_top-2)%12)+1
        self.month_for_mid=((self.month_for_mid-2)%12)+1
        self.month_for_bot=((self.month_for_bot-2)%12)+1

        if self.month_for_top==12:
            self.year_for_top-=1
            first_day-=10000
        else: first_day-=100
        if self.month_for_mid==12:
            self.year_for_mid-=1
        if self.month_for_bot==12:
            self.year_for_bot-=1
            last_day-=10000
        else: last_day-=100

        self.bot_month_frame.destroy()
        self.bot_month_frame=tk.Frame(self.calendar_frame)
        self.bot_month_frame=self.mid_month_frame
        self.bot_buttons=self.mid_buttons
        self.mid_month_frame=self.top_month_frame
        self.mid_buttons=self.top_buttons
        self.top_month_frame=tk.Frame(self.calendar_frame)
        self.top_buttons=self.make_month(self.top_month_frame,self.year_for_top,self.month_for_top)
        self.top_month_frame.pack(side="top", padx=0, pady=0)
        self.mid_month_frame.pack(side="top", padx=0, pady=0)
        self.bot_month_frame.pack(side="top", padx=0, pady=0)

        buttons = self.top_buttons + self.mid_buttons + self.bot_buttons
        number_of_top_buttons = len(self.top_buttons)
        number_of_mid_buttons = len(self.mid_buttons)
        number_of_bot_buttons = len(self.bot_buttons)

        self.register.update(0, number_of_top_buttons)

class ToolTip(object):
    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def show_tip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() 
        y = y + cy + self.widget.winfo_rooty() -23
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                      background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hide_tip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

    @classmethod
    def create_tool_tip(cls, widget, text):
        tool_tip = cls(widget) 
        def enter(event):
            tool_tip.show_tip(text)
        def leave(event):
            tool_tip.hide_tip()
        widget.bind('<Enter>', enter)
        widget.bind('<Leave>', leave)

    def delete_tool_tip(self, widget):
        widget.unbind('<Enter>')
        widget.unbind('<Leave>')
        self.hide_tip()


if __name__ == '__main__':
    main()