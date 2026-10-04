from typing import List
from ..models.mutation import Mutation

def detect_mutations_engine(aligned_reference: str, aligned_query: str) -> List[Mutation]:
    """
    Scans the complete alignment to identify substitution, insertion, and deletion events.
    Groups consecutive identical event types into single events.
    """
    mutations = []
    
    ref_coord = 0
    query_coord = 0
    
    current_type = None
    current_ref_seq = []
    current_query_seq = []
    start_ref_coord = 0
    start_query_coord = 0
    start_align_pos = 0
    
    def commit_mutation():
        if current_type:
            mutations.append(Mutation(
                type=current_type,
                reference_position=start_ref_coord,
                query_position=start_query_coord,
                reference_sequence="".join(current_ref_seq),
                query_sequence="".join(current_query_seq),
                alignment_position=start_align_pos
            ))
            
    for i in range(len(aligned_reference)):
        r = aligned_reference[i]
        q = aligned_query[i]
        
        if r != '-' and q != '-' and r != q:
            m_type = "substitution"
        elif r == '-' and q != '-':
            m_type = "insertion"
        elif r != '-' and q == '-':
            m_type = "deletion"
        else:
            m_type = None
            
        if m_type != current_type or m_type is None:
            commit_mutation()
            current_type = m_type
            current_ref_seq = []
            current_query_seq = []
            start_ref_coord = ref_coord
            start_query_coord = query_coord
            start_align_pos = i
            
        if current_type is not None:
            if r != '-':
                current_ref_seq.append(r)
            if q != '-':
                current_query_seq.append(q)
                
        # Increment coordinates
        if r != '-':
            ref_coord += 1
        if q != '-':
            query_coord += 1
            
    commit_mutation()
    return mutations
