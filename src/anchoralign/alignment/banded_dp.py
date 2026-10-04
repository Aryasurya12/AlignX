from ..models.alignment import AlignmentResult
from ..config import AnchorAlignConfig

def banded_dp_align(reference_gap: str, query_gap: str, config: AnchorAlignConfig, band_width: int) -> AlignmentResult:
    """
    Banded Dynamic Programming alignment.
    Cells outside the band |i - j| <= band_width are unreachable (-inf).
    """
    r = len(reference_gap)
    q = len(query_gap)
    
    INF = float('-inf')
    
    # DP matrix, initialize to -inf
    dp = [[INF for _ in range(q + 1)] for _ in range(r + 1)]
    
    dp[0][0] = 0
    
    for i in range(1, r + 1):
        if i <= band_width:
            dp[i][0] = i * config.gap_penalty
            
    for j in range(1, q + 1):
        if j <= band_width:
            dp[0][j] = j * config.gap_penalty
            
    boundary_touched = False
            
    # Fill DP within the band
    for i in range(1, r + 1):
        # The valid range of j for a given i is:
        # |i - j| <= band_width  =>  i - band_width <= j <= i + band_width
        j_start = max(1, i - band_width)
        j_end = min(q, i + band_width)
        
        for j in range(j_start, j_end + 1):
            match = dp[i-1][j-1] + (config.match_score if reference_gap[i-1] == query_gap[j-1] else config.mismatch_penalty)
            
            # For delete, we come from (i-1, j). Ensure (i-1, j) is within its band.
            delete = dp[i-1][j] + config.gap_penalty if j <= (i-1) + band_width and j >= (i-1) - band_width else INF
            
            # For insert, we come from (i, j-1). Ensure (i, j-1) is within its band.
            insert = dp[i][j-1] + config.gap_penalty if (j-1) <= i + band_width and (j-1) >= i - band_width else INF
            
            dp[i][j] = max(match, delete, insert)
            
    if dp[r][q] == INF:
        # Cannot align within band (e.g. sequence length difference > band_width)
        boundary_touched = True
        return AlignmentResult("", "", 0.0, "banded_dp", band_width, True)
            
    # Traceback
    i, j = r, q
    align_r = []
    align_q = []
    
    while i > 0 or j > 0:
        # Check boundary condition (is the optimal path on the edge of the band?)
        if abs(i - j) == band_width:
            boundary_touched = True
            
        if i > 0 and j > 0:
            score_diag = dp[i-1][j-1] + (config.match_score if reference_gap[i-1] == query_gap[j-1] else config.mismatch_penalty)
            if dp[i][j] == score_diag:
                align_r.append(reference_gap[i-1])
                align_q.append(query_gap[j-1])
                i -= 1
                j -= 1
                continue
        
        if i > 0:
            score_del = dp[i-1][j] + config.gap_penalty if j <= (i-1) + band_width and j >= (i-1) - band_width else INF
            if dp[i][j] == score_del and score_del != INF:
                align_r.append(reference_gap[i-1])
                align_q.append('-')
                i -= 1
                continue
                
        if j > 0:
            score_ins = dp[i][j-1] + config.gap_penalty if (j-1) <= i + band_width and (j-1) >= i - band_width else INF
            if dp[i][j] == score_ins and score_ins != INF:
                align_r.append('-')
                align_q.append(query_gap[j-1])
                j -= 1
                continue
                
    return AlignmentResult(
        aligned_reference="".join(reversed(align_r)),
        aligned_query="".join(reversed(align_q)),
        score=dp[r][q],
        strategy="banded_dp",
        band_width=band_width,
        boundary_touched=boundary_touched
    )
