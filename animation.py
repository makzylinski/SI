from __future__ import print_function

import decission_tree as dt
import time
from tkinter import *
import os
import tkinter as tk
import rozpoznawanie as rp
try:
    import matplotlib.pyplot as plt
except:
    raise


class AStarGraph(object):
    # Define a class board like grid with two barriers

    def __init__(self):
        self.barriers = []
        self.barriers.append(
            [(3, 3), (6, 3), (8, 3), (7, 3), (6, 4), (6, 5), (6, 6), (6, 7), (2, 6), (1, 6), (9, 3)])

    def heuristic(self, start, goal):
        # Use Chebyshev distance heuristic if we can move one square either
        # adjacent or diagonal
        D = 1
        D2 = 1
        dx = abs(start[0] - goal[0])
        dy = abs(start[1] - goal[1])
        return D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)

    def get_vertex_neighbours(self, pos):
        n = []
        # Moves allow link a chess king
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            x2 = pos[0] + dx
            y2 = pos[1] + dy
            if x2 < 0 or x2 > 9 or y2 < 0 or y2 > 9:
                continue
            n.append((x2, y2))
        return n

    def move_cost(self, a, b):
        for barrier in self.barriers:
            if b in barrier:
                return 100  # Extremely high cost to enter barrier squares
        return 1  # Normal movement cost


def AStarSearch(start, end, graph):
    G = {}  # Actual movement cost to each position from the start position
    F = {}  # Estimated movement cost of start to end going via this position

    # Initialize starting values
    G[start] = 0
    F[start] = graph.heuristic(start, end)

    closedVertices = set()
    openVertices = set([start])
    cameFrom = {}

    while len(openVertices) > 0:
        # Get the vertex in the open list with the lowest F score
        current = None
        currentFscore = None
        for pos in openVertices:
            if current is None or F[pos] < currentFscore:
                currentFscore = F[pos]
                current = pos

        # Check if we have reached the goal
        if current == end:
            # Retrace our route backward
            path = [current]
            while current in cameFrom:
                current = cameFrom[current]
                path.append(current)
            path.reverse()
            return path, F[end]  # Done!

        # Mark the current vertex as closed
        openVertices.remove(current)
        closedVertices.add(current)

        # Update scores for vertices near the current position
        for neighbour in graph.get_vertex_neighbours(current):
            if neighbour in closedVertices:
                continue  # We have already processed this node exhaustively
            candidateG = G[current] + graph.move_cost(current, neighbour)

            if neighbour not in openVertices:
                openVertices.add(neighbour)  # Discovered a new vertex
            elif candidateG >= G[neighbour]:
                continue  # This G score is worse than previously found

            # Adopt this G score
            cameFrom[neighbour] = current
            G[neighbour] = candidateG
            H = graph.heuristic(neighbour, end)
            F[neighbour] = G[neighbour] + H

    raise RuntimeError("A* failed to find a solution")


animation = tk.Tk()

canvas = Canvas(animation, width=500, height=500)  # rozmiar okna aplikacji
print(canvas.winfo_reqheight() - 4, "Szerokosc")


def create_grid(event=None):
    w = canvas.winfo_width()  # Get current width of canvas
    h = canvas.winfo_height()  # Get current height of canvas
    canvas.delete('grid_line')  # Will only remove the grid_line

    # Creates all vertical lines at intervals of 100
    for i in range(0, w, 50):
        canvas.create_line([(i, 0), (i, h)], tag='grid_line')

    # Creates all horizontal lines at intervals of 100
    for i in range(0, h, 50):
        canvas.create_line([(0, i), (w, i)], tag='grid_line')


truck = PhotoImage(file=os.getcwd() + "/truck.png")  # obraz obiektu cieżarówki
home = PhotoImage(file=os.getcwd() + "/home.png")  # obraz domków
paper = PhotoImage(file=os.getcwd() + "/paper.png")  # obraz papieru
plastic = PhotoImage(file=os.getcwd() + "/plastic.png")  # obraz plastiku
organic = PhotoImage(file=os.getcwd() + "/organic.png")  # obraz orpadów organicznych
glass = PhotoImage(file=os.getcwd() + "/glass.png")  # obraz szkła
grass = PhotoImage(file=os.getcwd() + "/grass.png")  # obraz trawy

xg = 50  # początkowa pozycja
yg = 50  # poczatkowa pozycja

homes = [[100, 150, 300, 300, 300, 400, 400, 50],
         [25, 150, 150, 350, 25, 25, 150, 300]]  # pozycje domów [0-1][0-8]

######### tablice z id obrazów obiektów śmieci
papers = []
plastics = []
organics = []
glasss = []

canvas.create_image(xg, yg, image=truck)  # umieść ciężarówkę na początkowej pozycji

canvas.bind('<Configure>', create_grid)

canvas.pack()

for i in range(0, 500, 25):
    canvas.create_image(0, i, image=grass)  ##przypisanie
for i in range(0, 500, 25):
    canvas.create_image(i, 0, image=grass)  ##przypisanie

