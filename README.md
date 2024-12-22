# Exempelprojekt i Python med UV som dependency management


## UV krävs
https://github.com/astral-sh/uv  
Installera Python 3.12 om du inte har det redan.

### Varför inte pip?  
Pip finns med i Python-installationen men har en del brister. Det duger för lite labbande, men:
- pip är dåligt på konflikthantering. Det kan installera inkompatibla paket, jag har råkat ut för det, som tur var fanns det tester.
- pip hanterar inte transienta beroenden. Det blir vad det blir när du kör det.
- En del pip-problem har tidigare lösts med att ha andra program som skapar kompletta filer med alla transienta beroenden, men nu finns modernare sätt.
- uv (liksom Poetry & pdm) har dina "top level"-beroenden (det du faktiskt vill använda) i en fil, och komplett lista av allt som behövs i en lock-fil. Inspirerat av Cargo i Rust (som uv är skrivet i). Det finns liknande i andra språk.

## pyproject.toml
Används för lite av varje. Det du vill installera, regler för formatters & linters mm. Använd den istället för spridda .ini-filer som man gjorde förr. Ersätter också `setup.py`för att göra paket att distribuera.

## Virtual environments.
Isolerade miljöer med den Python-version och de paket du vill ha installerade.
Olika repon har olika venv som kan ha olika innehåll. 
- repo 1: Python 3.11 och requests 2.29.0 mm
- repo 2: Python 3.12 och requests 2.32.3 mm

lock-filen säkerställer att du får en korrekt installation och finns incheckad i Git.  
Med UV går det mycket fortare att skapa venv så de betraktar dem som efemära. Tar det sekunder att skapa ett nytt behöver du inte känna dig fäst vid dem. Men sync-kommandot gör det också enklare än med pip att byta version av något och prova.  Om något skulle vara installerat "vid sidan om" (tex med pip)  så försvinner det när du kör `uv sync`. Bara det som finns i `uv.lock`får finnas i ditt venv efter att ha synkat

Utan venv kommer att allt att installeras i din system-Python vilket snabbt blir rörigt. Använd venv.   
Fördjupning: https://realpython.com/python-virtual-environments-a-primer/  

## Installation
Installera UV.

Sen finns det `make`-kommandon du kan använda. Kolla i `makefile`.  
`make install`sätter upp det mesta.

Använder du terminalen i din IDE behöver du aktivera venv där med `source .venv/bin/activate` (Mac/Linux) eller ` .venv\Scripts\activate` (Windows).

Kan du inte köra make-filer så får du köra dem ett och ett. 
Aktivering av venv inifrån en makefile är lite speciellt, använd kommandot i förra stycket när du gör det i terminalen 

## Nya dependencies  
Lägg till nya dependencies med `uv add`, de läggs till i pyproject.toml, uv.lock och installeras.
`uv add requests` till exempel.

Det går att lägga till grupper så du slipper utvecklingsrelaterat (test, linter osv) i prod.

### Linter & formatter
`ruff` snabb med vettiga defaultvärden. 
KOnfiguration av radlängd från default 88 till 120 finns i pyproject.toml
https://docs.astral.sh/ruff/

### pre-commit
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)  
Glömmer du linting, formatting, att köra tester och sånt?
`pre-commit` gör sånt automatiskt när du gör en commit. programmet installeras, men du måste sätta upp det på din dator med  `pre-commit install`. Det går att konfigurera reglerna så att tyngre saker bara körs pre-push. 

https://pre-commit.com

