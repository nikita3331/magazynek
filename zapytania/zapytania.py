from pymongo import MongoClient
from random import randint
from pprint import pprint
from datetime import datetime
import requests
import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication,QLineEdit,QMessageBox,QLabel,QVBoxLayout,QListWidget,QComboBox,QListWidgetItem
from PyQt5 import QtCore
import json
global ex

#dodac tabelki
url='https://zapkaappka.herokuapp.com/'
#url='http://127.0.0.1:5000/'
#QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
class myListWidget(QListWidget):
   def Clicked(self,item):
      buttonReply = QMessageBox.question(self, 'Usuwanie przedmiotu', "Czy usunac?",QMessageBox.Yes | QMessageBox.No)
      dane=item.data(QtCore.Qt.UserRole)
      if buttonReply == QMessageBox.Yes:
          #tu usuwamy

          producent=dane['producent']
          narzedzie=dane['narzedzie']
          imie=dane['osoba_imie']
          nazwisko=dane['osoba_nazwisko']
          #imie=ex.ludzie.input_imie.text()
          #nazwisko=ex.ludzie.input_nazwisko.text()
          payload = {"narzedzie": narzedzie, "ilosc": 1,"producent":producent,"osoba_imie":imie,"osoba_nazwisko":nazwisko}

          r = requests.post(url+'usun_wydanie/',json=payload)
          ex.ludzie.szukaj_pracownika()
   def Clicked_magazyn(self,item):
     buttonReply = QMessageBox.question(self, 'Usuwanie przedmiotu', "Czy usunac?",QMessageBox.Yes | QMessageBox.No)
     dane=item.data(QtCore.Qt.UserRole)
     if buttonReply == QMessageBox.Yes:
         #tu usuwamy
         producent=dane['producent']
         narzedzie=dane['narzedzie']
         kategoria=dane['kategoria']
         payload = {"narzedzie": narzedzie, "ilosc": 1,"producent":producent,"kategoria":kategoria}
         r = requests.post(url+'usun/',json=payload)
         ex.sprzet.laduj()
   def Clicked_combo_kategoria(self,item):
     buttonReply = QMessageBox.question(self, 'Usuwanie przedmiotu', "Czy usunac?",QMessageBox.Yes | QMessageBox.No)
     dane=item.data(QtCore.Qt.UserRole)
     if buttonReply == QMessageBox.Yes:
         #tu usuwamy
         producent=dane['producent']
         narzedzie=dane['narzedzie']
         kategoria=dane['kategoria']

         payload = {"narzedzie": narzedzie, "ilosc": 1,"producent":producent,"kategoria":kategoria}
         r = requests.post(url+'usun/',json=payload)
         ex.po_kategorii.laduj_itemki()



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


        label_input_kategoria = QLabel(self)
        label_input_kategoria.setText("Kategoria")
        label_input_kategoria.move(430-os_x, 20+h)
        self.input_kategoria = QLineEdit(self)
        self.input_kategoria.move(430-os_x, 40+h)
        self.input_kategoria.resize(100,40)
        button_kategoria = QPushButton('Dodaj kategorie', self)
        button_kategoria.clicked.connect(self.dodaj_kategorie)
        button_kategoria.resize(100,40)
        button_kategoria.move(550-os_x, 40+h)



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

        self.setGeometry(0, 0, 700, 600)
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
    def dodaj_kategorie(self):
        kategoria = self.input_kategoria.text()
        kat=kategoria.replace(" ","")
        katsa=kat.lower()
        payload = {"kategoria":katsa}
        r = requests.post(url+'kategorie/',json=payload)
        #QMessageBox.information("halko",str(r.text()))
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(r.text)
        retval = msg.exec_()
        self.dodaj_combo()
        self.input_kategoria.setText("")
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

    def zaladuj_wszystkie(self,dane):
        self.listWidget_ogolem.clear()
        for i in range(0,len(dane['odpowiedz'])):
            if dane['odpowiedz'][i]['narzedzie']!='kategorie':
                data_nowa=datetime.fromisoformat(dane['odpowiedz'][i]['data'])
                narzedzie=str(dane['odpowiedz'][i]['narzedzie'])
                producent=str(dane['odpowiedz'][i]['producent'])
                kategoria=str(dane['odpowiedz'][i]['kategoria'])
                ilosc_wszystkich=str(dane['odpowiedz'][i]['ilosc_wszystkich'])

                struna1=narzedzie+' '+producent+' '+kategoria+' '+ilosc_wszystkich
                struna2=str(data_nowa.day)+'-'+str(data_nowa.month)+'-'+str(data_nowa.year)
                itemek=struna1

                item = QListWidgetItem(itemek)
                data = ({'narzedzie':narzedzie,'producent':producent,'kategoria':kategoria})
                item.setData(QtCore.Qt.UserRole, data)
                self.listWidget_ogolem.addItem(item)
    def zaladuj_magazyn(self,dane):  #to bedzie lokalnie filtrowane
        self.listWidget_magazyn.clear()
        for i in range(0,len(dane['odpowiedz'])):
            if dane['odpowiedz'][i]['narzedzie']!='kategorie':
                data_nowa=datetime.fromisoformat(dane['odpowiedz'][i]['data'])
                narzedzie=str(dane['odpowiedz'][i]['narzedzie'])
                producent=str(dane['odpowiedz'][i]['producent'])
                kategoria=str(dane['odpowiedz'][i]['kategoria'])
                ilosc_wszystkich=str(dane['odpowiedz'][i]['ilosc_wszystkich'])
                ilosc_wydanych=dane['odpowiedz'][i]['ilosc_wydanych']


                dostepne=int(ilosc_wszystkich)-int(ilosc_wydanych)
                struna1=narzedzie+' '+producent+' '+kategoria+' '+str(dostepne)
                struna2=str(data_nowa.day)+'-'+str(data_nowa.month)+'-'+str(data_nowa.year)
                itemek=struna1

                item = QListWidgetItem(itemek)
                data = ({'narzedzie':narzedzie,'producent':producent,'kategoria':kategoria,'ilosc_wydanych':ilosc_wydanych,'ilosc_wszystkich':ilosc_wszystkich})
                item.setData(QtCore.Qt.UserRole, data)
                self.listWidget_magazyn.addItem(item)
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

        self.setGeometry(0, 0, 700, 600)
        self.setWindowTitle('Dodawanie sprzetu')

    def wydaj_sprzet(self):
        narzedzie = self.input_narzedzie.text()
        producent = self.input_producent.text()
        ilosc=int(self.input_ilosc.text())
        imie=self.input_imie.text()
        imj=imie.replace(" ","")
        imjj=imj.lower()
        nazwisko=self.input_nazwisko.text()
        naz=nazwisko.replace(" ","")
        nazz=naz.lower()
        payload = {"narzedzie": narzedzie, "producent": producent,"ilosc":ilosc, "osoba_imie": imjj,"osoba_nazwisko":nazz}
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



        self.setGeometry(0, 0, 700, 600)
        self.setWindowTitle('Sprawdzenie ludzi')

    def szukaj_pracownika(self):
        #wyczyscic
        self.listWidget.clear();
        osoba_imie = self.input_imie.text()
        ossa=osoba_imie.replace(" ","")
        ossaba=ossa.lower()
        osoba_nazwisko=self.input_nazwisko.text()
        nazi=osoba_nazwisko.replace(" ","")
        naziz=nazi.lower()
        payload = {"osoba_imie": ossaba, "osoba_nazwisko": naziz}
        r = requests.post(url+'wydane_osobie/',json=payload)
        dane=r.json()
        for i in range(0,len(dane['odpowiedz'])):
            data_nowa=datetime.fromisoformat(dane['odpowiedz'][i]['data'])
            narzedzie=str(dane['odpowiedz'][i]['narzedzie'])
            producent=str(dane['odpowiedz'][i]['producent'])
            ilosc=str(dane['odpowiedz'][i]['ilosc'])
            itemek=narzedzie+' '+producent+' '+ilosc+' '+str(data_nowa.day)+'-'+str(data_nowa.month)+'-'+str(data_nowa.year)
            item = QListWidgetItem(itemek)
            data = ({'narzedzie':narzedzie,'producent':producent,'osoba_imie':ossaba,'osoba_nazwisko':naziz,'ilosc':ilosc})
            item.setData(QtCore.Qt.UserRole, data)
            self.listWidget.addItem(item)




