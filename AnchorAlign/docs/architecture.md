# Architecture

## 1. Project Objective
To compare two DNA sequences efficiently by anchoring exact matches.

## 4. Pipeline Architecture
Reference + Query
        ↓
Preprocessing
        ↓
Anchor Engine
        ↓
Ordered Anchors
        ↓
Gap Engine
      ↓
Feature Extraction
      ↓
Rule-Based Classifier
      ↓
Strategy Selector
      ↓
   ┌───────┐
   ↓       ↓
Banded   Full
  DP      DP
   └───┬───┘
       ↓
  Aligned Gaps
        ↓
Reconstruction
        ↓
Mutation Engine
        ↓
Evaluation
        ↓
Visualization
