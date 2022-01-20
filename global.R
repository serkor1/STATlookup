library(shiny)
library(shinyWidgets)
library(bs4Dash)
library(dbplyr)
library(tidyverse)
library(data.table)
library(shinyjs)
library(rvest)


list.files(
  path = "r/",
  full.names = TRUE,
recursive = TRUE
) %>% map(
  .f = function(x) {
    
    source(x)
    
  }
)