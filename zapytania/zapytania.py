from pymongo import MongoClient
from random import randint
from pprint import pprint
from datetime import datetime
import requests
import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication,QLineEdit,QMessageBox,QLabel,QVBoxLayout,QListWidget,QComboBox
import json
global ex

url='https://zapkaappka.herokuapp.com/'

class myListWidget(QListWidget):
   def Clicked(self,item):
      przedmiot=item.text()
      buttonReply = QMessageBox.question(self, 'Usuwanie przedmiotu', "Czy usunac?",QMessageBox.Yes | QMessageBox.No)
      if buttonReply == QMessageBox.Yes:
          #tu usuwamy
          slowa=przedmiot.split()
          producent=slowa[1]
          narzedzie=slowa[0]
          imie=ex.ludzie.input_imie.text()
          nazwisko=ex.ludzie.input_nazwisko.text()
          payload = {"narzedzie": narzedzie, "ilosc": 1,"producent":producent,"osoba_imie":imie,"osoba_nazwisko":nazwisko}
          r = requests.post(url+'usun_wydanie/',json=payload)
          ex.ludzie.szukaj_pracownika()
   def Clicked_magazyn(self,item):
     przedmiot=item.text()
     buttonReply = QMessageBox.question(self, 'Usuwanie przedmiotu', "Czy usunac?",QMessageBox.Yes | QMessageBox.No)
     if buttonReply == QMessageBox.Yes:
         #tu usuwamy
         slowa=przedmiot.split()
         producent=slowa[1]
         narzedzie=slowa[0]
         payload = {"narzedzie": narzedzie, "ilosc": 1,"producent":producent}
         r = requests.post(url+'usun/',json=payload)
         ex.sprzet.laduj()



class Sprzet(QWidget):
    def __init__(self):
        super().__init__()
        self.width = 600
        self.height = 600
        self.initUI()
        self.polaczono=0
        self.dummy=0
        self.kategoria=0
    def initUI(self):
        #na magazynie
        #ogolem
        h=400
        os_x=30
        label_lista_magazyn = QLabel(self)
        label_lista_magazyn.setText("Dostępne w magazynie")
        label_lista_magazyn.move(50, 20)
        self.listWidget_magazyn= myListWidget(self)
        self.listWidget_magazyn.resize(250,300)
        self.listWidget_magazyn.move(50,50)
        self.listWidget_magazyn.itemClicked.connect(self.listWidget_magazyn.Clicked_magazyn)
        self.listWidget_magazyn.show()




        label_lista_ogolem = QLabel(self)
        label_lista_ogolem.setText("Dostępne ogółem")
        label_lista_ogolem.move(320, 20)
        self.listWidget_ogolem= myListWidget(self)
        self.listWidget_ogolem.resize(250,300)
        self.listWidget_ogolem.move(320,50)
        self.listWidget_ogolem.itemClicked.connect(self.listWidget_ogolem.Clicked_magazyn)
        self.listWidget_ogolem.show()

        self.laduj()

        self.combo = QComboBox(self)
        self.combo.resize(100,40)
        self.combo.move(430-os_x, 80+h)
        self.combo.currentIndexChanged.connect(self.selectionchange)
        self.combo.show()
        self.dodaj_combo()

        label_input_narzedzie = QLabel(self)
        label_input_narzedzie.setText("Narzedzie")
        label_input_narzedzie.move(70-os_x,60+h)
        self.input_narzedzie = QLineEdit(self)
        self.input_narzedzie.move(50-os_x, 80+h)
        self.input_narzedzie.resize(100,40)


        label_input_producent = QLabel(self)
        label_input_producent.setText("Producent")
        label_input_producent.move(200-os_x, 60+h)
        self.input_producent = QLineEdit(self)
        self.input_producent.move(180-os_x, 80+h)
        self.input_producent.resize(100,40)


        label_input_ilosc = QLabel(self)
        label_input_ilosc.setText("Ilość")
        label_input_ilosc.move(330-os_x, 60+h)
        self.input_ilosc = QLineEdit(self)
        self.input_ilosc.move(310-os_x, 80+h)
        self.input_ilosc.resize(100,40)


        qbtn = QPushButton('Dodaj ', self)
        qbtn.clicked.connect(self.dodaj_sprzet)
        qbtn.resize(100,40)
        qbtn.move(540-os_x, 80+h)

        self.setGeometry(200, 200, 700, 600)
        self.setWindowTitle('Dodawanie sprzetu')

    def dodaj_sprzet(self):
        narzedzie = self.input_narzedzie.text()
        producent = self.input_producent.text()
        ilosc=int(self.input_ilosc.text())
        payload = {"narzedzie": narzedzie, "producent": producent,"ilosc":ilosc,"kategoria":self.kategoria}
        r = requests.post(url+'dodaj/',json=payload)
        #QMessageBox.information("halko",str(r.text()))
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(r.text)
        retval = msg.exec_()
        self.laduj()
    def dodaj_combo(self):
        r = requests.get(url+'kategorie/')
        dane=r.json()
        self.combo.clear()
        kats=dane['odpowiedz'][0]['kategorie']
        for i in range(0,len(kats)):
            kat=kats[i]
            self.combo.addItem(kat)

    def selectionchange(self,i):
        self.kategoria=self.combo.currentText()
        print ("wybrana kategoria to",self.kategoria)

    def zaladuj_wszystkie(self,dane):
        self.listWidget_ogolem.clear()
        for i in range(0,len(dane['odpowiedz'])):
            data_nowa=datetime.fromisoformat(dane['odpowiedz'][i]['data'])
            struna1=str(dane['odpowiedz'][i]['narzedzie'])+' '+str(dane['odpowiedz'][i]['producent'])+' '+str(dane['odpowiedz'][i]['ilosc_wszystkich'])
            struna2=str(data_nowa.day)+'-'+str(data_nowa.month)+'-'+str(data_nowa.year)
            itemek=struna1+' '+struna2
            self.listWidget_ogolem.addItem(itemek)
    def zaladuj_magazyn(self,dane):  #to bedzie lokalnie filtrowane
        self.listWidget_magazyn.clear()
        for i in range(0,len(dane['odpowiedz'])):
            data_nowa=datetime.fromisoformat(dane['odpowiedz'][i]['data'])
            dostepne=int(dane['odpowiedz'][i]['ilosc_wszystkich'])-int(dane['odpowiedz'][i]['ilosc_wydanych'])
            struna1=str(dane['odpowiedz'][i]['narzedzie'])+' '+str(dane['odpowiedz'][i]['producent'])+' '+str(dostepne)
            struna2=str(data_nowa.day)+'-'+str(data_nowa.month)+'-'+str(data_nowa.year)
            itemek=struna1+' '+struna2
            self.listWidget_magazyn.addItem(itemek)
    def laduj(self):
        #otrzymamy rq i wrzucimy
        r = requests.post(url+'zobacz_wszystkie/')
        dane=r.json()
        self.zaladuj_magazyn(dane)
        self.zaladuj_wszystkie(dane)

