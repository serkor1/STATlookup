# Import Modules;
from webcrawler.modules import *


# Create Database Connection
connection = database("lprDB")

# Create Cursor and
# initialise Header Data
cursor = connection.cursor()



# Load data; and extract HTML
var_data = cursor.execute(
    '''
    SELECT * FROM variable
    '''
).fetchall()


print("Collecting Descriptions from LPR:")
print("------------------------------")
with alive_bar(len(var_data)) as bar:
    for row in var_data:

        # Extract ID to identify replacement
        # values
        id = row[0]
        content = row[6]


        # All the values inside
        # the html corpus are inside a div
        # where the divisor is H3

        soup = BeautifulSoup(content, 'html.parser')

        var_desc = []
        # Extract Variable Description
        for index in soup.find_all('div'):
            # Check for Variable Description
            is_desc = bool(
                re.search(
                    pattern= "<strong>.+beskrivelse",
                    string= str(index)
                )
            )

            if is_desc:
                var_desc = desc_collect(str(index), 'div').get_description('strong')[1]





        tab_desc = []
        # Extract Variable Description
        for index in soup.find_all('div'):
            # Check for Variable Description
            is_desc = bool(
                re.search(
                    pattern="<strong>Tabellens.+",
                    string=str(index)
                )
            )


            if is_desc:
                tab_desc = desc_collect(str(index), 'div').get_description('strong')[1]



        cursor.execute(
            '''
            UPDATE variable SET desc_gen_da = ?, desc_det_da = ? WHERE ID = ?
            ''', (tab_desc[0], var_desc[0], id)
        )

        connection.commit()

        bar()




