from databaseConnection import connection
from appJar import gui
from PIL import Image, ImageTk
import datetime


class window():

    def __init__(self):
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
        self.EfektAndJezyk = 1
        self.lista_sex = ["N", "F", "M"]
        self.lista_stat = []
        self.postacie_index = []
        self.pod_dod = ["Pod", "Dod"]
        for i in range(21):
            self.lista_stat.append(i)
        self.lista_tab = ["Karty Postaci", "Klasy & Umiejętności", "Rasy & Pochodzenie", "Zarządzanie danymi"]
        for t in range(len(self.lista_tab)):
            tmp = ""
            n = len(max(self.lista_tab)) - len(self.lista_tab[t])
            while (n > 0):
                tmp += " "
                n -= 1
            self.lista_tab[t] = self.lista_tab[t] + tmp
        self.lista_postaci = ["---------"]

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
        else:
            app.stop()

    def confirm(self, button):
        if button == "Cancel":
            app.destroySubWindow("Logowanie")
        else:
            app.enableMenuItem("Open", "Log Out")
            app.disableMenuItem("Open", "Login")
            usr = app.getEntry("Username")
            pwd = app.getEntry("Password ")
            self.database = connection(usr, pwd)
            app.destroySubWindow("Logowanie")

    def sendCharacter(self):
        nazwa = app.getEntry("Nazwa")
        levela = app.getOptionBox("Level Postaci")
        plec = app.getOptionBox("Płeć")
        rasa = app.getEntry("Rasa")
        pochodzenia = app.getEntry("Pochodzenie")
        klasa = app.getOptionBox("Klasa")
        wiek = app.getEntry("Wiek")
        wzrost = app.getEntry("Wzrost")
        waga = app.getEntry("Waga")
        skora = app.getEntry("Kolor skóry")
        wlosy = app.getEntry("Kolor włosów")
        oczy = app.getEntry("Kolor oczów")
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

    def doNothing(self):
        pass

    def makeLogin(self):
        with app.subWindow('Logowanie', modal=True):
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
        app.enableMenuItem("Open", "Login")
        app.disableMenuItem("Open", "Log Out")
        self.database = None
        self.lista = []
        self.createdInt = 1
        self.createdInt3 = 1
        self.lista_class = ["---------"]
        self.createdPostacie = 1
        self.lista_postaci = ["---------"]
        self.lista_races = ["---------"]
        self.canLoad = 1
        self.lista_krajow = ["---------"]
        self.createdKraj = 1
        self.lista_jezykow = ["---------"]
        self.lista_efektow = ["--------------------"]
        self.EfektAndJezyk = 1
        app.openTab("Start", self.lista_tab[1])
        app.changeOptionBox("Wybierz klasę", self.lista_class, 0, 0)
        app.changeOptionBox("Klasa", self.lista_class, 0, 0)
        app.changeOptionBox("Klasa :", self.lista_class, 0, 0)
        app.changeOptionBox("Rasa :", self.lista_races, 0, 0)
        app.changeOptionBox("Pochodzenie :", self.lista_krajow, 0, 0)
        app.changeOptionBox("Nazwa języka :", self.lista_jezykow)
        app.changeOptionBox("Efekt rasy :", self.lista_efektow)
        app.stopTab()
        app.infoBox("Wylogowywanie", "Nastąpiło poprawne wylogowanie z Bazy Danych", parent=None)

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
            app.changeOptionBox("Pochodzenie :", self.lista_krajow)

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

            app.openTab("Start", self.lista_tab[3])
            app.setStretch('column')
            app.setSticky('wen')
            app.addLabel('postac', '', 2, 0)
            app.setLabelBg("postac", "indianred")
            app.addLabel('postaca', '', 2, 1)
            app.setLabelBg("postaca", "indianred")
            app.addLabel('postacb', '', 2, 2)
            app.setLabelBg("postacb", "indianred")
            app.setSticky("news")
            app.setPadding([20, 20])
            app.addTable("tabela_pochodzeń", klasyLista, wrap="700", row=5)

            klasyLista = []
            klasyDBNaglowek = self.database.cursor().execute(
                "select column_name from user_tab_cols where table_name = 'RASY'")
            klasyDB = self.database.cursor().execute("select * from rasy r inner join efekty_rasowe e on r.nazwa_efektu = e.nazwa_efektu")

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
            app.setOptionBox("Pochodzenie :", postacDB[19])
            app.setOptionBox("Klasa :", postacDB[20])

            app.setEntry("Wiek :", postacDB[3])
            app.setEntry("Wzrost :", postacDB[4])
            app.setEntry("Waga :", postacDB[5])

            app.setEntry("Kolor skóry :", postacDB[7])
            app.setEntry("Kolor włosów :", postacDB[8])
            app.setEntry("Kolor oczów :", postacDB[9])

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
        pochodzenia = app.getOptionBox("Pochodzenie :")
        klasa = app.getOptionBox("Klasa :")
        wiek = app.getEntry("Wiek :")
        wzrost = app.getEntry("Wzrost :")
        waga = app.getEntry("Waga :")
        skora = app.getEntry("Kolor skóry :")
        wlosy = app.getEntry("Kolor włosów :")
        oczy = app.getEntry("Kolor oczów :")
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

    def createTableOfAbilities(self):
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
                app.setStretch("column")
                app.setSticky("ew")
                app.addImage(f"klasy{self.tabOfAb}", "dnd2.gif", colspan=3)
                app.setStretch("both")
                app.setSticky("news")
                app.setPadding([20, 20])
                app.addTable(f"tabela_umiejetnosci_dla_klas{self.tabOfAb}", umiejLista, wrap="500")

    def createNewCharacterWindow(self):
        with app.subWindow("Dodaj nową postać", modal=True):
            app.showSubWindow("Dodaj nową postać")
            app.setResizable(canResize=False)
            app.setSize(1280, 720)
            app.setBg(colour="beige", override=False)
            app.setStretch("column")
            app.setSticky("new")
            app.addImage("smokPostac", "dnd2.gif", 0, colspan=4)

            app.setPadding([20, 0])
            app.setStretch("column")
            app.setSticky("w")
            app.addLabel("KartaPos", "Karta Postaci", 1, 0)
            app.addButtons(["Zatwierdź postać"], win.sendCharacter, 1, 1)

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
            app.addLabelEntry("Kolor oczów", 5, 2)

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

            app.setPadding([0, 0])
            app.setSticky("nwes")
            app.addImage("krol", "krol.gif", 1, 3, rowspan=50)
            # app.addImage("avatar", "avatar.gif", 8, 1)

            # app.setImageSize("avatar", width=300, height=300)
            # app.setImage("avatar", "avatar.gif")


