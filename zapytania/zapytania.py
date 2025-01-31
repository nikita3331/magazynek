from pymongo import MongoClient
from random import randint
from pprint import pprint
from datetime import datetime
import requests
import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication,QLineEdit,QMessageBox,QLabel,QVBoxLayout,QListWidget,QComboBox,QListWidgetItem,QTableWidget,QTableWidgetItem,QGridLayout,QHeaderView
from PyQt5 import QtCore,QtGui
from PyQt5.QtGui import QPalette
import json
global ex

#generujemy obiegowke ,mail idzie do mamy z tabelki wybieramy pracownika i sprawdzamy jeszcze czy nic na nim nie ma

url='https://zapkaappka.herokuapp.com/'
#url='http://127.0.0.1:5000/'


class tabelka(QTableWidget):
    def ustaw(self):
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setRowCount(1)
        self.tableWidget.setColumnCount(5)
        self.tableWidget.move(250,50)
        self.tableWidget.resize(430,300)
        self.tableWidget.setHorizontalHeaderLabels(['narzędzie', 'producent','kategoria', 'wszystkie', 'dostępne'])
        self.tableWidget.itemClicked.connect(self.klikniety_magazyn)
        self.tableWidget.show()

class Sprzet(QWidget):
    def __init__(self):
        super().__init__()
        self.width = width_full
        self.height = height_full
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
        label_lista_ogolem.move(int((32/70)*self.width), int((2/60)*self.height))

        self.tableWidget = QTableWidget(self)
        wiersza = QtGui.QFont("Times", 15)
        self.tableWidget.setFont(wiersza)
        nazwa_kolumny = QtGui.QFont("Times", 20, QtGui.QFont.Bold)
        self.tableWidget.horizontalHeader().setFont(nazwa_kolumny)

        self.tableWidget.setRowCount(1)
        self.tableWidget.setColumnCount(5)
        self.tableWidget.move(int((10/70)*self.width), int((2/60)*self.height))
        self.tableWidget.resize(int((50/70)*self.width),int((35/60)*self.height) )
        self.tableWidget.setHorizontalHeaderLabels(['narzędzie', 'producent','kategoria', 'wszystkie', 'dostępne'])
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.itemClicked.connect(self.klikniety_magazyn)
        self.tableWidget.sortItems(0, QtCore.Qt.AscendingOrder)
        self.laduj()
        self.tableWidget.show()




        self.combo = QComboBox(self)
        self.combo.move(int((40/70)*self.width), int((48/60)*self.height))
        self.combo.resize(int((10/70)*self.width),int((4/60)*self.height) )
        self.combo.currentIndexChanged.connect(self.selectionchange)
        self.combo.show()
        self.dodaj_combo()

        label_input_narzedzie = QLabel(self)
        label_input_narzedzie.setText("Narzędzie")
        label_input_narzedzie.move(int((4/70)*self.width), int((46/60)*self.height))
        self.input_narzedzie = QLineEdit(self)
        self.input_narzedzie.move(int((2/70)*self.width), int((48/60)*self.height))
        self.input_narzedzie.resize(int((10/70)*self.width), int((4/60)*self.height))

        label_input_kategoria = QLabel(self)
        label_input_kategoria.setText("Kategoria")
        label_input_kategoria.move(int((40/70)*self.width),int((42/60)*self.height) )


        self.input_kategoria = QLineEdit(self)
        self.input_kategoria.move(int((40/70)*self.width), int((44/60)*self.height))
        self.input_kategoria.resize(int((10/70)*self.width),int((4/60)*self.height) )
        button_kategoria = QPushButton('Dodaj kategorie', self)
        button_kategoria.clicked.connect(self.dodaj_kategorie)
        button_kategoria.move(int((51/70)*self.width), int((44/60)*self.height))
        button_kategoria.resize(int((10/70)*self.width), int((4/60)*self.height))



        label_input_producent = QLabel(self)
        label_input_producent.setText("Producent")
        label_input_producent.move(int((17/70)*self.width),int((46/60)*self.height) )
        self.input_producent = QLineEdit(self)
        self.input_producent.move(int((15/70)*self.width), int((48/60)*self.height))
        self.input_producent.resize(int((10/70)*self.width), int((4/60)*self.height))


        label_input_ilosc = QLabel(self)
        label_input_ilosc.setText("Ilość")
        label_input_ilosc.move(int((30/70)*self.width), int((46/60)*self.height))
        self.input_ilosc = QLineEdit(self)
        self.input_ilosc.move(int((28/70)*self.width), int((48/60)*self.height))
        self.input_ilosc.resize(int((10/70)*self.width), int((4/60)*self.height))


        qbtn = QPushButton('Dodaj ', self)
        qbtn.clicked.connect(self.dodaj_sprzet)
        qbtn.move(int((51/70)*self.width),int((48/60)*self.height) )
        qbtn.resize(int((10/70)*self.width), int((4/60)*self.height))

        #self.setGeometry(0, 0, 700, 600)
        self.setWindowTitle('Dodawanie sprzetu')
    def klikniety_magazyn(self,item):
        buttonReply = QMessageBox.question(self, 'Usuwanie przedmiotu', "Czy usunąć?",QMessageBox.Yes | QMessageBox.No)
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
        self.tableWidget.setHorizontalHeaderLabels(['narzędzie', 'producent','kategoria', 'wszystkie', 'dostępne'])
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
                item0.setTextAlignment(QtCore.Qt.AlignHCenter)
                self.tableWidget.setItem(i,0,item0)

                item1 = QTableWidgetItem(str(producent))
                item1.setData(QtCore.Qt.UserRole, data)
                item1.setTextAlignment(QtCore.Qt.AlignHCenter)
                self.tableWidget.setItem(i,1,item1)

                item2 = QTableWidgetItem(str(kategoria))
                item2.setData(QtCore.Qt.UserRole, data)
                item2.setTextAlignment(QtCore.Qt.AlignHCenter)
                self.tableWidget.setItem(i,2,item2)

                item3 = QTableWidgetItem(str(ilosc_wszystkich))
                item3.setData(QtCore.Qt.UserRole, data)
                item3.setTextAlignment(QtCore.Qt.AlignHCenter)
                self.tableWidget.setItem(i,3,item3)

                item4 = QTableWidgetItem(str(dostepne))
                item4.setData(QtCore.Qt.UserRole, data)
                item4.setTextAlignment(QtCore.Qt.AlignHCenter)
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
        self.width = width_full
        self.height = height_full
        self.initUI()
        self.polaczono=0
        self.dummy=0
        self.imie_globalne=0
        self.nazwisko_globalne=0
    def initUI(self):
        label_input_narzedzie = QLabel(self)
        label_input_narzedzie.setText("Narzedzie")
        label_input_narzedzie.move(int((5/70)*self.width), int((5/60)*self.height))
        self.input_narzedzie = QLineEdit(self)
        self.input_narzedzie.move(int((5/70)*self.width),int((8/60)*self.height) )
        self.input_narzedzie.resize(int((10/70)*self.width), int((4/60)*self.height))

        label_input_producent = QLabel(self)
        label_input_producent.setText("Producent")
        label_input_producent.move(int((18/70)*self.width), int((5/60)*self.height))
        self.input_producent = QLineEdit(self)
        self.input_producent.move(int((18/70)*self.width),int((8/60)*self.height) )
        self.input_producent.resize(int((10/70)*self.width),int((4/60)*self.height) )


        self.tableWidget = QTableWidget(self)
        self.tableWidget.setRowCount(1)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.move(int((44/70)*self.width), int((5/60)*self.height))
        self.tableWidget.resize(int((23/70)*self.width),int((30/60)*self.height) )
        wiersza = QtGui.QFont("Times", 15)
        self.tableWidget.setFont(wiersza)
        nazwa_kolumny = QtGui.QFont("Times", 20, QtGui.QFont.Bold)
        self.tableWidget.horizontalHeader().setFont(nazwa_kolumny)
        self.tableWidget.setHorizontalHeaderLabels(['Imie', 'Nazwisko'])
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.itemClicked.connect(self.ustaw_imie_nazwisko)
        self.tableWidget.sortItems(0, QtCore.Qt.AscendingOrder)
        self.tableWidget.show()

        label_input_ilosc = QLabel(self)
        label_input_ilosc.setText("Ilość")
        label_input_ilosc.move(int((31/70)*self.width), int((5/60)*self.height))
        self.input_ilosc = QLineEdit(self)
        self.input_ilosc.move(int((31/70)*self.width),int((8/60)*self.height) )
        self.input_ilosc.resize(int((10/70)*self.width),int((4/60)*self.height) )

        qbtn = QPushButton('Wydaj', self)
        qbtn.clicked.connect(self.wydaj_sprzet)
        qbtn.move(int((31/70)*self.width), int((20/60)*self.height))
        qbtn.resize(int((10/70)*self.width), int((4/60)*self.height))

        #self.setGeometry(0, 0, 700, 600)
        self.setWindowTitle('Dodawanie sprzetu')
    def ustaw_imie_nazwisko(self,item):
        dane_item=item.data(QtCore.Qt.UserRole)
        self.imie_globalne=dane_item['imie']
        self.nazwisko_globalne=dane_item['nazwisko']

    def wydaj_sprzet(self):
        narzedzie = self.input_narzedzie.text()
        producent = self.input_producent.text()
        ilosc=int(self.input_ilosc.text())
        imie=self.imie_globalne
        nazwisko=self.nazwisko_globalne
        payload = {"narzedzie": narzedzie, "producent": producent,"ilosc":ilosc, "osoba_imie": imie,"osoba_nazwisko":nazwisko}
        r = requests.post(url+'wydaj/',json=payload)
        #QMessageBox.information("halko",str(r.text()))
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(r.text)
        retval = msg.exec_()
    def laduj_do_tabelki(self):
        r = requests.get(url+'wyswietl_pracownikow/')
        dane=r.json()
        self.tableWidget.clear()
        self.tableWidget.setHorizontalHeaderLabels(['imie', 'nazwisko'])
        self.tableWidget.setRowCount(len(dane['odpowiedz']))
        lista_moja=list(dane['odpowiedz'])
        #posortowana=sorted(lista_moja, key = lambda i: i['narzedzie'])
        for i in range(0,len(dane['odpowiedz'])):
            imie=str(lista_moja[i]['imie'])
            nazwisko=str(lista_moja[i]['nazwisko'])
            data = ({'imie':imie,'nazwisko':nazwisko})
            self.tableWidget.setSortingEnabled(False)
            item0 = QTableWidgetItem(str(imie))
            item0.setData(QtCore.Qt.UserRole, data)
            item0.setTextAlignment(QtCore.Qt.AlignHCenter)
            self.tableWidget.setItem(i,0,item0)

            item1 = QTableWidgetItem(str(nazwisko))
            item1.setData(QtCore.Qt.UserRole, data)
            item1.setTextAlignment(QtCore.Qt.AlignHCenter)
            self.tableWidget.setItem(i,1,item1)
            self.tableWidget.setSortingEnabled(True)