class Po_kategorii(QWidget):
    def __init__(self,parent):
        super().__init__()
        self.width = 600
        self.height = 600
        self.initUI()
        self.polaczono=0
        self.dummy=0
        self.kategoria_wyszukiwanie=0
    def initUI(self):
        self.listWidget_kategorie= myListWidget(self)
        self.listWidget_kategorie.resize(200,300)
        self.listWidget_kategorie.move(300,50)
        self.listWidget_kategorie.setWindowTitle('Lista przedmiotów')
        self.listWidget_kategorie.itemClicked.connect(self.listWidget_kategorie.Clicked_combo_kategoria)
        self.listWidget_kategorie.show()

        self.combo_wyszukiwanie = QComboBox(self)
        self.combo_wyszukiwanie.resize(100,40)
        self.combo_wyszukiwanie.move(100, 80)
        self.combo_wyszukiwanie.currentIndexChanged.connect(self.zmiana_combo)
        self.combo_wyszukiwanie.show()
        self.dodaj_combo()
        self.laduj_itemki()




        self.setGeometry(0, 0, 700, 600)
        self.setWindowTitle('Filtruj kategorie')


    def zmiana_combo(self,i):
        self.kategoria_wyszukiwanie=self.combo_wyszukiwanie.currentText()
        self.laduj_itemki()
    def laduj_itemki(self):
        self.listWidget_kategorie.clear();
        kategoria=self.kategoria_wyszukiwanie
        payload = {"kategoria": kategoria}
        r = requests.post(url+'zobacz_po_kategorii/',json=payload)
        dane=r.json()
        for i in range(0,len(dane['odpowiedz'])):
            data_nowa=datetime.fromisoformat(dane['odpowiedz'][i]['data'])
            narzedzie=str(dane['odpowiedz'][i]['narzedzie'])
            producent=str(dane['odpowiedz'][i]['producent'])
            kategoria=str(dane['odpowiedz'][i]['kategoria'])
            ilosc_wszystkich=str(dane['odpowiedz'][i]['ilosc_wszystkich'])
            ilosc_wydanych=dane['odpowiedz'][i]['ilosc_wydanych']


            dostepne=int(ilosc_wszystkich)-int(ilosc_wydanych)
            struna1=narzedzie+' '+producent+' '+ilosc_wszystkich
            struna2=str(dostepne)
            struna3=' '+str(data_nowa.day)+'-'+str(data_nowa.month)+'-'+str(data_nowa.year)
            itemek=struna1+' '+struna2



            item = QListWidgetItem(itemek)
            data = ({'narzedzie':narzedzie,'producent':producent,'kategoria':kategoria})
            item.setData(QtCore.Qt.UserRole, data)
            self.listWidget_kategorie.addItem(item)

    def dodaj_combo(self):
        r = requests.get(url+'kategorie/')
        dane=r.json()
        self.combo_wyszukiwanie.clear()
        kats=dane['odpowiedz'][0]['kategorie']
        for i in range(0,len(kats)):
            kat=kats[i]
            self.combo_wyszukiwanie.addItem(kat)


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
        self.po_kategorii = Po_kategorii(self)
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

        guzik_po_kategorii = QPushButton('Pokaż kategorie', self)
        guzik_po_kategorii.clicked.connect(self.guzik_kliknij_po_kategorii)
        guzik_po_kategorii.resize(guzik_po_kategorii.sizeHint())
        guzik_po_kategorii.move(380, 70)



        self.setGeometry(0, 0, 700, 600)
        self.setWindowTitle('Glowne okno')
        self.show()
    def guzik_sprzet(self):
        self.sprzet.laduj()
        self.sprzet.show()
    def guzik_kliknij_po_kategorii(self):
        self.po_kategorii.show()
        self.po_kategorii.dodaj_combo()
    def guzik_patrz_ludzi(self):
        self.ludzie.show()
    def guzik_kliknij_wydaj(self):
        self.wydaj.show()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    ex = Glowne()
    ex.show()
    print(app.primaryScreen().size())
    sys.exit(app.exec_())