for i in range(200, 500, 25):
    canvas.create_image(i, 500, image=grass)  ##przypisanie
for i in range(0, 500, 25):
    canvas.create_image(500, i, image=grass)  ##przypisanie

for i in range(300, 500, 25):
    canvas.create_image(i, 150, image=grass)  ##przypisanie

for i in range(200, 375, 25):
    canvas.create_image(300, i, image=grass)  ##przypisanie

for i in range(0, 175, 25):
    canvas.create_image(150, i, image=grass)  ##przypisanie

for i in range(0, 125, 25):
    canvas.create_image(i, 300, image=grass)  ##przypisanie
########## na każdym domku ikone śmieci


for i in range(0, len(homes[0])):
    canvas.create_image(homes[0][i], homes[1][i], image=home)  ##przypisanie

for i in range(0, len(homes[0])):
    organics.insert(i, canvas.create_image(homes[0][i] + 5, homes[1][i] + 5,
                                           image=organic))  ### .insert umieszcza id obiektu w odpowiedniej tablicy
for i in range(0, len(homes[0])):
    papers.insert(i, canvas.create_image(homes[0][i] - 5, homes[1][i] + 5, image=paper))
for i in range(0, len(homes[0])):
    plastics.insert(i, canvas.create_image(homes[0][i] - 5, homes[1][i] - 5, image=plastic))
for i in range(0, len(homes[0])):
    glasss.insert(i, canvas.create_image(homes[0][i] + 5, homes[1][i] - 5, image=glass))

print(canvas.coords(glasss[1]))
animation.update()
wysypisko = canvas.create_rectangle(200, 30, 50, 0, outline='red')  # prostokąt jako wysypisko
canvas.move(wysypisko, -25, 480)


def showpos(x, y):
    global xg
    xg += x
    global yg
    yg += y
    # print(xg, " , ", yg) # aktualna pozycja DEBUG


def truck_move(x, y):  # ruch ciezarowki
    global xg, yg
    showpos(x, y)
    canvas.move(1, x, y)  # przesun obiekt "1" o x i y
    canvas.create_line(xg, yg, xg + x, yg + y, fill="red")
    if (x == 1 and y == 0):
        if (xg % 50 == 0 and yg % 50 == 0):
            print("prawo")
    if (x == 0 and y == 1):
        if (xg % 50 == 0 and yg % 50 == 0):
            print("dół")
    if (x == -1 and y == 0):
        if (xg % 50 == 0 and yg % 50 == 0):
            print("lewo")
    if (x == 0 and y == -1):
        if (xg % 50 == 0 and yg % 50 == 0):
            print("góra")
    # print(xg, " ", x, "|", yg, " ", y)
    animation.update()
    time.sleep(0.01)  # czas oczekiwania


def go_to(x, y):  ## idz na koordynaty x,y
    global xg
    global yg
    if x > xg:
        while x != xg:
            truck_move(1, 0)
    if x < xg:
        while x != xg:
            truck_move(-1, 0)
    if y > yg:  ## -20 jako dopasowanie pozycji do domku
        while y != yg:
            truck_move(0, 1)
    if y < yg:
        while y != yg:
            truck_move(0, -1)
    # time.sleep(1)
    print("Jestem na ", xg, " na ", yg, ", chciałem na ", " x: ", x, " y: ", y)  # + 20


def go_to_list(list):  ## idz na koordynaty, lista koordynatów na trasie
    global xg, yg
    for pl in list:
        if pl[0] > xg:
            while pl[0] != xg:
                truck_move(1, 0)
        if pl[0] < xg:
            while pl[0] != xg:
                truck_move(-1, 0)
        if pl[1] > yg:  ## -20 jako dopasowanie pozycji do domku
            while pl[1] != yg:
                truck_move(0, 1)
        if pl[1] < yg:
            while pl[1] != yg:
                truck_move(0, -1)
        # time.sleep(.01)
        # print("Jestem na ", xg, " na ", yg, ", chciałem na ", " x: ", pl[0], " y: ", pl[1])  # + 20


def go_all_houses(len):  # idz do wszystkich domków
    global homes
    for i in range(0, len):
        go_to(homes[0][i], (homes[1][i]))


homes = [[100, 150, 250, 250, 300, 400, 400, 50],
         [50, 200, 150, 350, 50, 50, 200, 350]]

# przechowuje ile smieciarka wiezie
ile_papier = 0
ile_plastik = 0
ile_szklo = 0
ile_organiczne = 0