class Wydaj(QWidget):
    def __init__(self,parent):
        super().__init__()
        self.width = 800
        self.height = 600
        self.initUI()
        self.polaczono=0
        self.dummy=0

    def initUI(self):
        label_input_narzedzie = QLabel(self)
        label_input_narzedzie.setText("Narzedzie")
        label_input_narzedzie.move(50,50)
        self.input_narzedzie = QLineEdit(self)
        self.input_narzedzie.move(50, 80)
        self.input_narzedzie.resize(100,40)


        label_input_producent = QLabel(self)
        label_input_producent.setText("Producent")
        label_input_producent.move(180, 50)
        self.input_producent = QLineEdit(self)
        self.input_producent.move(180, 80)
        self.input_producent.resize(100,40)


        label_input_ilosc = QLabel(self)
        label_input_ilosc.setText("Ilość")
        label_input_ilosc.move(310, 50)
        self.input_ilosc = QLineEdit(self)
        self.input_ilosc.move(310, 80)
        self.input_ilosc.resize(100,40)


        label_input_osoba_imie = QLabel(self)
        label_input_osoba_imie.setText("Imie")
        label_input_osoba_imie.move(440, 50)
        self.input_imie = QLineEdit(self)
        self.input_imie.move(440, 80)
        self.input_imie.resize(100,40)


        label_input_osoba_nazwisko = QLabel(self)
        label_input_osoba_nazwisko.setText("Nazwisko")
        label_input_osoba_nazwisko.move(570, 50)
        self.input_nazwisko = QLineEdit(self)
        self.input_nazwisko.move(570, 80)
        self.input_nazwisko.resize(100,40)


        qbtn = QPushButton('Wydaj ', self)
        qbtn.clicked.connect(self.wydaj_sprzet)
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(140, 200)

        self.setGeometry(200, 200, 700, 600)
        self.setWindowTitle('Dodawanie sprzetu')

    def wydaj_sprzet(self):
        narzedzie = self.input_narzedzie.text()
        producent = self.input_producent.text()
        ilosc=int(self.input_ilosc.text())
        imie=self.input_imie.text()
        nazwisko=self.input_nazwisko.text()
        payload = {"narzedzie": narzedzie, "producent": producent,"ilosc":ilosc, "osoba_imie": imie,"osoba_nazwisko":nazwisko}
        r = requests.post(url+'wydaj/',json=payload)
        #QMessageBox.information("halko",str(r.text()))
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(r.text)
        retval = msg.exec_()