class Ludzie(QWidget):
    def __init__(self):
        super().__init__()
        self.width = width_full
        self.height = height_full
        self.initUI()
        self.polaczono=0
        self.dummy=0

    def initUI(self):

        self.tableWidget = QTableWidget(self)
        self.tableWidget.setRowCount(1)
        self.tableWidget.setColumnCount(4)
        self.tableWidget.move(int((30/70)*self.width), int((5/60)*self.height))
        self.tableWidget.resize(int((35/70)*self.width),int((30/60)*self.height) )
        wiersza = QtGui.QFont("Times", 15)
        self.tableWidget.setFont(wiersza)
        nazwa_kolumny = QtGui.QFont("Times", 20, QtGui.QFont.Bold)
        self.tableWidget.horizontalHeader().setFont(nazwa_kolumny)
        self.tableWidget.setHorizontalHeaderLabels(['narzedzie', 'producent', 'ilosc', 'data wydania'])
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.itemClicked.connect(self.kliknieta_tabela)
        self.tableWidget.sortItems(0, QtCore.Qt.AscendingOrder)
        self.tableWidget.show()


        self.tableWidget_imie_nazwisko = QTableWidget(self)
        self.tableWidget_imie_nazwisko.setRowCount(1)
        self.tableWidget_imie_nazwisko.setColumnCount(2)
        self.tableWidget_imie_nazwisko.move(int((5/70)*self.width), int((5/60)*self.height))
        self.tableWidget_imie_nazwisko.resize(int((23/70)*self.width),int((30/60)*self.height) )
        wiersza = QtGui.QFont("Times", 15)
        self.tableWidget_imie_nazwisko.setFont(wiersza)
        nazwa_kolumny = QtGui.QFont("Times", 20, QtGui.QFont.Bold)
        self.tableWidget_imie_nazwisko.horizontalHeader().setFont(nazwa_kolumny)
        self.tableWidget_imie_nazwisko.setHorizontalHeaderLabels(['imie', 'nazwisko'])
        self.tableWidget_imie_nazwisko.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget_imie_nazwisko.itemClicked.connect(self.szukaj_pracownika)
        self.tableWidget_imie_nazwisko.sortItems(0, QtCore.Qt.AscendingOrder)
        self.tableWidget_imie_nazwisko.show()


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
            self.szukaj_pracownika(item)
    def laduj_pracownikow(self):
        r = requests.get(url+'wyswietl_pracownikow/')
        dane=r.json()
        self.tableWidget_imie_nazwisko.clear()
        self.tableWidget_imie_nazwisko.setHorizontalHeaderLabels(['imie', 'nazwisko'])
        self.tableWidget_imie_nazwisko.setRowCount(len(dane['odpowiedz']))
        lista_moja=list(dane['odpowiedz'])
        #posortowana=sorted(lista_moja, key = lambda i: i['narzedzie'])
        for i in range(0,len(dane['odpowiedz'])):
            imie=str(lista_moja[i]['imie'])
            nazwisko=str(lista_moja[i]['nazwisko'])
            data = ({'osoba_imie':imie,'osoba_nazwisko':nazwisko})
            self.tableWidget_imie_nazwisko.setSortingEnabled(False)
            item0 = QTableWidgetItem(str(imie))
            item0.setData(QtCore.Qt.UserRole, data)
            item0.setTextAlignment(QtCore.Qt.AlignHCenter)
            self.tableWidget_imie_nazwisko.setItem(i,0,item0)

            item1 = QTableWidgetItem(str(nazwisko))
            item1.setData(QtCore.Qt.UserRole, data)
            item1.setTextAlignment(QtCore.Qt.AlignHCenter)
            self.tableWidget_imie_nazwisko.setItem(i,1,item1)
            self.tableWidget_imie_nazwisko.setSortingEnabled(True)
    def szukaj_pracownika(self,item):
        dane_item=item.data(QtCore.Qt.UserRole)

        payload = {"osoba_imie": dane_item['osoba_imie'], "osoba_nazwisko": dane_item['osoba_nazwisko']}
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
            data = ({'narzedzie':narzedzie,'producent':producent,'osoba_imie':dane_item['osoba_imie'],'osoba_nazwisko':dane_item['osoba_nazwisko'],'ilosc':ilosc})
            self.tableWidget.setSortingEnabled(False)
            item0 = QTableWidgetItem(str(narzedzie))
            item0.setData(QtCore.Qt.UserRole, data)
            item0.setTextAlignment(QtCore.Qt.AlignHCenter)
            self.tableWidget.setItem(i,0,item0)

            item1 = QTableWidgetItem(str(producent))
            item1.setData(QtCore.Qt.UserRole, data)
            item1.setTextAlignment(QtCore.Qt.AlignHCenter)
            self.tableWidget.setItem(i,1,item1)

            item2 = QTableWidgetItem(str(ilosc))
            item2.setData(QtCore.Qt.UserRole, data)
            item2.setTextAlignment(QtCore.Qt.AlignHCenter)
            self.tableWidget.setItem(i,2,item2)

            item3 = QTableWidgetItem(str(data_nowa.day)+'-'+str(data_nowa.month)+'-'+str(data_nowa.year))
            item3.setData(QtCore.Qt.UserRole, data)
            item3.setTextAlignment(QtCore.Qt.AlignHCenter)
            self.tableWidget.setItem(i,3,item3)
            self.tableWidget.setSortingEnabled(True)

