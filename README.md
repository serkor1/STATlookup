<!-- badges: start -->
[![](https://img.shields.io/badge/Shiny-shinyapps.io-blue?style=flat&labelColor=white&logo=RStudio&logoColor=blue)](https://serkor.shinyapps.io/STATlookup/)
<!-- badges: end -->




## STATlookup

A unified and efficient database of all variables found in the danish statistical databases. It includes all variables found in the following databses

1. [TIMES](https://www.dst.dk/da/Statistik/dokumentation/Times), Statistics Denmark
2. [High Quality Research Statistics](https://www.dst.dk/da/TilSalg/Forskningsservice/Dokumentation/hoejkvalitetsvariable), Statistics Denmark
3. [Health Specific Statistics](https://www.esundhed.dk/Dokumentation), Sundhedsstyrelsen

A live demo can be found at [ShinyApps](https://serkor.shinyapps.io/STATlookup/)


### Installation Guide

1. Build the Database

The database will be located in the main folder as `statDB.sqlite`. To build `statDB.sqlite`, you have to run `dstCollectRaw.py`, `lprCollectRaw.py` and `collectDB.py` in that order.

2. Run the application

The application is found inside `global.r`

**NOTE:** You might need to install missing `modules` and `packages`, before you can run either program.


### Bug Reports and Suggestions

Feel free to send `pull`-requests.
