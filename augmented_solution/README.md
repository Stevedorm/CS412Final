<pre>
This directory contains two augmented solutions, the first iteration ending in _partE
and the final being _new.

Strategy and Approach:
    I use a multi restart with a nearest neighbor and a 2-opt local search. <br>With each restart, the algorithm builds a greedy tour (deterministic nearest neighbor from a random start) <br>and improves it with two_opt until there can’t be anymore improvements or the time budget is met. <br>It tracks the best tour and best cost over all restarts, so if a restart is less optimal, it keeps the best one found. The number of restarts depends on the time budget and the size of V. <br>This approach allows me to get a good cost at the expense of a slightly slower algorithm.
<pre>