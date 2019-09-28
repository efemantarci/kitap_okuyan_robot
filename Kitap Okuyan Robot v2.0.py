#sistem modülleri
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from threading import Thread
import threading
import os
import time
import glob as gb
import json
import re
import urllib.request
#İndirilecek modüller
from PIL import Image,ImageTk
from pygame import mixer
import keyboard
from mutagen.mp3 import MP3
import cv2
import numpy
from gtts import gTTS 
import pytesseract
#mixer başlat
print("Mixer başlatılıyor")
mixer.init()

####with open("veri.json",encoding='utf-8', errors='ignore') as json_veri:
####     data = json.load(json_veri, strict=False)
####     print(data["ipbilgileri"][0])
####     print(data["ipbilgileri"][0]["ipadresi"])
####     print(data["ipbilgileri"][0]["basladımı"])
####     ipadresi = data["ipbilgileri"][0]["ipadresi"]
####     ipvarmı = data["ipbilgileri"][0]["basladımı"]
#başlangıç değerleri
isplaying = False
basılantuş = "yok"
sesklasörü = os.getcwd()
ismuted= False
eskises = 1
baslangicindex = 0
secilises = baslangicindex
oynatmalistesi = []
oynatılacak_ses = "yok"
saymadöngüsü = None
uzunluk = 999
loop_süresi = 10
sesi_gec = 0
ipadresi = None
v = "Girilmedi"
baslangicmı = True

baslangicsayfasi = 0

def baslangic_sayac():
    x = 0
    global baslangicmı
    global yükleniyor
    while baslangicmı:
        yükleniyor["text"] = yükleniyor["text"] + "."
        x +=1
        if x == 3:
            x = 0
            yükleniyor["text"] = "Yükleniyor"
        time.sleep(0.5)
