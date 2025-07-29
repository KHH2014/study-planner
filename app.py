# Import necessary modules.
import module
from tkinter import *
from tkinter.ttk import Notebook

window=Tk()
window.geometry("600x400")
notebook=Notebook(window)
toDo=Frame(window)
toDoLabel=Label(toDo, text="To Do", font="Georgia 24 bold")
toDoEntry=Entry(toDo)
toDoButton=Button(toDo, text="Add Task")
toDoLabel.grid(row=0, column=0, columnspan=3)
toDoEntry.grid(row=1, column=0, columnspan=2)
toDoButton.grid(row=1, column=2)
toDo.pack()
notebook.add(toDo, text="To Do")
notebook.pack(expand=True, fill=BOTH)

window.mainloop()