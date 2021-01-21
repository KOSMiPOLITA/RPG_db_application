drop sequence POSTACIE_SEQ;
create sequence POSTACIE_SEQ start with 1 increment by 1;

drop bitmap index klasy_bmp_idx on klasy(nazwa);
drop index poziom_idx on umiejetnosci(poziom);
drop index umiejetnosci_idx on umiejetnosci(nazwa);
drop index postacie_idx on postacie(nazwa_postaci);

create bitmap index klasy_bmp_idx on klasy(nazwa);
create index poziom_idx on umiejetnosci(poziom);
create index umiejetnosci_idx on umiejetnosci(nazwa);
create index postacie_idx on postacie(nazwa_postaci);

drop table Efekty_rasowe cascade constraints;
drop table Jezyki cascade constraints;
drop table Rasy cascade constraints;
drop table Strony_konfliktu cascade constraints;
drop table Kraje_pochodzenia cascade constraints;
drop table Umiejetnosci cascade constraints;
drop table Klasy cascade constraints;
drop table UmiejetnosciDlaKlas cascade constraints;
drop table Postacie cascade constraints;


create table Jezyki (
	nazwa varchar2(100) primary key );
	

create table Efekty_rasowe (
	nazwa_efektu varchar2(100) PRIMARY KEY,
	opis_efektu varchar2(400) NOT NULL,
	statystyka varchar2(3) NOT NULL check(statystyka in ('HP','STA','STR','DEX','CON','INT','WIS','CHA')),
	wartosc_wzm number(3) NOT NULL);


create table Rasy (
	nazwa varchar2(100) primary key,
  	opis_rasy varchar2(750) not null,
  	srd_dlugosc_zycia number(4) not null check(srd_dlugosc_zycia > 0),
	P_D varchar2(3) check(P_D in ('Pod','Dod')) not null, 	
  	nazwa_dodatku varchar2(150),
  	nazwa_efektu varchar2(100) references Efekty_rasowe(nazwa_efektu) not null,
	nazwa_jezyka varchar2(100) references Jezyki(nazwa) not null);
	

create table Strony_konfliktu (
  	nazwa varchar2(100) primary key,
  	od_kiedy date not null,
	glowna_siedziba varchar2(100) not null);
	

create table Kraje_pochodzenia (
  	nazwa varchar2(200) primary key,
	stolica varchar2(100) not null,
	jezyk_urzedowy varchar2(100) references Jezyki(nazwa) not null,
  	nazwa_strony varchar2(100) references Strony_konfliktu(nazwa) not null);
	
	
create table Umiejetnosci (
  	nazwa varchar2(100) primary key,
  	opis_umiejetnosci varchar2(750) not null,
  	poziom number(4) not null,
  	dmg number(4), heal number(4), def number (4),
	P_D varchar2(3) check(P_D in ('Pod','Dod')) not null,
	nazwa_dodatku varchar2(150));
	
	
create table Klasy (
  	nazwa varchar2(100) primary key,
  	opis_klasy varchar2(750) not null );
	
	
create table UmiejetnosciDlaKlas (
	klasa varchar2(100) references Klasy(nazwa),
	umiejetnosc varchar2(100) references Umiejetnosci(nazwa),
	PRIMARY KEY( klasa, umiejetnosc));


create table Postacie (
	id_karty NUMBER(5) PRIMARY KEY,
   	nazwa_postaci VARCHAR2(50) NOT NULL,
    poziom NUMBER(2) NOT NULL,
   	wiek NUMBER(4) NOT NULL,
    wzrost NUMBER(5, 2) NOT NULL,
    waga NUMBER(5, 2) NOT NULL,
    plec VARCHAR2(1) check(plec in ('M','F','N')),
    kolor_skory VARCHAR2(50),
    kolor_włosow VARCHAR2(50),
    kolor_oczow VARCHAR2(50),
	"HP" NUMBER(3) NOT NULL,
    "STA" NUMBER(3) NOT NULL,
    "STR" NUMBER(3) NOT NULL,
    "DEX" NUMBER(3) NOT NULL,
    "CON" NUMBER(3) NOT NULL,
    "INT" NUMBER(3) NOT NULL,
    "WIS" NUMBER(3) NOT NULL,
    "CHA" NUMBER(3) NOT NULL, 
	nazwa_rasy varchar2(100) references Rasy(nazwa) not null,
	nazwa_kraju varchar2(200) references Kraje_pochodzenia(nazwa) not null,
	nazwa_klasy varchar2(100) references Klasy(nazwa) not null );

