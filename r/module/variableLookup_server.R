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
              id    = ns("search_box"),
              status = "warning",
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
                    title = paste("Found in", header_name, "under", subheader_name),
                    subtitle = actionLink(inputId = ns(paste0("result_", i)), label = paste("Variable:", variable)),
                    color = "lightblue",fill = TRUE,
                    width = 12,
                    icon = icon("search", verify_fa = FALSE)
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

                        fluidRow(
                          variable_info(main_data),
                          variable_value(main_data)
                        ),


                        footer = span("Read more at", tags$a("DST",icon = icon("link", verify_fa = FALSE),href = main_data$link, target = "_blank"))

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