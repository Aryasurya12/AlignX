# Correctness

## Banded DP Limitations
Banded Dynamic Programming reduces the O(rq) search space to a diagonal band of width `b`. It provides the exact same optimal alignment score as Full DP **only if** the optimal alignment path lies entirely within the computed band. 

When structural variations like long insertions or deletions push the necessary traceback path outside of `|i - j| <= band_width`, Banded DP will either fail to find a valid alignment or will return a sub-optimal alignment bounded by the band limits. 

The implementation flags `boundary_touched = True` when the optimal path reaches the edges of the allowed band, indicating that expanding the band might yield a better score.
