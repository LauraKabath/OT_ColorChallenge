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

<ins>**Tetris Attack/Panel de Pon**</ins>

Tetris Attack/Panel de Pon
Tetris Attack je logická hra založená na rýchlom myslení a strategickom plánovaní. Hráč manipuluje s dvojicami blokov rôznych farieb na hracej ploche, pričom ich cieľom je vytvoriť vodorovné alebo zvislé rady minimálne troch rovnakých farieb, aby tieto bloky zmizli. Hra ponúka viacero úrovní obtiažnosti, nekonečný režim na zlepšovanie skóre a bonusové kolá „Clear the Board“ pre získanie extra bodov.

### **1.2 Herný zážitok**
Hra poskytuje zábavný a návykový zážitok, ktorý hráča núti strategicky uvažovať pri odstraňovaní farebných blokov. Vďaka jednoduchému ovládaniu a jasne definovanému cieľu je ideálna na oddych, pričom zároveň ponúka výzvu v podobe premysleného plánovania krokov na úplné vyčistenie hracej plochy.

### **1.3 Vývojový softvér**
- **Pygame-CE**: zvolený programovací jazyk,
-	**PyCharm 2023.3.4**: vybrané IDE,
-	**Pixabay.com**: zdroj zvukov do hry,
-	**Itch.io**: zdroj fontov do hry.
