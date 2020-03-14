from flask import Flask,request,jsonify
from flask_restful import Resource,Api
from pymongo import MongoClient
from random import randint
from pprint import pprint
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
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
        kategoria = json_data['kategoria']
        odpowiedz=db.magazyn.find( { "narzedzie":narzedzie ,"producent":producent,"kategoria":kategoria } )
        myresults = list(odpowiedz)
        ## szukamy czy jest juz taka kategoria

        if len(myresults)>0: #zwiekszamy ilosc jesli juz jest
            moje_wartosci_nowe=[]
            for i in myresults:
                 moje_wartosci_nowe.append({'narzedzie':i['narzedzie'],'producent':i['producent'],'ilosc_wszystkich':i['ilosc_wszystkich']})
            liczba_wydanych_baza=int(moje_wartosci_nowe[0]['ilosc_wszystkich'])
            lacznie=liczba_wydanych_baza+ilosc
            db.magazyn.update_one( { "narzedzie":narzedzie ,"producent":producent } ,{'$set':{"ilosc_wszystkich" :lacznie}})
        else: #dodajemy jesli nie ma w bazie
            db.magazyn.insert_one({"narzedzie": narzedzie, "ilosc_wszystkich" :ilosc,"kategoria":kategoria,"producent": producent,"ilosc_wydanych":0,"data":datetime.now()})

        return {'dodalismy':'wszystko'},201
class Usun(Resource):
    def get(self):
        return {'tu wysylamy':'post'}
    def post(self):
        json_data = request.get_json()
        narzedzie = json_data['narzedzie']
        ilosc = int(json_data['ilosc'])
        producent = json_data['producent']
        kategoria=json_data['kategoria']
        odpowiedz=db.magazyn.find( { "narzedzie":narzedzie ,"producent":producent,"kategoria":kategoria } )
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
            moje_wartosci.append({'narzedzie':i['narzedzie'],'producent':i['producent'],'data':i['data'].isoformat(),'ilosc':i['ilosc']})
        return {'odpowiedz':moje_wartosci},201
    def get(self):
        return {'tu wysylamy':'post'},201
class zobacz_wszystkie(Resource):
    def post(self):
        odpowiedz=db.magazyn.find()
        myresults = list(odpowiedz) #patrzymy ile ich jest w naszej bazie
        moje_wartosci=[]
        for i in myresults:
            moje_wartosci.append({'narzedzie':i['narzedzie'],'producent':i['producent'],'kategoria':i['kategoria'],'ilosc_wszystkich':i['ilosc_wszystkich'],'ilosc_wydanych':i['ilosc_wydanych'],'data':i['data'].isoformat()})
        return {'odpowiedz':moje_wartosci},201
    def get(self):
        return {'tu wysylamy':'post'},201
class zobacz_po_kategorii(Resource):
    def post(self):
        json_data = request.get_json()
        kategoria = json_data['kategoria']
        odpowiedz=db.magazyn.find({'kategoria':kategoria})
        myresults = list(odpowiedz) #patrzymy ile ich jest w naszej bazie
        moje_wartosci=[]
        for i in myresults:
            moje_wartosci.append({'narzedzie':i['narzedzie'],'producent':i['producent'],'kategoria':i['kategoria'],'ilosc_wszystkich':i['ilosc_wszystkich'],'ilosc_wydanych':i['ilosc_wydanych'],'data':i['data'].isoformat()})
        return {'odpowiedz':moje_wartosci},201
    def get(self):
        return {'tu wysylamy':'post'},201
class kategorie(Resource):
    def post(self): #dodajemy
        json_data = request.get_json()
        kategoria = json_data['kategoria']
        kat_fetched=db.magazyn.find( { "narzedzie":"kategorie" ,"producent":"kategorie"} )
        myresults = list(kat_fetched) #patrzymy ile ich jest w naszej bazie
        moje_wartosci=[]
        for i in myresults:
             moje_wartosci.append({'wszystko':i['kategorie']})
        nasze_kategorie=list(moje_wartosci[0]['wszystko'])
        if str(kategoria) not in nasze_kategorie:
            nasze_kategorie.append(str(kategoria))
            db.magazyn.update_one(  { "narzedzie":"kategorie" ,"producent":"kategorie"} ,{'$set':{"kategorie" :nasze_kategorie}})

        catcat=str(kategoria)
        return {'dodalismy':catcat},201
    def get(self): #odbieramy
        narzedzie = "kategorie"
        producent = "kategorie"
        odpowiedz=db.magazyn.find( { "narzedzie":narzedzie ,"producent":producent } )
        myresults = list(odpowiedz) #patrzymy ile ich jest w naszej bazie
        moje_wartosci=[]
        for i in myresults:
            moje_wartosci.append({'kategorie':i['kategorie']})
        return {'odpowiedz':moje_wartosci},201