class Po_kategorii(QWidget):
    def __init__(self,parent):
        super().__init__()
        self.width = width_full
        self.height = height_full
        self.initUI()
        self.polaczono=0
        self.dummy=0
        self.kategoria_wyszukiwanie=0

    def initUI(self):


        self.combo_wyszukiwanie = QComboBox(self)
        self.combo_wyszukiwanie.resize(int((1/7)*self.width),int((4/60)*self.height))
        self.combo_wyszukiwanie.move(int((1/7)*self.width),int((8/60)*self.height) )
        self.combo_wyszukiwanie.currentIndexChanged.connect(self.zmiana_combo)
        self.combo_wyszukiwanie.show()

        self.tableWidget = QTableWidget(self)
        self.tableWidget.setRowCount(4)
        self.tableWidget.setColumnCount(4)
        wiersza = QtGui.QFont("Times", 15)
        self.tableWidget.setFont(wiersza)
        nazwa_kolumny = QtGui.QFont("Times", 20, QtGui.QFont.Bold)
        self.tableWidget.horizontalHeader().setFont(nazwa_kolumny)
        self.tableWidget.resize(int((43/70)*self.width),int((30/60)*self.height))
        self.tableWidget.move(int((25/70)*self.width), int((5/60)*self.height))
        self.tableWidget.setHorizontalHeaderLabels(['narzedzie', 'producent', 'wszystkie', 'dostepne'])
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.itemClicked.connect(self.clicked_table)
        self.tableWidget.sortItems(0, QtCore.Qt.AscendingOrder)
        self.tableWidget.show()
        self.dodaj_combo()
        self.laduj_itemki()


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
            item0.setTextAlignment(QtCore.Qt.AlignHCenter)
            self.tableWidget.setItem(i,0,item0)

            item1 = QTableWidgetItem(str(producent))
            item1.setData(QtCore.Qt.UserRole, data)
            item1.setTextAlignment(QtCore.Qt.AlignHCenter)
            self.tableWidget.setItem(i,1,item1)

            item2 = QTableWidgetItem(str(ilosc_wszystkich))
            item2.setData(QtCore.Qt.UserRole, data)
            item2.setTextAlignment(QtCore.Qt.AlignHCenter)
            self.tableWidget.setItem(i,2,item2)

            item3 = QTableWidgetItem(str(dostepne))
            item3.setData(QtCore.Qt.UserRole, data)
            item3.setTextAlignment(QtCore.Qt.AlignHCenter)
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
class Dodaj_pracownika(QWidget):
    def __init__(self,parent):
        super().__init__()
        self.width = width_full
        self.height = height_full
        self.initUI()
        self.polaczono=0
        self.dummy=0


    def initUI(self):

        label_input_imie = QLabel(self)
        label_input_imie.setText("Imie")
        label_input_imie.move(int((1/70)*self.width), int((5/60)*self.height))
        self.input_imie = QLineEdit(self)
        self.input_imie.move(int((1/70)*self.width),int( (8/60)*self.height))
        self.input_imie.resize(int((10/70)*self.width),int((4/60)*self.height) )


        label_input_nazwisko = QLabel(self)
        label_input_nazwisko.setText("Nazwisko")
        label_input_nazwisko.move(int((14/70)*self.width),int((5/60)*self.height) )
        self.input_nazwisko = QLineEdit(self)
        self.input_nazwisko.move(int((14/70)*self.width),int((8/60)*self.height) )
        self.input_nazwisko.resize(int((10/70)*self.width),int((4/60)*self.height) )

        label_input_zawod = QLabel(self)
        label_input_zawod.setText("Zawód")
        label_input_zawod.move(int((27/70)*self.width),int((5/60)*self.height) )
        self.input_zawod = QLineEdit(self)
        self.input_zawod.move(int((27/70)*self.width),int((8/60)*self.height) )
        self.input_zawod.resize(int((10/70)*self.width),int((4/60)*self.height) )

        guzik = QPushButton('Dodaj', self)
        guzik.clicked.connect(self.dodaj_pracownika)
        guzik.move(int((14/70)*self.width), int((20/60)*self.height))
        guzik.resize(int((10/70)*self.width),int( (4/60)*self.height))

        self.tableWidget = QTableWidget(self)
        self.tableWidget.setRowCount(4)
        self.tableWidget.setColumnCount(3)
        wiersza = QtGui.QFont("Times", 15)
        self.tableWidget.setFont(wiersza)
        nazwa_kolumny = QtGui.QFont("Times", 20, QtGui.QFont.Bold)
        self.tableWidget.horizontalHeader().setFont(nazwa_kolumny)
        self.tableWidget.resize(int((30/70)*self.width),int((30/60)*self.height))
        self.tableWidget.move(int((38/70)*self.width), int((5/60)*self.height))
        self.tableWidget.setHorizontalHeaderLabels(['imie', 'nazwisko', 'zawod'])
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.itemClicked.connect(self.clicked_table)
        self.tableWidget.sortItems(0, QtCore.Qt.AscendingOrder)
        self.tableWidget.show()
        self.laduj_itemki()


        self.setWindowTitle('Dodaj pracownika')
    def clicked_table(self,item):
        buttonReply = QMessageBox.question(self, 'Usuwanie pracownika', "Czy usunąć?",QMessageBox.Yes | QMessageBox.No)
        dane=item.data(QtCore.Qt.UserRole)
        if buttonReply == QMessageBox.Yes:
         #tu usuwamy
            imie=dane['imie']
            nazwisko=dane['nazwisko']
            zawod=dane['zawod']
            payload = {"imie": imie, "nazwisko": nazwisko,"zawod":zawod}
            r = requests.post(url+'usun_pracownika_nowego/',json=payload)
            self.laduj_itemki()
    def dodaj_do_tabeli(self,dane):

        #dodac sortowanie
        self.tableWidget.clear()
        self.tableWidget.setHorizontalHeaderLabels(['imie', 'nazwisko', 'zawod'])
        self.tableWidget.setRowCount(len(dane['odpowiedz']))
        lista_moja=list(dane['odpowiedz'])
        for i in range(0,len(dane['odpowiedz'])):
            imie=str(lista_moja[i]['imie'])
            nazwisko=str(lista_moja[i]['nazwisko'])
            zawod=str(lista_moja[i]['zawod'])
            data = ({'imie':imie,'nazwisko':nazwisko,'zawod':zawod})

            self.tableWidget.setSortingEnabled(False)
            item0 = QTableWidgetItem(str(imie))
            item0.setData(QtCore.Qt.UserRole, data)
            item0.setTextAlignment(QtCore.Qt.AlignHCenter)
            self.tableWidget.setItem(i,0,item0)

            item1 = QTableWidgetItem(str(nazwisko))
            item1.setData(QtCore.Qt.UserRole, data)
            item1.setTextAlignment(QtCore.Qt.AlignHCenter)
            self.tableWidget.setItem(i,1,item1)

            item2 = QTableWidgetItem(str(zawod))
            item2.setData(QtCore.Qt.UserRole, data)
            item2.setTextAlignment(QtCore.Qt.AlignHCenter)
            self.tableWidget.setItem(i,2,item2)


    def dodaj_pracownika(self):
        imie=self.input_imie.text()
        immie=imie.replace(" ","")
        immmie=immie.lower()
        nazwisko=self.input_nazwisko.text()
        nazzwisko=nazwisko.replace(" ","")
        nazzzwisko=nazzwisko.lower()
        zawod=self.input_zawod.text()
        zawwod=zawod.replace(" ","")
        zawwwod=zawwod.lower()
        payload = {"imie": immmie,"nazwisko": nazzzwisko,"zawod": zawwwod}
        r = requests.post(url+'dodaj_pracownika_nowego/',json=payload)
        self.laduj_itemki()
    def laduj_itemki(self):
        r = requests.get(url+'wyswietl_pracownikow/')
        dane=r.json()
        self.dodaj_do_tabeli(dane)
