To run the tests, you must CD into the testcases folder and execute run_test_cases.sh or the respective shell file. compute_approx_wallclock.sh compares
the exact solution and the approximate solution.

This MUST be done in Git Bash or something similar, or else the tests wont execute.

In the output folder, the outputs are stored in .actual files (the actual input) and compared with the .out files.


TO RUN PLOT_RUNTIME:
    You need to update the top line with the path to the virtual environment. For me, I ran this in
    the terminal:<br>
        which python (on bash)<br>
        the copied that path to the top line, then I was able to run it normally
