from Tkinter import *
from random import shuffle
from math import *

class Data:
    """Class that holds all the data for the bracket"""
    def __init__(self):
        self.players = []
        self.pairings = {}

    def add_player(self, name):
        self.players.append(Player(name))

    def number_players(self):
        return len(self.players)

    def group_by_record(self, players):
        """creates dictionary that groups players by their relative scores"""
        self.group = {}
        for player in players:
            score = player.wins + player.draws / 2
            self.group[(score, player.byes)] = \
                self.group.get((score, player.byes), []) + [player, ]
        return self.group
    def least_byes(self):
        """creates list of players that have least amount of byes"""
        temp_players = self.players[:]
        temp_players.sort(key=lambda x: x.byes)
        for i in range(len(temp_players) - 1):
            if temp_players[i].byes < temp_players[i + 1].byes:
                return temp_players[:i + 1]
        return []

class Player:
    """Wrapper for any data for a player"""
    def __init__(self, name):
        self.name = name
        self.wins, self.losses, self.draws, self.byes = 0, 0, 0, 0
        
    def __str__(self):
        return "{0}\n{1}:{2}:{3}\n{4} byes".format(self.name, \
                                                   self.wins, self.losses,
                                                   self.draws, self.byes)

class GUI:
    """GUI code"""
    def __init__(self, master):
        self.player_input(master)
        self.enter_frame.pack()

    def player_input(self, master):
        """Allows initialization of players"""
        self.enter_frame = Frame(master)
        self.enter_field = Entry(self.enter_frame)
        
        self.enter_button = Button(self.enter_frame,
                                   text="ADD PLAYER 1",
                                   command=lambda: self.add_player( \
                                       self.enter_field, self.enter_button))
        self.finish_button = Button(self.enter_frame,
                                    text="DONE",
                                    command=lambda: self.init_seating(master))

        self.quit_button = Button(self.enter_frame,
                                  text="QUIT",
                                  command=q)
        master.bind('<Return>', self.enter_button["command"])
        
        self.enter_field.pack()
        self.enter_button.pack()
        self.finish_button.pack()
        self.quit_button.pack()

    def init_seating(self, master):
        """Seats all players at table for draft positions"""
        #destroy previous frames
        self.enter_frame.pack_forget()
        self.enter_frame.destroy()
        
        self.table = Frame(master, height=700, width=600)
        self.table.pack_propagate(0)
        self.canvas = Canvas(self.table, width=600, height=600)
        self.order = data.players[:]
        shuffle(self.order)

        draw_oval_center(300, 300, 250, "brown")
        for i in range(len(self.order)):
            x = 300 + 200 * cos(2 * pi * i / len(self.order))
            y = 300 + 200 * sin(2 * pi * i / len(self.order))
            draw_oval_center(x, y, 50, "green")
            new_text = Label(self.table, text=str(self.order[i]))
            new_text.place(x=x-40, y=y-20)
        self.canvas.pack()

        self.quit_button = Button(self.table,
                                  text="QUIT",
                                  command=q)
        self.pairings_button = Button(self.table,
                                      text="CREATE PAIRINGS",
                                      command=lambda: self.first_pairings(master))
        master.bind('<Return>', self.pairings_button["command"])
        self.quit_button.pack()
        self.pairings_button.pack()
        self.table.pack()

    def create_pairings(self, master):
        """Generates pairings for games"""
        bye_player = None
        if data.pairings == {}:
            order = data.players[:]
            shuffle(order)
            while len(order) > 0:
                if len(order) == 1:
                    bye_player = order[0]
                    bye_player.byes += 1
                    order.pop()
                else:
                    data.pairings[order[0]] = order[1]
                    order = order[2:]
        else:
            data.pairings = {}
            players = data.players[:]
            if data.number_players() % 2 == 1:
                temp = data.least_byes()
                if temp:
                    shuffle(temp)
                    bye_player = temp.pop()
                    bye_player.byes += 1
                    players.remove(bye_player)
            groupings = data.group_by_record(players)
            sorted_scores = groupings.keys()
            sorted_scores.sort(key=lambda x: sum(x))
            sorted_scores.reverse()
            for i in range(len(sorted_scores)):
                temp = groupings[sorted_scores[i]]
                shuffle(temp)
                while len(temp) > 0:
                    if len(temp) == 1:
                        groupings[sorted_scores[i + 1]].append(temp.pop())
                    else:
                        data.pairings[temp[0]] = temp[1]
                        temp = temp[2:]

        self.bracket = Frame(master)
        self.left_side = data.pairings.keys()
        self.result_fields = []
        for i in range(len(self.left_side)):
            Label(self.bracket, text=str(self.left_side[i]) + ' vs').\
                                grid(row=i, column=0)
            Label(self.bracket, text=str(data.pairings[self.left_side[i]])).\
                                grid(row=i, column=1)
            win, loss = Entry(self.bracket), Entry(self.bracket)
            draw = Entry(self.bracket)
            self.result_fields.append((win, loss, draw))
            win.grid(row=i, column=2)
            loss.grid(row=i, column=3)
            draw.grid(row=i, column=4)
            
        if bye_player:
            Label(self.bracket, text='Bye: ' + str(bye_player)).\
                                     grid(row=len(self.left_side))
            
        self.quit_button = Button(self.bracket,
                                  text="QUIT",
                                  command=q)
        self.pairings_button = Button(self.bracket,
                                      text="CREATE PAIRINGS",
                                      command=lambda: self.new_pairings(master))
        self.quit_button.grid()
        self.pairings_button.grid()
        self.bracket.pack()

    def first_pairings(self, master):
        self.table.pack_forget()
        self.table.destroy()
        self.create_pairings(master)

    def new_pairings(self, master):
        for i in range(len(self.left_side)):
            self.left_side[i].wins += int(self.result_fields[i][0].get())
            self.left_side[i].losses += int(self.result_fields[i][1].get())
            self.left_side[i].draws += int(self.result_fields[i][2].get())
            data.pairings[self.left_side[i]].wins += int(self.result_fields[i][1].get())
            data.pairings[self.left_side[i]].losses += int(self.result_fields[i][0].get())
            data.pairings[self.left_side[i]].draws += int(self.result_fields[i][2].get())
        self.bracket.pack_forget()
        self.bracket.destroy()
        self.create_pairings(master)

    def add_player(self, field, button):
        """helper function for adding players into the game"""
        data.add_player(field.get())
        button["text"] = "ADD PLAYER {0}".format(data.number_players() + 1)

def draw_oval_center(x, y, radius, new_fill):
    """Wrapper function that draws an oval given its center (x, y) and radius"""
    gui.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, \
                              fill=new_fill)

def q():
    root.quit()

data = Data()

root = Tk()
root.title('Magic Brackets')
gui = GUI(root)
root.mainloop()