alter table rasy add constraint chk_age check(srd_dlugosc_zycia > 50);

alter table postacie add constraint chk_wiek check(wiek > 0);
alter table postacie add constraint chk_wzrost check(wzrost > 50);
alter table postacie add constraint chk_waga check(waga > 0);

alter table postacie add constraint chk_hp check(hp > 0);
alter table postacie add constraint chk_sta check(sta > 0);

create role uzyt_bazy_rpg;
grant SELECT, INSERT, DELETE, UPDATE on inf141249.efekty_rasowe to uzyt_bazy_rpg;
grant SELECT, INSERT, DELETE, UPDATE on inf141249.jezyki to uzyt_bazy_rpg;
grant SELECT, INSERT, DELETE, UPDATE on inf141249.klasy to uzyt_bazy_rpg;
grant SELECT, INSERT, DELETE, UPDATE on inf141249.kraje_pochodzenia to uzyt_bazy_rpg;
grant SELECT, INSERT, DELETE, UPDATE on inf141249.postacie to uzyt_bazy_rpg;
grant SELECT, INSERT, DELETE, UPDATE on inf141249.rasy to uzyt_bazy_rpg;
grant SELECT, INSERT, DELETE, UPDATE on inf141249.strony_konfilktu to uzyt_bazy_rpg;
grant SELECT, INSERT, DELETE, UPDATE on inf141249.umiejetnosci to uzyt_bazy_rpg;
grant SELECT, INSERT, DELETE, UPDATE on inf141249.umiejetnoscidlaklas to uzyt_bazy_rpg;
GRANT SELECT, ALTER ON inf141249.POSTACIE_SEQ TO uzyt_bazy_rpg;

--PRRRRRRRRRRRRRRRRRRRRRRRRRROOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEDURY

drop package body RPG;
drop package RPG;

create or replace package RPG as

PROCEDURE NowyEfektRasowy
    (pNazwa IN VARCHAR2,
     pOpis IN VARCHAR2,
	 pStat in VARCHAR2,
	 pWart in NUMBER);


PROCEDURE UsunEfektRasowy
    (pNazwa IN VARCHAR2);


PROCEDURE NowyJezyk
    (pNazwa IN VARCHAR2);


PROCEDURE UsunJezyk
    (pNazwa IN VARCHAR2);

	
PROCEDURE NowaRasa
    (pNazwa IN VARCHAR2,
     pOpis IN VARCHAR2,
	 pSrd in NUMBER,
	 pP_D IN VARCHAR2,
	 pDodatek IN VARCHAR2,
	 pEfekt IN VARCHAR2,
	 pJezyk IN VARCHAR2);


PROCEDURE UsunRase
    (pNazwa IN VARCHAR2);


PROCEDURE NowaStrona
    (pNazwa IN VARCHAR2,
     pData IN DATE,
	 pSiedziba in VARCHAR2);


PROCEDURE UsunStrone
    (pNazwa IN VARCHAR2);


PROCEDURE NowyKraj
    (pNazwa IN VARCHAR2,
     pStolica IN VARCHAR2,
	 pJezyk in VARCHAR2,
	 pSiedziba IN VARCHAR2);


PROCEDURE UsunKraj
    (pNazwa IN VARCHAR2);


PROCEDURE NowaKlasa
    (pNazwa IN VARCHAR2,
     pOpis IN VARCHAR2);


PROCEDURE UsunKlase
    (pNazwa IN VARCHAR2);


PROCEDURE NowaUmiejetnoscDMG
    (pNazwa IN VARCHAR2,
     pOpis IN VARCHAR2,
	 pPoziom IN NUMBER,
	 pDMG IN NUMBER,
	 pP_D IN VARCHAR2,
	 pDod IN VARCHAR2,
     pKlasa0 IN VARCHAR2 DEFAULT NULL,
     pKlasa1 IN VARCHAR2 DEFAULT NULL,
     pKlasa2 IN VARCHAR2 DEFAULT NULL,
     pKlasa3 IN VARCHAR2 DEFAULT NULL,
     pKlasa4 IN VARCHAR2 DEFAULT NULL,
     pKlasa5 IN VARCHAR2 DEFAULT NULL,
     pKlasa6 IN VARCHAR2 DEFAULT NULL);
	 

