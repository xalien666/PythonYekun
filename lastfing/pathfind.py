import curses  # curses modulu metnler ucun istifade olunur. Ekranda metn uzerinde emeliyyatlar aparmaga hemcinin klaviatura ile islemeni temin edir
from curses import wrapper #modulu basladir ve proses bitdikden sonra  evvelki veziyyete qayidir
import queue #novbeni heyata kecirtmek ucun istifade olunan Python-un daxili moduludur
import time # Zaman moduludur. Daxilinde zaman funksiyalarini ehtiva edir.

# " "- yol, '#'- divarlar, O-baslangic , X- bitis
maze = [
    ["#", "O", "#", "#", "#", "#", "#", "#", "#","#", "#", "#", "#", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " "," ", " ", " ", " ", "#", " ", " ", "#"],
    ["#", " ", "#", "#", "#", "#", " ", "#"," ", " ", " ", " ", "#", " ", " ", "#"],
    ["#", " ", "#", " ", " ", "#", " ", "#"," ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", " ", " ", "#", " ", "#"," ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", " ", " ", "#", " ", "#"," ", " ", " ", " ", "#", " ", " ", "#"],
    ["#", " ", "#", "#", "#", "#", " ", "#"," ", " ", " ", " ", "#", " ", " ", "#"],
    ["#", " ", "#", " ", " ", "#", " ", "#"," ", " ", " ", " ", "#", " ", " ", "#"],
    ["#", " ", "#", " ", " ", "#", " ", "#"," ", " ", " ", " ", "#", " ", " ", "#"],
    ["#", " ", "#", " ", " ", "#", " ", "#"," ", " ", " ", " ", "#", " ", " ", "#"],
    ["#", " ", "#", " ", " ", "#", " ", "#"," ", " ", " ", " ", "#", " ", " ", "#"],
    ["#", " ", "#", " ", " ", "#", " ", "#","#", "#", "#", " ", "#", " ", " ", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " "," ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " "," ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " "," ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "X","#"]
]


def print_maze(maze, stdscr, path=[]): #labirinti ekrana cap etmek ucun funksiya

    BLUE = curses.color_pair(1) #curses.color_pair(1)-i (blue rengi 1 ID)  mavi degiskenine atanir.
    RED = curses.color_pair(2) #curses.color_pair(2)-i (red rengi 2 ID)  qirmizi degiskenine atanir.

    for i, row in enumerate(maze): #enumerate() nomreleme ucun istifade olunur i ve row dondurur.
        for j, value in enumerate(row): #j-column, enumarate nomreleme ucun istifade olunur, j ve valueni dondurur
            if (i, j) in path: #eger i,j pathin daxilinde olarsa
                stdscr.addstr(i, j*2, "X", RED) #i(row) j*2(column)u terminala cap edir. RED gedilen yolun rengidir
            else: # eger deyilse
                stdscr.addstr(i, j*2, value, BLUE) #i,j position(row,column). j*2- columnu arali cap edir. BLUE-"bitis"


def find_start(maze, start): #find_start funksiyasi
    for i, row in enumerate(maze):  #enumerate() nomreleme ucun istifade olunur i ve row dondurur.
        for j, value in enumerate(row):#j-column, enumarate nomreleme ucun istifade olunur, j ve valueni dondurur
            if value == start: # value starta beraber olarsa
                return i, j # i ve j koordinatlarini dondurur

    return None # Baslangic tapilmazsa None dondurur

def find_path(maze, stdscr): #find_path funksiyasi
    start = "O" #start noqtesi O
    end = "X" #finish X
    start_pos = find_start(maze, start) # find_start funksiyasini cagirir (burada start koordinatlari start_pos-a atanir)
    q = queue.Queue() #queue modulundan istifade etmek ucun queue.Queue() funksiyasini q-e atanib(qisalasdirma ucun)
    q.put((start_pos, [start_pos])) #put() metodu queue-ye element artirmaq ucun istifade olunur

    visited = set() #zset deyiskenini visitede atayir

    while not q.empty(): #empty() metodu Queue instansiyasinda her hansi elementin olub-olmadigini yoxlayir. Novbede hec bir element olmadiqda True qaytarir. Eks halda False qaytarir.
        current_pos, path = q.get() #get() metodu acar lugetde olarsa, gosterilen acarini deyerini qaytarir ve current_pos,path  atanir

        row, col = current_pos #current_positionu row ve col-a atanir
        stdscr.clear()  # terminali temizleyir
        print_maze(maze, stdscr, path) #print_maze funksiyasini cagirir
        time.sleep(0.2) #yolu tapmani gormek ucun 0.2s yavaslama
        stdscr.refresh() # terminali yenileyir

        if maze[row][col] == end: #eger row ve col end-e beraberdise en qisa yol tapilmisdir.
            return path # path-i dondurur
       
        neighbors = find_neighbors(maze, row, col) #call find_neighbors funksiyasini neighbors-a atayiriq
        for neighbor in neighbors: #for dongusu istifade ederek neighbors listindeki butun elementleri yoxlayiriq
            if neighbor in visited: #eger neighbor visitedin daxilindedirse
                continue #continue

            r, c = neighbor  #neighbor-u row ve columna atayiriq
            if maze[r][c] == "#": #eger mazede row ve column "#"-e beraber olarsa 
                continue #continue

            new_path = path + [neighbor] # neighboru listin icine saliriq daha sonra 2 listi toplayaraq new_path-a atayiriq
            q.put((neighbor, new_path)) #put ile queueye element elave edirik
            visited.add(neighbor) #add ile burada neighboru visitede elave edirik


def find_neighbors(maze, row, col): #find_neighbors funksiyasi
    neighbors = [] #neighbors adli bos list yaradir

    if row > 0:  # yuxari
        neighbors.append((row - 1, col)) #row-un evvelki veziyyeti ve column liste elave edir
    if row + 1 < len(maze):  # asagi
        neighbors.append((row + 1, col)) #rowun  sonraki veziyyeti ve column liste elave edir
    if col > 0:  # LEFT eger col > 0 olarsa
        neighbors.append((row, col - 1))# columndan evvelki veziyyet ve row liste elave edir
    if col + 1 < len(maze[0]):  # RIGHT 
        neighbors.append((row, col + 1)) #columndan sonraki veziyyeti ve row liste elave edir

    return neighbors #neighbors dondurur


def main(stdscr): #ekrana yazilari cixartmaqa imkan verir, hemcinin yaziya ve arxa plana reng elave etmek ucun istifade olunur

    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK) #Moterzenin ici uygun olaraq 1-ID, yazi rengi- goy, arxaplanin rengi -qara
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK) #Moterzenin ici uygun olaraq 1-ID, yazi rengi- qirmizi, arxaplanin rengi -qara

    find_path(maze, stdscr) #find_path funksiyasini cagirir
    stdscr.getch() #istifadeciden ne ise daxil etmesini gozleyir


wrapper(main) #wrapperi cagirir
