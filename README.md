# **OT_Color_Challenge – Game Design Document – SK**

Daný repozitár obsahuje záverečný projekt k predmetu Objektové technológie. Projekt predstavuje funkčný prototyp hry v Pygame na zvolenú tému. Pri tvorbe hry boli využité znalosti nadobudnuté počas prednášok a cvičení z predmetu.

**Autor**: Laura Kabáthová

**Vybraná téma**: Color as a gameplay feature – farba ako herná mechanika

---
## **1. Úvod**
Hra slúži ako podklad pre úspešnú obhajobu skúšky z predmetu Objektové technológie. Požiadavky zvolenej témy boli v navrhnutej hre splnené. Charakter hry spočíva v spájaní kociek rovnakej farby v mriežke, pričom hráč musí postupovať logicky, aby sa mu podarilo odstrániť všetky farebné kocky na hracej ploche.

### **1.1 Inšpirácia**
<ins>**Super Collapse!**</ins>

Super Collapse! je veľmi návyková hra, ktorá stavia na rýchlej logike a reflexoch.  Koncept hry spočíva v identifikácii a odstraňovaní skupiny troch alebo viacerých blokov rovnakej farby, čím sa tieto bloky „zbalia“ a uvoľnia miesto ďalším blokom nad nimi. V hre neustále pribúdajú nové riadky blokov, pričom rýchlosť prírastku sa zvyšuje. Hra je obohatená o rôzne herné mechaniky, ktoré napomáhajú hráčovi získať množstvo bodov a odstraňovať naraz viacero blokov.

<p align="center">
  <img src="https://github.com/LauraKabath/OT_ColorChallenge/blob/master/super_collapse.png" alt="SuperCollapse">
  <br>
  <em>Obrázok 1 Ukážka hry Super Collapse!</em>
</p>

<ins>**Tetris Attack/Panel de Pon**</ins>

Tetris Attack/Panel de Pon
Tetris Attack je logická hra založená na rýchlom myslení a strategickom plánovaní. Hráč manipuluje s dvojicami blokov rôznych farieb na hracej ploche, pričom ich cieľom je vytvoriť vodorovné alebo zvislé rady minimálne troch rovnakých farieb, aby tieto bloky zmizli. Hra ponúka viacero úrovní obtiažnosti, nekonečný režim na zlepšovanie skóre a bonusové kolá „Clear the Board“ pre získanie extra bodov.

<p align="center">
  <img src="https://github.com/LauraKabath/OT_ColorChallenge/blob/master/tetris_attack.png" alt="TetrisAttack">
  <br>
  <em>Obrázok 1 Ukážka hry Tetris Attack</em>
</p>

### **1.2 Herný zážitok**
Hra poskytuje zábavný a návykový zážitok, ktorý hráča núti strategicky uvažovať pri odstraňovaní farebných blokov. Vďaka jednoduchému ovládaniu a jasne definovanému cieľu je ideálna na oddych, pričom zároveň ponúka výzvu v podobe premysleného plánovania krokov na úplné vyčistenie hracej plochy.

### **1.3 Vývojový softvér**
- **Pygame-CE**: zvolený programovací jazyk,
-	**PyCharm 2023.3.4**: vybrané IDE,
-	**Pixabay.com**: zdroj zvukov do hry,
-	**Itch.io**: zdroj fontov do hry.

---
## **2. Koncept**

### **2.1 Prehľad hry**
Hráč používa myš na klikanie skupiny blokov rovnakej farby, aby ich odstránil z hracej plochy.  Počas hry sa postupne odomykajú špeciálne vylepšenia, ktoré mu vedia pomôcť v náročnej situácii.  Hráč musí premýšľať o tom, kedy a akým spôsobom vylepšenia použiť, aby vyčistil hraciu plochu čo najefektívnejšie a dosiahol tým najlepší výsledok.

### **2.2 Interpretácia témy (Swarms - príklad témy)**
**„Color as a gameplay feature“** – farba plní hlavnú úlohu mechanizmu interakcie hráča s herným prostredím. Na hracej ploche hráč strategicky odstraňuje bloky rovnakej farby. Po odstránení sa ich miesto automaticky upraví, čím sa vytvára priestor pre ďalšie ťahy. Farba neslúži iba ako vizuálny prvok, ale ako kľúčový nástroj stratégie, ktorý hráč využíva na dosiahnutie svojich herných cieľov a zvládanie čoraz zložitejších výziev.

### **2.3 Základné mechaniky**
-	**Odstraňovanie blokov**: hlavná mechanika spočíva v klikaní a odstraňovaní skupín blokov rovnakej farby z hracej plochy.
-	**Posúvanie blokov**: po odstránení blokov sa zvyšné bloky posúvajú nadol, v prípade odstránenia stĺpca sa bloky posunú aj doľava.
-	**Thunder Button**: po stlačení tlačidla sa náhodne vybrané polia blokov zmenia sa stanovenú farbu, čo umožní vytváranie nových väčších skupín blokov s cieľom získať vyšší bodový zisk. Tlačidlo sa aktivuje ak je v hracom poli menej ako 80 blokov.
-	**Boost Bomba**: odstráni bloky v dosahu jedného štvorca v štyroch smeroch, čím výrazne upraví rozloženie hracej plochy.
-	**Delete Button**: po stlačení tlačidla sa odstránia bloky jednej konkrétnej farby, farba je generovaná náhodne, čo hráčovi poskytne možnosť rýchlejšie vyčistiť hraciu plochu. Tlačidlo sa aktivuje ak je v hracom poli menej ako 55 blokov.
-	**Skóre a odmeny**: hráč je odmeňovaný bodmi za úspešné odstránenie blokov. Za väčšie skupiny odstránených blokov získa hráč viac bodov. Ak hráč použije špeciálne vylepšenie (Thunder Button, Boost Bomba, Delete Button) získané skóre bude podstatne nižšie.

### **2.4 Návrh tried**
- **Game**: trieda, v ktorej sa nachádza hlavná herná logika (štart menu, exit menu, hlavná herná slučka, výpočet skóre, aktivácia a deaktivácia špeciálnych vylepšení)
-	**Grid**: trieda predstavujúca hraciu plochu, zabezpečuje vykreslenie farebných blokov, označenie vybraných blokov,  odstraňovanie a posúvanie blokov. Taktiež zabezpečuje logiku špeciálnych vylepšení. 
-	**Player**: trieda hráča, ktorá uchováva informácie o nadobudnutých bodoch počas hry a na konci zabezpečí ich výpis.
-	**ColorButton**: trieda špeciálneho tlačidla, zabezpečuje vykreslenie, obsahuje metódy na aktivovanie a deaktivovanie, mení svoju farbu na základe splnenia podmienky a náhody.
-	**Boost, Button, Text**: triedy zabezpečujúce grafický dizajn hry.