PROCEDURE NowaUmiejetnoscDEF
    (pNazwa IN VARCHAR2,
     pOpis IN VARCHAR2,
	 pPoziom IN NUMBER,
	 pDEF IN NUMBER,
	 pP_D IN VARCHAR2,
	 pDod IN VARCHAR2,
     pKlasa0 IN VARCHAR2 DEFAULT NULL,
     pKlasa1 IN VARCHAR2 DEFAULT NULL,
     pKlasa2 IN VARCHAR2 DEFAULT NULL,
     pKlasa3 IN VARCHAR2 DEFAULT NULL,
     pKlasa4 IN VARCHAR2 DEFAULT NULL,
     pKlasa5 IN VARCHAR2 DEFAULT NULL,
     pKlasa6 IN VARCHAR2 DEFAULT NULL);
	 

PROCEDURE NowaUmiejetnoscHEAL
    (pNazwa IN VARCHAR2,
     pOpis IN VARCHAR2,
	 pPoziom IN NUMBER,
	 pHEAL IN NUMBER,
	 pP_D IN VARCHAR2,
	 pDod IN VARCHAR2,
     pKlasa0 IN VARCHAR2 DEFAULT NULL,
     pKlasa1 IN VARCHAR2 DEFAULT NULL,
     pKlasa2 IN VARCHAR2 DEFAULT NULL,
     pKlasa3 IN VARCHAR2 DEFAULT NULL,
     pKlasa4 IN VARCHAR2 DEFAULT NULL,
     pKlasa5 IN VARCHAR2 DEFAULT NULL,
     pKlasa6 IN VARCHAR2 DEFAULT NULL);


PROCEDURE UsunUmiejetnosc
    (pNazwa IN VARCHAR2);


PROCEDURE PolaczKlasaUmiejetnosc
    (pNazwa IN VARCHAR2,
     pNazwa2 IN VARCHAR2);


PROCEDURE RozwiazKlasaUmiejetnosc
    (pNazwa IN VARCHAR2,
	 pNazwa2 IN VARCHAR2);


PROCEDURE DodajPostac
	(pImie IN VARCHAR2,
	 pLevel IN NUMBER,
	 pWiek IN NUMBER,
	 pWzrost IN NUMBER,
	 pWaga IN NUMBER,
	 pPlec IN VARCHAR2 DEFAULT 'N',
	 pKolorS IN VARCHAR2 DEFAULT NULL,
	 pKolorW IN VARCHAR2 DEFAULT NULL,
	 pKolorO IN VARCHAR2 DEFAULT NULL,
	 pHP IN NUMBER,
	 pSTA IN NUMBER,
	 pSTR IN NUMBER,
	 pDEX IN NUMBER,
	 pCON IN NUMBER,
	 pINT IN NUMBER,
	 pWIS IN NUMBER,
	 pCHA IN NUMBER,
	 pRasa IN VARCHAR2,
	 pKraj IN VARCHAR2,
	 pKlasa IN VARCHAR2);


PROCEDURE UsunPostac
    (pId IN NUMBER);

end RPG;


create or replace package body RPG as


PROCEDURE NowyEfektRasowy
    (pNazwa IN VARCHAR2,
     pOpis IN VARCHAR2,
	 pStat in VARCHAR2,
	 pWart in NUMBER) IS
BEGIN
    INSERT INTO Efekty_rasowe values(pNazwa, pOpis, pStat, pWart);
END NowyEfektRasowy;


PROCEDURE UsunEfektRasowy
    (pNazwa IN VARCHAR2) IS
BEGIN
    DELETE FROM Efekty_rasowe where nazwa_efektu = pNazwa;
END UsunEfektRasowy;


PROCEDURE NowyJezyk
    (pNazwa IN VARCHAR2) IS
BEGIN
    INSERT INTO Jezyki values(pNazwa);
END NowyJezyk;


PROCEDURE UsunJezyk
    (pNazwa IN VARCHAR2) IS
