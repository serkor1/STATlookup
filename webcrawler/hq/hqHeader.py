# Import Modules;
from webcrawler.modules import *


# Create Database Connection
connection = database("hqDB")

# Create Cursor and
# initialise Header Data
cursor = connection.cursor()

connection.create_header()

print("Collecting HQ Headers:")
print("----------------------")
headers = get_html(
    url = 'https://www.dst.dk/da/TilSalg/Forskningsservice/Dokumentation/hoejkvalitetsvariable',
    selector = 'a.accordion__header'
)
subheader = get_html(
    url = 'https://www.dst.dk/da/TilSalg/Forskningsservice/Dokumentation/hoejkvalitetsvariable',
    selector = 'div.accordion__body'
)

with alive_bar(len(subheader)) as bar:
    for i in range(len(subheader)):

        # Get names
        name = headers[i].text


        # Count occurrences
        count = len(re.findall(
            string=str(subheader[i]),
            pattern="<a href=\"(.+)\""
        ))

        cursor.execute(
            '''
            INSERT INTO header (count, name)
            VALUES (?, ?)
            ''', (count, name)
        )

        bar()

connection.commit()
