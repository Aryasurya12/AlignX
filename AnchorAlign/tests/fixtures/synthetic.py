FIXTURES = {
    "case1": {
        "desc": "Identical sequences",
        "ref": "ACGTACGTACGT",
        "query": "ACGTACGTACGT",
        "expected_differences": 0
    },
    "case2": {
        "desc": "One substitution",
        "ref": "ACGTACGT",
        "query": "ACGTTCGT",
        "expected_differences": 1
    },
    "case3": {
        "desc": "Insertion",
        "ref": "ACGTACGT",
        "query": "ACGTGACGT",
        "expected_differences": 1
    },
    "case4": {
        "desc": "Deletion",
        "ref": "ACGTGACGT",
        "query": "ACGTACGT",
        "expected_differences": 1
    },
    "case5": {
        "desc": "Multiple differences",
        "ref": "ACGTACGTACGT",
        "query": "ACGTTTGTACGA",
        "expected_differences": 4
    },
    "case6": {
        "desc": "Repeated motifs",
        "ref": "ATATATATAT",
        "query": "ATATATATAT",
        "expected_differences": 0
    },
    "case7": {
        "desc": "No useful anchors",
        "ref": "ACGT",
        "query": "TGCA",
        "expected_differences": 4
    },
    "case8": {
        "desc": "Very short sequences",
        "ref": "A",
        "query": "A",
        "expected_differences": 0
    }
}
