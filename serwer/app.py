from flask import Flask,request,jsonify
from flask_restful import Resource,Api
from pymongo import MongoClient
from random import randint
from pprint import pprint
from datetime import datetime
client = MongoClient("mongodb+srv://nikita3331:babcia2@cluster0-lgk9o.mongodb.net/test?retryWrites=true&w=majority" ,connectTimeoutMS=30000, socketTimeoutMS=None, connect=False, maxPoolsize=1)
db=client.magazyn


#tutaj odbieramy zapytania z telefonu i mu je wysylamy z bazy


app=Flask(__name__)
api=Api(app)
class Dodaj(Resource):
    def post(self):
        json_data = request.get_json()
        narzedzie = json_data['narzedzie']
        ilosc = int(json_data['ilosc'])
        producent = json_data['producent']
        odpowiedz=db.magazyn.find( { "narzedzie":narzedzie ,"producent":producent } )
        myresults = list(odpowiedz)

        if len(myresults)>0:
            moje_wartosci_nowe=[]
            for i in myresults:
                 moje_wartosci_nowe.append({'narzedzie':i['narzedzie'],'producent':i['producent'],'ilosc_wszystkich':i['ilosc_wszystkich']})
            liczba_wydanych_baza=int(moje_wartosci_nowe[0]['ilosc_wszystkich'])
            lacznie=liczba_wydanych_baza+ilosc
            db.magazyn.update_one( { "narzedzie":narzedzie ,"producent":producent } ,{'$set':{"ilosc_wszystkich" :lacznie}})
        else:
            db.magazyn.insert_one({"narzedzie": narzedzie, "ilosc_wszystkich" :ilosc, "producent": producent,"ilosc_wydanych":0,"data":datetime.now()})
        return {'dodalismy':'wszystko'},201
class Usun(Resource):
    def get(self):
        return {'tu wysylamy':'post'}
    def post(self):
        json_data = request.get_json()
        narzedzie = json_data['narzedzie']
        ilosc = int(json_data['ilosc'])
        producent = json_data['producent']
        odpowiedz=db.magazyn.find( { "narzedzie":narzedzie ,"producent":producent } )
        moje_wartosci=[]
        myresults = list(odpowiedz)
        for i in myresults:
            moje_wartosci.append({'narzedzie':i['narzedzie'],'producent':i['producent'],'ilosc_wszystkich':i['ilosc_wszystkich']})
        if int(moje_wartosci[0]['ilosc_wszystkich'])>ilosc:
            wstaw=int(moje_wartosci[0]['ilosc_wszystkich'])-ilosc
            db.magazyn.update_one( { "narzedzie":narzedzie ,"producent":producent } ,{'$set':{"ilosc_wszystkich" :wstaw}})
            return {'usunelismy':ilosc},201
        elif int(moje_wartosci[0]['ilosc_wszystkich'])==ilosc:
            db.magazyn.delete_one( { "narzedzie":narzedzie ,"producent":producent } )
            return {'usunelismy':'wszystko'},201
        else:
            return {'za duzo':'do usuniecia'},201

class Szukaj(Resource):
    def get(self):
        json_data = request.get_json()
        narzedzie = json_data['narzedzie']
        ilosc = json_data['ilosc']
        producent = json_data['producent']
        odpowiedz=db.magazyn.find( { "narzedzie":narzedzie ,"producent":producent } )
        myresults = list(odpowiedz)
        moje_wartosci=[]
        for i in myresults:
            moje_wartosci.append({'narzedzie':i['narzedzie'],'producent':i['producent']})
        return {'odpowiedz':moje_wartosci},201
    def post(self):
        return {'tu wysylamy':'get'},201
