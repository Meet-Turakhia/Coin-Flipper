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
import pygame


root = tkinter.Tk()
var = tkinter.IntVar()
conn = sqlite3.connect("coin_flipper.db")
conn.execute("CREATE TABLE IF NOT EXISTS settings (id INTEGER PRIMARY KEY AUTOINCREMENT, money INT DEFAULT 1000 NOT NULL, goal INT DEFAULT 10000 NOT NULL, game_time INT DEFAULT 300 NOT NULL, devil_bias INT DEFAULT 50 NOT NULL, date_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP);")
conn.execute("CREATE TABLE IF NOT EXISTS leaderboard (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(255) UNIQUE DEFAULT 'Unknown' NOT NULL, money INT NOT NULL, goal INT NOT NULL, game_time INT NOT NULL, devil_bias INT NOT NULL,  date_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP);")


baseAnimation = "images/giphy.gif"
baseInfo = Image.open(baseAnimation)
baseFrameCnt = baseInfo.n_frames
baseFrames = [PhotoImage(file=baseAnimation, format='gif -index %i' % (i))
              for i in range(baseFrameCnt)]

file = baseAnimation
info = baseInfo
frameCnt = baseFrameCnt
frames = baseFrames
runCountdown = True


global name, money, goal, game_time, devil_bias


firstiterate = True


def show_leaderboard():
    conn = sqlite3.connect("coin_flipper.db")
    top2 = Toplevel(root)
    top2.geometry("500x500")
    top2.title("LeaderBoard 🥇")
    top2.configure(background="royalblue3")
    top2.iconphoto(False, coinFlipIcon)

    top2LeaderboardLabel = Label(
        top2, text="LeaderBoard", font=("Century", 15), bg="royalblue3", fg="goldenrod2")
    top2TextMessage = st.ScrolledText(top2, height=15.5, width=35, font=(
        "Century", 15), bg="royalblue3", fg="goldenrod2")

    allPlayers = conn.execute(
        "SELECT * FROM leaderboard ORDER BY money DESC, game_time ASC")
    leaderboardInfo = []
    leaderboardInfo.append("NAME MONEY GOAL TIME BIAS")
    for player in allPlayers:
        rowName = player[1]
        rowMoney = player[2]
        rowGoal = player[3]
        rowGame_time = player[4]
        rowDevil_bias = player[5]
        allPlayerInfo = rowName + " " + \
            str(rowMoney) + " " + str(rowGoal) + " " + \
            str(rowGame_time) + " " + str(rowDevil_bias)
        leaderboardInfo.append(allPlayerInfo)
    top2TextMessage["state"] = "normal"
    top2TextMessage.delete("1.0", "end")
    top2TextMessage["state"] = "disabled"
    top2LeaderboardLabel.place(x=200, y=25)
    for record in leaderboardInfo:
        top2TextMessage.configure(state="normal")
        top2TextMessage.insert(END, record + "\n")
        top2TextMessage.place(x=47, y=85)
        top2TextMessage.see("end")
        top2TextMessage.configure(state="disabled")
        root.update()


def clear_leaderboard():
    try:
        conn = sqlite3.connect("coin_flipper.db")
        confirm = messagebox.askyesno("Delete All Leaderboard Records", "Are you sure you want to delete all leaderboard records permanently?")
        if confirm:
            conn.execute("DELETE FROM leaderboard")
            conn.commit()
    except:
        messagebox.showerror("Clear LeaderBoard Error!", "There was an error while clearing the leaderboard try again!")


