import tkinter
from tkinter import *
from tkinter import messagebox, ttk
import threading
from PIL import Image
import time
import random
from time import strftime
import sqlite3
from tkinter import scrolledtext as st


root = tkinter.Tk()
var = tkinter.IntVar()
conn = sqlite3.connect("coin_flipper.db")
conn.execute("CREATE TABLE IF NOT EXISTS settings (id INTEGER PRIMARY KEY AUTOINCREMENT, money INT DEFAULT 1000 NOT NULL, goal INT DEFAULT 10000 NOT NULL, game_time INT DEFAULT 300 NOT NULL, devil_bias INT DEFAULT 50 NOT NULL, date_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP);")
conn.execute("CREATE TABLE IF NOT EXISTS leaderboard (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(255) UNIQUE NOT NULL, money INT NOT NULL, goal INT NOT NULL, game_time INT NOT NULL, devil_bias INT NOT NULL,  date_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP);")


baseAnimation = "images/giphy.gif"
baseInfo = Image.open(baseAnimation)
baseFrameCnt = baseInfo.n_frames
baseFrames = [PhotoImage(file=baseAnimation, format='gif -index %i' % (i))
              for i in range(baseFrameCnt)]

file = baseAnimation
info = baseInfo
frameCnt = baseFrameCnt
frames = baseFrames

countList = conn.execute("SELECT COUNT(*) FROM settings")
for count in countList:
    rowCount = count[0]
if rowCount > 0:
    rowList = conn.execute("SELECT * FROM settings WHERE id = (?)", (1,))
    for row in rowList:
        money = row[1]
        goal = row[2]
        game_time = row[3]
        devil_bias = row[4]
else:
    money = 1000
    goal = 10000
    game_time = 300
    devil_bias = 50
name = "Meet"


firstiterate = True


def game_over():
    conn = sqlite3.connect("coin_flipper.db")
    playerLabel.place_forget()
    gameTimeLabel.place_forget()
    moneyLabel.place_forget()
    goalLabel.place_forget()
    coinFlipLabel.place_forget()
    devilButton.place_forget()
    luckyButton.place_forget()
    entryWidget.place_forget()
    players = conn.execute("SELECT COUNT(*) FROM leaderboard WHERE name = (?)", (name,))
    for player in players:
        count = player[0]
    if count == 0:
        conn.execute(
            "INSERT INTO leaderboard (name, money, goal, game_time, devil_bias) VALUES ((?), (?), (?), (?), (?))", (name, money, goal, game_time, devil_bias,))
        conn.commit()
    else:
        conn.execute(
            "UPDATE leaderboard SET money = (?), goal = (?), game_time = (?), devil_bias = (?) WHERE name = (?)", (money, goal, game_time, devil_bias, "Meet",))
        conn.commit()
    allPlayers = conn.execute(
        "SELECT * FROM leaderboard ORDER BY money DESC")
    leaderboardInfo = []
    leaderboardInfo.append("NAME MONEY GOAL TIME BIAS")
    for player in allPlayers:
        rowName = player[1]
        rowMoney = player[2]
        rowGoal = player[3]
        rowGame_time = player[4]
        rowDevil_bias = player[5]
        allPlayerInfo = rowName + " " + str(rowMoney) + " " + str(rowGoal) + " " + str(rowGame_time) + " " + str(rowDevil_bias)
        leaderboardInfo.append(allPlayerInfo)
    leaderboardLabel.place(x=260, y=60)
    for record in leaderboardInfo:
        textMessage.configure(state="normal")
        textMessage.insert(END, record + "\n")
        textMessage.place(x=125, y=110)
        textMessage.see("end")
        textMessage.configure(state="disabled")



