import runpy


print("Creating High Quality Database form Statistics Denmark:")
print("-------------------------------------------------------")
# Run Header Program
runpy.run_path("hq/hqHeader.py")

# Run Subheader Program
runpy.run_path("hq/hqSubheader.py")

# Run Variable Program
runpy.run_path("hq/hqVariable.py")

# Run Description Progrtam
runpy.run_path("hq/hqDesc.py")



print("Creating TIMES Database from Statistics Denmark:")
print("------------------------------------------------")
# Run Header Program
runpy.run_path("times/timesHeader.py")

# Run Subheader Program
runpy.run_path("times/timesSubheader.py")

# Run Variable Program
runpy.run_path("times/timesVariable.py")


runpy.run_path("times/timesDesc.py")





print("Creating Health Related Database form eSundhed:")
print("-------------------------------------------------------")
# 1) Run Header Programme
runpy.run_path("lpr/lprHeader.py")

# 2) Run Subheader Programme
runpy.run_path('lpr/lprSubheader.py')

# 3) Run Variable Programme
runpy.run_path('lpr/lprVariable.py')

# 4) Run HTML programme
runpy.run_path("lpr/lprHTML.py")

# 5) Run Description Programme
runpy.run_path("lpr/lprDesc.py")