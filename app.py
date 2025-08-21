# Import necessary modules.
from datetime import datetime
import tkinter as tk
import platform
from ttkbootstrap import Notebook, Meter, Separator, Button, Label, Entry, LabelFrame, Frame, Scrollbar, Checkbutton, OptionMenu, Toplevel, StringVar
from ttkbootstrap.dialogs import Messagebox
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def refreshList():
    for i in toDoCanvasFrame.winfo_children():
        if isinstance(i, Checkbutton):
            if "selected" in i.state():
                for index, subject in enumerate(toDoList):
                    if subject == i.cget("text"):
                        del toDoList[index]
                        break
            i.destroy()
    count = 2
    for i in toDoList:
        if not i == "":
            globals()["check", str(count)] = Checkbutton(
                toDoCanvasFrame, text=i)
            globals()["check", str(count)].state(["!alternate"])
            globals()["check", str(count)].grid(
                row=count, column=0, columnspan=2)
            count += 1


def addTask():
    toDoList.append(toDoEntry.get())
    refreshList()


def windowClose():
    x = ""
    for i in toDoList:
        x += i+"&newTask;"
    try:
        file = open("list.txt", "x")
    except:
        file = open("list.txt", "w")
    file.write(x)
    x = ""
    for i in studyData:
        for key, value in i.items():
            x += key+"&Minutes;"+str(value)+"&newSubject;"
        x += "&newDay;"
    try:
        file = open("study_data.txt", "x")
    except:
        file = open("study_data.txt", "w")
    file.write(x)
    x = datetime.now().strftime("%V")
    try:
        file = open("week.txt", "x")
    except:
        file = open("week.txt", "w")
    file.write(x)
    x = ""
    for i in goals:
        x += str(i)+" "
    try:
        file = open("goals.txt", "x")
    except:
        file = open("goals.txt", "w")
    file.write(x)
    file.close()
    window.destroy()


def updateMeter(event=None):
    if dropdownVar.get() == "Overall":
        x = 0
        for i in studyData:
            for j in i.values():
                x += j
        y = 0
        for i in goals:
            y += i
        percent = x/y*100
        progressMeter.configure(amountused=percent)
        progressLabel.config(
            text=f"Overall, you've studied {x} minutes this week.")
    else:
        index = subjects.index(dropdownVar.get())
        percent = values[index]/goals[index]*100
        progressMeter.configure(amountused=percent)
        progressLabel.config(
            text=f"You've studied {values[index]} minutes this week.")


def updatePlots():
    updateMeter()
    if max(values) == 0:
        ax.clear()
        pie.draw()
        ax2.clear()
        week.draw()
        statsLabel.config(text="You haven't studied this week.")
        weekLabel.config(text="You haven't studied this week.")
    else:
        ax.clear()
        ax.pie(values, autopct="%1.1f%%")
        pie.draw()
        highest = values.index(max(values))
        colorString = ""
        colorInfo = ["blue", "orange", "green", "red",
                     "purple", "brown", "pink", "grey", "olive", "cyan"]
        for index, subject in enumerate(subjects):
            if index == len(subjects)-1:
                colorString += f"and {subject} is {colorInfo[index]}."
            else:
                colorString += f"{subject} is {colorInfo[index]}, "
        statsLabel.config(
            text=f"You've studied {subjects[highest]} the most this week. {colorString}")
        global yAxis
        yAxis = []
        for i in studyData:
            yAxis.append(sum(i.values()))
        ax2.clear()
        ax2.bar(xAxis, yAxis)
        week.draw()
        highest = yAxis.index(max(yAxis))
        days = ["Sunday", "Monday", "Tuesday",
                "Wednesday", "Thursday", "Friday", "Saturday"]
        weekLabel.config(
            text=f"You studied the most on {days[highest]} this week.")


