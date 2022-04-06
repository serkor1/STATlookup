# Import Modules;
from webcrawler.modules import *


# Create Database Connection
connection = database("lprDB")

# Create Cursor and
# initialise Header Data
cursor = connection.cursor()

connection.create_header()

# Collect all Registres
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

registers = lprCollector(
    url = "https://www.esundhed.dk/Dokumentation",
    selector= "#list-tab-registers", ctx=ctx
)

names = registers.get_name()
urls = registers.get_url()


print("Collecting Headers from LPR:")
print("----------------------------")
with alive_bar(len(names)) as bar:
    for i in range(len(names)):
        cursor.execute(
            '''
            INSERT INTO header (link, name)
            VALUES (?, ?)
            ''', (urls[i], names[i])
        )

        connection.commit()

        bar()