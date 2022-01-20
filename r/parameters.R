# Static Parameters


# Database Counter;
db_counter <- function() {
  
  # Connection to DB; ####
  connection <- DBI::dbConnect(
    RSQLite::SQLite(),
    dbname = "dstTIMES.sqlite"
  )

  variable_data <- tbl(connection, "variable")

  # Unique Variables as per links
  unique_variables <- variable_data %>% summarise(
    unique_variable = n_distinct(var)
  ) %>% collect()


  variable_data %>% summarise(
    unique_variable = n_distinct(link)
  ) %>% collect()

  # Unique Datasets as per header ID
  unique_datasets <- variable_data %>% summarise(
    unique_variable = n_distinct(subheader_id)
  ) %>% collect()

  unique_topics <- variable_data %>% summarise(
    unique_variable = n_distinct(header_id)
  ) %>% collect()



  fluidRow(
    column(
      width = 4,
      descriptionBlock(
        number = unique_variables,
        numberColor = "success",
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
  
  
  
  
}



header_choices <- function() {
  
  # Set_names gives the 
  # shown name
  # while map gives the actual
  # search value
  # Connection to DB; ####
  connection <- DBI::dbConnect(
    RSQLite::SQLite(),
    dbname = "dstTIMES.sqlite"
  )
  
  header_data <- tbl(connection, "header") %>%
    collect()
  
  map(
    1:nrow(header_data),
    function(i) {
      
      header_data$id[i]
      
    }
  ) %>% set_names(header_data$name)
  
  
  
} 