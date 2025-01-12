# WP2 Starter 

Dit is de starter repository voor WP2 2024. Deze bevat: 
- De [casus](CASUS.md)
- Een uitleg over hoe [ChatGPT te gebruiken in Python code](CHATGPT.md)
- Een lijst met [voorbeeld vragen](questions_extract.json) die we willen categoriseren
- Een SQLite [database](databases%2Fdatabase.db)database met tabellen voor gebruikers, vragen en AI prompts.
- De [database tool](lib%2Fdatabase%2Fdatabase_generator.py) om een nieuwe database mee te genereren. Deze is vrij aan te passen.   
- Een [voorbeeld uitwerking](voorbeeld_uitwerking/app.py) van het meest complexe deel van de opdracht

### Installatie

_Hieronder vind je de installatie-instructies voor het installeren en instellen van je app.
Om de app te runnen heb je de laatste python versie nodig of specifiek v3.13._

1. Clone de repo
   ```sh
   git clone https://github.com/Rac-Software-Development/wp2-2024-mvc-1c1-de-samengestelden.git
   ```
2. Voeg een python interpreter toe 
3. In Pycharm klik "Install requirements" of in terminal:
   ```sh
   pip install -r requirements.txt
   ```
5. Run main.py in IDE of in terminal:
   ```sh
   python main.py
   ```