def take_trash():  # zbiera śmieci z domu pod który podjechałą "śmieciarka"
    global xg, yg, glasss, papers, plastics, organics
    global ile_szklo, ile_papier, ile_plastik, ile_organiczne
    # go_to(xg, yg - 50)
    xgg = xg
    ygg = yg
    go_to(xg, yg)

    szklo = find_closest_trash((xg, yg), glasss)
    if dist((xg, yg), (canvas.coords(szklo)[0], canvas.coords(szklo)[1])) > 60:
        print("Brak szkla")
    else:
        predict = dt.test_data([['1', '0', '1', '1', '0', '0', '31', 'szklo']])
        if 'szklo' in predict:
            ile_szklo += 1
            canvas.delete(szklo)

    papier = find_closest_trash((xg, yg), papers)
    if dist((xg, yg), (canvas.coords(papier)[0], canvas.coords(papier)[1])) > 60:
        print("Brak papieri")
    else:
        predict = dt.test_data([['0', '0', '0', '1', '0', '1', '30', 'papier']])
        if 'papier' in predict:
            ile_papier += 1
            canvas.delete(papier)

    plastik = find_closest_trash((xg, yg), plastics)
    if dist((xg, yg), (canvas.coords(plastik)[0], canvas.coords(plastik)[1])) > 60:
        print("Brak plastiku")
    else:
        predict = dt.test_data([['1', '0', '1', '1', '0', '1', '6', 'plastik']])
        if 'plastik' in predict:
            ile_plastik += 1
            canvas.delete(plastik)

    organiczne = find_closest_trash((xg, yg), organics)
    if dist((xg, yg), (canvas.coords(organiczne)[0], canvas.coords(organiczne)[1])) > 60:
        print("Brak organicznych")
    else:
        predict = dt.test_data([['0', '1', '0', '0', '1', '1', '21', 'organiczne']])
        if 'organiczne' in predict:
            ile_organiczne += 1
            canvas.delete(organiczne)

    time.sleep(.4)
    animation.update()
    # go_to(xg, yg + 50)

    xg = xgg
    yg = ygg
    print("Jade dalej")
    # do tej funkcji jeszcze będę dopisywał drzewo decyzyjne,
    # ktore bedzie sprawdzalo jaki smiec podnosi i odpowiednio doda
    # do licznika smieci


def go_dump(x, y, len):  # jedzie na wysypisko o podanych cordach i wyrzuca
    global xg, yg
    where, cost = AStarSearch((xg / 50, yg / 50), (homes[0][domki] / 50, (homes[1][domki] / 50)), graph)
    # go_to(x, y)  # wjedz na wysypisko
    cele2 = []
    for ss in where:
        cele2.append(((ss[0] * 50), (ss[1] * 50)))

    go_to_list(cele2)
    go_to(x - 40, y)  # jedz do odpowiedniego miejsca
    for i in range(0, len):
        canvas.create_image(x - 40, y + 10 + (i * 5), image=paper)
        animation.update()
        time.sleep(.5)
    go_to(x - 10, y)  # jedz do odpowiedniego miejsca
    for i in range(0, len):
        canvas.create_image(x - 10, y + 10 + (i * 5), image=glass)
        animation.update()
        time.sleep(.5)
    go_to(x + 20, y)
    for i in range(0, len):
        canvas.create_image(x + 20, y + 10 + (i * 5), image=organic)
        animation.update()
        time.sleep(.5)
    go_to(x + 50, y)
    for i in range(0, len):
        canvas.create_image(x + 50, y + 10 + (i * 5), image=plastic)
        animation.update()
        time.sleep(.5)
    print("Wyladowalem:")
    print("Szklo: ", ile_szklo)
    print("Papier: ", ile_papier)
    print("Plastik: ", ile_plastik)
    print("Organiczne: ", ile_organiczne)


def find_closest_trash(curr, open):  # curr[0]-x [1]-y, open lista x/y znajduje najbliższy obiekt śmieci
    minim = float("inf")
    for ss in open:
        if (abs(curr[0] - canvas.coords(ss)[0]) + abs(curr[1] - canvas.coords(ss)[1])) < minim:
            minim = (abs(curr[0] - canvas.coords(ss)[0]) + abs(curr[1] - canvas.coords(ss)[1]))
    for ss in open:
        if (abs(curr[0] - canvas.coords(ss)[0]) + abs(curr[1] - canvas.coords(ss)[1])) == minim:
            open.remove(ss)
            return ss


def dist(a, b):  # algorytm heurytyczny
    (x1, y1) = a
    (x2, y2) = b
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


graph = AStarGraph()
drzewo = dt.print_tree(dt.my_tree)
nr_domu = ["Czworka", "Szostka", "Jedynka", "Osemka", "Czworka", "Siodemka", "Siodemka", "Zero"]
for domki in range(0, len(homes[0])):  # głowna pętla

    print((homes[0][domki] / 50, (homes[1][domki] / 50)))

    result, cost = AStarSearch((xg / 50, yg / 50), (homes[0][domki] / 50, (homes[1][domki] / 50)), graph)

    ffw = []
    for ss in result:
        ffw.append(((ss[0] * 50), (ss[1] * 50)))

    go_to_list(ffw)
    print(result)
    print(cost)

    print("Sprawdzam numer domu")
    spr = rp.xtest[domki]
    pred_spr = rp.clf.predict([spr])        # nr domu: 4,6,1,8,4,7,7,0

    if(nr_domu[domki] == pred_spr):
        print("Rozpoznano numer: ", pred_spr)
    else:
        break
    #print(pred_spr)

    take_trash()
    print(ile_szklo)
    print("next")

go_dump(100, 450, len(homes[0]))
print(drzewo)