def start_game():
    try:
        try:
            options_menu.entryconfig("Settings ⚙", state="disabled")
            options_menu.entryconfig("Play/Restart 🎮", state="disabled")
            options_menu.entryconfig("Quit 🏳", state="disabled")
        except:
            pass
        coinFlipLabel.place(x=80, y=0)
        conn = sqlite3.connect("coin_flipper.db")
        global name, money, goal, game_time, devil_bias, runCountdown

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
        runCountdown = True

        leaderboardLabel.place_forget()
        textMessage.place_forget()
        startButton.place_forget()
        devilButton.place_forget()
        luckyButton.place_forget()
        entryWidget.place_forget()
        moneyLabel.place_forget()
        goalLabel.place_forget()
        resultLabel.place_forget()
        playerLabel.place_forget()
        gameTimeLabel.place_forget()
        root.update()

        nameLabel.place(x=120, y=450)
        nameInput.place(x=257, y=454)
        rootEntryButton.place(x=455, y=453)
        root.update()

        rootEntryButton.wait_variable(var)

        name = nameInput.get()
        nameLabel.place_forget()
        nameInput.place_forget()
        rootEntryButton.place_forget()
        root.update()

        moneyLabel["text"] = moneyLabel["text"].split(": ")[0]
        moneyLabel["text"] = moneyLabel["text"] + ": " + str(money)

        goalLabel["text"] = goalLabel["text"].split(": ")[0]
        goalLabel["text"] = goalLabel["text"] + ": " + str(goal)

        playerLabel["text"] = playerLabel["text"].split(": ")[0]
        playerLabel["text"] = playerLabel["text"] + ": " + str(name)


        devilButton.place(x=135, y=450)
        luckyButton.place(x=430, y=450)
        entryWidget.place(x=227, y=457)
        moneyLabel.place(x=455, y=10)
        goalLabel.place(x=455, y=40)
        resultLabel.place(x=280, y=400)
        playerLabel.place(x=10, y=10)
        gameTimeLabel.place(x=10, y=40)
        root.update()

        gameTimeLabel["text"] = "Time: "
        threading.Thread(target = countdown).start()
        try:
            options_menu.entryconfig("Settings ⚙", state="normal")
            options_menu.entryconfig("Quit 🏳", state="normal")
        except:
            pass
    except:
        messagebox.showerror("Game Start/Restart Error!", "There was an error while starting the game")


def game_over():
    try:
        try:
            options_menu.entryconfig("Quit 🏳", state="disabled")
            options_menu.entryconfig("Settings ⚙", state="normal")
            options_menu.entryconfig("Play/Restart 🎮", state="normal")
        except:
            pass
        global runCountdown
        runCountdown = False
        conn = sqlite3.connect("coin_flipper.db")
        playerLabel.place_forget()
        gameTimeLabel.place_forget()
        moneyLabel.place_forget()
        goalLabel.place_forget()
        coinFlipLabel.place_forget()
        devilButton.place_forget()
        luckyButton.place_forget()
        entryWidget.place_forget()

        nameLabel.place_forget()
        nameInput.place_forget()
        rootEntryButton.place_forget()

        root.update()

        players = conn.execute(
            "SELECT COUNT(*) FROM leaderboard WHERE name = (?)", (name,))
        settingsList = conn.execute("SELECT * FROM settings WHERE id = (?)", (1,))
        for setting in settingsList:
            totalTime = setting[3]
        timeTaken = totalTime - game_time
        for player in players:
            count = player[0]
        if count == 0:
            conn.execute(
                "INSERT INTO leaderboard (name, money, goal, game_time, devil_bias) VALUES ((?), (?), (?), (?), (?))", (name, money, goal, timeTaken, devil_bias,))
            conn.commit()
        else:
            historicPlayerInfoList = conn.execute("SELECT * FROM leaderboard WHERE name = (?)", (name,))
            for historicalPlayerInfo in historicPlayerInfoList:
                historicMoney = historicalPlayerInfo[2]
            if historicMoney < money:
                conn.execute(
                    "UPDATE leaderboard SET money = (?), goal = (?), game_time = (?), devil_bias = (?) WHERE name = (?)", (money, goal, timeTaken, devil_bias, "Meet",))
                conn.commit()
        allPlayers = conn.execute(
            "SELECT * FROM leaderboard ORDER BY money DESC, game_time ASC")
        leaderboardInfo = []
        leaderboardInfo.append("NAME MONEY GOAL TIME BIAS")
        for player in allPlayers:
            rowName = player[1]
            rowMoney = player[2]
            rowGoal = player[3]
            rowGame_time = player[4]
            rowDevil_bias = player[5]
            allPlayerInfo = rowName + " " + \
                str(rowMoney) + " " + str(rowGoal) + " " + \
                str(rowGame_time) + " " + str(rowDevil_bias)
            leaderboardInfo.append(allPlayerInfo)
        textMessage["state"] = "normal"
        textMessage.delete("1.0", "end")
        textMessage["state"] = "disabled"
        leaderboardLabel.place(x=260, y=60)
        for record in leaderboardInfo:
            textMessage.configure(state="normal")
            textMessage.insert(END, record + "\n")
            textMessage.place(x=125, y=110)
            textMessage.see("end")
            textMessage.configure(state="disabled")
            root.update()
    except:
        messagebox.showerror("Game Over Error!", "Could'nt finish and summarise your game, please try again!")


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
        root.update()

        entryButton.wait_variable(var)

        money = int(inputMoney.get())
        goal = int(inputGoal.get())
        game_time = int(inputTime.get())
        devil_bias = int(inputBias.get())

        conn.execute("UPDATE settings SET money = (?), goal = (?), game_time = (?), devil_bias = (?) WHERE id = (?)",
                     (money, goal, game_time, devil_bias, 1))
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
        root.update()

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
        global firstiterate, after, frames, frameCnt, money, devil_bias

        devilButton["state"] = "disabled"
        luckyButton["state"] = "disabled"
        resultLabel["text"] = ""
        root.update()

        bet = entryWidget.get()
        moneyUpdate = True
        if bet.isdigit():
            bet = int(bet)
            if bet > money:
                messagebox.showerror(
                    "Insufficinet Balance!", "You have insufficient balance to place this bet, try again!")
                devilButton["state"] = "normal"
                luckyButton["state"] = "normal"
                root.update()
                return
        else:
            moneyUpdate = False

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

        tempDevil_bias = devil_bias / 100
        if randomNum < tempDevil_bias:
            file = "images/devil.gif"
            resultLabel["text"] = "You Won!"
            if moneyUpdate:
                money = money + bet
                moneyLabel["text"] = moneyLabel["text"].split(": ")[0]
                moneyLabel["text"] = moneyLabel["text"] + ": " + str(money)
                pygame.mixer.Channel(0).play(
                    pygame.mixer.Sound('music/win.wav'))
                root.update()

        if randomNum >= tempDevil_bias:
            file = "images/lucky.gif"
            resultLabel["text"] = "You Lose!"
            if moneyUpdate:
                money = money - bet
                moneyLabel["text"] = moneyLabel["text"].split(": ")[0]
                moneyLabel["text"] = moneyLabel["text"] + ": " + str(money)
                pygame.mixer.Channel(0).play(
                    pygame.mixer.Sound('music/lose.wav'))
                root.update()

        info = Image.open(file)
        frameCnt = info.n_frames
        frames = [PhotoImage(file=file, format='gif -index %i' % (i))
                  for i in range(frameCnt)]
        update(0, False)
        firstiterate = False
        if money == goal:
            messagebox.showinfo("Congratulations!",
                                "You have completed the goal, congratulations, you can keep on playing but quit from options when done to record your data and see where you stand on leaderboard!")
            # game_over()
        if money <= 0:
            messagebox.showerror(
                "Game Over", "You are out of money and hence game is over, try again :( ")
            game_over()
        devilButton["state"] = "normal"
        luckyButton["state"] = "normal"
        root.update()

    except:
        devilButton["state"] = "normal"
        luckyButton["state"] = "normal"
        root.update()
        messagebox.showerror("Toss error occured!",
                             "Error occured while tossing the coin, try again!")