BEGIN
    DELETE FROM Jezyki where nazwa = pNazwa;
END UsunJezyk;

	
PROCEDURE NowaRasa
    (pNazwa IN VARCHAR2,
     pOpis IN VARCHAR2,
	 pSrd in NUMBER,
	 pP_D IN VARCHAR2,
	 pDodatek IN VARCHAR2,
	 pEfekt IN VARCHAR2,
	 pJezyk IN VARCHAR2) IS
BEGIN
    INSERT INTO Rasy values(pNazwa, pOpis, pSrd, pP_D, pDodatek, pEfekt, pJezyk);
END NowaRasa;


PROCEDURE UsunRase
    (pNazwa IN VARCHAR2) IS
BEGIN
    DELETE FROM Rasy where nazwa = pNazwa;
END UsunRase;



PROCEDURE NowaStrona
    (pNazwa IN VARCHAR2,
     pData IN DATE,
	 pSiedziba in VARCHAR2) IS
BEGIN
    INSERT INTO Strony_konfliktu values(pNazwa, pData, pSiedziba);
END NowaStrona;


PROCEDURE UsunStrone
    (pNazwa IN VARCHAR2) IS
BEGIN
    DELETE FROM Strony_konfliktu where nazwa = pNazwa;
END UsunStrone;


PROCEDURE NowyKraj
    (pNazwa IN VARCHAR2,
     pStolica IN VARCHAR2,
	 pJezyk in VARCHAR2,
	 pSiedziba IN VARCHAR2) IS
BEGIN
    INSERT INTO Kraje_pochodzenia values(pNazwa, pStolica, pJezyk, pSiedziba);
END NowyKraj;


PROCEDURE UsunKraj
    (pNazwa IN VARCHAR2) IS
BEGIN
    DELETE FROM Kraje_pochodzenia where nazwa = pNazwa;
END UsunKraj;


PROCEDURE NowaKlasa
    (pNazwa IN VARCHAR2,
     pOpis IN VARCHAR2) IS
BEGIN
    INSERT INTO Klasy values(pNazwa, pOpis);
END NowaKlasa;


PROCEDURE UsunKlase
    (pNazwa IN VARCHAR2) IS
BEGIN
    DELETE FROM Klasy where nazwa = pNazwa;
END UsunKlase;


PROCEDURE NowaUmiejetnoscDMG
    (pNazwa IN VARCHAR2,
     pOpis IN VARCHAR2,
	 pPoziom IN NUMBER,
	 pDMG IN NUMBER,
	 pP_D IN VARCHAR2,
	 pDod IN VARCHAR2,
     pKlasa0 IN VARCHAR2 DEFAULT NULL,
     pKlasa1 IN VARCHAR2 DEFAULT NULL,
     pKlasa2 IN VARCHAR2 DEFAULT NULL,
     pKlasa3 IN VARCHAR2 DEFAULT NULL,
     pKlasa4 IN VARCHAR2 DEFAULT NULL,
     pKlasa5 IN VARCHAR2 DEFAULT NULL,
     pKlasa6 IN VARCHAR2 DEFAULT NULL) IS
BEGIN
    INSERT INTO Umiejetnosci (nazwa, opis_umiejetnosci, poziom, dmg, P_D, nazwa_dodatku) values(pNazwa, pOpis, pPoziom, pDMG, pP_D, pDod);
    IF pKlasa0 IS NOT NULL THEN
        INSERT INTO UmiejetnosciDlaKlas values(pKlasa0, pNazwa);
	END IF;
	IF pKlasa1 IS NOT NULL THEN
        INSERT INTO UmiejetnosciDlaKlas values(pKlasa1, pNazwa);
	END IF;
	IF pKlasa2 IS NOT NULL THEN
        INSERT INTO UmiejetnosciDlaKlas values(pKlasa2, pNazwa);
	END IF;
	IF pKlasa3 IS NOT NULL THEN
        INSERT INTO UmiejetnosciDlaKlas values(pKlasa3, pNazwa);
	END IF;
	IF pKlasa4 IS NOT NULL THEN
        INSERT INTO UmiejetnosciDlaKlas values(pKlasa4, pNazwa);
	END IF;
	IF pKlasa5 IS NOT NULL THEN
        INSERT INTO UmiejetnosciDlaKlas values(pKlasa5, pNazwa);
	END IF;
	IF pKlasa6 IS NOT NULL THEN
        INSERT INTO UmiejetnosciDlaKlas values(pKlasa6, pNazwa);
	END IF;
