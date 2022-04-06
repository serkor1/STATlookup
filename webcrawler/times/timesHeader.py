# Import Modules;
from webcrawler.modules import *


# Create Database Connection
connection = database("timesDB")

# Create Cursor and
# initialise Header Data
cursor = connection.cursor()

connection.create_header()




headers = get_html(
    url = 'https://www.dst.dk/da/Statistik/dokumentation/Times',
    selector = 'a.accordion__header'
)
subheader = get_html(
    url = 'https://www.dst.dk/da/Statistik/dokumentation/Times',
    selector = 'div.accordion__body'
)

print("Collecting TIMES Headers:")
print("-------------------------")
with alive_bar(len(subheader)) as bar:
    for i in range(len(subheader)):

        # Get names
        name = headers[i].text


        # Count occurrences
        count = len(re.findall(
            string=str(subheader[i]),
            pattern="<li><a href=\"(.+)\""
        ))

        cursor.execute(
            '''
            INSERT INTO header (count, name)
            VALUES (?, ?)
            ''', (count, name)
        )

        connection.commit()

        bar()







