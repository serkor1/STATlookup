variableLookup_UI <- function(id) {
  
  # Create Namespace
  ns <- NS(id)
  
  tagList(
    
    uiOutput(ns("search_output")),
    
    uiOutput(ns("variable_output"))
    
  )
  
  
  
}