END NowaUmiejetnoscDMG;

PROCEDURE NowaUmiejetnoscDEF
    (pNazwa IN VARCHAR2,
     pOpis IN VARCHAR2,
	 pPoziom IN NUMBER,
	 pDEF IN NUMBER,
	 pP_D IN VARCHAR2,
	 pDod IN VARCHAR2,
     pKlasa0 IN VARCHAR2 DEFAULT NULL,
     pKlasa1 IN VARCHAR2 DEFAULT NULL,
     pKlasa2 IN VARCHAR2 DEFAULT NULL,
     pKlasa3 IN VARCHAR2 DEFAULT NULL,
     pKlasa4 IN VARCHAR2 DEFAULT NULL,
     pKlasa5 IN VARCHAR2 DEFAULT NULL,
     pKlasa6 IN VARCHAR2 DEFAULT NULL) IS
BEGIN
    INSERT INTO Umiejetnosci (nazwa, opis_umiejetnosci, poziom, def, P_D, nazwa_dodatku) values(pNazwa, pOpis, pPoziom, pDEF, pP_D, pDod);
	IF pKlasa0 IS NOT NULL THEN
        INSERT INTO UmiejetnosciDlaKlas values(pKlasa0, pNazwa);
	END IF;
	IF pKlasa1 IS NOT NULL THEN
        INSERT INTO UmiejetnosciDlaKlas values(pKlasa1, pNazwa);
	END IF;
	IF pKlasa2 IS NOT NULL THEN
        INSERT INTO UmiejetnosciDlaKlas values(pKlasa2, pNazwa);
	END IF;
	IF pKlasa3 IS NOT NULL THEN
        INSERT INTO UmiejetnosciDlaKlas values(pKlasa3, pNazwa);
	END IF;
	IF pKlasa4 IS NOT NULL THEN
        INSERT INTO UmiejetnosciDlaKlas values(pKlasa4, pNazwa);
	END IF;
	IF pKlasa5 IS NOT NULL THEN
        INSERT INTO UmiejetnosciDlaKlas values(pKlasa5, pNazwa);
	END IF;
	IF pKlasa6 IS NOT NULL THEN
        INSERT INTO UmiejetnosciDlaKlas values(pKlasa6, pNazwa);
	END IF;
END NowaUmiejetnoscDEF;

PROCEDURE NowaUmiejetnoscHEAL
    (pNazwa IN VARCHAR2,
     pOpis IN VARCHAR2,
	 pPoziom IN NUMBER,
	 pHEAL IN NUMBER,
	 pP_D IN VARCHAR2,
	 pDod IN VARCHAR2,
     pKlasa0 IN VARCHAR2 DEFAULT NULL,
     pKlasa1 IN VARCHAR2 DEFAULT NULL,
     pKlasa2 IN VARCHAR2 DEFAULT NULL,
     pKlasa3 IN VARCHAR2 DEFAULT NULL,
     pKlasa4 IN VARCHAR2 DEFAULT NULL,
     pKlasa5 IN VARCHAR2 DEFAULT NULL,
     pKlasa6 IN VARCHAR2 DEFAULT NULL) IS
BEGIN
    INSERT INTO Umiejetnosci (nazwa, opis_umiejetnosci, poziom, heal, P_D, nazwa_dodatku) values(pNazwa, pOpis, pPoziom, pHEAL, pP_D, pDod);
	IF pKlasa0 IS NOT NULL THEN
        INSERT INTO UmiejetnosciDlaKlas values(pKlasa0, pNazwa);
	END IF;
	IF pKlasa1 IS NOT NULL THEN
        INSERT INTO UmiejetnosciDlaKlas values(pKlasa1, pNazwa);
	END IF;
	IF pKlasa2 IS NOT NULL THEN
        INSERT INTO UmiejetnosciDlaKlas values(pKlasa2, pNazwa);
	END IF;
	IF pKlasa3 IS NOT NULL THEN
        INSERT INTO UmiejetnosciDlaKlas values(pKlasa3, pNazwa);
	END IF;
	IF pKlasa4 IS NOT NULL THEN
        INSERT INTO UmiejetnosciDlaKlas values(pKlasa4, pNazwa);
	END IF;
	IF pKlasa5 IS NOT NULL THEN
        INSERT INTO UmiejetnosciDlaKlas values(pKlasa5, pNazwa);
	END IF;
	IF pKlasa6 IS NOT NULL THEN
        INSERT INTO UmiejetnosciDlaKlas values(pKlasa6, pNazwa);
	END IF;
