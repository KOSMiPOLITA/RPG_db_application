from databaseConnection import connection
from appJar import gui
from PIL import Image, ImageTk
import datetime


class window():

    def __init__(self):
        self.iterator = 0
        self.database = None
        self.lista = []
        self.canLoad = 1
        self.createdInt = 1
        self.createdInt3 = 1
        self.tabOfAb = 1
        self.createdPostacie = 1
        self.createdRace = 1
        self.lista_krajow = ["---------"]
        self.createdKraj = 1
        self.lista_class = ["---------"]
        self.lista_races = ["---------"]
        self.lista_jezykow = ["---------"]
        self.lista_efektow = ["--------------------"]
        self.lista_stron_kon = ["------------"]
        self.EfektAndJezyk = 1
        self.createdStrony = 1
        self.canLoadEffect = 1
        self.canLoadRace = 1
        self.canLoadNation = 1
        self.lista_sex = ["N", "F", "M"]
        self.lista_stat = []
        self.postacie_index = []
        self.pod_dod = ["Pod", "Dod"]
        self.lista_statystyk = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]
        self.lista_wartosci = [1, 2, 3]
        for i in range(21):
            self.lista_stat.append(i)
        self.lista_tab = ["Karty Postaci", "Lista klas", "Rasy & Efekty", "Kraje pochodzenia", "Lista Ras i Krajów"]
        for t in range(len(self.lista_tab)):
            tmp = ""
            n = len(max(self.lista_tab)) - len(self.lista_tab[t])
            while (n > 0):
                tmp += " "
                n -= 1
            self.lista_tab[t] = self.lista_tab[t] + tmp
        self.lista_postaci = ["---------"]
        self.lista_war_umiej = ["-"]
        for i in range(51):
            self.lista_war_umiej.append(i)

    def createDB(self):
        if self.database is not None and self.createdInt == 1:
            a = self.database.cursor().execute('select * from klasy')
            for row in a:
                self.lista.append(row)
            app.openTab("Start", self.lista_tab[1])
            for obiekt in self.lista:
                app.label(obiekt)
            self.createdInt = 0
            self.createdInt3 = 0

    def login(self, btn):
        if btn == 'LOGIN':
            self.makeLogin()
            app.showSubWindow('Logowanie')
            app.emptyCurrentContainer()
        else:
            app.stop()

    def confirm(self, button):
        if button == "Cancel":
            app.destroySubWindow("Logowanie")
        else:
            app.enableMenuItem("Połącz", "Log Out")
            app.enableMenuItem("Dodaj", "Dodaj Postać")
            app.enableMenuItem("Dodaj", "Dodaj Rasę")
            app.enableMenuItem("Dodaj", "Dodaj Kraj")
            app.enableMenuItem("Umiejętności", "Nowa umiejętność")
            app.enableMenuItem("Umiejętności", "Dostępne umiejętności")
            app.disableMenuItem("Połącz", "Login")
            usr = app.getEntry("Username")
            pwd = app.getEntry("Password ")
            self.database = connection(usr, pwd)
            app.setTabbedFrameDisableAllTabs("Start", disabled=False)
            app.destroySubWindow("Logowanie")

    def sendCharacter(self):
        nazwa = app.getEntry("Nazwa")
        levela = app.getOptionBox("Level Postaci")
        plec = app.getOptionBox("Płeć")
        rasa = app.getOptionBox("Rasa")
        pochodzenia = app.getOptionBox("Pochodzenie")
        klasa = app.getOptionBox("Klasa")
        wiek = app.getEntry("Wiek")
        wzrost = app.getEntry("Wzrost")
        waga = app.getEntry("Waga")
        skora = app.getEntry("Kolor skóry")
        wlosy = app.getEntry("Kolor włosów")
        oczy = app.getEntry("Kolor oczu")
        hp = app.getEntry("HP")
        sta = app.getEntry("STA")
        strg = app.getOptionBox("STR")
        dex = app.getOptionBox("DEX")
        con = app.getOptionBox("CON")
        inte = app.getOptionBox("INT")
        wis = app.getOptionBox("WIS")
        cha = app.getOptionBox("CHA")
        self.database.cursor().execute(
            f"insert into Postacie values (POSTACIE_SEQ.NEXTVAL,'{nazwa}', {levela}, {wiek}, {wzrost}, {waga}, '{plec}', '{skora}',"
            f"'{wlosy}', '{oczy}', {hp}, {sta}, {strg}, {dex}, {con}, {inte}, {wis}, {cha}, '{rasa}', '{pochodzenia}', '{klasa}')")
        self.database.cursor().execute("commit")
        app.infoBox("Nowa Postać   ", "Nastąpiło poprawne dodanie postaci do bazy danych", parent=None)
        self.lista_postaci.append(nazwa)
        app.changeOptionBox("Lista postaci : ", self.lista_postaci)
        app.destroySubWindow("Dodaj nową postać")

    def sendRace(self):
        nazwa = app.getEntry("Nazwa rasy")
        opis = app.getTextArea("Opis rasy")
        srd = app.getEntry("Długość życia")
        pd = app.getOptionBox("Pod / Dod")
        dodatek = app.getEntry("Dodatek")
        efekt = app.getOptionBox("Efekt rasy")
        jezyk = app.getOptionBox("Nazwa języka")
        self.database.cursor().execute(
            f"insert into Rasy values ('{nazwa}', '{opis}', {srd}, '{pd}', '{dodatek}', '{efekt}', '{jezyk}')")
        efekt_lista = self.database.cursor().execute(
            f"select * from efekty_rasowe where nazwa_efektu = '{efekt}'"
        )
        for row in efekt_lista:
            efekt_lista1 = row
        self.database.cursor().execute("commit")
        app.infoBox("Nowa Rasa  ", "Nastąpiło poprawne dodanie rasy do bazy danych", parent=None)
        self.lista_races.append(nazwa)
        if dodatek == None:
            dodatek = ""
        app.changeOptionBox("Rasa :", self.lista_races)
        app.changeOptionBox("Lista ras : ", self.lista_races)
        app.addTableRows("tabela_pochodzeń1", [[nazwa, opis, srd, pd, dodatek, jezyk, efekt_lista1[0], efekt_lista1[1], efekt_lista1[2], efekt_lista1[3]]])
        app.destroySubWindow("Dodaj nową rasę")


    def sendNation(self):
        kraj = app.getEntry("Nazwa Kraju pochodzenia")
        stolica = app.getEntry("Stolica")
        strona = app.getOptionBox("Strona konfliktu")
        jezyk = app.getOptionBox("Język urzędowy")
        self.database.cursor().execute(
            f"insert into kraje_pochodzenia values('{kraj}', '{stolica}', '{jezyk}', '{strona}')")
        self.database.cursor().execute("commit")
        app.infoBox("Nowy kraj  ", "Nastąpiło poprawne dodanie kraju pochodzenia do bazy danych", parent=None)
        self.lista_krajow.append(kraj)
        app.changeOptionBox("Kraj :", self.lista_krajow)
        app.changeOptionBox("Lista Krajów pochodzenia : ", self.lista_krajow)
        app.openTab("Start", self.lista_tab[4])
        app.addTableRows("tabela_pochodzeń", [[kraj, stolica, jezyk, strona]])
        app.destroySubWindow("Dodaj nowy kraj pochodzenia")

    def sendEffect(self):
        nazwa = app.getEntry("Nazwa efektu :")
        opis = app.getTextArea("Opis efektu :")
        stat = app.getOptionBox("Stat :")
        wart = app.getOptionBox("Wartość :")
        self.database.cursor().execute(
            f"insert into Efekty_rasowe values ('{nazwa}', '{opis}', '{stat}', {wart})")
        self.database.cursor().execute("commit")
        app.infoBox("Nowa Rasa  ", "Nastąpiło poprawne dodanie efektu do bazy danych", parent=None)
        self.lista_efektow.append(nazwa)
        app.changeOptionBox("Efekt rasy :", self.lista_efektow)

    def sendJezyk(self):
        nazwa = app.getEntry("Nazwa nowego języka :")
        self.database.cursor().execute(
            f"insert into Jezyki values ('{nazwa}')")
        self.database.cursor().execute("commit")
        app.infoBox("Nowy język  ", "Nastąpiło poprawne dodanie języka do bazy danych", parent=None)
        self.lista_jezykow.append(nazwa)
        app.changeOptionBox("Nazwa języka :", self.lista_jezykow)
        app.changeOptionBox("Język urzędowy :", self.lista_jezykow)

    def sendSpell(self):
        nazwa = app.getEntry("Nazwa umiej.")
        poziom = app.getEntry("Poziom umiej.")
        opis = app.getTextArea("opis_umiej")
        dmg = app.getOptionBox("DMG")
        heal = app.getOptionBox("HEAL")
        defe = app.getOptionBox("DEF")
        pd = app.getOptionBox("P_D")
        dodatek = app.getEntry("Dodatek")
        lista = []
        lista.append(app.getOptionBox("Klasa 1st"))
        lista.append(app.getOptionBox("Klasa 2nd"))
        lista.append(app.getOptionBox("Klasa 3rd"))
        lista.append(app.getOptionBox("Klasa 4th"))
        lista.append(app.getOptionBox("Klasa 5th"))
        lista_ost = []
        for i in lista:
            if i is not None and i != "---------" and i not in lista_ost:
                lista_ost.append(i)
        if dmg is None:
            dmg = "NULL"
        if heal is None:
            heal = "NULL"
        if defe is None:
            defe = "NULL"
        self.database.cursor().execute(
            f"insert into umiejetnosci values('{nazwa}', '{opis}', {poziom}, "
            f"{dmg}, {heal}, {defe}, '{pd}', '{dodatek}')")
        for row in lista_ost:
            print(row)
            self.database.cursor().execute(
                f"insert into umiejetnoscidlaklas values ('{row}', '{nazwa}')")
        self.database.cursor().execute("commit")
        app.infoBox("Nowa umiejętność", "Nastąpiło poprawne dodanie umiejętności do bazy danych", parent=None)
        app.destroySubWindow("Dodaj nową umiejętność")

    def doNothing(self):
        pass

    def makeLogin(self):
        with app.subWindow('Logowanie', modal=True):
            app.emptyCurrentContainer()
            app.setResizable(canResize=False)
            app.showSubWindow("Logowanie")
            app.setBg("indianred")
            # duma = app.addImage("dragon", "login.gif")
            # app.setBgImage(duma)
            # photo = ImageTk.PhotoImage(Image.open("login.gif"))
            app.setSize(400, 200)
            app.setSticky("new")
            app.addImage("smog", "goraLogin.gif")

            app.setPadding([20, 5])
            app.addLabelEntry("Username")
            app.addLabelSecretEntry("Password ")

            app.addButtons(["Login ", "Cancel"], self.confirm)
            app.setFocus("Username")

            app.setPadding([0, 0])
            app.setSticky("sew")
            app.addImage("smog2", "dolLogin.gif")

    def makeLogOut(self):
        app.setTabbedFrameDisableAllTabs("Start", disabled=True)
        app.enableMenuItem("Połącz", "Login")
        app.disableMenuItem("Połącz", "Log Out")
        app.disableMenuItem("Dodaj", "Dodaj Postać")
        app.disableMenuItem("Dodaj", "Dodaj Rasę")
        app.disableMenuItem("Dodaj", "Dodaj Kraj")
        app.disableMenuItem("Umiejętności", "Nowa umiejętność")
        app.disableMenuItem("Umiejętności", "Dostępne umiejętności")
        self.database = None
        self.lista = []
        self.createdInt = 1
        self.createdInt3 = 1
        self.lista_class = ["---------"]
        self.createdPostacie = 1
        self.lista_postaci = ["---------"]
        self.lista_races = ["------------"]
        self.canLoad = 1
        self.lista_krajow = ["---------"]
        self.createdKraj = 1
        self.lista_jezykow = ["---------"]
        self.lista_efektow = ["--------------------"]
        self.EfektAndJezyk = 1
        self.createdStrony = 1
        self.canLoadNation = 1
        self.lista_stron_kon = ["------------"]
        app.openTab("Start", self.lista_tab[1])
        app.changeOptionBox("Wybierz klasę", self.lista_class)
        app.changeOptionBox("Rasa :", self.lista_races)
        app.changeOptionBox("Kraj :", self.lista_krajow)
        app.changeOptionBox("Lista ras : ", self.lista_races)
        app.changeOptionBox("Klasa :", self.lista_class)
        app.changeOptionBox("Lista postaci : ", self.lista_postaci)
        app.changeOptionBox("Lista Krajów pochodzenia : ", self.lista_krajow)
        app.changeOptionBox("Strona konfliktu :", self.lista_stron_kon)
        app.changeOptionBox("Nazwa języka :", self.lista_jezykow)
        app.changeOptionBox("Język urzędowy :", self.lista_jezykow)
        app.changeOptionBox("Efekt rasy :", self.lista_efektow)
        app.stopTab()
        app.infoBox("Wylogowywanie", "Nastąpiło poprawne wylogowanie z Bazy Danych", parent=None)

    def createTableOfStronyKonfliktu(self):
        if self.database is not None and self.createdStrony == 1:
            self.lista_stron_kon = []
            self.createdStrony = 0
            stronyDB = self.database.cursor().execute('select * from strony_konfliktu')
            for row in stronyDB:
                self.lista_stron_kon.append(row[0])
            app.changeOptionBox("Strona konfliktu :", self.lista_stron_kon)

    def createTableOfCharacters(self):
        if self.database is not None and self.createdPostacie == 1:
            self.lista_postaci = []
            self.postacie_index = []
            self.createdPostacie = 0
            postacieDB = self.database.cursor().execute('select * from postacie')
            for row in postacieDB:
                self.lista_postaci.append(row[1])
                self.postacie_index.append([row[0], row[1]])
            app.changeOptionBox("Lista postaci : ", self.lista_postaci)

    def createTableOfEfektAndJezyk(self):
        if self.database is not None and self.EfektAndJezyk == 1:
            self.lista_jezykow = []
            self.lista_efektow = []
            self.EfektAndJezyk = 0
            efektDB = self.database.cursor().execute('select * from efekty_rasowe')
            jezykDB = self.database.cursor().execute('select * from jezyki')
            for row in efektDB:
                self.lista_efektow.append(row[0])
            for row in jezykDB:
                self.lista_jezykow.append(row[0])
            app.changeOptionBox("Nazwa języka :", self.lista_jezykow)
            app.changeOptionBox("Język urzędowy :", self.lista_jezykow)
            app.changeOptionBox("Efekt rasy :", self.lista_efektow)

    def createTableOfNations(self):
        if self.database is not None and self.createdKraj == 1:
            self.lista_krajow = []
            self.createdKraj = 0
            kreajeLista = []
            kreajeDBNaglowek = self.database.cursor().execute(
                "select column_name from user_tab_cols where table_name = 'KRAJE_POCHODZENIA'")
            kreajeDB = self.database.cursor().execute('select * from kraje_pochodzenia')
            '''tmp = []
            for row in kreajeDBNaglowek:
                row = str(row).replace("('", "").replace("',)", "")
                tmp.append(row)
            kreajeLista.append(tmp)'''
            for row in kreajeDB:
                # tmp = []
                self.lista_krajow.append(row[0])
                # for item in row:
                #    tmp.append(item)
                # kreajeLista.append(tmp)
            app.changeOptionBox("Kraj :", self.lista_krajow)
            app.changeOptionBox("Lista Krajów pochodzenia : ", self.lista_krajow)


    def createTableOfRaces(self):
        if self.database is not None and self.createdRace == 1:
            self.lista_races = []
            self.createdRace = 0
            rasyLista = []
            rasyDBNaglowek = self.database.cursor().execute(
                "select column_name from user_tab_cols where table_name = 'RASY'")
            rasyDB = self.database.cursor().execute('select * from rasy')
            '''tmp = []
            for row in rasyDBNaglowek:
                row = str(row).replace("('", "").replace("',)", "")
                tmp.append(row)
            rasyLista.append(tmp)'''
            for row in rasyDB:
                # tmp = []
                self.lista_races.append(row[0])
                # for item in row:
                #    tmp.append(item)
                # rasyLista.append(tmp)
            app.changeOptionBox("Rasa :", self.lista_races)
            app.changeOptionBox("Lista ras : ", self.lista_races)

    def createTableOfPochodzenie(self):
        if self.database is not None and self.createdInt3 == 1:
            self.createdInt3 = 0
            klasyLista = []
            klasyDBNaglowek = self.database.cursor().execute(
                "select column_name from user_tab_cols where table_name = 'KRAJE_POCHODZENIA'")
            klasyDB = self.database.cursor().execute('select * from kraje_pochodzenia')
            tmp = []
            for row in klasyDBNaglowek:
                row = str(row).replace("('", "").replace("',)", "")
                tmp.append(row)
            klasyLista.append(tmp)
            for row in klasyDB:
                tmp = []
                for item in row:
                    tmp.append(item)
                klasyLista.append(tmp)

            app.openTab("Start", self.lista_tab[4])
            app.setStretch('column')
            app.setSticky('wen')
            app.setSticky("news")
            app.setPadding([20, 20])
            app.addTable("tabela_pochodzeń", klasyLista, wrap="700", row=5)

            klasyLista = []
            klasyDBNaglowek = self.database.cursor().execute(
                "select column_name from user_tab_cols where table_name = 'RASY'")
            klasyDB = self.database.cursor().execute("select nazwa, opis_rasy, srd_dlugosc_zycia, "
                                                     "p_d, nazwa_dodatku, nazwa_jezyka, e.nazwa_efektu, opis_efektu, statystyka, "
                                                     "wartosc_wzm from rasy r inner join efekty_rasowe e on r.nazwa_efektu = e.nazwa_efektu")
            tmp = []
            for row in klasyDBNaglowek:
                row = str(row).replace("('", "").replace("',)", "")
                tmp.append(row)
            klasyDBNaglowek = self.database.cursor().execute(
                "select column_name from user_tab_cols where table_name = 'EFEKTY_RASOWE'")
            for row in klasyDBNaglowek:
                row = str(row).replace("('", "").replace("',)", "")
                tmp.append(row)
            klasyLista.append(tmp)
            klasyLista[0].pop(5)
            for row in klasyDB:
                tmp = []
                for item in row:
                    tmp.append(item)
                klasyLista.append(tmp)
            app.setSticky("new")
            app.addTable("tabela_pochodzeń1", klasyLista, wrap="500", colspan=3, row=3)

            app.stopTab()

    def createTableOfClass(self):
        if self.database is not None and self.createdInt == 1:
            self.lista_class = []
            self.createdInt = 0
            klasyLista = []
            klasyDBNaglowek = self.database.cursor().execute(
                "select column_name from user_tab_cols where table_name = 'KLASY'")
            klasyDB = self.database.cursor().execute('select * from klasy')
            tmp = []
            for row in klasyDBNaglowek:
                row = str(row).replace("('", "").replace("',)", "")
                tmp.append(row)
            klasyLista.append(tmp)
            for row in klasyDB:
                tmp = []
                self.lista_class.append(row[0])
                for item in row:
                    tmp.append(item)
                klasyLista.append(tmp)
            app.openTab("Start", self.lista_tab[0])
            app.changeOptionBox("Klasa :", self.lista_class, 1, 0)
            app.stopTab()
            app.openTab("Start", self.lista_tab[1])
            app.changeOptionBox("Wybierz klasę", self.lista_class, 1, 0)
            app.setStretch("both")
            app.setSticky("news")
            app.setPadding([20, 20])
            app.addTable("tabela_klas", klasyLista, wrap="700", colspan=3)
            app.stopTab()

    def loadCharacterData(self):
        if self.database is not None and self.canLoad == 1:
            character = app.getOptionBox("Lista postaci : ")
            postacDB = self.database.cursor().execute(f"select * from postacie where nazwa_postaci = '{character}'")
            for row in postacDB:
                postacDB = row
            app.setEntry("Nazwa :", postacDB[1])
            app.setOptionBox("Level Postaci :", postacDB[2])
            app.setOptionBox("Płeć :", postacDB[6])

            app.setOptionBox("Rasa :", postacDB[18])
            app.setOptionBox("Kraj :", postacDB[19])
            app.setOptionBox("Klasa :", postacDB[20])

            app.setEntry("Wiek :", postacDB[3])
            app.setEntry("Wzrost :", postacDB[4])
            app.setEntry("Waga :", postacDB[5])

            app.setEntry("Kolor skóry :", postacDB[7])
            app.setEntry("Kolor włosów :", postacDB[8])
            app.setEntry("Kolor oczu :", postacDB[9])

            app.setSticky("e")
            app.setEntry("HP :", postacDB[10])
            app.setSticky("w")
            app.setEntry("STA :", postacDB[11])
            app.setSticky("w")
            # app.addLabelEntry("Plik z avatarem", 7, 1, colspan=2)

            app.setSticky("e")
            app.setOptionBox("STR :", postacDB[12])
            app.setOptionBox("DEX :", postacDB[13])
            app.setOptionBox("CON :", postacDB[14])
            app.setOptionBox("INT :", postacDB[15])
            app.setOptionBox("WIS :", postacDB[16])
            app.setOptionBox("CHA :", postacDB[17])

    def editCharachterData(self):
        postac = app.getOptionBox("Lista postaci : ")
        nazwa = app.getEntry("Nazwa :")
        levela = app.getOptionBox("Level Postaci :")
        plec = app.getOptionBox("Płeć :")
        rasa = app.getOptionBox("Rasa :")
        pochodzenia = app.getOptionBox("Kraj :")
        klasa = app.getOptionBox("Klasa :")
        wiek = app.getEntry("Wiek :")
        wzrost = app.getEntry("Wzrost :")
        waga = app.getEntry("Waga :")
        skora = app.getEntry("Kolor skóry :")
        wlosy = app.getEntry("Kolor włosów :")
        oczy = app.getEntry("Kolor oczu :")
        hp = app.getEntry("HP :")
        sta = app.getEntry("STA :")
        strg = app.getOptionBox("STR :")
        dex = app.getOptionBox("DEX :")
        con = app.getOptionBox("CON :")
        inte = app.getOptionBox("INT :")
        wis = app.getOptionBox("WIS :")
        cha = app.getOptionBox("CHA :")
        self.database.cursor().execute(
            f"update postacie set nazwa_postaci = '{nazwa}', poziom = {levela}, plec = '{plec}', nazwa_rasy = '{rasa}', "
            f"nazwa_kraju = '{pochodzenia}', nazwa_klasy= '{klasa}', wiek = {wiek}, wzrost = {wzrost}, waga = {waga}, "
            f"kolor_skory = '{skora}', kolor_włosow ='{wlosy}', kolor_oczow = '{oczy}', hp = {hp}, sta = {sta},  "
            f"str = {strg}, dex = {dex}, con = {con}, int = {inte}, wis = {wis}, cha = {cha} where nazwa_postaci = '{postac}'")
        for pse in range(len(self.lista_postaci)):
            if self.lista_postaci[pse] == postac:
                self.lista_postaci[pse] = nazwa
                app.changeOptionBox("Lista postaci : ", self.lista_postaci)
        self.database.cursor().execute("commit")
        app.infoBox("Zmień dane", "Dane wskazanej postaci zostały poprawnie zmienione", parent=None)

    def loadRaceData(self):
        if self.database is not None and self.canLoadRace == 1:
            rasa = app.getOptionBox("Lista ras : ")
            rasaDB = self.database.cursor().execute(f"select * from rasy where nazwa = '{rasa}'")
            for row in rasaDB:
                rasaDB = row
            app.clearTextArea("Opis rasy :", callFunction=True)
            app.setTextArea("Opis rasy :", rasaDB[1])
            app.setEntry("Długość życia :", rasaDB[2])
            app.setOptionBox("Pod / Dod :", rasaDB[3])
            app.setEntry("Dodatek :", rasaDB[4])
            app.setOptionBox("Efekt rasy :", rasaDB[5])
            app.setOptionBox("Nazwa języka :", rasaDB[6])

    def loadNationData(self):
        if self.database is not None and self.canLoadNation == 1:
            kraj = app.getOptionBox("Lista Krajów pochodzenia : ")
            krajDB = self.database.cursor().execute(f"select * from kraje_pochodzenia where nazwa = '{kraj}'")
            for row in krajDB:
                krajDB = row
            app.setEntry("Stolica :", krajDB[1])
            app.setOptionBox("Strona konfliktu :", krajDB[3])
            app.setOptionBox("Język urzędowy :", krajDB[2])

    def editKraje(self):
        kraj = app.getOptionBox("Lista Krajów pochodzenia : ")
        stolica = app.getEntry("Stolica :")
        strona = app.getOptionBox("Strona konfliktu :")
        jezyk = app.getOptionBox("Język urzędowy :")
        self.database.cursor().execute(
            f"update kraje_pochodzenia set nazwa = '{kraj}', stolica = '{stolica}', jezyk_urzedowy = '{jezyk}', nazwa_strony = '{strona}' where nazwa = '{kraj}'")
        self.database.cursor().execute("commit")
        app.infoBox("Zmień dane", "Dane wskazanego kraju zostały poprawnie zmienione", parent=None)

    def editRasy(self):
        rasa = app.getOptionBox("Lista ras : ")
        opis = app.getTextArea("Opis rasy :")
        srd = app.getEntry("Długość życia :")
        pd = app.getOptionBox("Pod / Dod :")
        dod = app.getEntry("Dodatek :")
        efekt = app.getOptionBox("Efekt rasy :")
        jezyk = app.getOptionBox("Nazwa języka :")
        self.database.cursor().execute(
            f"update rasy set nazwa = '{rasa}', opis_rasy = '{opis}', srd_dlugosc_zycia = {srd}, p_d = '{pd}', nazwa_dodatku = '{dod}', "
            f"nazwa_efektu = '{efekt}', nazwa_jezyka = '{jezyk}' where nazwa = '{rasa}'")
        '''for pse in range(len(self.lista_races)):
            if self.lista_races[pse] == rasa:
                self.lista_races[pse] = nazwa
                app.changeOptionBox("Lista ras : ", self.lista_races)
                app.changeOptionBox("Rasa :", self.lista_races)'''
        self.database.cursor().execute("commit")
        app.infoBox("Zmień dane", "Dane wskazanej rasy zostały poprawnie zmienione", parent=None)

    def createTableOfAbilities(self):
        self.iterator += 1
        if self.tabOfAb > 1:
            app.destroySubWindow("Umiejętność wybranej klasy")
        if self.database is not None:
            self.tabOfAb += 1;
            klasa = app.getOptionBox("Wybierz klasę")
            self.createdInt2 = 0;
            umiejLista = []
            umiejDBNaglowek = self.database.cursor().execute(
                "select column_name from user_tab_cols where table_name = 'UMIEJETNOSCI'")
            query = (
                f"select nazwa, opis_umiejetnosci, poziom, dmg, heal, def, p_d, nazwa_dodatku from Umiejetnosci u inner join UmiejetnosciDlaKlas uk on uk.umiejetnosc = u.nazwa where uk.klasa = '{klasa}'")
            umiejDB = self.database.cursor().execute(query)
            tmp = []
            for row in umiejDBNaglowek:
                row = str(row).replace("('", "").replace("',)", "")
                tmp.append(row)
            umiejLista.append(tmp)
            for row in umiejDB:
                tmp = []
                self.lista_class.append(row[0])
                for item in row:
                    if item == None:
                        item = '-'
                    tmp.append(item)
                umiejLista.append(tmp)
            self.tabOfAb += 1
            with app.subWindow("Umiejętność wybranej klasy", modal=True):
                app.showSubWindow("Umiejętność wybranej klasy")
                app.setSize(1280, 720)
                app.setBg(colour="beige", override=False)
                app.setStretch("column")
                app.setSticky("ew")
                app.addImage(f"klasy{self.iterator}", "dnd2.gif", colspan=3)
                app.setStretch("both")
                app.setSticky("news")
                app.setPadding([20, 20])
                app.addTable(f"tabela_umiejetnosci_dla_klas{self.iterator}", umiejLista, wrap="500")

    def createNewCharacterWindow(self):
        self.iterator += 1
        with app.subWindow("Dodaj nową postać", modal=True):
            app.showSubWindow("Dodaj nową postać")
            app.emptyCurrentContainer()
            app.setResizable(canResize=False)
            app.setSize(1280, 720)
            app.setBg(colour="beige", override=False)
            app.setStretch("column")
            app.setSticky("new")
            app.addImage(f"smokPostac{self.iterator}", "dnd2.gif", 0, colspan=4)

            app.setPadding([20, 0])
            app.setStretch("column")
            app.setSticky("w")
            app.addLabel(f"KartaPos{self.iterator}", "~~Karta Postaci~~", 1, 0)


            app.setSticky("w")
            app.addLabelEntry("Nazwa", 2, 0)
            app.addLabelOptionBox("Level Postaci", win.lista_stat, 2, 1)
            app.addLabelOptionBox("Płeć", win.lista_sex, 2, 2)

            app.addLabelOptionBox("Rasa", win.lista_races, 3, 0)
            app.addLabelOptionBox("Pochodzenie", win.lista_krajow, 3, 1)
            app.addLabelOptionBox("Klasa", win.lista_class, 3, 2)

            app.addLabelEntry("Wiek", 4, 0)
            app.addLabelEntry("Wzrost", 4, 1)
            app.addLabelEntry("Waga", 4, 2)

            app.addLabelEntry("Kolor skóry", 5, 0)
            app.addLabelEntry("Kolor włosów", 5, 1)
            app.addLabelEntry("Kolor oczu", 5, 2)

            app.setSticky("e")
            app.addLabelEntry("HP", 6, 0)
            app.setSticky("w")
            app.addLabelEntry("STA", 6, 1)
            app.setSticky("w")
            # app.addLabelEntry("Plik z avatarem", 7, 1, colspan=2)

            app.setSticky("e")
            app.addLabelOptionBox("STR", win.lista_stat, 7, 0)
            app.addLabelOptionBox("DEX", win.lista_stat, 7, 1)
            app.addLabelOptionBox("CON", win.lista_stat, 8, 0)
            app.addLabelOptionBox("INT", win.lista_stat, 8, 1)
            app.addLabelOptionBox("WIS", win.lista_stat, 9, 0)
            app.addLabelOptionBox("CHA", win.lista_stat, 9, 1)
            app.addButtons(["Zatwierdź postać"], win.sendCharacter, 9, 2)

            app.setPadding([0, 0])
            app.setSticky("nwes")
            app.addImage(f"krol{self.iterator}", "krol.gif", 1, 3, rowspan=50)

    def createNewRaceWindow(self):
        self.iterator += 1
        with app.subWindow("Dodaj nową rasę", modal=True):
            app.showSubWindow("Dodaj nową rasę")
            app.emptyCurrentContainer()
            app.setResizable(canResize=False)
            app.setSize(1280, 760)
            app.setBg(colour="beige", override=False)
            app.setStretch("column")
            app.setSticky("new")
            app.addImage(f"nowarasatlo{self.iterator}", "dnd2.gif", colspan=4)
            app.setSticky("w")
            app.setPadding([20, 0])
            app.addLabel("Dodawanie Rasy", "~~Dodawanie Rasy~~", 1, 0)
            app.addLabel("puste30", "", 1, 1)
            app.addLabel("puste31", "", 1, 2)
            app.addLabelEntry("Nazwa rasy", 2, 0, colspan=2)
            app.addLabel("RasaDoWczytania", "Opis rasy", 3, 0)
            app.setSticky("nwes")
            app.addTextArea("Opis rasy", 4, 0, colspan=2, rowspan=4)
            app.setSticky("w")
            app.addLabelEntry("Długość życia", 8, 0)
            app.addLabelOptionBox("Pod / Dod", win.pod_dod, 9, 0)
            app.setSticky("we")
            app.addLabelEntry("Dodatek", 10, 0)
            app.setSticky("w")
            app.addLabelOptionBox("Efekt rasy", win.lista_efektow, 11, 0)
            app.addLabelOptionBox("Nazwa języka", win.lista_jezykow, 12, 0)
            app.addButtons(['Dodaj rasę'], win.sendRace, 12, 1)

            app.setPadding([0, 0])
            app.setSticky("nes")
            app.addImage(f"krol22{self.iterator}", "krol.gif", 1, 3, rowspan=50)

    def createNewNationWindow(self):
        self.iterator += 1
        with app.subWindow("Dodaj nowy kraj pochodzenia", modal=True):
            app.showSubWindow("Dodaj nowy kraj pochodzenia")
            app.emptyCurrentContainer()
            app.setResizable(canResize=False)
            app.setSize(1280, 760)
            app.setBg(colour="beige", override=False)
            app.setStretch("column")
            app.setSticky("new")
            app.addImage(f"nowykrajtlo{self.iterator}", "dnd2.gif", colspan=3)
            app.setSticky("w")
            app.setPadding([20, 0])
            app.addLabel("Dodawanie Kraju pochodzenia", "~~Dodawanie Kraju pochodzenia~~", 1, 0)
            app.addLabel("puste330", "", 1, 1)
            app.addLabel("puste331", "", 1, 2)
            app.setSticky("w")
            app.setPadding([20, 10])

            app.addLabelEntry("Nazwa Kraju pochodzenia", 2, 0)
            app.addLabelEntry("Stolica", 3, 0)
            app.addLabelOptionBox("Strona konfliktu", win.lista_stron_kon, 4, 0)
            app.addLabelOptionBox("Język urzędowy", win.lista_jezykow, 5, 0)
            app.addButtons(['Dodaj kraj'], win.sendNation, 5, 1)

            app.setPadding([0, 0])
            app.setSticky("nes")
            app.addImage(f"krolnowyKraj{self.iterator}", "krol.gif", 1, 2, rowspan=50)

    def createNewUmiejetnosc(self):
        self.iterator += 1
        with app.subWindow("Dodaj nową umiejętność", modal=True):
            app.showSubWindow("Dodaj nową umiejętność")
            app.emptyCurrentContainer()
            app.setResizable(canResize=False)
            app.setSize(1300, 720)
            app.setBg(colour="beige", override=False)
            app.setStretch("column")
            app.setSticky("new")
            app.addImage(f"nowaumiejtlo{self.iterator}", "dnd2.gif", colspan=5)
            app.setSticky("w")
            app.setPadding([20, 5])
            app.addLabel("~~Nowa umiejętność~~", "~~Nowa umiejętność~~", 1, 0, colspan=2)
            app.addLabelEntry("Nazwa umiej.", 2, 0)
            app.addLabelEntry("Poziom umiej.", 2, 1)
            app.addLabel("Opis umiejetnosci :", "Opis umiejętności", 3, 0)
            app.setSticky("wne")
            #app.addEntry("Dupa", 3, 2, rowspan=2)
            app.addTextArea("opis_umiej", 4, 0, colspan=4)
            app.setSticky("w")
            app.addLabelOptionBox("DMG", win.lista_war_umiej, 5, 0)
            app.addLabelOptionBox("HEAL", win.lista_war_umiej, 5, 1)
            app.addLabelOptionBox("DEF", win.lista_war_umiej, 5, 2)
            app.addLabelOptionBox("P_D", win.pod_dod, 6, 0)
            app.addLabelEntry("Dodatek", 6, 1)
            lista_klas = win.lista_class
            if "---------" not in lista_klas:
                lista_klas.insert(0, "---------")
            app.addLabelOptionBox("Klasa 1st", lista_klas, 7, 0)
            app.addLabelOptionBox("Klasa 2nd", lista_klas, 7, 1)
            app.addLabelOptionBox("Klasa 3rd", lista_klas, 7, 2)
            app.addLabelOptionBox("Klasa 4th", lista_klas, 8, 0)
            app.addLabelOptionBox("Klasa 5th", lista_klas, 8, 1)
            app.addButtons(["OK"], win.sendSpell, 8, 2)
            app.setPadding([0, 0])
            app.setSticky("nes")
            app.addImage(f"krolNowaUmiej{self.iterator}", "krol.gif", 1, 3, rowspan=50)

    def makeChooseCharacterForCheckingSpells(self):
        with app.subWindow('Wybór postaci', modal=True):
            app.emptyCurrentContainer()
            app.setResizable(canResize=False)
            app.showSubWindow("Wybór postaci")
            app.setBg("indianred")
            app.setSize(400, 200)
            app.setSticky("new")
            app.addImage("smogA", "goraLogin.gif")

            app.setPadding([20, 5])
            app.addLabelOptionBox("Wybierz postać :", self.lista_postaci)

            app.addButtons(["Choose", "Cancel"], self.showMySpells)

            app.setPadding([0, 0])
            app.setSticky("sew")
            app.addImage("smogB", "dolLogin.gif")

    def showMySpells(self, button):
        self.iterator += 1
        cur_character = app.getOptionBox("Wybierz postać :")
        if button == "Cancel":
            app.destroySubWindow("Wybór postaci")
        else:
            app.destroySubWindow("Wybór postaci")
            umiejLista = []
            tmp = []
            danePostaci = self.database.cursor().execute(f"select poziom, nazwa_klasy from postacie "
                                                         f"where nazwa_postaci = '{cur_character}'")
            for row in danePostaci:
                Postac = row
            umiejDBNaglowek = self.database.cursor().execute(
                "select column_name from user_tab_cols where table_name = 'UMIEJETNOSCI'")
            for row in umiejDBNaglowek:
                row = str(row).replace("('", "").replace("',)", "")
                tmp.append(row)
            umiejLista.append(tmp)
            query = (
                f"select nazwa, opis_umiejetnosci, poziom, dmg, heal, def, p_d, nazwa_dodatku from Umiejetnosci u "
                f"inner join UmiejetnosciDlaKlas uk on uk.umiejetnosc = u.nazwa "
                f"where uk.klasa = '{Postac[1]}' and u.poziom <= {Postac[0]}")
            umiejDB = self.database.cursor().execute(query)
            for row in umiejDB:
                tmp = []
                self.lista_class.append(row[0])
                for item in row:
                    if item == None:
                        item = '-'
                    tmp.append(item)
                umiejLista.append(tmp)

            with app.subWindow(f"Umiejętności postaci: {cur_character}", modal=True):
                app.showSubWindow(f"Umiejętności postaci: {cur_character}")
                app.emptyCurrentContainer()
                app.setResizable(canResize=False)
                app.setSize(1300, 720)
                app.setBg(colour="beige", override=False)
                app.setStretch("column")
                app.setSticky("new")
                app.addImage(f"showumiejtlo{self.iterator}", "dnd2.gif", colspan=5)
                app.setSticky("w")
                app.setPadding([20, 5])
                app.addLabel(f"~~Lista umiejętności postaci {self.iterator}", f"~~Lista umiejętności postaci: {cur_character}~~", 1, 0, colspan=2)
                app.setSticky("news")
                app.setPadding([20, 20])
                app.addTable(f"tabela_umiejetnosci_dla_klas {self.iterator}", umiejLista, wrap="500")

