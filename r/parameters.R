# Static Parameters; ####


# Database Counter;
db_counter <- function(connection = db_connection) {
  
  message("Attempting to load db_counter()")
  

  variable_data <- tbl(connection, "variable")

  # Unique Variables as per links
  unique_variables <- variable_data %>% summarise(
    unique_variable = n_distinct(var)
  ) %>% collect()


  # Unique Datasets as per header ID
  unique_datasets <- variable_data %>% summarise(
    unique_variable = n_distinct(subheader_id)
  ) %>% collect()

  unique_topics <- variable_data %>% summarise(
    unique_variable = n_distinct(header_id)
  ) %>% collect()



  generate_ui <- fluidRow(
    column(
      width = 4,
      descriptionBlock(
        number = unique_variables,
        numberColor = "primary",
        text = NULL,
        header = "Unique Variables",
        rightBorder = TRUE,
        marginBottom = FALSE
      )
    ),

    column(
      width = 4,
      descriptionBlock(
        number = unique_datasets,
        numberColor = "primary",
        text = NULL,
        header = "Unique Datasets",
        rightBorder = TRUE,
        marginBottom = FALSE
      )
    ),

    column(
      width = 4,
      descriptionBlock(
        number = unique_topics,
        numberColor = "primary",
        text = NULL,
        header = "Unique Databases",
        rightBorder = FALSE,
        marginBottom = FALSE
      )
    )
  )
  
  
  message("db_counter() is loaded!")
  
  
  return(
    generate_ui
  )
  
}



header_choices <- function(connection = db_connection) {
  
  # Set_names gives the 
  # shown name
  # while map gives the actual
  # search value
  # Connection to DB; ####
  
  header_data <- tbl(connection, "header") %>%
    collect()
  
  map(
    1:nrow(header_data),
    function(i) {
      
      header_data$id[i]
      
    }
  ) %>% set_names(str_trunc(header_data$name, width = 40, side = "right"))
  
  
  
} 