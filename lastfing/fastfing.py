import curses # curses modulu metnler ucun istifade olunur. Ekranda metn uzerinde emeliyyatlar aparmaga hemcinin klaviatura ile islemeni temin edir
from curses import wrapper #modulu basladir ve proses bitdikden sonra  evvelki veziyyete qayidir
import time # Zaman moduludur. Daxilinde zaman funksiyalarini ehtiva edir.
import random #tesadufi reqemler yaratmaga imkan verir,  ve ya  tesadufi hereketleri yerine yetirmek ucun istifade edilir
#################################################################################################################################

def start_screen(stdscr): #terminali basladma funksiyasidir
	stdscr.clear() #  terminali temizleyir
	stdscr.addstr("Welcome to the Speed Typing Test!") #terminala 'Welcome to the Speed Typing Test!' yazir
	stdscr.addstr("\nPress any key to begin!") #terminala yeni setirde (\n) 'Press any key to begin!" yazir
	stdscr.refresh()# butun terminali refresh edir
	stdscr.getkey()#istifadecinin getkey() daxil etmesini gozleyir. Eger hecne yazilmirsa yazilanlar silinir.
#################################################################################################################################

def display_text(stdscr, target, current, wpm=0): #ekrana yazini yazdirdiqda yazinin renglerinin deyisilmesi ucun funksiyadir
	stdscr.addstr(target) #target parametri cap edir
	stdscr.addstr(1, 0, f"WPM: {wpm}") #1,0 koordinatlar. f"WPM: {wpm}- wpmi terminala elave edir.

   
	for i, char in enumerate(current): #enumerate ile current textdeki elementleri ve onlarin indexlerini nomreleyir
		correct_char = target[i] # targetdeki her bir yazinin indeksi correct_charda saxlayiriq
		color = curses.color_pair(1) # curses.color_pair(1)-i color degiskende saxlayiriq. 1- yasil rengin ID-sidir
		if char != correct_char: #eger daxil edilen yazi  target textdeki yaziya beraber olmasa reng qirmiziya cevrilsin
			color = curses.color_pair(2) #curses.color_pair(2)-i color degiskende saxlayiriq. 2-qirmizi rengin ID-sidir

		stdscr.addstr(0, i, char, color) #0, i textin koordinatlari. char, color elave olunur terminala

		
######################################################################################################################################################################
def load_text(): #evvelceden hazirladigimiz tekst dosyasini cagirma funksiyasi
	with open("C:\\Users\\Asus\\Desktop\\PYL\\lastfing\\yazi.txt", "r") as f: #textimizi f adi ile aciriq. burada << r >>-fayllari oxumaq ucun istifade olunur
		lines = f.readlines() #readlines funksiyasi yazilari oxuyaraq yazilardan ibaret list yaradir
		return random.choice(lines).strip() #yaranan listden tesadufi olaraq 1-ni secir. strip()  orijinal setirin evvelinden ve ya sonundan verilmis simvollari silir
#######################################################################################################################################################################


def wpm_test(stdscr): #wpm_test funksiyasi
	target_text = load_text() # load_text funksiyasi target_texte yazilir
	current_text = [] # current_text adinda bos list yaradilir hansiki bizim daxil etdiyimiz bu listde saxlanilacaq
	wpm = 0 # wpm baslangic qiymeti
	start_time = time.time() #vaxti yazdirmaq ucun start_time deyiskenine yaziriq
	stdscr.nodelay(True) #gecikme olmamasi ucun istifade olunur
   
	while True: #wpm-in hesablanmasi ucun
		time_elapsed = max(time.time() - start_time, 1) # cari zamandan baslangic zamani cixaraq qalan vaxti aliriq. max ve 1 for zero division error olmamasi ucun istifade olunur
		wpm = round((len(current_text) / (time_elapsed / 60)) / 5) # wpm-in hesablanmasi burada  round - yuvarlaqlasdirma ucun istifade olunur

		stdscr.clear()  # terminali temizleyir
		
		display_text(stdscr, target_text, current_text, wpm) #verilen parametrleri cagirir
		stdscr.refresh() # terminali yenileyir

		if "".join(current_text) == target_text: # join() metodu butun elementleri  bir setirde birlesdirir.
			stdscr.nodelay(False) # terminal gecikme rejimine teyin edilir

			break # donguden cxir ve donguden sonra novbeti koda kecir
		try:
			key = stdscr.getkey() #stdscr.getkey-i key degiskeninde saxlayiriq
		except:
			continue  #dongunun evveline qaytarir

		if ord(key) == 27: #eger key deyeri 27 (ESC) olarsa serti yerine yetirir.
			break # donguden cxir ve donguden sonra novbeti koda kecir

# backspace-e basanda metnin silinmesi ucun
		if key in ("KEY_BACKSPACE", '\b', "\x7f"): #backspace "KEY_BACKSPACE", '\b', "\x7f" 3-den biri ile verilir. 3 acar sozden biri istifade olunarsa key
			if len(current_text) > 0: #eger current_textin uzunlugu 0-dan boyukdurse
				current_text.pop() #biz backspace-e basanda .pop() funksiyasindan istifade edib daxil etdiyimiz son element silinir
		elif len(current_text) < len(target_text): # target_text uzunlugu current_text uzunlugundan boyuk olduqda
			current_text.append(key) #istifadecinin daxil etdiyi butun yazilar append funksiyasi vasitesile liste elave olunur

######################################################################################################################################################################
def main(stdscr): #ekrana yazilari cixartmaqa imkan verir, hemcinin yaziya ve arxa plana reng elave etmek ucun istifade olunur
	curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK) #Moterzenin ici uygun olaraq 1-ID, yazi rengi- yasil, arxaplanin rengi -qara
	curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK) #Moterzenin ici uygun olaraq 2-ID, yazi rengi- qirmizi, arxaplanin rengi -qara
	curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK) #Moterzenin ici uygun olaraq 3-ID, yazi rengi- ag, arxaplanin rengi -qara
	start_screen(stdscr) #verilen funksiyani cagirir
	while True: # while dongusu True olanadek
		wpm_test(stdscr) #verilen funksiyani cagirir
		stdscr.addstr(2, 0, "You completed the text! Press any key to continue...") #burada 2-sutun 0-setir kordinatlaridir, "You completed the text! Press any key to continue..." cap edir
		key = stdscr.getkey() #stdscr.getkey()-i bir degiskende saxlayiriq or degisken atayiriq
		
		if ord(key) == 27: #eger key deyeri 27 (ESC) olarsa serti yerine yetirir.
			break # donguden cxir ve donguden sonra novbeti koda kecir

wrapper(main) #wrapperi cagirir
