# pump_tracker

## Project overview:
**The following files belong to the frontend:**
 - [main.py](./main.py)
 - [appBase.py](./appBase.py)
 - [homePage.py](./homePage.py)
 - [loginPage.py](./loginPage.py)
 - [accountPage.py](./accountPage.py)
 - [settingsPage.py](./settingsPage.py)
 - [settings.py](./settings.py)

**The backend is contained within:**
 - [backend.py](./backend.py)

**Additional utility/setup files include:**
 - [database.py](./database.py)
 - [generate.py](./generate.py)

## Usage instructions:

### Running the app:
```sh
pip install -r requirements.txt
python main.py
```

**If using venv:**
```sh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

### Creating the database:
To run the database creation script, use
```sh
python database.py
```

This will use the [DDL file](./ddl.sql) to create the database schema in the sqlite file
`database.db`. It will then insert the test data from [test_data.sql](./test_data.sql)
into the database.


### Generating account credentials:
To generate account credentials, use
```sh
python generate.py <password to hash>
```

This will generate a new secure bcrypted hash from the given password for use
in the database.