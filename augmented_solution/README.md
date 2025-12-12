<pre>
This directory contains two augmented solutions, the 
first iteration ending in _partE and the final being _new.
The one that really matters is _new, 

Strategy and Approach:
    I use a multi restart with a nearest neighbor and a 2-opt local search. <br>With each restart, the algorithm builds a greedy tour (deterministic nearest neighbor from a random start) <br>and improves it with two_opt until there can’t be anymore improvements or the time budget is met. <br>It tracks the best tour and best cost over all restarts, so if a restart is less optimal, it keeps the best one found. <br>The number of restarts depends on the time budget and the size of V. <br>This approach allows me to get a good cost at the expense of a slightly slower algorithm.

compute_all_three_wallclock.sh - computes all three implementations and stores results in a csv
run_test_cases_new.sh - runs test cases, with some randomness they might say failed but they execute so they are "passing" and not the exact output it is being diff-ed to.
run_examples.sh - computes the lower bound and delta using cs412_tsp_approx_lb.py
run_test_cases_new.sh - runs the tests with the "new" (augmented solution)
collect_lower_bounds.py - collects the lower bounds to be plotted and writes to the lower_bound_results.csv
<pre>