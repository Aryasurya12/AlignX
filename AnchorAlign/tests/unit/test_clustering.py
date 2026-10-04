import pytest
from anchoralign.mutations.clustering import cluster_mutations
from anchoralign.models.mutation import Mutation
from anchoralign.config import AnchorAlignConfig

def test_clustering_k0():
    config = AnchorAlignConfig(clustering_k=0)
    m1 = Mutation("substitution", 10, 10, "A", "C", 10)
    m2 = Mutation("substitution", 12, 12, "A", "C", 12)
    
    clusters = cluster_mutations([m1, m2], config)
    assert len(clusters) == 2

def test_clustering_small_k():
    config = AnchorAlignConfig(clustering_k=1)
    m1 = Mutation("substitution", 10, 10, "A", "C", 10)
    m2 = Mutation("substitution", 11, 11, "A", "C", 11)
    m3 = Mutation("substitution", 50, 50, "A", "C", 50)
    
    clusters = cluster_mutations([m1, m2, m3], config)
    assert len(clusters) == 2
    assert clusters[0]["mutation_count"] == 2
    assert clusters[1]["mutation_count"] == 1

def test_empty_mutations():
    config = AnchorAlignConfig(clustering_k=5)
    clusters = cluster_mutations([], config)
    assert len(clusters) == 0

def test_deletion_distance():
    config = AnchorAlignConfig(clustering_k=2)
    m1 = Mutation("deletion", 10, 10, "AAA", "", 10)
    # The deletion spans ref positions 10, 11, 12. Ends at 13.
    m2 = Mutation("substitution", 14, 10, "C", "G", 13)
    
    # Distance is 14 - 13 = 1 (which is <= 2)
    clusters = cluster_mutations([m1, m2], config)
    assert len(clusters) == 1
    assert clusters[0]["mutation_count"] == 2