class Obiegowka(QWidget):
    def __init__(self,parent):
        super().__init__()
        self.width = width_full
        self.height = height_full
        self.initUI()
        self.polaczono=0
        self.dummy=0


    def initUI(self):




        self.tableWidget = QTableWidget(self)
        self.tableWidget.setRowCount(4)
        self.tableWidget.setColumnCount(3)
        wiersza = QtGui.QFont("Times", 15)
        self.tableWidget.setFont(wiersza)
        nazwa_kolumny = QtGui.QFont("Times", 20, QtGui.QFont.Bold)
        self.tableWidget.horizontalHeader().setFont(nazwa_kolumny)
        self.tableWidget.resize(int((30/70)*self.width),int((30/60)*self.height))
        self.tableWidget.move(int((38/70)*self.width), int((5/60)*self.height))
        self.tableWidget.setHorizontalHeaderLabels(['imie', 'nazwisko', 'zawod'])
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.itemClicked.connect(self.generuj)
        self.tableWidget.sortItems(0, QtCore.Qt.AscendingOrder)
        self.tableWidget.show()
        self.laduj_itemki()


        self.setWindowTitle('Generowanie obiegówki')
    def generuj(self,item):
        buttonReply = QMessageBox.question(self, 'Generowanie obiegówki', "Czy wygenerować?",QMessageBox.Yes | QMessageBox.No)
        dane=item.data(QtCore.Qt.UserRole)
        if buttonReply == QMessageBox.Yes:
         #tu usuwamy
            imie=dane['imie']
            nazwisko=dane['nazwisko']
            zawod=dane['zawod']
            email='olena-vasylevska@wp.pl'
            payload = {"imie": imie, "nazwisko": nazwisko,"zawod":zawod,"email":email}
            r = requests.post(url+'obiegowka/',json=payload)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText(r.text)
            retval = msg.exec_()
    def dodaj_do_tabeli(self,dane):

        #dodac sortowanie
        self.tableWidget.clear()
        self.tableWidget.setHorizontalHeaderLabels(['imie', 'nazwisko', 'zawod'])
        self.tableWidget.setRowCount(len(dane['odpowiedz']))
        lista_moja=list(dane['odpowiedz'])
        for i in range(0,len(dane['odpowiedz'])):
            imie=str(lista_moja[i]['imie'])
            nazwisko=str(lista_moja[i]['nazwisko'])
            zawod=str(lista_moja[i]['zawod'])
            data = ({'imie':imie,'nazwisko':nazwisko,'zawod':zawod})

            self.tableWidget.setSortingEnabled(False)
            item0 = QTableWidgetItem(str(imie))
            item0.setData(QtCore.Qt.UserRole, data)
            item0.setTextAlignment(QtCore.Qt.AlignHCenter)
            self.tableWidget.setItem(i,0,item0)

            item1 = QTableWidgetItem(str(nazwisko))
            item1.setData(QtCore.Qt.UserRole, data)
            item1.setTextAlignment(QtCore.Qt.AlignHCenter)
            self.tableWidget.setItem(i,1,item1)

            item2 = QTableWidgetItem(str(zawod))
            item2.setData(QtCore.Qt.UserRole, data)
            item2.setTextAlignment(QtCore.Qt.AlignHCenter)
            self.tableWidget.setItem(i,2,item2)

    def laduj_itemki(self):
        r = requests.get(url+'wyswietl_pracownikow/')
        dane=r.json()
        self.dodaj_do_tabeli(dane)





