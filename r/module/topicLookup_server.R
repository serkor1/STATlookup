topicLookup_server <- function(id, connection = NULL, header_data = NULL, subheader_data =NULL, search_query =NULL) {
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
          
          message("In TopicLookup Server Module!")
          message("Search Header ID: ", paste(search_query()))
          
          
          # Filter data;
          subheader = subheader_data %>% filter(
            header_id == !!search_query()
          ) %>% collect() %>% mutate(
            name = str_trunc(name, width = 40, side = "right")
          )

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
                `live-search` = TRUE,
                width = 'auto',
                size = 10
                ),width = 'auto'
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
          
          message("Search Subheader ID: ", paste(input$search_subheader))

          # Filter data;
          # Assign with <<- so it
          # transfers to other observer
          variable_list <<- tbl(connection, "variable") %>%
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
            
            req(input$search_subheader)

            pickerInput(
              inputId = ns("search_variable"),
              label = NULL,
              choices = choices,
              options = list(
                title = "Pick Variable:",
                `live-search` = TRUE,
                width = 'auto',
                size = 10
              ),
              width = 'auto'
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
          
          # Require some input;
          # from search variables
          req(input$search_variable)
          message("Search Variable ID: ", paste(input$search_variable))
          # Isolate the data so it does not take 
          # dependency on above observer
          unique_variable <- isolate({
            variable_list %>%
              filter(id == !!input$search_variable) %>%
              collect()
            }) 
          
          
          output$variable_output <- renderUI(
            {
              
              bs4Card(
                title = "Information",
                width = 12,
                status = "primary",
                closable = TRUE,
                collapsible = TRUE,
                icon = icon("info-circle", verify_fa = FALSE),
                
                
                fluidRow(
                  
                  variable_info(
                    unique_variable
                  ),
                  variable_value(
                    unique_variable
                  )
                  
                  
                  
                ),footer = span("Read more", tags$a(icon("external-link-alt", verify_fa = FALSE),"here",href = unique_variable$link, target = "_blank"))
                
                
                
              )
                
              
              
              
              
              
            }
          )
          
          
        }
      )
      
      
    }
  )
  
}