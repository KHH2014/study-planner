def addTask(x):
    try:
        file=open("list.txt", "x")
    except:
        file=open("list.txt", "a")
    file.write(x+"&newTask;")
    file.close()