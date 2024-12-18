Exempelprojekt i Python med UV som dependency management


## UV krävs
https://github.com/astral-sh/uv

Varför inte pip?  
Pip finns med i Python-installationen men har en del brister. Det duger för lite labbande, men:
- pip är dålig på konflikthantering. Det kan installera inkompatibla paket.
- pip hanterar inte transienta beroenden. Det blir vad det blir när du kör det.
- En del pip-problem kan lösas med att ha andra program som skapar kompletta filer med alla transienta beroenden, men nu finns modernare sätt.
- uv (liksom Poetry & pdm) har dina "top level"-beroenden (det du faktikst vill använda) i en fil, och komplett lista av allt som behövs i en lock-fil. Inspirerat av Cargo i Rust (som uv är skrivet i).

## pyproject.toml
Används för lite av varje. Det du vill installera, regler för formatters & linters mm. Använd den istället för spridda .ini-filer som man gjorde förr. Ersätter också `setup.py`för att göra paket att distribuera.

## Virtual environments.
Isolerade miljöer med den Python-version och de paket du vill ha installerade.
Olika repon har olika venv som kan ha olika innehåll. 
- Python 3.11 och requests 2.29.0 mm
- Python 3.12 och requests 2.32.3 mm

lock-filen säkerställer att du får en korrekt installation
med UV går det mycket fortrare att skapa venv så de betraktar dem som efemära. Tar det millisekunder att skapa ett nytt behöver du inte känna dig fäst vid dem. Utan venv kommer att allt att installeras i din system-Python vilket snabbt blir rörigt. Använd venv. 


## Installation
efter att ha installerat UV, kör `uv venv` i repo-rooten och följ instruktionerna för att aktivera ditt nyskapade virtual environment. Det är olika på Mac/linux och Windows.

```
$ uv venv
Using CPython 3.12.2 interpreter at: /Library/Frameworks/Python.framework/Versions/3.12/bin/python3.12
Creating virtual environment at: .venv
Activate with: source .venv/bin/activate
```
Prompten kommer att ändras med venv-namnet i parantes
`(python.init) $ `

Lägg till nya saker med `uv add`, de läggs till i pyproject.toml. uv.lock och installeras.
`uv add requests` till exempel

### Linter & formatter
`ruff`; snabb med vettiga defaultvärden. 
En ändring av radlängd till 120 finns i pyproject.toml
https://docs.astral.sh/ruff/

### pre-commit
glömmer du linting, formatting, att köra tester och sånt?
`pre-commit`körs sånt automatiskt när du gör en commit. programmet installeras, men du måste sätta upp det på din dator med  `pre-commit install`. Detgår att konfigurera så att tyngre saker bara körs vid push.

https://pre-commit.com

Reglerna finns i `.pre-commit-config.yaml`  
Jag har lagt till att testerna körs, att koden kollas och formatteras med Ruff och att det inte sker commits till main/master branch. Det går att skippa pre-commit checks, kolla pre-commit-dokumentationen.

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)

Du behöver köra git commit från en terminal i ett aktiverat venv, annars finns inte ruff och pytest.

### Test
pytest installeras, test-exemplen använder Pytest-specifika detaljer.
Din IDE behöver configueras för vilken test runner du använder.

### Loggning
Loguru installeras, informativa loggar med minimal setup. Default-level är debug. Level styrs med miljövariabel `LOGURU_LEVEL`
https://loguru.readthedocs.io/en/stable/overview.html
```
from loguru import logger
logger.info("log message)
```

### Environment variables
Ifall du behöver såna
skapa en fil som heter .env. Den skall INTE vara i versionshanteringen (stoppas av .gitignore-filen).  


Format i filen:
```
MY_ENV = "something"
```

ta med denna kod i en fil så läses dina miljövariabler in från fil.
```
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
```

Med miljövariabler, tänk på att MY_VAR = "False" gör att MY_VAR får en sträng och blir True vid en enkel jämförelse. 


En miljövariabel som skall ha ett boolskt värde kräver nåt i den här stilen:
```
MY_BOOL_VAR = os.getenv("MY_BOOL_VAR", "").lower() == "true"
```
Förklaring
`os.getenv("MY_BOOL_VAR", "")`hämtar MY_BOOL_VAR, default till tom sträng för att undvika att den blir None om variablen inte är satt.  
Exempel:
```
export MY_BOOL_VAR=False
my_var = os.getenv(MY_BOOL_VAR)
`.lower()`gör om strängen till lowercase.  
`== "true"` jämför strängen med "true" för att kunna sätta variabeln till True eller False.  


### Annat du kan behöva:
- http client: requests https://docs.python-requests.org/en/latest/index.html
- api: FastApi https://fastapi.tiangolo.com
- Databas ORM: SQLAlchemy https://www.sqlalchemy.org
- Data validation: Pydantic  https://docs.pydantic.dev/latest/

### Tutorials
https://realpython.com är generellt bra. 