def log(mins):
    x = datetime.now().weekday()
    if x == 6:
        x = 0
    else:
        x += 1
    try:
        if subjectVar.get() == "Select":
            Messagebox.show_error(
                message="Select a subject.")
        else:
            studyData[x][subjectVar.get()] = int(mins)
            logWindow.destroy()
            values = []
            for i in studyData:
                for index, subject in enumerate(i.values()):
                    if len(values) <= index:
                        values.append(subject)
                    else:
                        values[index] = values[index]+subject
            updatePlots()
    except ValueError:
        Messagebox.show_error(message="Enter a number.")


def logDialog():
    global logWindow
    logWindow = Toplevel()
    logWindow.title("Log Activity")
    logWindow.resizable(0, 0)
    logWindow.columnconfigure(0, weight=1)
    logWindow.columnconfigure(1, weight=1)
    entryLabel = Label(logWindow, text="Minutes:")
    entryLabel.grid(row=0, column=0, padx=5, pady=5)
    logEntry = Entry(logWindow, width=10)
    logEntry.grid(row=0, column=1, padx=5, pady=5)
    logDropdownLabel = Label(logWindow, text="Subject:")
    logDropdownLabel.grid(row=1, column=0, padx=5, pady=5)
    logDropdown = OptionMenu(logWindow, subjectVar, *subjectOptions)
    logDropdown.grid(row=1, column=1, padx=5, pady=5)
    logSubmit = Button(logWindow, text="Log",
                       command=lambda: log(logEntry.get()))
    logSubmit.grid(row=2, column=0, columnspan=2)


def setGoals():
    if Messagebox.yesno(message="Are you sure you want to change your goals?"):
        changedSubjects=[]
        for i in goalWindow.winfo_children():
            if isinstance(i, Checkbutton):
                if "selected" in i.state():
                    changedSubjects.append(i.cget("text"))
        global goals
        goals=[]
        for i in goalWindow.winfo_children():
            if isinstance(i, Entry):
                if not i.get()=="":
                    try:
                        goals.append(int(i.get()))
                    except ValueError:
                        goals.append(30)
        if len(goals)==len(changedSubjects):
            for i in studyData:
                for j in changedSubjects:
                    if j not in i:
                        i[j]=0
                for j in list(i.keys()):
                    if j not in changedSubjects:
                        i.pop(j)
            Messagebox.show_warning(message="The app will now close. Reopen for changes to take effect.")
            windowClose()
        else:
            Messagebox.show_error(message="Enter a goal for each checked subject and try again.")
def goalDialog():
    global goalWindow
    global checkMath
    global entryMath
    global checkSocialStudies
    global entrySocialStudies
    global checkEnglish
    global entryEnglish
    global checkSpanish
    global entrySpanish
    global checkFrench
    global entryFrench
    global checkScience
    global entryScience
    goalWindow = Toplevel()
    goalWindow.title("Log Activity")
    goalWindow.resizable(0, 0)
    goalWindow.columnconfigure(0, weight=1)
    goalWindow.columnconfigure(1, weight=1)
    checkMath=Checkbutton(goalWindow, text="Math")
    checkMath.state(["!alternate"])
    checkMath.grid(row=0, column=0, padx=5, pady=5)
    entryMath=Entry(goalWindow, width=10)
    entryMath.grid(row=0, column=1, padx=5, pady=5)
    checkSocialStudies=Checkbutton(goalWindow, text="Social Studies")
    checkSocialStudies.state(["!alternate"])
    checkSocialStudies.grid(row=1, column=0, padx=5, pady=5)
    entrySocialStudies=Entry(goalWindow, width=10)
    entrySocialStudies.grid(row=1, column=1, padx=5, pady=5)
    checkEnglish=Checkbutton(goalWindow, text="English")
    checkEnglish.state(["!alternate"])
    checkEnglish.grid(row=2, column=0, padx=5, pady=5)
    entryEnglish=Entry(goalWindow, width=10)
    entryEnglish.grid(row=2, column=1, padx=5, pady=5)
    checkSpanish=Checkbutton(goalWindow, text="Spanish")
    checkSpanish.state(["!alternate"])
    checkSpanish.grid(row=3, column=0, padx=5, pady=5)
    entrySpanish=Entry(goalWindow, width=10)
    entrySpanish.grid(row=3, column=1, padx=5, pady=5)
    checkFrench=Checkbutton(goalWindow, text="French")
    checkFrench.state(["!alternate"])
    checkFrench.grid(row=4, column=0, padx=5, pady=5)
    entryFrench=Entry(goalWindow, width=10)
    entryFrench.grid(row=4, column=1, padx=5, pady=5)
    checkScience=Checkbutton(goalWindow, text="Science")
    checkScience.state(["!alternate"])
    checkScience.grid(row=5, column=0, padx=5, pady=5)
    entryScience=Entry(goalWindow, width=10)
    entryScience.grid(row=5, column=1, padx=5, pady=5)
    goalLabel=Label(goalWindow, text="List of common subjects is U.S. based")
    goalLabel.grid(row=6, column=0, columnspan=2, padx=5, pady=5)
    goalButton=Button(goalWindow, text="Change", command=setGoals)
    goalButton.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

