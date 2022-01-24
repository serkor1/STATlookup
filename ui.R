#
# This is the user-interface definition of a Shiny web application. You can
# run the application by clicking 'Run App' above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#


bs4DashPage(
  dark = TRUE,
  header = bs4DashNavbar(
    title = bs4DashBrand(
    title = div(icon("project-diagram"), strong("STAT Lookup"), align = "center"),
      color = "primary",
    ),skin = "dark"
    
    
  ),
  
  sidebar = bs4DashSidebar(
    
    skin = "dark",
    fixed = TRUE,
    width = "350px",
    collapsed = FALSE,
    minified = FALSE,
    status = "lightblue",
    db_counter(),
    hr(),
    
    bs4SidebarMenu(
      id = "by_dataset",
      flat = FALSE,
      compact = TRUE,
      
      sidebarHeader("Search by Variable"),
      
      searchInput(
        inputId = "global_search",
        label = NULL,
        btnSearch = icon("search", fa_verify = FALSE),
        # btnReset = icon("remove", fa_verify = FALSE),
        placeholder = "Search for variable, eg. RECNUM",
        width = "100%"
      ),
      
      sidebarHeader("Or search by Topic"),
      
      pickerInput(
        inputId = "search_header",
        label = NULL,
        choices = header_choices(),
        options = list(
          title = "Pick Topic",
          width = 'auto'),
        width = 'auto'
      ),
      
      topicLookup_sidebar("topic_lookup")


    )
    
  ),
  
  body = bs4DashBody(
    useShinyjs(),
    # Search Output
    # from the global search
    variableLookup_UI('var_lookup'),
    topicLookup_ui('topic_lookup')
    
  ),
  
  footer = bs4DashFooter(
    fixed = TRUE,
    left = version,
    right = tags$a(
      icon("github"),
      href = "https://github.com/serkor1/STATlookup",
      class = "my_class",
      "Github",
      target = "_blank"
    )
  ),preloader = list()
  
)