class Wydaj(Resource): #do poporawy
    def post(self):
        json_data = request.get_json()
        narzedzie = json_data['narzedzie']
        ilosc = json_data['ilosc']
        producent = json_data['producent']
        osoba_imie = json_data['osoba_imie']
        osoba_nazwisko = json_data['osoba_nazwisko']

        odpowiedz=db.magazyn.find( { "narzedzie":narzedzie ,"producent":producent } )
        # myresults = list(odpowiedz) #patrzymy ile ich jest w naszej bazie
        # moje_wartosci=[]
        # for i in myresults:
        #     moje_wartosci.append({'narzedzie':i['narzedzie'],'producent':i['producent']})
        #liczba_wszystkich=len(moje_wartosci)
        moje_wartosci_nowe=[]
        myresults = list(odpowiedz)
        if len(myresults)>0:
            for i in myresults:
                 moje_wartosci_nowe.append({'narzedzie':i['narzedzie'],'producent':i['producent'],'ilosc_wszystkich':i['ilosc_wszystkich'],'ilosc_wydanych':i['ilosc_wydanych']})

        liczba_wszystkich=int(moje_wartosci_nowe[0]['ilosc_wszystkich'])
        liczba_wydanych=int(moje_wartosci_nowe[0]['ilosc_wydanych'])
        liczba_dostepnych=liczba_wszystkich-liczba_wydanych
        # odpowiedz_nowa=db.wydanie.find( { "narzedzie":narzedzie ,"producent":producent } )
        # myresults_nowe = list(odpowiedz_nowa) #patrzymy ile ich jest w naszej bazie
        # moje_wartosci_nowe=[]
        # for i in myresults_nowe:
        #     moje_wartosci_nowe.append({'narzedzie':i['narzedzie'],'producent':i['producent']})
        # liczba_wydanych=len(moje_wartosci_nowe)
        # liczba_dostepnych=liczba_wszystkich-liczba_wydanych
        # if int(ilosc)<=liczba_dostepnych:
        #     for i in range(0,int(ilosc)):
        #         db.wydanie.insert_one( { "narzedzie":narzedzie ,"producent":producent ,"ilosc":1,"osoba_imie":osoba_imie,"osoba_nazwisko":osoba_nazwisko,"data":datetime.now()} )
        #     return {'odpowiedz':'wydalismy'},201
        # else:
        #     return {'odpowiedz':'nie udalo sie wydac'},201

        if int(ilosc)<=liczba_dostepnych:
            suma=liczba_wydanych+int(ilosc)
            db.magazyn.update_one( { "narzedzie":narzedzie ,"producent":producent } ,{'$set':{"ilosc_wydanych" :suma}})
            db.wydanie.insert_one( { "narzedzie":narzedzie ,"producent":producent ,"ilosc":int(ilosc),"osoba_imie":osoba_imie,"osoba_nazwisko":osoba_nazwisko,"data":datetime.now()} )
            return {'odpowiedz':'wydalismy'},201
        else:
            return {'odpowiedz':'nie udalo sie wydac'},201
    def get(self):
        return {'tu wysylamy':'post'},201
class Usun_wydanie(Resource):
    def post(self):
        json_data = request.get_json()
        narzedzie = json_data['narzedzie']
        ilosc = json_data['ilosc']
        producent = json_data['producent']
        osoba_imie = json_data['osoba_imie']
        osoba_nazwisko = json_data['osoba_nazwisko']


        # odpowiedz_nowa=db.wydanie.find( { "narzedzie":narzedzie ,"producent":producent } )
        # myresults_nowe = list(odpowiedz_nowa) #patrzymy ile ich jest w naszej bazie
        # moje_wartosci_nowe=[]
        # for i in myresults_nowe:
        #     moje_wartosci_nowe.append({'narzedzie':i['narzedzie'],'producent':i['producent']})
        # liczba_wydanych=len(moje_wartosci_nowe)
        # if int(ilosc)<=liczba_wydanych:
        #     for i in range(0,int(ilosc)):
        #         db.wydanie.delete_one( { "narzedzie":narzedzie ,"producent":producent ,"ilosc":1,"osoba_imie":osoba_imie,"osoba_nazwisko":osoba_nazwisko} )
        #     return {'odpowiedz':'wydalismy'},201
        # else:
        #     return {'odpowiedz':'nie udalo sie wydac'},201

        odpowiedz_nowa=db.wydanie.find( { "narzedzie":narzedzie ,"producent":producent ,"osoba_imie":osoba_imie,"osoba_nazwisko":osoba_nazwisko} )
        myresults_nowe = list(odpowiedz_nowa) #patrzymy ile ich jest w naszej bazie
        moje_wartosci_nowe=[]
        if len(myresults_nowe)>0:
            for i in myresults_nowe:
                 moje_wartosci_nowe.append({'narzedzie':i['narzedzie'],'producent':i['producent'],'ilosc':i['ilosc']})
        liczba_wydanych=int(moje_wartosci_nowe[0]['ilosc'] )

        odpowiedz=db.magazyn.find( { "narzedzie":narzedzie ,"producent":producent } )
        myresults_noweczka = list(odpowiedz)
        moje_wart=[]
        if len(myresults_noweczka)>0:
            for i in myresults_noweczka:
                 moje_wart.append({'narzedzie':i['narzedzie'],'producent':i['producent'],'ilosc_wydanych':i['ilosc_wydanych']})

        liczba_wydanych_wszystkim=int(moje_wart[0]['ilosc_wydanych'])
        roznica=liczba_wydanych_wszystkim-liczba_wydanych
        db.magazyn.update_one( { "narzedzie":narzedzie ,"producent":producent } ,{'$set':{"ilosc_wydanych" :roznica}})
        db.wydanie.delete_one( { "narzedzie":narzedzie ,"producent":producent ,"osoba_imie":osoba_imie,"osoba_nazwisko":osoba_nazwisko} )
        return {'odpowiedz':'usunelismy wydanie'},201
    def get(self):
        return {'tu wysylamy':'post'},201

