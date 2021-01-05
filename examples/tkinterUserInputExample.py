import tkinter as tk

def keyPress(event):
    print(event)
    if event.keysym == 'Return':
        root.destroy()
        print('Stopping test')

def keyRelease(event):
    print(event)

def getUserInput():
    root = tk.Tk()
    frame = tk.Frame(root, width= 1, height= 1)
    frame.bind("<KeyPress>", keyPress)
    frame.bind("<KeyRelease>", keyRelease)
    frame.pack()
    frame.focus_set()
    root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    frame = tk.Frame(root, width= 1, height= 1)
    frame.bind("<KeyPress>", keyPress)
    frame.bind("<KeyRelease>", keyRelease)
    frame.pack()
    frame.focus_set()
    root.mainloop()