if __name__ == "__main__":
    win = window()
    with gui('Baza Danych RPG') as app:
        app.setResizable(canResize=True)
        app.setSize(1280, 880)
        fileMenu = ["Login", "Log Out"]
        fileMenu2 = ["Dodaj Postać", "Dodaj Rasę", "Dodaj Kraj"]
        fileMenu3 = ["Nowa umiejętność", "Dostępne umiejętności"]
        app.addMenuList("Połącz", fileMenu, [win.makeLogin, win.makeLogOut])
        app.addMenuList("Dodaj", fileMenu2, [win.createNewCharacterWindow, win.createNewRaceWindow, win.createNewNationWindow])
        app.addMenuList("Umiejętności", fileMenu3, [win.createNewUmiejetnosc, win.makeChooseCharacterForCheckingSpells])
        app.disableMenuItem("Połącz", "Log Out")
        app.disableMenuItem("Dodaj", "Dodaj Postać")
        app.disableMenuItem("Dodaj", "Dodaj Rasę")
        app.disableMenuItem("Dodaj", "Dodaj Kraj")
        app.disableMenuItem("Umiejętności", "Nowa umiejętność")
        app.disableMenuItem("Umiejętności", "Dostępne umiejętności")
        app.startTabbedFrame("Start")

        #TAG PIERWSZY---------------------------------------------------------------------------------------------------
        app.startTab(win.lista_tab[0])

        app.setStretch("column")
        app.setSticky("new")
        app.addImage("tlo1", "dnd2.gif", 0, colspan=4)
        app.setBg(colour="beige", override=False)
        app.setStretch('column')
        app.setSticky('wen')
        app.addLabel('bottom1', '', 1, colspan=4)
        app.setLabelBg("bottom1", "darkred")

        app.setStretch('column')
        app.setSticky("we")
        app.setPadding([20, 0])
        app.addLabelOptionBox("Lista postaci : ", win.lista_postaci, 2, 0, colspan=2)
        app.addLabel("pustaGlowna1", "", 2, 2)
        app.setSticky("w")
        app.addButtons(["Edytuj Postać"], win.loadCharacterData, 2, 2)
        app.setStretch("column")
        app.setSticky("w")
        app.addLabel("KartaPos_g", "~~Karta Postaci~~", 3, 0, colspan=3)

        app.addLabelEntry("Nazwa :", 4, 0)
        app.addLabelOptionBox("Level Postaci :", win.lista_stat, 4, 1)
        app.addLabelOptionBox("Płeć :", win.lista_sex, 4, 2)

        app.setSticky("we")
        app.addLabelOptionBox("Rasa :", win.lista_races, 5, 0)
        app.addLabelOptionBox("Kraj :", win.lista_krajow, 5, 1)
        app.addLabelOptionBox("Klasa :", win.lista_class, 5, 2)

        app.setSticky("w")
        app.addLabelEntry("Wiek :", 6, 0)
        app.addLabelEntry("Wzrost :", 6, 1)
        app.addLabelEntry("Waga :", 6, 2)

        app.addLabelEntry("Kolor skóry :", 7, 0)
        app.addLabelEntry("Kolor włosów :", 7, 1)
        app.addLabelEntry("Kolor oczu :", 7, 2)

        app.setSticky("e")
        app.addLabelEntry("HP :", 8, 0)
        app.setSticky("w")
        app.addLabelEntry("STA :", 8, 1)
        app.setSticky("w")

        app.setSticky("e")
        app.addLabelOptionBox("STR :", win.lista_stat, 9, 0)
        app.addLabelOptionBox("DEX :", win.lista_stat, 9, 1)
        app.addLabelOptionBox("CON :", win.lista_stat, 10, 0)
        app.addLabelOptionBox("INT :", win.lista_stat, 10, 1)
        app.addLabelOptionBox("WIS :", win.lista_stat, 11, 0)
        app.addLabelOptionBox("CHA :", win.lista_stat, 11, 1)
        app.setSticky("we")
        app.addButtons(['Zmień dane'], win.editCharachterData, 11, 2)

        app.setPadding([0, 0])
        app.setSticky("nes")
        app.addImage("krolGlowny", "krol.gif", 2, 3, rowspan=50)
        app.registerEvent(win.createTableOfCharacters)
        app.registerEvent(win.createTableOfRaces)
        app.registerEvent(win.createTableOfNations)
        app.registerEvent(win.createTableOfStronyKonfliktu)
        app.stopTab()


        #TAG DRUGI---------------------------------------------------------------------------------------------------

        app.startTab(win.lista_tab[1])
        app.setStretch("column")
        app.setSticky("new")
        app.addImage("tlo2", "dnd2.gif", 0, colspan=2)
        app.setBg(colour="beige", override=False)
        app.setStretch('column')
        app.setSticky('wen')
        app.addLabel('bottom2', '', 1, colspan=2)
        app.setLabelBg("bottom2", "darkred")

        app.setStretch('column')
        app.setSticky('wen')
        app.setPadding([20, 20])

        app.addLabelOptionBox("Wybierz klasę", win.lista_class, 2, 0)
        app.addButtons(["Wyświetl umiejętności klasy"], win.createTableOfAbilities, 2, 1)

        app.registerEvent(win.createTableOfClass)
        app.registerEvent(win.createTableOfPochodzenie)
        # app.addLabel("loop", "New Row", app.getRow(), 0)
        # app.addButtons(["Show Classes"], win.createTableOfClass)
        app.stopTab()

        #TAG TRZECI---------------------------------------------------------------------------------------------------

        app.startTab(win.lista_tab[2])
        app.setStretch("column")
        app.setSticky("new")
        app.addImage("tlo3", "dnd2.gif", colspan=5)
        app.setBg(colour="beige", override=False)
        app.setStretch('column')
        app.setSticky('wen')
        app.addLabel('bottom3', '', 1, colspan=5)
        app.setLabelBg("bottom3", "darkred")

        app.setSticky("we")
        app.setPadding([20, 10])

        app.addLabelOptionBox("Lista ras : ", win.lista_races, 2, 0)
        app.addButtons(["Edytuj Rasę"], win.loadRaceData, 2, 1)
        app.setSticky("w")
        app.addLabel("Edytowanie Rasy :", "~~Edytowanie Rasy~~", 3, 0)
        app.addLabel("pusty91", "                            ", 3, 2)
        #app.addLabelEntry("Nazwa rasy :", 4, 0, colspan=3)
        app.addLabel("RasaDoWczytania2", "Opis rasy :", 4, 0)
        app.setSticky("nwes")
        app.addTextArea("Opis rasy :", 5, 0, colspan=2, rowspan=4)
        app.setSticky("w")
        app.addLabelEntry("Długość życia :", 9, 0)
        app.addLabelOptionBox("Pod / Dod :", win.pod_dod, 10, 0)
        app.setSticky("we")
        app.addLabelEntry("Dodatek :", 11, 0)
        app.setSticky("w")
        app.addLabelOptionBox("Efekt rasy :", win.lista_efektow, 12, 0)
        app.addLabelOptionBox("Nazwa języka :", win.lista_jezykow, 13, 0)
        app.addButtons(['Zmień dane '], win.editRasy, 13, 1)

        app.addLabel("Dodaj nowy efekt", "Nowy efekt rasowy :", 2, 3)
        app.addButtons(['Dodaj efekt'], win.sendEffect, 2, 4)
        app.setSticky("we")
        app.addLabelEntry("Nazwa efektu :", 3, 3, colspan=2)
        app.setSticky("w")
        app.addLabel("EfektDoWczytania", "Opis efektu :", 4, 3, colspan=2)
        app.setSticky("nwes")
        app.addTextArea("Opis efektu :", 5, 3, colspan=2, rowspan=3)
        app.setSticky("w")
        app.addLabelOptionBox("Stat :", win.lista_statystyk, 8, 3)
        app.addLabelOptionBox("Wartość :", win.lista_wartosci, 8, 4)
        app.addLabel("puste92", "", 9, 3, colspan=2)
        app.setSticky("we")
        app.setPadding([0, 0])
        app.addLabel("puste93", "", 10, 3, colspan=2)
        app.setLabelBg("puste93", "darkred")
        app.setSticky("w")
        app.setPadding([20, 10])
        app.addLabel("Dodaj nowy język", "Nowy język :", 11, 3)
        app.addButtons(['Dodaj język'], win.sendJezyk, 11, 4)
        app.setSticky("we")
        app.addLabelEntry("Nazwa nowego języka :", 12, 3, colspan=2)


        app.registerEvent(win.createTableOfEfektAndJezyk)
        app.stopTab()


        #TAG CZWARTY---------------------------------------------------------------------------------------------------

        app.startTab(win.lista_tab[3])
        app.setStretch("column")
        app.setSticky("new")
        app.addImage("tlo4", "dnd2.gif", colspan=3)
        app.setBg(colour="beige", override=False)
        app.setStretch('column')
        app.setSticky('wen')
        app.addLabel('bottom4', '', 1, colspan=3)
        app.setLabelBg("bottom4", "darkred")

        app.setSticky("we")
        app.setPadding([20, 10])

        app.addLabelOptionBox("Lista Krajów pochodzenia : ", win.lista_krajow, 2, 0)
        app.setSticky("w")
        app.addButtons(["Edytuj Kraj"], win.loadNationData, 2, 1)

        app.addLabel("Edytowanie Kraju pochodzenia :", "~~Edytowanie Kraju pochodzenia~~", 3, 0)

        #app.addLabelEntry("Nazwa Kraju pochodzenia :", 4, 0)
        app.addLabelEntry("Stolica :", 4, 0)
        app.addLabelOptionBox("Strona konfliktu :", win.lista_stron_kon, 5, 0)
        app.addLabelOptionBox("Język urzędowy :", win.lista_jezykow, 6, 0)
        app.addButtons(['Zmień dane   '], win.editKraje, 6, 1)

        app.setPadding([0, 0])
        app.setSticky("nes")
        app.addImage("krolKraje", "krol.gif", 2, 2, rowspan=50)
        app.stopTab()

        # TAG PIĄTY---------------------------------------------------------------------------------------------------

        app.startTab(win.lista_tab[4])
        app.setStretch("column")
        app.setSticky("new")
        app.addImage("tlo5", "dnd2.gif", colspan=3)
        app.setBg(colour="beige", override=False)
        app.setStretch('column')
        app.setSticky('wen')
        app.addLabel('bottom5', '', 1, colspan=3)
        app.setLabelBg("bottom5", "darkred")

        app.stopTab()
        app.stopTabbedFrame()

        app.setTabbedFrameBg("Start", "darkred")

        app.setTabbedFrameDisableAllTabs("Start", disabled=True)
        # app.setTabBg(title = "Start", tab = win.lista_tab[0], colour="darkred")
        # app.buttons(['LOGIN', 'EXIT'], win.login)
        # app.registerEvent(win.createDB)
        # app.setTabbedFrameSelectedTab("Start", "2")