# AlignX Live Demonstration Script

**Duration:** 5-7 Minutes

## Step 1: Environment Setup
- Explain: "AlignX is an interactive research tool for structural DNA alignment."
- Run: `streamlit run streamlit_app.py`.
- Open browser.

## Step 2: The UI Overview
- Click on the **Run Alignment** tab.
- Explain: "Here we input sequences and tune the anchor/DP heuristics."

## Step 3: Loading an Example
- From the Presets dropdown, select `Long Indel (Requires adaptive band)`.
- Click **Load Preset**.
- Explain: "This loads a 150bp sequence containing a massive 80bp indel surrounded by conserved anchor blocks."

## Step 4: Execution
- Check `Run Full DP Baseline`.
- Click **Run AlignX Pipeline**.
- Explain: "While this runs, AlignX is executing KMP pattern matching, discovering anchors, predicting the DP gap bounds, and executing."

## Step 5: Visualizing Results
- Open **Overview & Export**. Show the metrics: 0 mismatches, 1 large gap.
- Open **Anchor & Gap Analysis**. Point to the exact coordinates where the long indel forced a gap.
- Open **Algorithm Decisions**. Explain: "Notice here that the band width was estimated to be wide enough to encompass the 80bp gap. The boundary was not touched, avoiding fallback."

## Step 6: Baseline Verification
- Open **Baseline Comparison**.
- Explain: "Our score and exact sequence matching precisely equal the Full DP O(N*M) output, confirming mathematical correctness."

## Step 7: Export
- Show the "Download Execution Report" JSON button in the Overview tab to highlight reproducibility.

## Fallback Plan
- If Full DP baseline hangs on large inputs, uncheck the box and explain that standard DP takes quadratic time and crashes the browser. Show pre-computed Phase 7 Explorer data instead.
