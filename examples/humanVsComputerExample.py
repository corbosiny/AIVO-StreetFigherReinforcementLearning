import retro
import tkinter as tk
import time
import threading

FRAME_RATE = 1.0 / 115.0                # How fast the user input is sampled

userInput = [0] * 12                    # Global variable to store the current user input
lock = threading.Lock()                 # Lock to eliminate race conditions when updating userInput
readyForInputEvent = threading.Event()  # Event flag to signal the input thread on when new user input is requested

# Mappings of keys to what index they are inside the input vector
Z_INDEX = 1
X_INDEX = 0
C_INDEX = 8
A_INDEX  = 10
S_INDEX = 9
D_INDEX = 11
UP_INDEX = 4
DOWN_INDEX = 5
LEFT_INDEX = 6
RIGHT_INDEX = 7       
keyToIndexDict = {'z' : Z_INDEX, 'x' : X_INDEX , 'c' : C_INDEX, 'a' : A_INDEX, 's' : S_INDEX, 'd' : D_INDEX, 'Left' : LEFT_INDEX, "Right" : RIGHT_INDEX, "Up" : UP_INDEX, "Down" : DOWN_INDEX}

def sampleUserInput():
    """Returns the current user input on the keyboard"""
    readyForInputEvent.set()
    time.sleep(FRAME_RATE)
    readyForInputEvent.clear()
    return userInput

def clearUserInputIndex(index):
    updateUserInputIndex(index, 0)

def setUserInputIndex(index):
    updateUserInputIndex(index, 1)

def updateUserInputIndex(index, value):
    if index < 0 or index >= len(userInput):
        return
    
    readyForInputEvent.wait()
    lock.acquire()
    userInput[index] = value
    lock.release()

def keyPressed(event):
    try:
        index = keyToIndexDict[event.keysym]
        setUserInputIndex(index)
    except:
        pass # Not a valid game input, just ignore

def keyReleased(event):
    try:
        index = keyToIndexDict[event.keysym]
        clearUserInputIndex(index)
    except:
        pass

def bindKeyEvents(frame):
    frame.bind("<KeyPress>", keyPressed)
    frame.bind("<KeyRelease>", keyReleased)
    return frame

def monitorUserInput():
    root = tk.Tk()
    frame = tk.Frame(root, width = 1, height = 1)
    frame = bindKeyEvents(frame)
    frame.pack()
    frame.focus_set()
    root.mainloop()

def main(game= 'StreetFighterIISpecialChampionEdition-Genesis',  state= "chunli"):
    """Repeatdely runs through games with the human as ryu vs chunli"""
    env = retro.make(game= game, state= state, players= 2)
    env.reset()
    env.render()
    thread = threading.Thread(target= monitorUserInput)
    thread.start()
    while True:
        aiAction = env.action_space.sample()
        playerAction = sampleUserInput()
        action = playerAction + list(aiAction[12:])
        _, _, done, _ = env.step(action)
        env.render()
        if done: env.reset()
    env.close()

if __name__ == "__main__":
    main()