def settings():
    conn = sqlite3.connect("coin_flipper.db")
    top = Toplevel(root)
    top.geometry("500x500")
    top.title("Settings ⚙")
    top.configure(background="royalblue3")
    top.iconphoto(False, coinFlipIcon)
    inputMoneyLabel = Label(
        top, text="Input Start Money(Numeric Value):", font=("Century", 15), bg="royalblue3", fg="goldenrod2")
    inputGoalLabel = Label(
        top, text="Input Goal(Numeric Value):", font=("Century", 15), bg="royalblue3", fg="goldenrod2")
    inputTimeLabel = Label(
        top, text="Enter Game Time(in seconds):", font=("Century", 15), bg="royalblue3", fg="goldenrod2")
    inputBiasLabel = Label(
        top, text="Enter Devil Bias(in percent):", font=("Century", 15), bg="royalblue3", fg="goldenrod2")
    entryButton = Button(top, text="Enter!", command=lambda: var.set(1), font=(
        'Century', 10), cursor='hand2', bg="gold2", fg="orange3")
    inputMoney = Entry(top, bg="goldenrod2", fg="blue", font=("Century", 12))
    inputGoal = Entry(top, bg="goldenrod2", fg="blue", font=("Century", 12))
    inputTime = Entry(top, bg="goldenrod2", fg="blue", font=("Century", 12))
    inputBias = Entry(top, bg="goldenrod2", fg="blue", font=("Century", 12))

    countList = conn.execute("SELECT COUNT(*) FROM settings")
    for count in countList:
        rowCount = count[0]
    if rowCount > 0:
        rowList = conn.execute("SELECT * FROM settings WHERE id = (?)", (1,))
        for row in rowList:
            money = row[1]
            goal = row[2]
            game_time = row[3]
            devil_bias = row[4]
        inputMoney.insert(END, str(money))
        inputGoal.insert(END, str(goal))
        inputTime.insert(END, str(game_time))
        inputBias.insert(END, str(devil_bias))

        inputMoneyLabel.place(x=80, y=20)
        inputMoney.place(x=160, y=70)
        inputGoalLabel.place(x=120, y=120)
        inputGoal.place(x=160, y=170)
        inputTimeLabel.place(x=120, y=220)
        inputTime.place(x=160, y=270)
        inputBiasLabel.place(x=125, y=320)
        inputBias.place(x=160, y=370)
        entryButton.place(x=220, y=440)

        entryButton.wait_variable(var)

        money = int(inputMoney.get())
        goal = int(inputGoal.get())
        game_time = int(inputTime.get())
        devil_bias = int(inputBias.get())

        conn.execute("UPDATE settings SET money = (?), goal = (?), game_time = (?), devil_bias = (?) WHERE id = (?)", (money, goal, game_time, devil_bias, 1))
        conn.commit()

    else:
        inputMoneyLabel.place(x=80, y=20)
        inputMoney.place(x=160, y=70)
        inputGoalLabel.place(x=120, y=120)
        inputGoal.place(x=160, y=170)
        inputTimeLabel.place(x=120, y=220)
        inputTime.place(x=160, y=270)
        inputBiasLabel.place(x=125, y=320)
        inputBias.place(x=160, y=370)
        entryButton.place(x=220, y=440)

        entryButton.wait_variable(var)

        money = int(inputMoney.get())
        goal = int(inputGoal.get())
        game_time = int(inputTime.get())
        devil_bias = int(inputBias.get())

        conn.execute("INSERT INTO settings (money, goal, game_time, devil_bias) VALUES ((?), (?), (?), (?))",
                     (money, goal, game_time, devil_bias,))
        conn.commit()

    top.destroy()



def callback(input):
    if input.isdigit():
        return True
    elif input == "":
        return True
    else:
        return False


def devil():
    try:
        devilButton["state"] = "disabled"
        luckyButton["state"] = "disabled"
        resultLabel["text"] = ""

        global firstiterate, after, frames, frameCnt, money

        if not firstiterate:
            root.after_cancel(after)
            file = baseAnimation
            info = baseInfo
            frameCnt = baseFrameCnt
            frames = baseFrames
            update(0, False)
        root.after_cancel(after)
        update(0, True)
        time.sleep(3)

        global afterfast

        root.after_cancel(afterfast)
        randomNum = random.random()
        bet = entryWidget.get()
        moneyUpdate = True
        if bet.isdigit():
            bet = int(bet)
        else:
            moneyUpdate = False

        if randomNum > 0.5:
            file = "images/devil.gif"
            resultLabel["text"] = "You Won!"
            if moneyUpdate:
                money = money + bet
                moneyLabel["text"] = moneyLabel["text"].split(": ")[0]
                moneyLabel["text"] = moneyLabel["text"] + ": " + str(money)

        if randomNum <= 0.5:
            file = "images/lucky.gif"
            resultLabel["text"] = "You Lose!"
            if moneyUpdate:
                money = money - bet
                moneyLabel["text"] = moneyLabel["text"].split(": ")[0]
                moneyLabel["text"] = moneyLabel["text"] + ": " + str(money)

        info = Image.open(file)
        frameCnt = info.n_frames
        frames = [PhotoImage(file=file, format='gif -index %i' % (i))
                for i in range(frameCnt)]
        update(0, False)
        firstiterate = False
        devilButton["state"] = "normal"
        luckyButton["state"] = "normal"
        
    except:
        devilButton["state"] = "normal"
        luckyButton["state"] = "normal"
        messagebox.showerror("Toss error occured!", "Error occured while tossing the coin, try again!")


def lucky():
    try:
        devilButton["state"] = "disabled"
        luckyButton["state"] = "disabled"
        resultLabel["text"] = ""

        global firstiterate, after, frames, frameCnt, money

        if not firstiterate:
            root.after_cancel(after)
            file = baseAnimation
            info = baseInfo
            frameCnt = baseFrameCnt
            frames = baseFrames
            update(0, False)
        root.after_cancel(after)
        update(0, True)
        time.sleep(3)

        global afterfast

        root.after_cancel(afterfast)
        randomNum = random.random()
        bet = entryWidget.get()
        moneyUpdate = True
        if bet.isdigit():
            bet = int(bet)
        else:
            moneyUpdate = False

        if randomNum > 0.5:
            file = "images/devil.gif"
            resultLabel["text"] = "You Lose!"
            if moneyUpdate:
                money = money - bet
                moneyLabel["text"] = moneyLabel["text"].split(": ")[0]
                moneyLabel["text"] = moneyLabel["text"] + ": " + str(money)

        if randomNum <= 0.5:
            file = "images/lucky.gif"
            resultLabel["text"] = "You Won!"
            if moneyUpdate:
                money = money + bet
                moneyLabel["text"] = moneyLabel["text"].split(": ")[0]
                moneyLabel["text"] = moneyLabel["text"] + ": " + str(money)

        info = Image.open(file)
        frameCnt = info.n_frames
        frames = [PhotoImage(file=file, format='gif -index %i' % (i))
                for i in range(frameCnt)]
        update(0, False)
        firstiterate = False
        devilButton["state"] = "normal"
        luckyButton["state"] = "normal"

    except:
        devilButton["state"] = "normal"
        luckyButton["state"] = "normal"
        messagebox.showerror("Toss error occured!",
                             "Error occured while tossing the coin, try again!")


