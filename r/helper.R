# Display Variable Information
variable_info <- function(variable_data) {
  
  #' @param variable_data a tibble with variable information
  #' @return A UI with converted HTML texts
  information <- variable_data$html %>% 
    read_html() %>% 
    html_elements('p') %>% 
    html_text()
  
  
  bs4Card(
    title = paste("Variable:", variable_data$var),
    width = 4,
    collapsible = FALSE,
    headerBorder = TRUE,
    div(style = "width: auto; overflow-y: scroll; height:300px",
        
        p(strong("Full name")),
        
        variable_data$var_name,
        
        br(),
        
        p(strong("Short Description")),
        
        information[[2]],
        
        br(),
        
        p(strong("Long Description")),
        
        information[[3]]
        
        )
    
    
  )
  
}

variable_value <- function(variable_data) {
  
  #' @param variable_data a tibble with variable information
  #' @return A UI with converted HTML texts
  information <- variable_data$html %>% 
    read_html() %>% 
    html_table()
  
  
  
      bs4Card(
        title = "Values",
        width = 8,
        collapsible = FALSE,
        headerBorder = TRUE,
        div(style = "width: auto; overflow-y: scroll; height:300px",
            renderTable(
              information,
              width = "100%",
            )
            )
        
        
        
      )
      
 
  
  
  
}