Reglerna finns i `.pre-commit-config.yaml`  
Jag har lagt till att testerna körs, att koden kollas och formatteras med Ruff och att det inte sker commits till main/master branch. Även kodkvalitet kollas och går värdena över tröskelvärden går det inte att committa.  [Fler hooks/regler här.](https://github.com/pre-commit/pre-commit-hooks)  

Det går att skippa pre-commit checks, kolla pre-commit-dokumentationen. 

Du behöver köra `git commit` från en terminal i ett aktiverat venv, annars finns inte ruff och pytest.

Använd `name:`-parametern så blir det tydligare vad som körs. Annars visas id.
```
$ pre-commit run --all-files
Run tests........................Passed
ruff check (linter)..............Passed
ruff format......................Passed
Xenon code complexity checker....Passed
Don't commit to main/master......Passed
```
Behöver koden formatteras kommer commiten inte att gå igenom. Men nu är koden formatterad så nästa gång går det bra.

```
- hook id: ruff-format
- files were modified by this hook
1 file reformatted, 2 files left unchanged
```


### Test
#### Pytest
Pytest installeras, test-exemplen använder Pytest-specifika detaljer.
Din IDE behöver configueras för vilken test runner du använder.
kör testerna med `pytest -v -s`för att få ut all info. 
Test coverage hanteras av [pytest-cov](https://pytest-cov.readthedocs.io/en/latest/index.html) som skriver ut i terminalen men även kan göra html-rapporter där du kan se vilken kod som täcks och inte täcks av testerna.

#### Unittest
En fördel med inbyggda `unittest`(som är en testrunner som du kan köra vilka testtyper du vill med) är att den har mocking inbyggd. Annars verkar [pytest-mock](https://pytest-mock.readthedocs.io/en/latest/) populär.

### Sökvägar och filhantering
Använd `pathlib` istället för gamla `os.path`
https://realpython.com/python-pathlib/

### Loggning
[Loguru](https://loguru.readthedocs.io/en/stable/overview.html) installeras, informativa loggar med minimal setup. Default-level är debug. Level styrs med miljövariabel `LOGURU_LEVEL`
```
from loguru import logger
logger.info("log message)
```

### Strängformattering
`f-string`är enklast och läsbarast.
```
logger.debug(f"Environment variable {env_var_name} was {result}")
```

### __init__.py and code that runs automatically
See comments in `my-code/__init__.py`

### Kodkvalitet
[xenon](https://github.com/rubik/xenon) körs som pre-commit check. Inställningen är att det inte får bli sämre än "A" (bäst) på de olika kategorierna. Vill du köra och titta på resultatet så installera [radon](https://radon.readthedocs.io/en/stable/intro.html). Skriver du mer komplex kod kanske du måste höja tröskeln för pre-commit checks, men det är väl bra att det är lite jobbigt att göra det?

### type hints
Python är otypat. Det finns dock "type hints" som ger tips om vilka typer som förväntas, och vilken typ som returneras. Det är dokumentation och en hjälp för din IDE att klaga om det är en annan typ.  
Använd [Pydantic](https://docs.pydantic.dev/latest/) för faktisk validering, använd `isInstance`för att kolla typ (dvs kolla om objektet är en instans av en klass)

```
def is_string(param:str)->bool:
	return isinstance(param, str)
```


### Environment variables
Ifall du behöver såna
skapa en fil som heter .env. Den skall INTE vara i versionshanteringen (stoppas av .gitignore-filen).  
som kan läsas in av dotenv-bilioteket.


Format i filen:
```
MY_ENV="something"
```
ta med denna kod i en fil så läses dina miljövariabler in från fil.
```
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
```

Med miljövariabler, tänk på att MY_VAR = "False" gör att MY_VAR får en sträng och blir True vid en enkel jämförelse. Exempel på hur boolska värden kan hanteras finns i `src/environment_variables.py`



### Annat du kan behöva:
- http client: requests https://docs.python-requests.org/en/latest/index.html
- api: FastApi https://fastapi.tiangolo.com
- Databas ORM: SQLAlchemy https://www.sqlalchemy.org

### Tutorials
https://realpython.com är generellt bra. 


### PEP 8 – Style Guide for Python Code
https://peps.python.org/pep-0008/

### Easter egg
```
$ python
Python 3.12.2 (v3.12.2:6abddd9f6a, Feb  6 2024, 17:02:06) [Clang 13.0.0 (clang-1300.0.29.30)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import this
```

Prova `import this`. Och som du ser finns det [hjälp-funktion](https://realpython.com/ref/builtin-functions/help/). Kan vara bra om du är offline.

Saknar du braces så kan du köra `from __future__ import braces`

### Make & pre-commit
Det är lite duplicering mellan filerna. Det går att köra `make commit`från pre-commit och göra en del saker på det sättet, då blir det mer tillgängligt för användning ofta än om det bara finns i pre-commit. men det kräver installation av `make`om du inte har det. Anpassa som du vill och behöver. [Makefile Cookbook](https://makefiletutorial.com)

### Semikolon
Semikolon ignoreras av Python, upptäcks av linters och tas bort av formatters


### Interaktiv programmering
Du kan starta Python och skriva ditt program direkt. 
```
$ python
Python 3.12.2 (v3.12.2:6abddd9f6a, Feb  6 2024, 17:02:06) [Clang 13.0.0 (clang-1300.0.29.30)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> print("hello world")
hello world
>>> foo = 42
>>> foo
42
>>> print(foo)
42
>>> from __future__ import braces 
  File "<stdin>", line 1
SyntaxError: not a chance
>>> import this
The Zen of Python, by Tim Peters

Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!
>>> 
```
Avsluta Python-sessionen med `quit()`eller `Ctrl-d`
