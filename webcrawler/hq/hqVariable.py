# Import Modules;
from webcrawler.modules import *

# Create Database Connection
connection = database("hqDB")

# Create Cursor and
# initialise Header Data
cursor = connection.cursor()

connection.create_variable()


# Read subheader data;
subheader_data = cursor.execute(
    '''
    SELECT * FROM subheader
    '''
).fetchall()


print("Collecting HQ Variables:")
print("------------------------")
iteration = 0
with alive_bar(len(subheader_data)) as bar:
    for row in subheader_data:
        iteration += 1

        id  = row[0]
        header_id = row[1]
        url = row[2]


        get_content = hqCollector(
            url = url,
            selector='div.hojkval'
        )

        # Get the URLS inside the variable
        # table
        urls = get_content.get_url(selector='table')

        # Get the table container
        name_container = str(get_content.get_name(selector='tr'))


        if len(name_container) == 0:
            continue


        var = re.findall(
        string=str(name_container),
        pattern=".+>(\S+)</a>"
        )


        var_name = re.findall(
            string=str(name_container),
            pattern="<td>(?!<)(.+)</td>"
        )

        for i in range(len(var_name)):

            html_content = get_html(
                url = urls[i],
                selector= 'div.hojkval'
            )

            cursor.execute(
                '''
                INSERT OR IGNORE INTO variable (header_id, subheader_id, link, var, var_name, html)
                VALUES (?, ?, ?, ?, ?, ?)
                ''', (header_id, id, urls[i], var[i], var_name[i], str(html_content[0]))
            )

        connection.commit()

        bar()