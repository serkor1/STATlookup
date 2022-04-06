import sqlite3

class database:
    # This function creates the database
    # that are needed to store the information
    def __init__(self, database):
        self.database = database

        self.connection = sqlite3.connect(
            database + ".sqlite"
        )

    def cursor(self):
        self.cursor = self.connection.cursor()

        return self.cursor

    def commit(self):
        return self.connection.commit()

    def create_header(self):
        self.cursor.executescript(
            '''
            DROP TABLE IF EXISTS header;
            CREATE TABLE header (
                id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                count INTEGER,
                name  TEXT UNIQUE,
                link TEXT
            )
            '''
        )

    def create_subheader(self):
        self.cursor.executescript(
            '''
            DROP TABLE IF EXISTS subheader;
            CREATE TABLE subheader (
                id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                header_id INTEGER,
                link TEXT,
                name  TEXT,
                html  TEXT,
                desc_da TEXT
            )
            '''
        )

    def create_variable(self):
        self.cursor.executescript(
            '''
            DROP TABLE IF EXISTS variable;
            CREATE TABLE variable (
                id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                header_id       INTEGER,
                subheader_id   INTEGER,
                link TEXT UNIQUE,
                var TEXT,
                var_name TEXT,
                html TEXT,
                desc_gen_da TEXT,
                desc_det_da TEXT,
                var_values TEXT
            )
            '''
        )
