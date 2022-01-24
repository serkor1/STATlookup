rm(list = ls()); gc()

# Version
version <- "Version b1.0"


library(shiny,quietly = TRUE, warn.conflicts = FALSE)
library(shinyWidgets,quietly = TRUE, warn.conflicts = FALSE)
library(bs4Dash,quietly = TRUE, warn.conflicts = FALSE)
library(dbplyr,quietly = TRUE, warn.conflicts = FALSE)
library(tidyverse,quietly = TRUE, warn.conflicts = FALSE)
library(data.table,quietly = TRUE, warn.conflicts = FALSE)
library(shinyjs,quietly = TRUE, warn.conflicts = FALSE)
library(rvest,quietly = TRUE, warn.conflicts = FALSE)
library(glue,quietly = TRUE, warn.conflicts = FALSE)
library(waiter,quietly = TRUE, warn.conflicts = FALSE)

list.files(
  path = "r/",
  full.names = TRUE,
  recursive = TRUE
) %>% map(
  .f = function(x) {
    
    source(x)
    
  }
)



# Connection; #####
db_connection <- DBI::dbConnect(
  RSQLite::SQLite(),
  dbname = "statDB.sqlite"
)
