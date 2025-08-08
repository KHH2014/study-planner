# Import necessary modules.
import tkinter as tk
from ttkbootstrap import *

def refreshList():
    for i in toDoCanvasFrame.winfo_children():
        if isinstance(i, Checkbutton):
            if "selected" in i.state():
                for j in range(len(toDoList)):
                    if toDoList[j]==i.cget("text"):
                        del toDoList[j]
                        break
            i.destroy()
    count=2
    for i in toDoList:
        if not i=="":
            globals()["check", str(count)]=Checkbutton(toDoCanvasFrame, text=i)
            globals()["check", str(count)].state(["!alternate"])
            globals()["check", str(count)].grid(row=count, column=0, columnspan=2)
            count+=1
    listRefreshButton.grid(row=count, column=0, columnspan=2)
def addTask():
    toDoList.append(toDoEntry.get())
    refreshList()
def windowClose():
    x=""
    for i in toDoList:
        x+=i+"&newTask;"
    try:
        file=open("list.txt", "x")
    except:
        file=open("list.txt", "w")
    file.write(x)
    window.destroy()

try:
    file=open("list.txt", "r")
    toDoList=[]
    for i in file.read().split("&newTask;"):
        toDoList.append(i)
except:
    toDoList=[]
window=tk.Tk()
window.title("Study Planner")
window.resizable(0, 0)
window.geometry("600x400")
window.protocol("WM_DELETE_WINDOW", windowClose)
notebook=Notebook(window)

# The "To Do" tab.
toDo=Frame(window)
toDo.pack()
toDoCanvas=tk.Canvas(toDo)
toDoCanvas.pack(side="left", fill="both", expand=1)
toDoCanvasScrollbar=Scrollbar(toDo, command=toDoCanvas.yview)
toDoCanvasScrollbar.pack(side="right", fill="y")
toDoCanvasFrame=Frame(toDoCanvas, height=300, width=500)
toDoCanvas.create_window((70, 0), window=toDoCanvasFrame, anchor="nw")
toDoLabel=Label(toDoCanvasFrame, text="To Do", font="TkDefaultFont 24 bold")
toDoLabel.grid(row=0, column=0, columnspan=2)
toDoEntry=Entry(toDoCanvasFrame)
toDoEntry.grid(row=1, column=0)
toDoButton=Button(toDoCanvasFrame, text="Add Task", command=addTask)
toDoButton.grid(row=1, column=1)
listRefreshButton=Button(toDoCanvasFrame, text="Refresh", command=refreshList, bootstyle="outline")
listRefreshButton.grid(row=2, column=0, columnspan=2)
refreshList()

toDoCanvas.config(yscrollcommand=toDoCanvasScrollbar)
toDoCanvas.bind("<Configure>", lambda event: toDoCanvas.configure(scrollregion=toDoCanvas.bbox("all")))
notebook.add(toDo, text="To Do")
notebook.pack(expand=True, fill="both")

window.mainloop()