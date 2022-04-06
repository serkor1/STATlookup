from webcrawler.modules import *

class hqCollector:

    base_url = "https://www.dst.dk"

    # Initialise Class
    def __init__(self, url, selector):
        # All elements of interest is inside
        # div.hojkval
        self.url = url

        # Extract HTML soup
        tmpSoup = BeautifulSoup(
            requests.get(url).content,
            'html.parser'
        ).select(selector)

        self.content = str(tmpSoup[0])


    def get_base(self):
        return self.content

    def get_url(self, selector):
        # Use the selector to point
        # towards the URL containers
        tmpSoup = BeautifulSoup(
            self.content,
            'html.parser'
        ).select(selector)

        url = re.findall(
            string=str(tmpSoup),
            pattern=".+href=[\"\'](.*?)[\"\'] title=\"\S+\""
        )

        url = [f'https://www.dst.dk{index}' for index in url]

        return list(flatten(url))

    def get_name(self, selector):
        tmpSoup = BeautifulSoup(
            self.content,
            'html.parser'
        ).select(selector)


        return tmpSoup




# # Test the function
# get_content = hqCollector(
#             url = "https://www.dst.dk/da/TilSalg/Forskningsservice/Dokumentation/hoejkvalitetsvariable/familieindkomst",
#             selector='div.hojkval'
#         )
#
# # Get the URLS inside the variable
# # table
# urls = get_content.get_url(selector='table')
#
# # Get the table container
# name_container = get_content.get_name(selector='tr')
#
# for index in name_container:
#     print(index)
#     print("-----")
#
# Names = re.findall(
#         string=str(name_container),
#         pattern=".+>(\S+)</a>"
#     )
#
# other_names = re.findall(
#     string=str(name_container),
#     pattern="<td>(?!<)(.+)</td>"
# )
#
#
#
# print(other_names)




