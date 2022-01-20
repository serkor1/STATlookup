import runpy
import os



print(
    '''
    ==========================================================
    | This program starts the webscraping of DST (TIMES).    |
    | Make sure you have the updated version locally before  |
    | you continue this program                              |
    ==========================================================
    '''
)


run_program = str(input(
    '''
    Are you sure you want to run the program? [Yes/No]
    '''
)).lower()



# Start program conditional on the
# input
if run_program == "yes":
    print(
        '''
        Starting Program!
        '''
    )

    runpy.run_path(
        "dstHeader.py"
    )

    runpy.run_path(
        "dstSubheader.py"
    )

    # runpy.run_path(
    #     "dstVariable.py"
    # )

    print(
        '''
        Done!
        '''
    )


elif run_program == "no":
    print(
        '''
        Aborted!
        '''
    )


else:
    print(
        '''
        Invalid Input!
        '''
    )