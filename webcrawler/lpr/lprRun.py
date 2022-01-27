import runpy


# 1) Run Header Programme
runpy.run_path("lprHeader.py")

# 2) Run Subheader Programme
runpy.run_path('lprSubheader.py')

# 3) Run Variable Programme
runpy.run_path('lprVariable.py')

# 4) Run HTML Programme
runpy.run_path('lprHTML.py')