class Dodaj_pracownika_nowego(Resource):
    def post(self):
        json_data = request.get_json()
        imie = json_data['imie']
        nazwisko = json_data['nazwisko']
        zawod = json_data['zawod']
        odpowiedz=db.pracownicy.find( { "imie":imie ,"nazwisko":nazwisko,"zawod":zawod} )
        myresults = list(odpowiedz)# patrzymy czy taki pracownik juz jest
        if len(myresults)==0: #dodajemy jesli nie ma
            db.pracownicy.insert_one({"imie": imie, "nazwisko" :nazwisko,"zawod":zawod})
        return {'dodalismy':'pracownika'},201
class Usun_pracownika_nowego(Resource):
    def post(self):
        json_data = request.get_json()
        imie = json_data['imie']
        nazwisko = json_data['nazwisko']
        zawod = json_data['zawod']
        db.pracownicy.delete_one({ "imie":imie ,"nazwisko":nazwisko,"zawod":zawod}) #usuwamy z bazy prawocnikow
        #sciagamy te ktore sa wydane
        odpowiedz=db.wydanie.find( { "osoba_imie":imie ,"osoba_nazwisko":nazwisko } )
        myresults = list(odpowiedz) #patrzymy ile ich jest w naszej bazie
        moje_wartosci=[]
        for i in myresults:

            db.magazyn.update_one(  { "narzedzie":i['narzedzie'] ,"producent":i['producent']} ,{'$inc':{"ilosc_wydanych" :-int(i['ilosc'])}})
            db.wydanie.delete_one({ "osoba_imie":imie ,"osoba_nazwisko":nazwisko}) #to na sam koniec

#trzeba jeszcze zaktualizowac te ktore sa wydane

        return {'usunelismy':imie},201
class wyswietl_pracownikow(Resource):
    def get(self):
        odpowiedz=db.pracownicy.find()
        myresults = list(odpowiedz) #patrzymy ile ich jest w naszej bazie
        moje_wartosci=[]
        for i in myresults:
            moje_wartosci.append({'imie':i['imie'],'nazwisko':i['nazwisko'],'zawod':i['zawod']})
        return {'odpowiedz':moje_wartosci},201
class Obiegowka(Resource):
    def post(self):
        json_data = request.get_json()
        imie = json_data['imie']
        nazwisko = json_data['nazwisko']
        zawod = json_data['zawod']
        email=json_data['email']
        SENDGRID_API_KEY='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'
        odpowiedz=db.wydanie.find( { "osoba_imie":imie ,"osoba_nazwisko":nazwisko } )
        myresults = list(odpowiedz) #patrzymy ile ich jest w naszej bazie
        dzien_tyg=datetime.now()
        if len(myresults)==0:
            tytul='Obiegówka '+str(imie)+' '+str(nazwisko)
            content=str(imie)+' '+str(nazwisko)+' zdał wszystkie rzeczy i został odprawiony w dniu '+str(dzien_tyg.day)+'-'+str(dzien_tyg.month)+'-'+str(dzien_tyg.year)
            message = Mail(from_email='magazyn.logos@logos.pl',to_emails=str(email),subject=tytul,html_content=content)
            try:
                sg = SendGridAPIClient(SENDGRID_API_KEY)
                response = sg.send(message)
                return {'Wygenerowalismy dla ':imie},201
            except Exception as e:
                return {'Błąd ':e.message},201
        else:
            return {'Osoba  ':'ma na sobie przedmioty'},201










api.add_resource(Dodaj,'/dodaj/')
api.add_resource(Usun,'/usun/')
api.add_resource(Szukaj,'/szukaj/')
api.add_resource(Wydaj,'/wydaj/')
api.add_resource(Usun_wydanie,'/usun_wydanie/')
api.add_resource(Wydane_osobie,'/wydane_osobie/')
api.add_resource(zobacz_wszystkie,'/zobacz_wszystkie/')
api.add_resource(kategorie,'/kategorie/')
api.add_resource(zobacz_po_kategorii,'/zobacz_po_kategorii/')
api.add_resource(Dodaj_pracownika_nowego,'/dodaj_pracownika_nowego/')
api.add_resource(Usun_pracownika_nowego,'/usun_pracownika_nowego/')
api.add_resource(wyswietl_pracownikow,'/wyswietl_pracownikow/')
api.add_resource(Obiegowka,'/obiegowka/')







if __name__=='__main__':
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)
