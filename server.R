#
# This is the server logic of a Shiny web application. You can run the
# application by clicking 'Run App' above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

library(shiny)

# Define server logic required to draw a histogram
shinyServer(
  function(input, output) {
    
    # Establish Connection; ####
    # to server and Silently load
    # Header and Subheader data
    
    
    # Header Data:
    header_data <- tbl(
      db_connection, 'header'
    )
    
    subheader_data <- tbl(
      db_connection, 'subheader'
    )
    
    
    # Global Search Output; ####
   
    variableLookup_server(
      "var_lookup",
      subheader_data = subheader_data,
      header_data = header_data,
      connection = db_connection,
      search_query = reactive(input$global_search)
    )

    topicLookup_server(
      "topic_lookup",
      subheader_data = subheader_data,
      header_data = header_data,
      connection = db_connection,
      search_query = reactive(input$search_header)
    )
    
      
    
    
    
    

    waiter::waiter_hide()
    
    
    # End of Server; #####
    
    
    
  }
  
)
