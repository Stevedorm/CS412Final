<pre>
There are some additional shell files, python scripts, csv's, and images in this directory. These are mainly for plotting the data from locally testing into a nice, displayable format.
The a_a png files are comparing the cost and runtimes of the approximate and augmented solutions to the TSP problem. The a_e png files show the dta from the approximate and exact solutions

To run the tests, you must CD into the testcases folder and execute run_test_cases.sh or the respective shell file. compute_approx_wallclock.sh compares the exact solution and the approximate solution.

This MUST be done in Git Bash or something similar, or else the tests wont execute.

In the output folder, the outputs are stored in .actual files (the actual input) and compared with the .out files.


TO RUN PLOT_RUNTIME:
    You need to update the top line with the path to the virtual environment. For me, I ran this in
    the terminal:<br>
        which python (on bash)<br>
        the copied that path to the top line, then I was able to run it normally
</pre>
