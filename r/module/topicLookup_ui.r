topicLookup_ui <- function(id) {
  ns <- NS(id)
  
  
  tagList(
    
    uiOutput(ns("variable_output"))
    
  )
  
  
  
}


topicLookup_sidebar <- function(id) {
  ns <- NS(id)
  
  
  tagList(

    uiOutput(
      ns("subheader_list")
    ),
    
    uiOutput(
      ns("variable_list")
    )
    
  )
  
  
  
}