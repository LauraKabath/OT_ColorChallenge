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
  <em>Obrázok 2 Ukážka hry Tetris Attack</em>
</p>

### **1.2 Herný zážitok**
Hra poskytuje zábavný a návykový zážitok, ktorý hráča núti strategicky uvažovať pri odstraňovaní farebných blokov. Vďaka jednoduchému ovládaniu a jasne definovanému cieľu je ideálna na oddych, pričom zároveň ponúka výzvu v podobe premysleného plánovania krokov na úplné vyčistenie hracej plochy.

### **1.3 Vývojový softvér**
- **Pygame-CE**: zvolený programovací jazyk,
-	**PyCharm 2023.3.4**: vybrané IDE,
-	**Pixabay.com**: zdroj zvukov do hry,
-	**Itch.io**: zdroj fontov do hry,
-	**Freepik.com**: zdroj grafických assetov do hry.

---
## **2. Koncept**

### **2.1 Prehľad hry**
Hráč používa myš na klikanie skupiny blokov rovnakej farby, aby ich odstránil z hracej plochy.  Počas hry sa postupne odomykajú špeciálne vylepšenia, ktoré mu vedia pomôcť v náročnej situácii.  Hráč musí premýšľať o tom, kedy a akým spôsobom vylepšenia použiť, aby vyčistil hraciu plochu čo najefektívnejšie a dosiahol tým najlepší výsledok.

### **2.2 Interpretácia témy (Color as a gameplay feature – farba ako herná mechanika)**
**„Color as a gameplay feature“** – farba plní hlavnú úlohu mechanizmu interakcie hráča s herným prostredím. Na hracej ploche hráč strategicky odstraňuje bloky rovnakej farby. Po odstránení sa ich miesto automaticky upraví, čím sa vytvára priestor pre ďalšie ťahy. Farba neslúži iba ako vizuálny prvok, ale ako kľúčový nástroj stratégie, ktorý hráč využíva na dosiahnutie svojich herných cieľov a zvládanie čoraz zložitejších výziev.

### **2.3 Základné mechaniky**
-	**Odstraňovanie blokov**: hlavná mechanika spočíva v klikaní a odstraňovaní skupín blokov rovnakej farby z hracej plochy.
-	**Posúvanie blokov**: po odstránení blokov sa zvyšné bloky posúvajú nadol, v prípade odstránenia stĺpca sa bloky posunú aj doľava.
-	**Thunder Button**: po stlačení tlačidla sa náhodne vybrané polia blokov zmenia sa stanovenú farbu, čo umožní vytváranie nových väčších skupín blokov s cieľom získať vyšší bodový zisk. Úspešnosť blesku indikuje intenzita zvuku po spustení tlačidla. Tlačidlo sa aktivuje ak je v hracom poli menej ako 80 blokov.
-	**Boost Bomba**: odstráni bloky v dosahu jedného štvorca v štyroch smeroch, čím výrazne upraví rozloženie hracej plochy.
-	**Delete Button**: po stlačení tlačidla sa odstránia bloky jednej konkrétnej farby, farba je generovaná na základe počtu kociek na hracej ploche, čo hráčovi poskytne možnosť rýchlejšie vyčistiť hraciu plochu. Tlačidlo sa aktivuje ak je v hracom poli menej ako 55 blokov.
-	**Skóre a odmeny**: hráč je odmeňovaný bodmi za úspešné odstránenie blokov. Za väčšie skupiny odstránených blokov získa hráč viac bodov. Ak hráč použije špeciálne vylepšenie (Thunder Button, Boost Bomba, Delete Button) získané skóre bude podstatne nižšie.

### **2.4 Návrh tried**
- **Game**: trieda, v ktorej sa nachádza hlavná herná logika (štart menu, exit menu, hlavná herná slučka, výpočet skóre, aktivácia a deaktivácia špeciálnych vylepšení)
-	**Grid**: trieda predstavujúca hraciu plochu, zabezpečuje vykreslenie farebných blokov, označenie vybraných blokov, odstraňovanie a posúvanie blokov. Taktiež zabezpečuje logiku špeciálnych vylepšení.
-	**Cube**: trieda predstavujúca sprite farebného bloku. Zabezpečuje padanie a posunutie bloku.
-	**Player**: trieda hráča, ktorá uchováva informácie o nadobudnutých bodoch počas hry a na konci zabezpečí ich výpis.
-	**ColorButton**: trieda špeciálneho tlačidla, zabezpečuje vykreslenie, obsahuje metódy na aktivovanie a deaktivovanie, mení svoju farbu na základe splnenia podmienky a náhody.
-	**Thunder, Explosion, Boom**: triedy predstavujúce animované sprity v hre.
-	**Boost, Button, Text, Background**: triedy zabezpečujúce grafický dizajn hry.

---
## **3. Grafika**