if __name__ == "__main__":
    win = window()
    with gui('Baza Danych RPG') as app:
        app.setResizable(canResize=True)
        app.setSize(1280, 720)
        fileMenu = ["Login", "Log Out"]
        app.addMenuList("Open", fileMenu, [win.makeLogin, win.makeLogOut])
        app.disableMenuItem("Open", "Log Out")

        app.startTabbedFrame("Start")

        app.startTab(win.lista_tab[0])
        app.setStretch("column")
        app.setSticky("new")
        app.addImage("tlo1", "dnd2.gif", 0, colspan=4)
        app.setSticky("we")
        app.setPadding([20, 0])
        app.addLabelOptionBox("Lista postaci : ", win.lista_postaci, 1, 0, colspan=2)
        app.addLabel("pustaGlowna1", "", 1, 2)
        app.setSticky("w")
        app.addButtons(["Edytuj Postać"], win.loadCharacterData, 2, 0)
        app.addButtons(["Nowa Postać   "], win.createNewCharacterWindow, 2, 1)

        app.setStretch("column")
        app.setSticky("w")
        app.addLabel("KartaPos_g", "Karta Postaci", 3, 0)
        app.addButtons(["Zmień dane postać"], win.doNothing, 3, 1)

        app.setSticky("w")
        app.addLabelEntry("Nazwa :", 4, 0)
        app.addLabelOptionBox("Level Postaci :", win.lista_stat, 4, 1)
        app.addLabelOptionBox("Płeć :", win.lista_sex, 4, 2)

        app.addLabelOptionBox("Rasa :", win.lista_races, 5, 0)
        app.addLabelOptionBox("Pochodzenie :", win.lista_krajow, 5, 1)
        app.addLabelOptionBox("Klasa :", win.lista_class, 5, 2)

        app.addLabelEntry("Wiek :", 6, 0)
        app.addLabelEntry("Wzrost :", 6, 1)
        app.addLabelEntry("Waga :", 6, 2)

        app.addLabelEntry("Kolor skóry :", 7, 0)
        app.addLabelEntry("Kolor włosów :", 7, 1)
        app.addLabelEntry("Kolor oczów :", 7, 2)

        app.setSticky("e")
        app.addLabelEntry("HP :", 8, 0)
        app.setSticky("w")
        app.addLabelEntry("STA :", 8, 1)
        app.setSticky("w")
        # app.addLabelEntry("Plik z avatarem", 7, 1, colspan=2)

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
        app.addImage("krolGlowny", "krol.gif", 1, 3, rowspan=50)
        app.registerEvent(win.createTableOfCharacters)
        app.registerEvent(win.createTableOfRaces)
        app.registerEvent(win.createTableOfNations)
        # app.addImage("avatar", "avatar.gif", 8, 1)

        # app.setImageSize("avatar", width=300, height=300)
        # app.setImage("avatar", "avatar.gif")

        app.setBg(colour="beige", override=False)
        app.stopTab()

        app.startTab(win.lista_tab[1])
        app.setStretch("column")
        app.setSticky("new")
        app.addImage("tlo2", "dnd2.gif", 0, colspan=2)

        app.setStretch('column')
        app.setSticky('wen')
        app.addLabel('bottom3', '', 1, colspan=2)
        app.setLabelBg("bottom3", "darkred")

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

        app.startTab(win.lista_tab[2])
        app.setStretch("column")
        app.setSticky("new")
        app.addImage("tlo3", "dnd2.gif", colspan=4)

        app.setSticky("w")
        app.setPadding([20, 10])
        app.addLabel("Dodawanie Rasy", "Dodawanie Rasy", 1, 0)
        app.addLabel("puste31", "", 1, 1)
        app.addLabel("Dodawanie Pochodzenia", "Dodawanie Pochodzenia", 1, 2)
        app.addLabel("puste32", "", 1, 3)
        app.addLabelEntry("Nazwa rasy :", 2, 0)
        app.addLabel("RasaDoWczytania", "Opis rasy:", 3, 0)
        app.setSticky("nwes")
        app.addTextArea("Opis rasy :", 4, 0, colspan=1, rowspan=4)
        app.setSticky("w")
        app.addLabelEntry("Długość życia:", 8, 0)
        app.addLabelOptionBox("Pod / Dod :", win.pod_dod, 9, 0)
        app.addLabelOptionBox("Efekt rasy :", win.lista_efektow, 10, 0)
        app.addLabelOptionBox("Nazwa języka :", win.lista_jezykow, 11, 0)
        app.addButtons(['Dodaj rasę'], win.doNothing, 11, 1)
        app.registerEvent(win.createTableOfEfektAndJezyk)
        app.stopTab()

        app.startTab(win.lista_tab[3])
        app.setStretch("column")
        app.setSticky("new")
        app.addImage("tlo4", "dnd2.gif")

        app.setStretch('column')
        app.setSticky('wen')
        app.addLabel('bottom2', '', 1, colspan=2)
        app.setLabelBg("bottom2", "darkred")



        app.addLabel("")

        app.stopTab()
        app.stopTabbedFrame()

        app.setTabbedFrameBg("Start", "darkred")
        # app.setTabBg(title = "Start", tab = win.lista_tab[0], colour="darkred")
        # app.buttons(['LOGIN', 'EXIT'], win.login)
        # app.registerEvent(win.createDB)
        # app.setTabbedFrameSelectedTab("Start", "2")