try:
    file = open("list.txt", "r", encoding="utf-8")
    toDoList = []
    for i in file.read().split("&newTask;"):
        toDoList.append(i)
except OSError:
    toDoList = []
try:
    file = open("study_data.txt", "r", encoding="utf-8")
    studyData = []
    for i in file.read().split("&newDay;"):
        if not i == "":
            dayDictionary = {}
            for j in i.split("&newSubject;"):
                if not j == "":
                    is_subject = True
                    for k in j.split("&Minutes;"):
                        if is_subject:
                            subject = k
                            is_subject = False
                        else:
                            minutes = k
                    dayDictionary[subject] = int(minutes)
            studyData.append(dayDictionary)
    if len(studyData) == 0:
        raise Exception()
except:
    studyData = []
    for i in range(7):
        studyData.append({"Math": 0, "Social Studies": 0, "English": 0})
subjects = []
subjectOptions=["Select"]
dropdownOptions = ["Overall", "Overall"]
for i in studyData[0]:
    dropdownOptions.append(i)
    subjects.append(i)
    subjectOptions.append(i)
try:
    file = open("week.txt", "r")
    if not datetime.now().strftime("%V") == file.read() and not file.read() == "":
        for i in studyData:
            for j in i:
                i[j] = 0
except OSError:
    pass
try:
    file = open("goals.txt", "r")
    goals = [int(i) for i in file.read().split(" ")]
except:
    goals = []
    for i in enumerate(studyData[0]):
        goals.append(30)
values = []
for i in studyData:
    for index, subject in enumerate(i.values()):
        if len(values) <= index:
            values.append(subject)
        else:
            values[index] = values[index]+subject
window = tk.Tk()
if platform.system()=="darwin":
    window.tk.call("tk", "scaling", 1.0)
window.title("Study Planner")
window.resizable(0, 0)
window.protocol("WM_DELETE_WINDOW", windowClose)
dropdownVar = StringVar(window, value="Overall")
subjectVar = StringVar(window, value="Select")
notebook = Notebook(window)

# The "To Do" tab.
toDo = tk.Frame(notebook, padx=20)
toDo.columnconfigure(index=0, weight=1)
toDo.columnconfigure(index=3, weight=1)
toDoLabel = Label(toDo, text="To Do", font="TkDefaultFont 24 bold")
toDoLabel.grid(row=0, column=1, columnspan=2)
toDoEntry = Entry(toDo)
toDoEntry.grid(row=1, column=1, padx=5)
toDoButton = Button(toDo, text="Add Task", command=addTask)
toDoButton.grid(row=1, column=2, padx=5)
toDoLabelFrame = LabelFrame(toDo, text="Tasks")
toDoLabelFrame.grid(row=2, column=1, columnspan=2)
toDoCanvas = tk.Canvas(toDoLabelFrame)
toDoCanvas.pack(side="left", fill="both", expand=1)
toDoCanvasScrollbar = Scrollbar(toDoLabelFrame, command=toDoCanvas.yview)
toDoCanvasScrollbar.pack(side="right", fill="y")
toDoCanvasFrame = Frame(toDoCanvas, height=300, width=500)
toDoCanvas.create_window((0, 0), window=toDoCanvasFrame, anchor="nw")