class Glowne(QWidget):
    def __init__(self):
        super().__init__()
        self.width = width_full
        self.height = height_full
        self.initUI()
        self.polaczono=0
        self.dummy=0




    def initUI(self):
        #700x600

        qbtn = QPushButton('Pokaż sprzęt', self)
        qbtn.clicked.connect(self.guzik_sprzet)
        #qbtn.resize(int((1/8)*self.width),int((5/60)*self.height))
        qbtn.move(int(self.width*(2/70)),int((7/60)*self.height) )




        guzik_ludzie = QPushButton('Szukaj pracowników ', self)
        guzik_ludzie.clicked.connect(self.guzik_patrz_ludzi)
        #guzik_ludzie.resize(int((1/8)*self.width),int((5/60)*self.height))
        guzik_ludzie.move(int((14/70)*self.width),int( (7/60)*self.height))

        guzik_wydaj = QPushButton('Wydaj sprzęt ', self)
        guzik_wydaj.clicked.connect(self.guzik_kliknij_wydaj)
        #guzik_wydaj.resize(int((1/8)*self.width),int((5/60)*self.height))
        guzik_wydaj.move(int((27/70)*self.width), int((7/60)*self.height))

        guzik_po_kategorii = QPushButton('Pokaż kategorie', self)
        guzik_po_kategorii.clicked.connect(self.guzik_kliknij_po_kategorii)
        #guzik_po_kategorii.resize(int((1/8)*self.width),int((5/60)*self.height))
        guzik_po_kategorii.move(int((40/70)*self.width), int((7/60)*self.height))

        guzik_dodaj_pracownika = QPushButton('Dodaj pracowników', self)
        guzik_dodaj_pracownika.clicked.connect(self.guzik_dodaj_pracownik)
        #guzik_dodaj_pracownika.resize(int((1/8)*self.width),int((5/60)*self.height))
        guzik_dodaj_pracownika.move(int((53/70)*self.width), int((7/60)*self.height))

        guzik_obiegowka = QPushButton('Obiegówka   ', self)
        guzik_obiegowka.clicked.connect(self.daj_obiegowke)
        #guzik_obiegowka.resize(int((1/8)*self.width),int((5/60)*self.height))
        guzik_obiegowka.move(int((27/70)*self.width), int((15/60)*self.height))




        #self.setGeometry(0, 0, 700, 600)
        self.setWindowTitle('Główne okno')
        #self.show()
    def guzik_sprzet(self):

        self.sprzet = Sprzet()
        self.sprzet.laduj()
        guzik_styl = QtGui.QFont("Times", 20, QtGui.QFont.Bold)
        self.sprzet.setFont(guzik_styl)
        self.sprzet.showMaximized()
    def guzik_kliknij_po_kategorii(self):
        self.po_kategorii = Po_kategorii(self)
        guzik_styl = QtGui.QFont("Times", 20, QtGui.QFont.Bold)
        self.po_kategorii.setFont(guzik_styl)
        self.po_kategorii.showMaximized()
        self.po_kategorii.dodaj_combo()
    def guzik_dodaj_pracownik(self):
        self.pracownik = Dodaj_pracownika(self)
        guzik_styl = QtGui.QFont("Times", 20, QtGui.QFont.Bold)
        self.pracownik.setFont(guzik_styl)
        self.pracownik.showMaximized()
    def guzik_patrz_ludzi(self):
        self.ludzie = Ludzie()
        guzik_styl = QtGui.QFont("Times", 20, QtGui.QFont.Bold)
        self.ludzie.setFont(guzik_styl)
        self.ludzie.showMaximized()
        self.ludzie.laduj_pracownikow()
    def guzik_kliknij_wydaj(self):
        self.wydaj = Wydaj(self)
        guzik_styl = QtGui.QFont("Times", 20, QtGui.QFont.Bold)
        self.wydaj.setFont(guzik_styl)
        self.wydaj.showMaximized()
        self.wydaj.laduj_do_tabelki()
    def daj_obiegowke(self):
        self.obiegowka = Obiegowka(self)
        guzik_styl = QtGui.QFont("Times", 20, QtGui.QFont.Bold)
        self.obiegowka.setFont(guzik_styl)
        self.obiegowka.showMaximized()
        self.obiegowka.laduj_itemki()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    palette = QPalette()
    palette.setColor(QPalette.Button, QtCore.Qt.green)
    app.setPalette(palette)
    sz=app.primaryScreen().size()
    global width_full
    width_full=sz.width()
    global height_full
    height_full=sz.height()

    ex = Glowne()
    guzik_styl = QtGui.QFont("Times", 20, QtGui.QFont.Bold)
    ex.setFont(guzik_styl)
    ex.showMaximized()






    sys.exit(app.exec_())
