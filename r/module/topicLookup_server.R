topicLookup_server <- function(id, connection = NULL, header_data = NULL, subheader_data =NULL,search_query =NULL) {
  moduleServer(
    id, function(input,output,session) {
      
      ns <- NS(id)
      
      # Create Subheader List
      # based on header input
      observeEvent(
        search_query(),
        ignoreNULL = TRUE,
        ignoreInit = TRUE,
        {
          
          # Filter data;
          subheader = subheader_data %>% filter(
            header_id == !!search_query()
          ) %>% collect()
          
          # Generate Choices;
          choices = map(
            1:nrow(subheader),
            function(i) {
              
              subheader$id[i]
              
            }
          ) %>% set_names(subheader$name)
          
          output$subheader_list = renderUI({
            
            pickerInput(
              inputId = ns("search_subheader"),
              label = NULL, 
              choices = choices,
              options = list(
                title = "Pick subtopic",
                `live-search` = TRUE)
            )
            
          })
          
          
        }
      )
      
      # Create List of variables
      observeEvent(
        input$search_subheader,
        ignoreNULL = TRUE,
        ignoreInit = TRUE,
        {
          
          req(input$search_subheader)

          # Filter data;
          variable_list =  tbl(connection, "variable") %>%
            filter(subheader_id == !!input$search_subheader & header_id == !!search_query()) %>%
            collect()

          # Generate Choices;
          choices = map(
            1:nrow(variable_list),
            function(i) {

              variable_list$id[i]

            }
          ) %>% set_names(variable_list$var)

          output$variable_list = renderUI({

            pickerInput(
              inputId = ns("search_variable"),
              label = NULL,
              choices = choices,
              options = list(
                title = "Pick Variable:",
                `live-search` = TRUE
              )
            )

          })
          
        }
      )
      
      
      # Show Variable Description;
      observeEvent(
        input$search_variable,
        ignoreNULL = TRUE,
        ignoreInit = TRUE,
        {
          
          req(input$search_variable)
          
          
          
          
          output$variable_output <- renderUI(
            {
              req(input$search_variable)
              
              variable_list =  tbl(connection, "variable") %>%
                filter(subheader_id == !!input$search_subheader & header_id == !!search_query() & id == !!input$search_variable) %>%
                collect()
              
              
              
              bs4Card(
                title = "Information",
                width = 12,
                status = "primary",
                closable = TRUE,
                collapsible = TRUE,
                
                
                fluidRow(
                  
                  variable_info(
                    variable_list
                  ),
                  variable_value(
                    variable_list
                  )
                  
                  
                  
                ),footer = span("Read more at", tags$a("DST",icon = icon("link", verify_fa = FALSE),href = variable_list$link, target = "_blank"))
                
                
                
              )
              
              
              
              
            }
          )
          
          
        }
      )
      
      
    }
  )
  
}