END NowaUmiejetnoscHEAL;


PROCEDURE UsunUmiejetnosc
    (pNazwa IN VARCHAR2) IS
BEGIN
    DELETE FROM Umiejetnosci where nazwa = pNazwa;
END UsunUmiejetnosc;


PROCEDURE PolaczKlasaUmiejetnosc
    (pNazwa IN VARCHAR2,
     pNazwa2 IN VARCHAR2) IS
BEGIN
    INSERT INTO UmiejetnosciDlaKlas values(pNazwa, pNazwa2);
END PolaczKlasaUmiejetnosc;


PROCEDURE RozwiazKlasaUmiejetnosc
    (pNazwa IN VARCHAR2,
	 pNazwa2 IN VARCHAR2) IS
BEGIN
    DELETE FROM UmiejetnosciDlaKlas where klasa = pNazwa and umiejetnosc = pNazwa2;
END RozwiazKlasaUmiejetnosc;


PROCEDURE DodajPostac
	(pImie IN VARCHAR2,
	 pLevel IN NUMBER,
	 pWiek IN NUMBER,
	 pWzrost IN NUMBER,
	 pWaga IN NUMBER,
	 pPlec IN VARCHAR2 DEFAULT 'N',
	 pKolorS IN VARCHAR2 DEFAULT NULL,
	 pKolorW IN VARCHAR2 DEFAULT NULL,
	 pKolorO IN VARCHAR2 DEFAULT NULL,
	 pHP IN NUMBER,
	 pSTA IN NUMBER,
	 pSTR IN NUMBER,
	 pDEX IN NUMBER,
	 pCON IN NUMBER,
	 pINT IN NUMBER,
	 pWIS IN NUMBER,
	 pCHA IN NUMBER,
	 pRasa IN VARCHAR2,
	 pKraj IN VARCHAR2,
	 pKlasa IN VARCHAR2) IS
BEGIN
	INSERT INTO Postacie values(POSTACIE_SEQ.NEXTVAL, pImie, pLevel, pWiek, pWzrost, pWaga, pPlec, pKolorS, pKolorW, 
								pKolorO, pHP, pSTA, pSTR, pDEX, pCON, pINT, pWIS, pCHA, pRasa, pKraj, pKlasa);
END;


PROCEDURE UsunPostac
    (pId IN NUMBER) IS
BEGIN
    DELETE FROM Postacie where id_karty = pId;
END UsunPostac;


end RPG;

insert into strony_konfilktu values('Rebelia', to_date('20/08/1012','DD/MM/YYYY'),'Bright Moon');
insert into strony_konfilktu values('Horda', to_date('11/12/1011','DD/MM/YYYY'),'Strefa Trwogi');
insert into strony_konfilktu values('Neutralni', to_date('12/05/1019','DD/MM/YYYY'),'???');

insert into efekty_rasowe values('Cats Claws', 'Because of your claws, you have a climbing speed of 20 feet. In addition, your claws are natural weapons, which you can use to make unarmed strikes.', 'DEX', 2);
insert into rasy values('Tabaxi', 'Hailing from a strange and distant land, wandering tabaxi are catlike humanoids driven by curiosity to collect interesting artifacts, gather tales and stories, and lay eyes on all the worlds wonders. ', 125, 'Pod', null, 'Cats Claws', 'common');
insert into kraje_pochodzenia values('Polska', 'Warszawa', 'common', 'Horda');
insert into kraje_pochodzenia values('Flania', 'Vertua', 'common', 'Rebelia');
insert into kraje_pochodzenia values('Imperium', '???', 'common', 'Horda');
insert into efekty_rasowe values('Draconic Ancestry', 'You have draconic ancestry. Choose one type of dragon from the Draconic Ancestry table. Your breath weapon and damage resistance are determined by the dragon type.', 'STR', 2);
insert into jezyki values('draconic');
insert into rasy values('Dragonborn', 'Born of dragons, as their name proclaims, the dragonborn walk proudly through a world that greets them with fearful incomprehension. ', 225, 'Pod', null, 'Draconic Ancestry', 'draconic');
insert into jezyki values('infernal');
insert into efekty_rasowe values('Infernal Legacy', 'You know the thaumaturgy cantrip. When you reach 3rd level, you can cast the hellish rebuke spell as a 2nd-level spell once with this trait and regain the ability to do so when you finish a long rest.', 'CHA', 2);

