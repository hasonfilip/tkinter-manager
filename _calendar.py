#!/usr/bin/env python3

import datetime
import tkinter as tk

class Calendar:

    def __init__(self,parent) -> None:
        self.main_frame=tk.Frame(parent, borderwidth=1, relief="solid")

        current_year=datetime.datetime.now().year
        current_month=datetime.datetime.now().month  # 1-12
        current_day=datetime.datetime.now().day      # 1-31

        yearAdditionInTwoMonths=0
        yearAdditionInOneMonth=0
        if current_month>=11:
            if current_month==12:
                yearAdditionInOneMonth=1
            yearAdditionInTwoMonths=1

        self.year_for_top=current_year
        self.month_for_top=current_month
        self.year_for_bot=current_year + yearAdditionInTwoMonths
        self.month_for_bot=((current_month+1)%12)+1

        self.months=["Leden","Únor","Březen","Duben","Květen","Červen","Červenec","Srpen","Září","Říjen","Listopad","Prosinec"]

        self.up_image = tk.PhotoImage(file="arrow_up.png")
        self.down_image = tk.PhotoImage(file="arrow_down.png")


        upButton=tk.Button(self.main_frame, image=self.up_image, width=32, height=16, command=self.scrollUp)

        self.topLabel=tk.Label(self.main_frame, text=self.months[current_month-1]+" "+str(current_year), width=12, height=1)#, borderwidth=1, relief="solid")
        self.topMonth=tk.Frame(self.main_frame)#, borderwidth=1, relief="solid")
     
        self.midLabel=tk.Label(self.main_frame, text=self.months[((current_month)%12)+1]+" "+str(current_year+yearAdditionInOneMonth), width=12, height=1)#, borderwidth=1, relief="solid")
        self.midMonth=tk.Frame(self.main_frame)#, borderwidth=1, relief="solid")
      
        self.botLabel=tk.Label(self.main_frame, text=self.months[((current_month+1)%12)+1]+" "+str(current_year+yearAdditionInTwoMonths), width=12, height=1)#, borderwidth=1, relief="solid")
        self.botMonth=tk.Frame(self.main_frame)#, borderwidth=1, relief="solid")

        downButton=tk.Button(self.main_frame, image=self.down_image, width=32, height=16, command=self.scrollDown)

        ##############################

        upButton.pack(side="top", padx=0, pady=5)

        self.topLabel.pack(side="top", padx=0, pady=(0,5))
        self.topMonth.pack(side="top", padx=0, pady=0)

        self.midLabel.pack(side="top", padx=0, pady=5)
        self.midMonth.pack(side="top", padx=10, pady=0)

        self.botLabel.pack(side="top", padx=0, pady=5)
        self.botMonth.pack(side="top", padx=0, pady=0)

        downButton.pack(side="top", padx=0, pady=5)
    

        self.top_days=self.makeMonth(self.topMonth,current_year,current_month)
        self.mid_days=self.makeMonth(self.midMonth,current_year+yearAdditionInOneMonth,((current_month)%12)+1)
        self.bot_days=self.makeMonth(self.botMonth,current_year+yearAdditionInTwoMonths,((current_month+1)%12)+1)

        self.top_days[current_day-1].config(bg="#89cff0")   # highlights current day

    

    def makeMonth(self, parent, year:int, month:int) -> list:
        days = []
        firstDayOfMonth=datetime.datetime(year, month, 1).weekday() # 0-6

        labels_frame=tk.Frame(parent, borderwidth=1, relief="solid")
        days_frame=tk.Frame(parent, borderwidth=1, relief="solid")

        labels_frame.pack(side="top", padx=0, pady=0)
        days_frame.pack(side="top", padx=0, pady=0)

        if month==2:
            if (year%4 == 0) and ((year%100 != 0) or (year%400 == 0)):
                numberOfDays=29
            else:
                numberOfDays=28
        elif (month<8 and (month%2) == 1) or (month>=8 and (month%2) == 0):
            numberOfDays=31
        else:
            numberOfDays=30

        days_of_week=["Po","Út","St","Čt","Pá","So","Ne"]
        for i in range(7):
            label = tk.Label(labels_frame, text=days_of_week[i], width=2, height=1)
            label.grid(row=0, column=i, padx=2, pady=0)
            
        for i in range(numberOfDays):
                day_number=firstDayOfMonth+i
                day_button = tk.Button(days_frame, text=str(i+1), width=2, height=1)
                day_button.grid(row=2+(day_number//7), column=day_number%7, padx=0, pady=0)
                days.append(day_button)
        return days
    
    def destroyMonth(self, month:list) -> None:
        for day in month:
            day.destroy()
    
    def scrollUp(self) -> None:
        self.month_for_top=((self.month_for_top-1)%12)+1
        self.month_for_bot=((self.month_for_bot-1)%12)+1
        if self.month_for_top==12:
            self.year_for_top-=1
        if self.month_for_bot==12:
            self.year_for_bot-=1

        self.destroyMonth(self.bot_days)
        self.bot_days=self.mid_days
        self.botLabel.config(text=self.midLabel.cget("text"))
        self.mid_days=self.top_days
        self.midLabel.config(text=self.topLabel.cget("text"))
        #self.top_days=self.makeMonth(self.topMonth,self.year_for_top,self.month_for_top)
        #self.topLabel.config(text=self.months[self.month_for_top-1]+" "+str(self.year_for_top))


    def scrollDown(self) -> None:
        pass

    def update():
        pass