listRefreshButton = Button(
    toDo, text="Refresh", command=refreshList, bootstyle="outline")
listRefreshButton.grid(row=3, column=1, columnspan=2, pady=10)

# The "Study" tab.
study = tk.Frame(notebook)
studyCanvas = tk.Canvas(study)
studyCanvas.pack(side="left", fill="both", expand=1)
studyCanvasScrollbar = Scrollbar(study, command=studyCanvas.yview)
studyCanvasScrollbar.pack(side="right", fill="y")
studyCanvasFrame = Frame(studyCanvas)
studyCanvas.create_window((0, 0), window=studyCanvasFrame, anchor="nw")
progressFrame = LabelFrame(studyCanvasFrame, text="Progress")
progressFrame.pack()
selectionFrame = Frame(progressFrame)
selectionFrame.pack(fill="x")
dropdown = OptionMenu(selectionFrame, dropdownVar, *dropdownOptions, command=updateMeter)
dropdown.pack(side="right", padx=10, pady=10)
dropdownLabel = Label(selectionFrame, text="Select a subject:")
dropdownLabel.pack(side="right", padx=10, pady=10)
dropdownSeparator = Separator(progressFrame)
dropdownSeparator.pack(fill="x")
progressMeter = Meter(progressFrame, metertype="semi", textright="%")
progressMeter.pack(side="left", padx=10, pady=10)
progressLabel = Label(
    progressFrame, text="You have studied 120 minutes this week.", wraplength=250)
progressLabel.pack(padx=20, pady=20)
statsFrame = LabelFrame(studyCanvasFrame, text="Stats")
statsFrame.pack()
fig, ax = plt.subplots(figsize=(2, 2))
pie = FigureCanvasTkAgg(fig, master=statsFrame)
pie.get_tk_widget().grid(row=0, column=0)
ax.pie([1, 1, 1], autopct="%1.1f%%")
pie.draw()
statsLabel = Label(
    statsFrame, text="You have mostly studied math (blue) this week.", wraplength=250)
statsLabel.grid(row=0, column=1, padx=20, pady=20, sticky="nw")
statsSeparator = Separator(statsFrame)
statsSeparator.grid(row=1, column=0, columnspan=2, sticky="ew")
xAxis = ["Su", "M", "T", "W", "Th", "F", "S"]
yAxis = [0, 0, 0, 0, 0, 0, 0]
fig2, ax2 = plt.subplots(figsize=(2, 2))
week = FigureCanvasTkAgg(fig2, master=statsFrame)
week.get_tk_widget().grid(row=2, column=0)
ax2.bar(xAxis, yAxis)
week.draw()
weekLabel = Label(
    statsFrame, text="You studied the most on Tuesday.", wraplength=250)
weekLabel.grid(row=2, column=1, padx=20, pady=20, sticky="nw")
optionsFrame = Frame(studyCanvasFrame)
optionsFrame.pack()
logButton = Button(optionsFrame, text="Log Activity", command=logDialog)
logButton.pack(side="left", padx=5, pady=10)
setButton = Button(optionsFrame, text="Change Weekly Goals", bootstyle="light", command=goalDialog)
setButton.pack(padx=5, pady=10)

refreshList()
updatePlots()
toDoCanvas.config(yscrollcommand=toDoCanvasScrollbar.set)
toDoCanvasFrame.bind("<Configure>", lambda event: toDoCanvas.configure(
    scrollregion=toDoCanvas.bbox("all")))
studyCanvas.config(yscrollcommand=studyCanvasScrollbar.set)
studyCanvasFrame.bind("<Configure>", lambda event: studyCanvas.configure(
    scrollregion=studyCanvas.bbox("all")))
notebook.add(toDo, text="To Do")
notebook.add(study, text="Study")
notebook.pack(expand=True, fill="both")

window.mainloop()