def lucky():
    try:
        global firstiterate, after, frames, frameCnt, money, devil_bias

        devilButton["state"] = "disabled"
        luckyButton["state"] = "disabled"
        resultLabel["text"] = ""
        root.update()

        bet = entryWidget.get()
        moneyUpdate = True
        if bet.isdigit():
            bet = int(bet)
            if bet > money:
                messagebox.showerror(
                    "Insufficinet Balance!", "You have insufficient balance to place this bet, try again!")
                devilButton["state"] = "normal"
                luckyButton["state"] = "normal"
                root.update()
                return
        else:
            moneyUpdate = False

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
            if bet > money:
                messagebox.showerror(
                    "Insufficinet Balance!", "You have insufficient balance to place this bet, try again!")
                return
        else:
            moneyUpdate = False

        tempDevil_bias = devil_bias / 100
        if randomNum < tempDevil_bias:
            file = "images/devil.gif"
            resultLabel["text"] = "You Lose!"
            if moneyUpdate:
                money = money - bet
                moneyLabel["text"] = moneyLabel["text"].split(": ")[0]
                moneyLabel["text"] = moneyLabel["text"] + ": " + str(money)
                pygame.mixer.Channel(0).play(
                    pygame.mixer.Sound('music/lose.wav'))
                root.update()

        if randomNum >= tempDevil_bias:
            file = "images/lucky.gif"
            resultLabel["text"] = "You Won!"
            if moneyUpdate:
                money = money + bet
                moneyLabel["text"] = moneyLabel["text"].split(": ")[0]
                moneyLabel["text"] = moneyLabel["text"] + ": " + str(money)
                pygame.mixer.Channel(0).play(
                    pygame.mixer.Sound('music/win.wav'))
                root.update()

        info = Image.open(file)
        frameCnt = info.n_frames
        frames = [PhotoImage(file=file, format='gif -index %i' % (i))
                  for i in range(frameCnt)]
        update(0, False)
        firstiterate = False
        if money == goal:
           messagebox.showinfo("Congratulations!",
                               "You have completed the goal, congratulations, you can keep on playing but quit from options when done to record your data and see where you stand on leaderboard!")
           # game_over()
        if money <= 0:
            messagebox.showerror(
                "Game Over", "You are out of money and hence game is over, try again :( ")
            game_over()
        devilButton["state"] = "normal"
        luckyButton["state"] = "normal"
        root.update()

    except:
        devilButton["state"] = "normal"
        luckyButton["state"] = "normal"
        root.update()
        messagebox.showerror("Toss error occured!",
                             "Error occured while tossing the coin, try again!")