### **3.1 Interpretácia témy (Color as a gameplay feature – farba ako herná mechanika)**
V hre sa kladie dôraz na vizuálnu jednoduchosť a príťažlivosť, pričom využíva jasné a živé farby ako základný prvok herného dizajnu. Každá farba má kľúčovú úlohu pri hernej interakcii, pričom dizajn cielene pomáha hráčovi intuitívne pochopiť pravidlá hry a strategické možnosti.  Celkový dizajn hry sa nesie v minimalistickom 2D štýle, ktorý kladie dôraz na kontrast a prehľadnosť.

### **3.2 Dizajn**
Dizajn hry je tvorený voľne dostupnými assetmi z (https://www.freepik.com/), vlastnou grafikou a fontom. Grafické prostredie pozostáva z farebných 2D blokov (obdĺžnikov, štvorcov), ktoré sú hlavnými hernými objektmi. Každý blok je odlíšený svojou farbou (žltá, červená, zelená, modrá, fialová, oranžová). Animácie, ako miznutie blokov či ich preskupovanie, sú plynulé a nenápadné, pričom efektívne zdôrazňujú dynamiku herného prostredia.

<p align="center">
  <img src="https://github.com/LauraKabath/OT_ColorChallenge/blob/master/grid_level.png" alt="GridLevel">
  <br>
  <em>Obrázok 3 Ukážka hracej plochy</em>
</p>

Herné boosty – špeciálne vylepšenia sú vizuálne znázornené ikonami alebo tlačidlami, napr. bomba pre boost - bomba. Tieto prvky nielen esteticky zapadajú do herného prostredia, ale aj okamžite naznačujú svoju funkciu.

<p align="center">
  <img src="https://github.com/LauraKabath/OT_ColorChallenge/blob/master/boosts.png" alt="GridLevel">
  <br>
  <em>Obrázok 4 Ukážka boostu bomba</em>
</p>

<p align="center">
  <img src="https://github.com/LauraKabath/OT_ColorChallenge/blob/master/buttons.png" alt="Buttons">
  <br>
  <em>Obrázok 5 Ukážka tlačidiel</em>
</p>

Herné boosty [blesku](https://www.freepik.com/free-vector/realistic-lightnings-collection_16143900.htm#fromView=search&page=1&position=15&uuid=d6e5ff62-8664-428d-9385-ac7143840272&new_detail=true), [bomby](https://www.freepik.com/free-vector/explosion-effect-collection-cartoon-design_4833064.htm#fromView=search&page=1&position=46&uuid=2fd4f348-f89c-4d1f-b7c8-c80bb5f49a13&query=bomb+explosion), [explózie](https://www.freepik.com/free-vector/set-explosion-effect-cartoon-comic-style_11053545.htm#fromView=search&page=1&position=2&uuid=db970cb2-c90c-4e0a-80ab-8d6b6348f437) sú doplnené vizuálnym sprievodom. Assety boli použité z freepik.com.

<p align="center">
  <img src="https://github.com/LauraKabath/OT_ColorChallenge/blob/master/thunders.png" alt="Thunders">
  <br>
  <em>Obrázok 6 Ukážka blesku</em>
</p>

<p align="center">
  <img src="https://github.com/LauraKabath/OT_ColorChallenge/blob/master/explosions.png" alt="Explosions">
  <br>
  <em>Obrázok 7 Ukážka explózie</em>
</p>

Ako font v hre bol vybraný asset z itch.io, konkrétne avenue-pixel (https://jdjimenez.itch.io/avenue-pixel), ktorý dolaďuje celkový dizajn hry.

---
## **4. Zvuk**

### **4.1 Hudba**
Aby sa hráč mohol plne sústrediť na riešenie úloh, hudba v pozadí je vynechaná. Namiesto toho sa prirodzenou hudbou do pozadia hry stáva hráčovo strategické klikanie myšou, ktoré vytvára rytmus a dodáva hre osobité tempo. Tento prístup zohľadňuje potrebu hráča sústrediť sa na herné stratégie.

### **4.2 Zvuky**
Zvuky v hre sú navrhnuté tak, aby zvýraznili dôležité herné udalosti a prispeli k vytvoreniu pohlcujúceho zážitku pre hráča. Každá významná akcia, ako napríklad kliknutie na bloky, ich odstránenie, explózia bomby, použitie tlačidla alebo efekt blesku, je sprevádzaná charakteristickým zvukovým efektom, ktorý okamžite informuje hráča o vykonaní akcie. Po úspešnom dokončení všetkých úrovní hráča odmení potlesk.

---
## **5. Herný zážitok**

### **5.1 Používateľské rozhranie**
Používateľné rozhranie ladí s celkovým grafickým štýlom hry. Štartovacia obrazovka obsahuje možnosť spustiť hru a koncová obrazovka predstavuje tabuľku bodov, ktoré hráč nahral s možnosťou ukončiť hru.

### **5.2 Ovládanie**
<ins>**Myš**</ins> 
- **Ľavé tlačidlo**: klikanie a odstraňovanie blokov, klikanie na tlačidlá.
- **Pravé tlačidlo**: aktivácia a použitie boostu - bomba.
- **Stlačenie kolieska myši**: deaktivácia boostu - bomba.
