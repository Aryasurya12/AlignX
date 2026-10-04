from anchoralign.pipeline.orchestrator import run_pipeline
from anchoralign.config import AnchorAlignConfig

def run_demo():
    ref = "ACGTACGTACGT"
    query = "ACGTACGAACGT"
    config = AnchorAlignConfig(L_min=3, clustering_k=3)
    
    res = run_pipeline(ref, query, config)
    
    print(f"Reference length: {res.reference_length}")
    print(f"Query length: {res.query_length}")
    print(f"Anchor count: {len(res.anchors)}")
    for a in res.anchors:
        print(f"  Anchor: ref:{a.reference_start}-{a.reference_end} q:{a.query_start}-{a.query_end}")
    print(f"Gap count: {len(res.gaps)}")
    for g in res.gaps:
        print(f"  Gap: {g.id} ref:{g.reference_start}-{g.reference_end} q:{g.query_start}-{g.query_end}")
    print(f"Selected strategies: {[g.selected_strategy for g in res.gaps]}")
    print(f"Alignment:")
    print(f"Ref:   {res.final_alignment.aligned_reference}")
    print(f"Query: {res.final_alignment.aligned_query}")
    print(f"Mutation count: {len(res.mutations)}")
    for m in res.mutations:
        print(f"  {m.type} at ref:{m.reference_position} q:{m.query_position} (ref:'{m.reference_sequence}' query:'{m.query_sequence}')")
    print(f"Compound event count: {len(res.compound_events)}")
    
run_demo()
