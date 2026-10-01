from ..models.alignment import AlignmentResult
from ..config import AnchorAlignConfig

def full_dp_align(reference_gap: str, query_gap: str, config: AnchorAlignConfig) -> AlignmentResult:
    """
    Full Global Dynamic Programming alignment (Needleman-Wunsch).
    """
    r = len(reference_gap)
    q = len(query_gap)
    
    # DP matrix
    # dp[i][j] stores the score of aligning reference[:i] and query[:j]
    dp = [[0 for _ in range(q + 1)] for _ in range(r + 1)]
    
    # Initialization
    for i in range(1, r + 1):
        dp[i][0] = i * config.gap_penalty
    for j in range(1, q + 1):
        dp[0][j] = j * config.gap_penalty
        
    # Fill DP
    for i in range(1, r + 1):
        for j in range(1, q + 1):
            match = dp[i-1][j-1] + (config.match_score if reference_gap[i-1] == query_gap[j-1] else config.mismatch_penalty)
            delete = dp[i-1][j] + config.gap_penalty
            insert = dp[i][j-1] + config.gap_penalty
            # Tie breaking: Diagonal (match/mismatch), Deletion (ref gap), Insertion (query gap)
            dp[i][j] = max(match, delete, insert)
            
    # Traceback
    i, j = r, q
    align_r = []
    align_q = []
    
    while i > 0 or j > 0:
        if i > 0 and j > 0:
            score_diag = dp[i-1][j-1] + (config.match_score if reference_gap[i-1] == query_gap[j-1] else config.mismatch_penalty)
            if dp[i][j] == score_diag:
                align_r.append(reference_gap[i-1])
                align_q.append(query_gap[j-1])
                i -= 1
                j -= 1
                continue
        
        if i > 0:
            score_del = dp[i-1][j] + config.gap_penalty
            if dp[i][j] == score_del:
                align_r.append(reference_gap[i-1])
                align_q.append('-')
                i -= 1
                continue
                
        if j > 0:
            align_r.append('-')
            align_q.append(query_gap[j-1])
            j -= 1
            continue
            
    return AlignmentResult(
        aligned_reference="".join(reversed(align_r)),
        aligned_query="".join(reversed(align_q)),
        score=dp[r][q],
        strategy="full_dp",
        band_width=0,
        boundary_touched=False
    )
