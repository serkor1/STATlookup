variableLookup_server <- function(id, connection, header_data, subheader_data,search_query) {
  moduleServer(
    id, function(input, output, session) {
      
      
      ns <- NS(id)
      
      
      
     
      # Require Search by header
      # from UI
      

      observeEvent(
        search_query(),
        ignoreNULL = TRUE,
        ignoreInit = TRUE,
        {
          
          req(search_query())
          
          
          message("\nIn VariableLookup server module!")
          message("--------------------------------")
          message("Search Query: ", paste(search_query()))
          
          updateCard(
            "search_box",
            action = "restore"
          )
          updateCard(
            "result",
            action = "remove"
          )


          # Search for variable
          # in from global search
          found_variable <- tbl(connection, "variable") %>%
            filter(var %like% paste0(!!search_query(),"%")) %>%
            collect()

          count_variable <- nrow(found_variable)

          # Search Results;
          output$search_output <- renderUI({
            
            
            bs4Card(
              title = paste("Found", count_variable, "variables"),
              width = 12,
              elevation = 0,
              maximizable = FALSE,
              id    = ns("search_box"),
              status = "primary",
              icon = icon("search", verify_fa = FALSE),
              collapsible = TRUE,
              div(style = "width: auto; overflow-y: scroll; height:300px",
              1:count_variable %>% map(
                .f = function(i) {

                  # parameters
                  header_id = found_variable$header_id[i]
                  header_name = header_data %>%
                    filter(id == header_id) %>%
                    select("name") %>% collect()

                  subheader_id = found_variable$subheader_id[i]
                  subheader_name = subheader_data %>%
                    filter(id == subheader_id) %>%
                    select("name") %>% collect()
                  
                  variable = found_variable$var[i]



                  infoBox(
                    title = HTML(paste("In", strong(subheader_name), "under", strong(header_name))),
                    # subtitle = actionLink(
                    #   inputId = ns(paste0("result_", i)),
                    #   label = paste("Variable:", variable),
                    #   style = "color: #fff"
                    #   ),
                    subtitle = HTML(paste((strong("Found Variable:")), variable)),
                    color = "primary",fill = TRUE,
                    width = 12,
                    icon = tags$i(
                      actionLink(icon("external-link-alt", verify_fa = FALSE, style = "color: #fff"), inputId = ns(paste0("result_", i)), label = NULL))
                  )


                }
              )
            )
            )

          })

          1:count_variable %>% map(
            .f = function(i) {

              observeEvent(
                input[[paste0("result_", i)]],
                ignoreNULL = TRUE,
                ignoreInit = TRUE,
                {
                  # Close the search results;
                  updateCard(
                    "search_box",
                    action = "toggle"
                  )
                  
                  message("\nIn VariableLookup server module!")
                  message("--------------------------------")
                  message("Open Search Result ", paste(input[[paste0("result_", i)]]))


                  # parameters
                  header_id = found_variable$header_id[i]
                  header_name = header_data %>%
                    filter(id == header_id) %>%
                    select("name") %>% collect()

                  subheader_id = found_variable$subheader_id[i]
                  subheader_name = subheader_data %>%
                    filter(id == subheader_id) %>%
                    select("name") %>% collect()

                  # Variable data;
                  main_data <- found_variable[i,]


                  # Output the Searrch Query;

                  output$variable_output <- renderUI(
                    {

                      bs4Card(
                        title = "Information",
                        width = 12,
                        status = "primary",
                        id = ns("result"),
                        closable = TRUE,
                        collapsible = TRUE,
                        icon = icon("info-circle", verify_fa = FALSE),

                        fluidRow(
                          variable_info(main_data),
                          variable_value(main_data)
                        ),


                        footer = span("Read more", tags$a(icon("external-link-alt", verify_fa = FALSE),"here",href = main_data$link, target = "_blank"))

                      )




                    }
                  )

                }
              )

            }
          )
          
          


        }
      )
      
      
      

      
    }
  )
}