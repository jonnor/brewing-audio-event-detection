

## Semi-automatic labeling

If there is a single
Know that there should be a quite regular pattern.
Distance between events should be near the same. With few outliers
And values in range.. 0.5 to 30 seconds 
And event length should be very regular.

There are however exceptions.
For example when gargling/burping appears, it becomes hard to count individual events
More like a start/stop of a *class*. Or a consider "gargling" as separate event from "plop"

In some cases, the plops seem to be clustered.
Many coming at once, then a pause, then many again.

From the event distance, and lengths, one can estimate expected number of events per time period
Can compare autolabeled event count vs this. Desirable to have near 100%
Can be used for hyper-parameter search for autolabling

Snorkel as a tool for combining labeling heuristics?
https://github.com/snorkel-team/snorkel