def görüntü():
    time.sleep(3)
    global url
    global baslangic
    global baslangicmı
    global w
    print("Görüntü alınıyor")
    while True:
        if not baslangicmı:
            ctime1,ctime2 = time.localtime().tm_min , time.localtime().tm_sec
            img = Image.open(urllib.request.urlopen(url))
            width, height = img.size
            print(width,height)
            image = numpy.array(img)
            #rgb2bgr
            image = image[:, :, ::-1].copy()
            #90 derece döndür
            image = numpy.rot90(image)
            image = cv2.resize(image,(0,0),fx=7,fy=7)
            image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
            #Binarization (ayarlanacak)
            ##retval, image = cv2.threshold(image,200,255, cv2.THRESH_BINARY)
            image = cv2.GaussianBlur(image,(11,11),0)
            image = cv2.medianBlur(image,9)
            ##retval, resim = cv2.threshold(resim, 150, 255, cv2.THRESH_BINARY)
            print("resim alındı")
            try:
                text = pytesseract.image_to_string(image,lang="TUR")
            except:
                messagebox.showerror("Text Hatası","Yazı bulunamadı. Kamerayı doğru tuttuğunuza emin olun")
            text = text.lower()
            try:
                sayfa = re.findall('\d+',text)
                sayfanum = sayfa[len(sayfa) - 1]
            except:
                print("sayfa bulunamadı dayı deniliyor")
                sayfanum = "Dayı"
            print(text)
            w["text"] = text
            try:
                tts = gTTS(text = text, lang = "tr")
                tts.save('sesler/sayfa{s}.mp3'.format(s = sayfanum))
            except:
                messagebox.showerror("Ses Hatası","Çektiğiniz fotoğrafta metin olduğundan emin olun.")
            btime1,btime2 = time.localtime().tm_min , time.localtime().tm_sec
            if ctime1 == btime1:
                saniye = btime2-ctime2
            else:
                saniye = (60-ctime2) + btime2
            print("Döngü " + str(saniye) + " saniye sürdü")
            print("Döngü tamamlandı 5 saniye bekleniyor")
            if(sayfanum // 2 == 0):
                print("Kamera sağa")
            else:
                print("Kamera sola")
            time.sleep(5)
        else:
            yükleniyorsayacı = Thread(target=baslangic_sayac)
            yükleniyorsayacı.start()
            yükleme.set(0)
            ctime1,ctime2 = time.localtime().tm_min , time.localtime().tm_sec
            try:
                img = Image.open(urllib.request.urlopen(url))
            except:
                messagebox.showerror("Bağlantı Hatası", "Bağlantı hatası oluştu.\n IP adresinizi doğru girdiğinize ve internete bağlı olduğunuza emin olun.\nProgram bu mesajdan sonra kapatılacaktır.")
                kapat()
            yükleme.set(15)
            width, height = img.size
            print(width,height)
            image = numpy.array(img)
            yükleme.set(25)
            #rgb2bgr
            image = image[:, :, ::-1].copy()
            #90 derece döndür
            image = numpy.rot90(image)
            image = cv2.resize(image,(0,0),fx=7,fy=7)
            image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
            yükleme.set(40)
            #Binarization (ayarlanacak)
            ##retval, image = cv2.threshold(image,200,255, cv2.THRESH_BINARY)
            image = cv2.GaussianBlur(image,(11,11),0)
            image = cv2.medianBlur(image,9)
            ##retval, resim = cv2.threshold(resim, 150, 255, cv2.THRESH_BINARY)
            print("resim alındı")
            yükleme.set(50)
            try:
                text = pytesseract.image_to_string(image,lang="TUR")
            except:
                messagebox.showerror("Text Hatası","Yazı bulunamadı. Kamerayı doğru tuttuğunuza emin olun")
            yükleme.set(75)
            text = text.lower()
            try:
                sayfa = re.findall('\d+',text)
                sayfanum = sayfa[len(sayfa) - 1]
                baslangicsayisi = sayfanum
            except:
                print("sayfa bulunamadı dayı deniliyor")
                sayfanum = "Dayı"
            yükleme.set(80)
            print(text)
            try:
                tts = gTTS(text = text, lang = "tr")
                tts.save('sesler/sayfa{s}.mp3'.format(s = sayfanum))
            except:
                messagebox.showerror("Ses Hatası","Çektiğiniz fotoğrafta metin olduğundan emin olun.")
            yükleme.set(90)
            btime1,btime2 = time.localtime().tm_min , time.localtime().tm_sec
            if ctime1 == btime1:
                saniye = btime2-ctime2
            else:
                saniye = (60-ctime2) + btime2
            yükleme.set(99)
            print("Döngü " + str(saniye) + " saniye sürdü")
            print("Döngü tamamlandı 5 saniye bekleniyor")
            baslangicmı = False
            yükleme.place_forget()
            yükleniyor.place_forget()
            anadöngüler()
            infobutonları()
            boşlukbutonları()
            oynatmabutonları()
            time.sleep(5)
def girdial(event=None):
    global v
    global url
    global ipadresi
    ipadresi = a.get()
    v = ipadresi
    url = "http://"+ ipadresi +"/photoaf.jpg"
    print(url)
    görüntüişleme = Thread(target=görüntü)
    görüntüişleme.start()
    a.place_forget()
    b.place_forget()
    c.place_forget()
    yükleme.place(rely=0.4,relwidth=0.9,relx=0.03)
    yükleniyor.place(rely=0.3,relwidth=0.9,relx=0.03)



root = Tk()
root.title("Kitap Okuyan Robot v2.1")
root.geometry("1200x600")

root.bind('<Return>',girdial)
print(v)
running = threading.Event()


v = StringVar(root, value=ipadresi)
##    url = "http://"+ ipadresi +"/photoaf.jpg"

def klasördeki_sesler():
    global loop_süresi
    global baslangicindex
    global oynatmalistesi
    liste = []
    while True:
        ctime1,ctime2 = time.localtime().tm_min , time.localtime().tm_sec
        mp3 = gb.glob("sesler/*.mp3")
        for ses in mp3:
            if not ses in oynatmalistesi:
                listeye_ekle(ses)                           
        btime1,btime2 = time.localtime().tm_min , time.localtime().tm_sec
        if ctime1 == btime1:
            saniye = btime2-ctime2
        else:
            saniye = (60-ctime2) + btime2
        print("Döngü " + str(saniye) + " saniye sürdü...")
        kalan_sure = loop_süresi - saniye
        print(str(kalan_sure) + " saniye bekleniyor...")
        time.sleep(kalan_sure)
        baslangicindex = len(oynatmalistesi) + 1
def sesi_hemen_geç(event = None):
    global seslisteyazısı
    global secilises
    global baslangicindex
    seslisteyazısı.selection_clear(0, END)
    secilises += 1
    baslangicindex += 1
    seslisteyazısı.select_set(secilises)
    seslisteyazısı.event_generate("<<ListboxSelect>>")
    play_button()            
def ses_geç():
    global sürebelirteci
    global secilises
    global baslangicindex
    global seslisteyazısı
    global uzunluk
    while True:
        if mixer.music.get_pos() == -1 and isplaying:
            #Sonraki sese geç
            print("Diğer ses geçiliyor")
            seslisteyazısı.selection_clear(0, END)
            secilises += 1
            baslangicindex += 1
            seslisteyazısı.select_set(secilises)
            seslisteyazısı.event_generate("<<ListboxSelect>>")
            sesi_gec = False
            play_button()            
        else:
            #Şu oynatma çizgisi
            çarpım = 100/uzunluk
            sürebelirteci.set(mixer.music.get_pos()/1000 * çarpım)
def sayaç(t):
    global isplaying
    global baslangicindex
    global running
    simdikizaman = 0
    while running.is_set():
        while simdikizaman <t and mixer.music.get_busy():
            if not isplaying:
                continue
            else:
                dakika,saniye = divmod(simdikizaman,60)
                dakika,saniye= round(dakika),round(saniye)
                süre = "{:02d}:{:02d}".format(dakika,saniye)
                kalansüre["text"] = "Geçen süre =>" + süre
                print(mixer.music.get_pos()/1000)
                time.sleep(1)
                simdikizaman +=1
    simdikizaman = 0
    
def detayları_yaz():
    global saymadöngüsü
    global uzunluk
    global sesdosya
    global oynatılacak_ses
    global running
    altyazı["text"] = os.path.basename(oynatılacak_ses) + "Oynatılıyor"
    dosyadetayı["text"] = os.path.basename(oynatılacak_ses) + " Oynatılıyor"
    if oynatılacak_ses.endswith(".mp3"):
        mp3 = MP3(oynatılacak_ses)
        uzunluk = mp3.info.length
        print(uzunluk)
    else:
        a = mixer.Sound(oynatılacak_ses)
        uzunluk = a.get_length()
    dakika,saniye = divmod(uzunluk,60)
    dakika,saniye = round(dakika),round(saniye)
    zaman = '{:02d}:{:02d}'.format(dakika,saniye)
    fullsüre["text"] = "Full süre => " + zaman
    # yaklaşık 3 saniye gecikme var. Çözülmeli
    #time.sleep(3)         
    running.clear()
    running.set()
    saymadöngüsü = Thread(target=sayaç,args=(uzunluk,))
    saymadöngüsü.start()
def kapat():
    stop_button()
    root.destroy()
def play_button():
    global isplaying
    global secili_ses
    global baslangicindex
    global oynatılacak_ses
    global saymadöngüsü
    if not isplaying:
        secili_ses = seslisteyazısı.curselection()                
        secili_ses = int(secili_ses[0])
        oynatılacak_ses = oynatmalistesi[secili_ses]
        mixer.music.load(oynatılacak_ses)
        print(oynatılacak_ses + " yüklendi!")
        mixer.music.play()
        detayları_yaz()
        isplaying = True
    else:
        mixer.music.stop()
        saymadöngüsü = Thread(target=sayaç,args=(1,))
        saymadöngüsü.start()
        secili_ses = seslisteyazısı.curselection()
        secili_ses = int(secili_ses[0])
        print(secili_ses)
        oynatılacak_ses = oynatmalistesi[secili_ses]
        mixer.music.load(oynatılacak_ses)
        mixer.music.play()
        detayları_yaz()
        isplaying = True
def pause_button(event = None):
    global isplaying
    print("Şarkı Bekletiliyor")
    if isplaying:
        mixer.music.pause()
        altyazı["text"] = "Bekletiliyor"
        isplaying = False
    else:
        mixer.music.unpause()
        altyazı["text"] = "Oynatılıyor"
        isplaying = True    
def stop_button():
    mixer.music.stop()
    print("Şarkı Durduruldu")
    altyazı["text"] = "Durduruldu"
def sound_button():
    global ismuted
    global eskises
    global soundbutton
    if not ismuted:
        eskises = mixer.music.get_volume()
        print(eskises)
        mixer.music.set_volume(0)
        scaler.set(0)
        ismuted = True
        soundbutton.configure(image=ph5)
    else:
        mixer.music.set_volume(eskises)
        scaler.set(eskises * 100)
        ismuted = False
        soundbutton.configure(image=ph4)
def yardım_menusu():
    messagebox.showinfo(title="Yardım",message="Kullanım:\n1- Telefonunuza IP Webcam adlı uygulamayı kurun\n2- Bilgisayar ile aynı bağlantıda olduğunuza emin olduktan sonra kamerayı açın ve IP adresinizi öğrenin\n3- Telefonunuzu kitabın bir sayfasına yerleştirin. (Önemli, çünkü kodun hızlı çalışması için direk başlatıyorum. Bu problemin üzerinde çalışıyorum\n4- Kodu çalıştırıp IP adresinizi girin.\n5- Belli bir süre sonra .mp3 uzantılı dosya belirecektir, tıklayıp oynatma tuşuna basın. (Bunun da üzerinde çalışıyorum.)\n6- Bu işlemlerden sonra kod kendisi foto çekip kendisi ses dosyaları arasında geçiş sağlayacaktır.\n7- Şu anlık sayfaları kendiniz çevirmeli ve telefonu kendiniz oynatmalısınız. Bu sıkıntı arkadaşlarım arduino kodunu yazınca düzelecektir.")
def hakkımızda():
    messagebox.showinfo(title="Hakkımızda",message="Selçuklu Fen Lisesi Tulpar Ekibi tarafından yapılmıştır. \n İletişim için : \n Tulpar Ekibi = tulparrobotik@gmail.com \n Arızalar için = efemantaroglu@gmail.com")
def ses_duzeyi(seviye):
    seviye = int(seviye)/100
    mixer.music.set_volume(seviye)
def foto_ekle():
    global fotodosya
    fotodosya = filedialog.askopenfilename()
def ses_ekle():
    global sesdosya
    sesdosya = filedialog.askopenfilename()
    listeye_ekle(sesdosya)
def ses_klasörü():
    global sesklaörü
    sesklasörü = filedialog.askopenfile()
def listeye_ekle(dosya):
    global seslisteyazısı
    global baslangicindex
    seslisteyazısı.insert(baslangicindex,os.path.basename(dosya))
    oynatmalistesi.append(dosya)
    print(oynatmalistesi)
    baslangicindex += 1
    
    
#fotoları çek
im = Image.open("simgeler/oynat.png")
ph1 = ImageTk.PhotoImage(im)
im = Image.open("simgeler/pause.png")
ph2 = ImageTk.PhotoImage(im)
im = Image.open("simgeler/durdur.png")
ph3 = ImageTk.PhotoImage(im)
im = Image.open("simgeler/sesli.png")
ph4 = ImageTk.PhotoImage(im)
im = Image.open("simgeler/sessiz.png")
ph5 = ImageTk.PhotoImage(im)
im = Image.open("simgeler/buton.png")
butonresmi = ImageTk.PhotoImage(im)
#Menüler
menubar = Menu(root)
root.config(menu=menubar)
#Dosya menüsü
dosyaMenu = Menu(menubar)
dosyaMenu.add_command(label="Kapat", command=kapat)
dosyaMenu.add_command(label="Fotoğraf Ekle", command=foto_ekle)
dosyaMenu.add_command(label="Ses Ekle", command=ses_ekle)
dosyaMenu.add_command(label="Ses Klasörünü Değiştir (BETA)", command=ses_klasörü)
menubar.add_cascade(label="Dosya", menu=dosyaMenu)
#Yardım menüsü
yardımMenu = Menu(menubar)
yardımMenu.add_command(label="Yardım",command=yardım_menusu)
menubar.add_cascade(label="Yardım",menu=yardımMenu)
yardımMenu.add_command(label="Hakkımızda",command=hakkımızda)
#İnfo ekranı
infoekran = Frame(root,relief=SUNKEN,bd=2,bg="white")
infoekran.pack_propagate(0)


w = Label(infoekran, text="IP adresini nasıl alabilirim?\n1-Google Play Store'dan 'IP Webcam'adlı uygulamayı indirin\n2-Uygulamayı açınca en aşağıya inip \"Start Server'a basın\" \n 3-IP Adresinizi üst kısma girip butona tıklayın.\nOkunan sayfalar buraya gelecektir..." )


def infobutonları():
    infoekran.place(relx=0.03,rely=0.1,relwidth=0.3,relheight=0.75)
    w.pack()
#Boşluk
boşluk = Frame(root,relief=SUNKEN,width=200,height=450)
boşluk.grid_propagate(0)


girdimetni = Label(boşluk,text="IP Adresi")


boşluk.grid_columnconfigure(1, minsize=10)

girdi = Entry(boşluk,bd=5,textvariable=v)


girdibutonu = Button(boşluk,text="Onayla",command=girdial)


boşlukframe = Frame(boşluk,relief=SUNKEN,bd=2,bg="white")

seslistebaslik = Label(boşlukframe,text="Ses Listesi")

seslisteyazısı = Listbox(boşlukframe)


def boşlukbutonları():
    boşluk.place(relx=0.35,rely=0.1)
    girdimetni.grid(column = 0,row=0)
    girdi.grid(column=2,row=0)
    girdibutonu.place(rely=0.07,relwidth=1)
    boşlukframe.place(rely=0.14,relwidth=1,relheight=0.93)
    seslistebaslik.place(rely=0.007,relx=0.53,relwidth=1.1,anchor=CENTER)
    seslisteyazısı.place(relx=0.001,rely=0.037,relwidth=1.1,relheight=0.9)

#Oynatma Kısmı
oynatmakısmı = Frame(root,relief=SUNKEN,width=450,height=450)

playbutton = Button(oynatmakısmı,image=ph1,anchor=CENTER,command=play_button)
playbutton.image = ph1

pausebutton = Button(oynatmakısmı,image=ph2,anchor=CENTER,command=pause_button)
pausebutton.image = ph2

stopbutton = Button(oynatmakısmı,image=ph3,anchor=CENTER,command=stop_button)
stopbutton.image = ph3

soundbutton = Button(oynatmakısmı,image=ph4,anchor=CENTER,command=sound_button)
soundbutton.image = ph4

scaler = Scale(oynatmakısmı,from_=0,to=100,orient=HORIZONTAL,command=ses_duzeyi)
scaler.set(100)

sürebelirteci = Scale(oynatmakısmı,from_=0,to=100,orient=HORIZONTAL,showvalue=0)
sürebelirteci.set(0)

altyazı = Label(root,text="Kitap Okuyan Robot                                                                                                                                                       Tulpar Ekibi",anchor=SW,relief=SUNKEN)


dosyadetayı = Label(oynatmakısmı,text="Ses bekleniyor. Ses oynaması için listeden seçip oynatma tuşuna basın.")

fullsüre = Label(oynatmakısmı,text="Full süre => --:--")


geçensüre = Label(oynatmakısmı,text="Geçen süre => --:--")


kalansüre = Label(oynatmakısmı,text="Kalan süre => --:--")


#Buttonları getir
def oynatmabutonları():
    oynatmakısmı.pack_propagate(0)
    oynatmakısmı.place(relx=0.53,rely=0.1,relwidth=0.4,relheight=0.75)
    altyazı.pack(side=BOTTOM,fill=X)
    dosyadetayı.place(rely=0.05,relx=0.40)
    fullsüre.place(rely=0.10,relx=0.40)
    geçensüre.place(rely=0.15,relx=0.40)
    kalansüre.place(rely=0.15,relx=0.40)
    playbutton.place(relx=0.28,rely=0.65)
    pausebutton.place(relx=0.43,rely=0.65)
    stopbutton.place(relx=0.58,rely=0.65)
    scaler.place(relx=0.2,rely=0.82,relwidth=0.7,relheight=0.1)
    sürebelirteci.place(relx=0.1,rely=0.4,relwidth=0.8,relheight=0.1)
    soundbutton.place(relx=0.05,rely=0.82)

#klavye tuşları
root.bind('<Right>',sesi_hemen_geç)
root.bind('<space>',pause_button)
root.bind('<m>',sound_button)

##if ipvarmı:
##    girdial()

c = Label(root,text = "IP adresiniz:")
c.place(rely = 0.1,relx=0.25)
a = Entry(root,bd=5)
a.place(rely=0.2,relx=0.25)
b = Button(root,text = "Onayla",command=girdial)
b.place(rely=0.3,relwidth=0.5,relx=0.25)
yükleme = Scale(root,from_=0,to=100,orient=HORIZONTAL)
yükleniyor = Label(root,text="Yükleniyor")

girdi.config(state='disabled')


#klavyekontrolü = Thread(target=klavye)
#klavyekontrolü.start()
def anadöngüler():
    seskontrolü = Thread(target=ses_geç)
    seskontrolü.start()

    listekontrolü = Thread(target=klasördeki_sesler)
    listekontrolü.start()

root.protocol("WM_WINDOW_DELETE",kapat)
root.protocol("WM_WINDOW_DELETE",quit)
root.mainloop()