def update(ind, fastSpin):
    try:
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
    except:
        messagebox.showerror("Coin Animation Error!", "There was an error while displaying coin animation!")


def countdown():
    try:
        global game_time, runCountdown
        while game_time:
            mins, secs = divmod(game_time, 60)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            gameTimeLabel["text"] = gameTimeLabel["text"].split(": ")[0]
            gameTimeLabel["text"] = gameTimeLabel["text"] + ": " + timer
            root.update()
            time.sleep(1)
            game_time -= 1
            if not runCountdown:
                return
        if runCountdown:
            messagebox.showinfo(
            "Time is Up!", "The game time is over, quit from options when you feel, to record your data and see where you stand on leaderboard!")
            # game_over()
    except:
        messagebox.showerror("Count Down Error!", "There was an error while displaying countdown!")


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
startButton = Button(root, text="Start Game!", command=lambda: threading.Thread(
    target=start_game).start(), font=('Century', 15), cursor='hand2', background="gold2", foreground="orange3")
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
rootEntryButton = Button(root, text="Enter!", command=lambda: var.set(1), font=(
    'Century', 10), cursor='hand2', bg="gold2", fg="orange3")
leaderboardLabel = Label(
    root, text="LeaderBoard", font=("Century", 15), bg="royalblue3", fg="goldenrod2")
textMessage = st.ScrolledText(root, height=15.5, width=35, font=(
    "Century", 15), bg="royalblue3", fg="goldenrod2")
nameLabel = Label(
    root, text="Enter Name: ", font=("Century", 15), bg="royalblue3", fg="goldenrod2")
nameInput = Entry(root, bg="goldenrod2", fg="blue", font=("Century", 12))


# create menu
my_menu = Menu(root)
root.config(menu=my_menu)

# create options menu
options_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Options 🛠", menu=options_menu)
options_menu.add_command(label="Play/Restart 🎮", command=lambda: threading.Thread(
    target=start_game).start())
options_menu.add_command(label="Settings ⚙", command=lambda: threading.Thread(
    target=settings).start())
options_menu.add_command(label="Show LeaderBoard 🥇", command=lambda: threading.Thread(
    target=show_leaderboard).start())
options_menu.add_command(label="Clear LeaderBoard‼", command=lambda: threading.Thread(
    target=clear_leaderboard).start())
options_menu.add_command(label="Quit 🏳", command=lambda: threading.Thread(
            target=game_over).start())
options_menu.entryconfig("Settings ⚙", state="disabled")
options_menu.entryconfig("Play/Restart 🎮", state="disabled")
options_menu.entryconfig("Quit 🏳", state="disabled")


titleLabel.place(x=245, y=10)
meshIconLabel.place(x=590, y=460)
startButton.place(x=250, y=450)
# devilButton.place(x=135, y=450)
# luckyButton.place(x=430, y=450)
# entryWidget.place(x=227, y=457)
moneyLabel.place(x=455, y=10)
goalLabel.place(x=455, y=40)
resultLabel.place(x=280, y=400)
playerLabel.place(x=10, y=10)
gameTimeLabel.place(x=10, y=40)
update(0, False)
root.iconphoto(False, coinFlipIcon)

pygame.mixer.init()
pygame.mixer.music.load('music/background.mp3')
pygame.mixer.music.play(-1)

root.mainloop()