class Wydane_osobie(Resource):
    def post(self):
        json_data = request.get_json()
        osoba_imie = json_data['osoba_imie']
        osoba_nazwisko = json_data['osoba_nazwisko']

        odpowiedz=db.wydanie.find( { "osoba_imie":osoba_imie ,"osoba_nazwisko":osoba_nazwisko } )
        myresults = list(odpowiedz) #patrzymy ile ich jest w naszej bazie
        moje_wartosci=[]
        for i in myresults:
            moje_wartosci.append({'narzedzie':i['narzedzie'],'producent':i['producent'],'data':i['data'].isoformat()})
        return {'odpowiedz':moje_wartosci},201
    def get(self):
        return {'tu wysylamy':'post'},201
class zobacz_wszystkie(Resource):
    def post(self):
        odpowiedz=db.magazyn.find()
        myresults = list(odpowiedz) #patrzymy ile ich jest w naszej bazie
        moje_wartosci=[]
        for i in myresults:
            moje_wartosci.append({'narzedzie':i['narzedzie'],'producent':i['producent'],'ilosc_wszystkich':i['ilosc_wszystkich'],'ilosc_wydanych':i['ilosc_wydanych'],'data':i['data'].isoformat()})
        return {'odpowiedz':moje_wartosci},201
    def get(self):
        return {'tu wysylamy':'post'},201
class kategorie(Resource):
    def post(self): #dodajemy
        json_data = request.get_json()
        narzedzie = json_data['narzedzie']
        ilosc = json_data['ilosc']
        producent = json_data['producent']
        osoba_imie = json_data['osoba_imie']
        osoba_nazwisko = json_data['osoba_nazwisko']
        odpowiedz=db.magazyn.find()
        myresults = list(odpowiedz) #patrzymy ile ich jest w naszej bazie
        moje_wartosci=[]
        for i in myresults:
            moje_wartosci.append({'narzedzie':i['narzedzie'],'producent':i['producent'],'ilosc_wszystkich':i['ilosc_wszystkich'],'ilosc_wydanych':i['ilosc_wydanych'],'data':i['data'].isoformat()})
        return {'odpowiedz':moje_wartosci},201
    def get(self): #odbieramy
        narzedzie = "kategorie"
        producent = "kategorie"
        odpowiedz=db.magazyn.find( { "narzedzie":narzedzie ,"producent":producent } )
        myresults = list(odpowiedz) #patrzymy ile ich jest w naszej bazie
        moje_wartosci=[]
        for i in myresults:
            moje_wartosci.append({'kategorie':i['kategorie']})
        return {'odpowiedz':moje_wartosci},201





api.add_resource(Dodaj,'/dodaj/')
api.add_resource(Usun,'/usun/')
api.add_resource(Szukaj,'/szukaj/')
api.add_resource(Wydaj,'/wydaj/')
api.add_resource(Usun_wydanie,'/usun_wydanie/')
api.add_resource(Wydane_osobie,'/wydane_osobie/')
api.add_resource(zobacz_wszystkie,'/zobacz_wszystkie/')
api.add_resource(kategorie,'/kategorie/')



if __name__=='__main__':
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)