begin
  rpg.nowaumiejetnoscdmg('Acid Splash', 'You hurl a bubble of acid. Choose one or two creatures you can see within range.', 0, 3, 'Pod', null, 'Sorcerer', 'Wizard');
  rpg.nowaumiejetnoscdmg('Control Flames', 'You choose nonmagical flame that you can see within range and that fits within a 5-foot cube. ', 0, 5, 'Pod', null, 'Sorcerer', 'Wizard', 'Druid');
  rpg.nowaumiejetnoscdmg('Eldritch Blast', 'A beam of crackling energy streaks toward a creature within range. Make a ranged spell attack against the target. ', 0, 5, 'Pod', null, 'Warlock');
  rpg.nowaumiejetnoscdef('Encode Thoughts', 'You pull a memory, an idea, or a message from your mind and transform it into a tangible string of glowing energy called a thought strand, which persists for the duration or until you cast this spell again.', 0, 0, 'Dod', 'Guildmasters Guide to Ravnica', 'Wizard');
  rpg.nowaumiejetnoscdmg('Vicious Mockery', 'A enemy takes 2 psychic damage and have disadvantage on the next attack roll it ', 0, 2, 'Pod', null, 'Bard');
  rpg.nowaumiejetnoscdef('Charm Person', 'You attempt to charm a humanoid you can see within range. It must make a Wisdom saving throw, and does so with advantage if you or your companions are fighting it.', 1, 0, 'Pod', null, 'Bard', 'Druid', 'Sorcerer', 'Warlock', 'Wizard');
  rpg.nowaumiejetnoscheal('Cure Wounds', 'A creature you touch regains a number of hit points equal to 4.', 1, 4, 'Pod', null, 'Bard', 'Cleric', 'Paladin', 'Ranger');
  rpg.nowaumiejetnoscdmg('Dissonant Whispers', 'You whisper a discordant melody that only one creature of your choice within range can hear, wracking it with terrible pain. The target must make a Wisdom saving throw.', 1, 9, 'Dod', 'Players Handbook ', 'Bard');
  rpg.nowaumiejetnoscdef('Mage Armor', 'You touch a willing creature who is not wearing armor, and a protective magical force surrounds it until the spell ends. ', 1, 13, 'Pod', null, 'Sorcerer', 'Wizard');
  
  rpg.nowaklasa('Barbarian', 'A fierce warrior of primitive background who can enter a battle rage');
  rpg.nowaklasa('Bard', 'An inspiring magician whose power echoes the music of creation');
  rpg.nowaklasa('Cleric', 'A priestly champion who wields divine magic in service of a higher power');
  rpg.nowaklasa('Druid', 'A priest of the Old Faith, wielding the powers of nature and adopting animal forms');
  rpg.nowaklasa('Figter', 'A master of martial combat, skilled with a variety of weapons and armor');
  rpg.nowaklasa('Monk', 'A master of martial arts, harnessing the power of the body in pursuit of physical and spirital perfection');
  rpg.nowaklasa('Paladin', 'A holy warrior bound to a sacred oath');
  rpg.nowaklasa('Ranger', 'A warrior who combats threats on the edges of civilization');
  rpg.nowaklasa('Rogue', 'A scoundrel who uses stealth and trickery to overcome obstacles and enemies');
  rpg.nowaklasa('Sorcerer', 'A spellcaster who draws on inherent magic from a gift or bloodline');
  rpg.nowaklasa('Warlock', 'A wielder of magic that is derived from a bargain with an extraplanar entity');
  rpg.nowaklasa('Wizard', 'A scholary magic-user capable of manipulatin the structures of reality');
end;