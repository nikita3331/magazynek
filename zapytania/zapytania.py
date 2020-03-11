from pymongo import MongoClient
from random import randint
from pprint import pprint
from datetime import datetime
import requests
import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication,QLineEdit,QMessageBox,QLabel,QVBoxLayout,QListWidget,QComboBox,QListWidgetItem,QTableWidget,QTableWidgetItem
from PyQt5 import QtCore
import json
global ex

#dodac tabelki
url='https://zapkaappka.herokuapp.com/'
#url='http://127.0.0.1:5000/'
#QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

class tabelka(QTableWidget):
    def ustaw(self):
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setRowCount(1)
        self.tableWidget.setColumnCount(5)
        self.tableWidget.move(250,50)
        self.tableWidget.resize(430,300)
        self.tableWidget.setHorizontalHeaderLabels(['narzedzie', 'producent','kategoria', 'wszystkie', 'dostepne'])
        self.tableWidget.itemClicked.connect(self.klikniety_magazyn)
        self.tableWidget.show()

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

        label_lista_ogolem = QLabel(self)
        label_lista_ogolem.setText("Stan magazynu")
        label_lista_ogolem.move(320, 20)
        self.tableWidget = QTableWidget(self)

        self.tableWidget.setRowCount(1)
        self.tableWidget.setColumnCount(5)
        self.tableWidget.move(250,50)
        self.tableWidget.resize(430,300)
        self.tableWidget.setHorizontalHeaderLabels(['narzedzie', 'producent','kategoria', 'wszystkie', 'dostepne'])

        self.tableWidget.itemClicked.connect(self.klikniety_magazyn)

        self.tableWidget.sortItems(0, QtCore.Qt.AscendingOrder)
        self.laduj()
        self.tableWidget.show()




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
        button_kategoria.move(540-os_x, 40+h)



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
    def klikniety_magazyn(self,item):
        buttonReply = QMessageBox.question(self, 'Usuwanie przedmiotu', "Czy usunac?",QMessageBox.Yes | QMessageBox.No)
        dane=item.data(QtCore.Qt.UserRole)
        if buttonReply == QMessageBox.Yes:
    #tu usuwamy
            producent=dane['producent']
            narzedzie=dane['narzedzie']
            kategoria=dane['kategoria']
            payload = {"narzedzie": narzedzie, "ilosc": 1,"producent":producent,"kategoria":kategoria}
            r = requests.post(url+'usun/',json=payload)
            self.laduj()
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

    def zaladuj_magazyn(self,dane):  #to bedzie lokalnie filtrowane
        self.tableWidget.clear()
        self.tableWidget.setHorizontalHeaderLabels(['narzedzie', 'producent','kategoria', 'wszystkie', 'dostepne'])
        self.tableWidget.setRowCount(len(dane['odpowiedz']))


        lista_moja=list(dane['odpowiedz'])
        #posortowana=sorted(lista_moja, key = lambda i: i['narzedzie'])
        for i in range(0,len(dane['odpowiedz'])):

            if lista_moja[i]['narzedzie']!='kategorie' :

                narzedzie=str(lista_moja[i]['narzedzie'])
                producent=str(lista_moja[i]['producent'])
                kategoria=str(lista_moja[i]['kategoria'])
                ilosc_wszystkich=str(lista_moja[i]['ilosc_wszystkich'])
                ilosc_wydanych=lista_moja[i]['ilosc_wydanych']
                dostepne=int(ilosc_wszystkich)-int(ilosc_wydanych)
                data = ({'narzedzie':narzedzie,'producent':producent,'kategoria':kategoria,'ilosc_wydanych':ilosc_wydanych,'ilosc_wszystkich':ilosc_wszystkich})
                self.tableWidget.setSortingEnabled(False)

                item0 = QTableWidgetItem(str(narzedzie))
                item0.setData(QtCore.Qt.UserRole, data)
                self.tableWidget.setItem(i,0,item0)

                item1 = QTableWidgetItem(str(producent))
                item1.setData(QtCore.Qt.UserRole, data)
                self.tableWidget.setItem(i,1,item1)

                item2 = QTableWidgetItem(str(kategoria))
                item2.setData(QtCore.Qt.UserRole, data)
                self.tableWidget.setItem(i,2,item2)

                item3 = QTableWidgetItem(str(ilosc_wszystkich))
                item3.setData(QtCore.Qt.UserRole, data)
                self.tableWidget.setItem(i,3,item3)

                item4 = QTableWidgetItem(str(dostepne))
                item4.setData(QtCore.Qt.UserRole, data)
                self.tableWidget.setItem(i,4,item4)
                self.tableWidget.setSortingEnabled(True)

        #self.tableWidget.removeRow(0)



    def laduj(self):
        #otrzymamy rq i wrzucimy
        r = requests.post(url+'zobacz_wszystkie/')
        dane=r.json()
        self.zaladuj_magazyn(dane)

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

        self.tableWidget = QTableWidget(self)
        self.tableWidget.setRowCount(1)
        self.tableWidget.setColumnCount(4)
        self.tableWidget.move(300,50)
        self.tableWidget.resize(350,300)
        self.tableWidget.setHorizontalHeaderLabels(['narzedzie', 'producent', 'ilosc', 'data'])
        self.tableWidget.itemClicked.connect(self.kliknieta_tabela)
        self.tableWidget.sortItems(0, QtCore.Qt.AscendingOrder)
        self.tableWidget.show()

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
    def kliknieta_tabela(self,item):
        buttonReply = QMessageBox.question(self, 'Usuwanie przedmiotu', "Czy usunac?",QMessageBox.Yes | QMessageBox.No)
        dane=item.data(QtCore.Qt.UserRole)
        if buttonReply == QMessageBox.Yes:
            producent=dane['producent']
            narzedzie=dane['narzedzie']
            imie=dane['osoba_imie']
            nazwisko=dane['osoba_nazwisko']
            payload = {"narzedzie": narzedzie, "ilosc": 1,"producent":producent,"osoba_imie":imie,"osoba_nazwisko":nazwisko}
            r = requests.post(url+'usun_wydanie/',json=payload)
            self.szukaj_pracownika()
    def szukaj_pracownika(self):
        osoba_imie = self.input_imie.text()
        ossa=osoba_imie.replace(" ","")
        ossaba=ossa.lower()
        osoba_nazwisko=self.input_nazwisko.text()
        nazi=osoba_nazwisko.replace(" ","")
        naziz=nazi.lower()
        payload = {"osoba_imie": ossaba, "osoba_nazwisko": naziz}
        r = requests.post(url+'wydane_osobie/',json=payload)
        dane=r.json()
        self.tableWidget.clear()
        self.tableWidget.setHorizontalHeaderLabels(['narzedzie', 'producent', 'ilosc', 'data'])
        self.tableWidget.setRowCount(len(dane['odpowiedz']))
        lista_moja=list(dane['odpowiedz'])
        #posortowana=sorted(lista_moja, key = lambda i: i['narzedzie'])
        for i in range(0,len(dane['odpowiedz'])):
            data_nowa=datetime.fromisoformat(lista_moja[i]['data'])
            narzedzie=str(lista_moja[i]['narzedzie'])
            producent=str(lista_moja[i]['producent'])
            ilosc=str(lista_moja[i]['ilosc'])
            data = ({'narzedzie':narzedzie,'producent':producent,'osoba_imie':ossaba,'osoba_nazwisko':osoba_nazwisko,'ilosc':ilosc})
            self.tableWidget.setSortingEnabled(False)
            item0 = QTableWidgetItem(str(narzedzie))
            item0.setData(QtCore.Qt.UserRole, data)
            self.tableWidget.setItem(i,0,item0)

            item1 = QTableWidgetItem(str(producent))
            item1.setData(QtCore.Qt.UserRole, data)
            self.tableWidget.setItem(i,1,item1)

            item2 = QTableWidgetItem(str(ilosc))
            item2.setData(QtCore.Qt.UserRole, data)
            self.tableWidget.setItem(i,2,item2)

            item3 = QTableWidgetItem(str(data_nowa.day)+'-'+str(data_nowa.month)+'-'+str(data_nowa.year))
            item3.setData(QtCore.Qt.UserRole, data)
            self.tableWidget.setItem(i,3,item3)
            self.tableWidget.setSortingEnabled(True)

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


        self.combo_wyszukiwanie = QComboBox(self)
        self.combo_wyszukiwanie.resize(100,40)
        self.combo_wyszukiwanie.move(100, 80)
        self.combo_wyszukiwanie.currentIndexChanged.connect(self.zmiana_combo)
        self.combo_wyszukiwanie.show()

        self.tableWidget = QTableWidget(self)
        self.tableWidget.setRowCount(4)
        self.tableWidget.setColumnCount(4)
        self.tableWidget.move(250,50)
        self.tableWidget.resize(430,300)
        self.tableWidget.setHorizontalHeaderLabels(['narzedzie', 'producent', 'wszystkie', 'dostepne'])
        self.tableWidget.itemClicked.connect(self.clicked_table)
        self.tableWidget.sortItems(0, QtCore.Qt.AscendingOrder)
        self.tableWidget.show()
        self.dodaj_combo()
        self.laduj_itemki()



        self.setGeometry(0, 0, 700, 600)
        self.setWindowTitle('Filtruj kategorie')
    def clicked_table(self,item):
        buttonReply = QMessageBox.question(self, 'Usuwanie przedmiotu', "Czy usunac?",QMessageBox.Yes | QMessageBox.No)
        dane=item.data(QtCore.Qt.UserRole)
        if buttonReply == QMessageBox.Yes:
         #tu usuwamy
            producent=dane['producent']
            narzedzie=dane['narzedzie']
            kategoria=dane['kategoria']

            payload = {"narzedzie": narzedzie, "ilosc": 1,"producent":producent,"kategoria":kategoria}
            r = requests.post(url+'usun/',json=payload)
            self.laduj_itemki()
    def dodaj_do_tabeli(self,dane):

        #dodac sortowanie
        self.tableWidget.clear()
        self.tableWidget.setHorizontalHeaderLabels(['narzedzie', 'producent', 'wszystkie', 'dostepne'])
        self.tableWidget.setRowCount(len(dane['odpowiedz']))
        lista_moja=list(dane['odpowiedz'])
        posortowana=sorted(lista_moja, key = lambda i: i['narzedzie'])
        for i in range(0,len(dane['odpowiedz'])):
            narzedzie=str(lista_moja[i]['narzedzie'])
            producent=str(lista_moja[i]['producent'])
            kategoria=str(lista_moja[i]['kategoria'])
            ilosc_wszystkich=str(lista_moja[i]['ilosc_wszystkich'])
            ilosc_wydanych=lista_moja[i]['ilosc_wydanych']
            dostepne=int(ilosc_wszystkich)-int(ilosc_wydanych)
            data = ({'narzedzie':narzedzie,'producent':producent,'kategoria':kategoria,'ilosc_wszystkich':ilosc_wszystkich,'dostepne':dostepne})
            self.tableWidget.setSortingEnabled(False)
            item0 = QTableWidgetItem(str(narzedzie))
            item0.setData(QtCore.Qt.UserRole, data)
            self.tableWidget.setItem(i,0,item0)

            item1 = QTableWidgetItem(str(producent))
            item1.setData(QtCore.Qt.UserRole, data)
            self.tableWidget.setItem(i,1,item1)

            item2 = QTableWidgetItem(str(ilosc_wszystkich))
            item2.setData(QtCore.Qt.UserRole, data)
            self.tableWidget.setItem(i,2,item2)

            item3 = QTableWidgetItem(str(dostepne))
            item3.setData(QtCore.Qt.UserRole, data)
            self.tableWidget.setItem(i,3,item3)
            self.tableWidget.setSortingEnabled(True)
    def zmiana_combo(self,i):
        self.kategoria_wyszukiwanie=self.combo_wyszukiwanie.currentText()
        self.laduj_itemki()
    def laduj_itemki(self):
        kategoria=self.kategoria_wyszukiwanie
        payload = {"kategoria": kategoria}
        r = requests.post(url+'zobacz_po_kategorii/',json=payload)
        dane=r.json()
        self.dodaj_do_tabeli(dane)

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
        self.sprzet = Sprzet()
        self.sprzet.laduj()
        self.sprzet.show()
    def guzik_kliknij_po_kategorii(self):
        self.po_kategorii = Po_kategorii(self)
        self.po_kategorii.show()
        self.po_kategorii.dodaj_combo()
    def guzik_patrz_ludzi(self):
        self.ludzie = Ludzie()
        self.ludzie.show()
    def guzik_kliknij_wydaj(self):
        self.wydaj = Wydaj(self)
        self.wydaj.show()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    ex = Glowne()
    ex.show()
    print(app.primaryScreen().size())
    sys.exit(app.exec_())
