rm(list = ls()); gc()

# Version
version <- "Version b1.0"



# Packages; ####
# This script will automatically
# intstall missing packages
list.of.packages <- c(
  "shiny",
  "shinyWidgets",
  "bs4Dash",
  "dbplyr",
  "tidyverse",
  "data.table",
  "shinyjs",
  "rvest",
  "glue",
  "waiter"
  )

new.packages <- list.of.packages[!(list.of.packages %in% installed.packages()[,"Package"])]
if(length(new.packages)) install.packages(new.packages)

library(shiny)
library(shinyWidgets)
library(bs4Dash)
library(dbplyr)
library(tidyverse)
library(data.table)
library(shinyjs)
library(rvest)
library(glue)
library(waiter)


# Load R functions; ¤¤¤¤
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
