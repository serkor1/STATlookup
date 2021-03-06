# Import Modules;
from webcrawler.modules import *


# Create Database Connection
connection = database("timesDB")

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

iteration = 0
print("Extracting Variables:")
print("=====================")
with alive_bar(len(subheader_data)) as bar:
    for row in subheader_data:

        id  = row[0]
        header_id = row[1]
        url = row[2]

        # Generate Objects
        variable = timesCollector(
            url         = url,
            selector    = 'div.cludoContent',
            do_ul       = True,
            is_variable = True
        )

        # Get Names
        variable_names = variable.get_name()
        variable_url = variable.get_url()

        # Get additional variables
        # these are urls to the variables
        additional_url = variable.get_additional()


        if len(additional_url) != 0:
            for url in additional_url:
                additional_variable = timesCollector(
                    url         = url,
                    selector    = 'div.cludoContent',
                    do_ul       = False,
                    is_variable = False
                )

                additional_names = additional_variable.get_name()
                additional_url = additional_variable.get_url()

                variable_names = variable_names + additional_names
                variable_url   = variable_url + additional_url


        # Flatten the lists
        variable_names = list(
            flatten(variable_names)
        )

        variable_url = list(
            flatten(variable_url)
        )



        for index in range(len(variable_url)):


            # Split Variable Names
            # into var and var_name
            split = re.split(
                string= str(variable_names[index]),
                pattern=",",
                maxsplit=1
            )

            # This checks whether the
            # name in index 1, has letters.
            # If not, it must be empty.
            check_name = bool(
                re.match(
                    string = split[1].lower().strip(),
                    pattern= "[a-z]+"
                )
            )

            # If there is only one split,
            # it must be that the title is missing.
            if not check_name:
                split = list(flatten([split[0], split[0]]))


            var = split[0].lower().strip()
            var_name = split[1].title().strip()



            html_content = get_html(
                url = variable_url[index],
                selector='div.cludoContent'
            )



            cursor.execute(
                '''
                INSERT OR IGNORE INTO variable (header_id, subheader_id, link, var, var_name, html)
                VALUES (?, ?, ?, ?, ?, ?)
                ''', (header_id, id, variable_url[index], var, var_name, str(html_content[0]))
            )

        connection.commit()

        bar()