class Ludzie(QWidget):
    def __init__(self):
        super().__init__()
        self.width = 600
        self.height = 600
        self.initUI()
        self.polaczono=0
        self.dummy=0

    def initUI(self):
        self.listWidget= myListWidget(self)
        self.listWidget.resize(200,300)
        self.listWidget.move(300,50)
        self.listWidget.setWindowTitle('Lista przedmiotów')
        self.listWidget.itemClicked.connect(self.listWidget.Clicked)
        self.listWidget.show()

        label_input_imie = QLabel(self)
        label_input_imie.setText("Imie")
        label_input_imie.move(50,50)
        self.input_imie = QLineEdit(self)
        self.input_imie.move(50, 80)
        self.input_imie.resize(100,40)


        label_input_nazwisko = QLabel(self)
        label_input_nazwisko.setText("Nazwisko")
        label_input_nazwisko.move(180, 50)
        self.input_nazwisko = QLineEdit(self)
        self.input_nazwisko.move(180, 80)
        self.input_nazwisko.resize(100,40)


        qbtn = QPushButton('Szukaj ', self)
        qbtn.clicked.connect(self.szukaj_pracownika)
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(140, 200)



        self.setGeometry(200, 200, 700, 600)
        self.setWindowTitle('Sprawdzenie ludzi')

    def szukaj_pracownika(self):
        #wyczyscic
        self.listWidget.clear();
        osoba_imie = self.input_imie.text()
        osoba_nazwisko=self.input_nazwisko.text()
        payload = {"osoba_imie": osoba_imie, "osoba_nazwisko": osoba_nazwisko}
        r = requests.post(url+'wydane_osobie/',json=payload)
        dane=r.json()
        for i in range(0,len(dane['odpowiedz'])):
            data_nowa=datetime.fromisoformat(dane['odpowiedz'][i]['data'])

            itemek=str(dane['odpowiedz'][i]['narzedzie'])+' '+str(dane['odpowiedz'][i]['producent']+' '+str(data_nowa.day)+'-'+str(data_nowa.month)+'-'+str(data_nowa.year))
            self.listWidget.addItem(itemek);







class Glowne(QWidget):
    def __init__(self):
        super().__init__()
        self.width = 800
        self.height = 600
        self.initUI()
        self.polaczono=0
        self.dummy=0
        self.sprzet = Sprzet()
        self.ludzie = Ludzie()
        self.wydaj = Wydaj(self)
    def initUI(self):


        qbtn = QPushButton('Pokaż sprzęt', self)
        qbtn.clicked.connect(self.guzik_sprzet)
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(100, 70)

        guzik_ludzie = QPushButton('Szukaj pracowników ', self)
        guzik_ludzie.clicked.connect(self.guzik_patrz_ludzi)
        guzik_ludzie.resize(guzik_ludzie.sizeHint())
        guzik_ludzie.move(180, 70)

        guzik_wydaj = QPushButton('Wydaj sprzęt ', self)
        guzik_wydaj.clicked.connect(self.guzik_kliknij_wydaj)
        guzik_wydaj.resize(guzik_wydaj.sizeHint())
        guzik_wydaj.move(300, 70)



        self.setGeometry(200, 200, 700, 600)
        self.setWindowTitle('Glowne okno')
        self.show()
    def guzik_sprzet(self):
        self.sprzet.laduj()
        self.sprzet.show()

    def guzik_patrz_ludzi(self):
        self.ludzie.show()
    def guzik_kliknij_wydaj(self):
        self.wydaj.show()



if __name__ == '__main__':
    app = QApplication(sys.argv)

    ex = Glowne()
    ex.show()

    sys.exit(app.exec_())
