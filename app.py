# Import necessary modules.
import module
from tkinter import *
from tkinter.ttk import Notebook

toDoList={}
window=Tk()
window.geometry("600x400")
notebook=Notebook(window)

# The "To Do" tab.
toDo=Frame(window)
toDoLabel=Label(toDo, text="To Do", font="Georgia 24 bold")
toDoEntry=Entry(toDo)
toDoButton=Button(toDo, text="Add Task", command=lambda: module.addTask(toDoEntry.get()) )
listCanvasScrollbar=Scrollbar(toDo)
listCanvas=Canvas(toDo, bg="white", height=200, width=450, yscrollcommand=listCanvasScrollbar.set)
toDoLabel.grid(row=0, column=1, columnspan=3)
toDoEntry.grid(row=1, column=1)
toDoButton.grid(row=1, column=2)
listCanvas.grid(row=2, column=1, columnspan=2)
listCanvasScrollbar.grid(row=2, column=3, sticky="nsw")
toDo.grid_columnconfigure(0, weight=1)
toDo.grid_columnconfigure(4, weight=1)
toDo.pack()

notebook.add(toDo, text="To Do")
notebook.pack(expand=True, fill=BOTH)

window.mainloop()