def update(ind, fastSpin):
    global after, afterfast

    if ind >= frameCnt:
        ind = 0

    try:
        frame = frames[ind]
    except:
        frame = frames[0]

    ind += 1
    coinFlipLabel.configure(image=frame)

    if fastSpin == False:
        after = root.after(100, update, ind, fastSpin)
    else:
        afterfast = root.after(2, update, ind, fastSpin)


def countdown():
    global game_time
    while game_time:
        mins, secs = divmod(game_time, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        gameTimeLabel["text"] = gameTimeLabel["text"].split(": ")[0]
        gameTimeLabel["text"] = gameTimeLabel["text"] + ": " + timer
        time.sleep(1)
        game_time -= 1
    messagebox.showinfo("Time is Up!", "The game time is over, do check the leaderboard for your score!")
    # game_over()


root.geometry("650x520")
root.title("Coin Flipper")
root.configure(background="royalblue3")
meshIcon = PhotoImage(file="images/meshicon.png")
meshIconLabel = Label(root, image=meshIcon, bg="goldenrod2")
coinFlipIcon = PhotoImage(file="images/lucky.gif")
coinFlipLabel = Label(root, bg="royalblue3")
coinFlipLabel.place(x=80, y=0)
titleLabel = Label(
    root, text="Coin Flipper", font=("Century", 20), bg="royalblue3", fg="goldenrod2")
devilButton = Button(root, text="Devil!", command=lambda: threading.Thread(
    target=devil).start(), font=('Century', 15), cursor='hand2', background="gold2", foreground="orange3")
luckyButton = Button(root, text="Lucky!", command=lambda: threading.Thread(
    target=lucky).start(), font=('Century', 15), cursor='hand2', background="gold2", foreground="orange3")
moneyLabel = Label(
    root, text="Money: ", font=("Century", 15), bg="royalblue3", fg="goldenrod2")
goalLabel = Label(
    root, text="Goal: ", font=("Century", 15), bg="royalblue3", fg="goldenrod2")
playerLabel = Label(
    root, text="Player: ", font=("Century", 15), bg="royalblue3", fg="goldenrod2")
gameTimeLabel = Label(
    root, text="Time: ", font=("Century", 15), bg="royalblue3", fg="goldenrod2")
resultLabel = Label(
    root, text="", font=("Century", 15), bg="royalblue3", fg="goldenrod2")
entryWidget = Entry(root, bg="goldenrod2", fg="blue", font=("Century", 12))
reg = root.register(callback)
entryWidget.config(validate="key",
             validatecommand=(reg, '%P'))
entryButton = Button(root, text="Enter!", command=lambda: var.set(1), font=(
    'Century', 10), cursor='hand2', bg="gold2", fg="orange3")
leaderboardLabel = Label(
    root, text="LeaderBoard", font=("Century", 15), bg="royalblue3", fg="goldenrod2")
textMessage = st.ScrolledText(root, height=15.5, width=35, font=(
    "Century", 15), bg="royalblue3", fg="goldenrod2")


# create menu
my_menu = Menu(root)
root.config(menu=my_menu)

# create options menu
options_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Options 🛠", menu=options_menu)
options_menu.add_command(label="Play/Replay 🎮", command=lambda: threading.Thread(
    target=game_over).start())
options_menu.add_command(label="settings ⚙", command = lambda: threading.Thread(
    target=settings).start())
options_menu.add_command(label="Quit 🏳", command=lambda: threading.Thread(
    target=game_over).start())

moneyLabel["text"] = moneyLabel["text"].split(": ")[0]
moneyLabel["text"] = moneyLabel["text"] + ": " + str(money)

goalLabel["text"] = goalLabel["text"].split(": ")[0]
goalLabel["text"] = goalLabel["text"] + ": " + str(goal)

titleLabel.place(x=245, y=10)
devilButton.place(x=135, y=450)
luckyButton.place(x=430, y=450)
entryWidget.place(x=227, y=457)
moneyLabel.place(x=455, y=10)
goalLabel.place(x=455, y=40)
resultLabel.place(x=280, y=400)
playerLabel.place(x=10, y=10)
gameTimeLabel.place(x=10, y=40)
update(0, False)
root.iconphoto(False, coinFlipIcon)
threading.Thread(target = countdown).start()
root.mainloop()
