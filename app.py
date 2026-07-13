import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from collections import Counter, defaultdict

# 1. Page Configuration & Setup
st.set_page_config(page_title="Wingo Trend Matrix Omni-Engine", page_icon="📈", layout="wide")
st.title("📈 Wingo Trend Matrix Omni-Engine")
st.subheader("Statistical Analysis & Predictive Modeling Dashboard")

# 2. State Management Initialization (50-Round Maximum Capacity Retention Loop)
if 'result_history' not in st.session_state:
    st.session_state.result_history = []
if 'period_history' not in st.session_state:
    st.session_state.period_history = []
if 'prediction_history' not in st.session_state:
    st.session_state.prediction_history = []
if 'actual_outcome_history' not in st.session_state:
    st.session_state.actual_outcome_history = []

MAX_HISTORY = 50

# 3. Informational Telemetry Bar
st.markdown("### 🌐 Operational Telemetry Status")
t_col1, t_col2, t_col3 = st.columns(3)
with t_col1:
    st.success(f"📊 Historical Vector Database Capacity: {len(st.session_state.result_history)} / {MAX_HISTORY} Rounds Locked")
with t_col2:
    st.info("🧬 Analysis Engine: Ensemble Voting Matrix Active")
with t_col3:
    st.warning("⚖️ Validation Mode: Real-Engine Backtesting Active")

st.write("---")

# 4. Manual Data Logging & Control Section
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📥 Manual Parametric Input Control Panel")

    log_result = st.number_input("Last Active Result Number (0-9):", min_value=0, max_value=9, value=0, step=1, key="res_in")
    log_period = st.number_input("Last 3-Digits of Period ID (000-999):", min_value=0, max_value=999, value=100, step=1, key="per_in")

    b1, b2 = st.columns(2)
    with b1:
        if st.button("🚀 Push Node Parameters to State"):
            if len(st.session_state.result_history) >= MAX_HISTORY:
                st.session_state.result_history.pop(0)
                st.session_state.period_history.pop(0)
            if len(st.session_state.actual_outcome_history) >= (MAX_HISTORY - 1):
                st.session_state.actual_outcome_history.pop(0)

            st.session_state.result_history.append(log_result)
            st.session_state.period_history.append(log_period)

            current_size = "BIG" if log_result >= 5 else "SMALL"
            if len(st.session_state.result_history) > 1:
                st.session_state.actual_outcome_history.append(current_size)

            st.success("✔️ Vector data node appended successfully to system history state array.")
            st.rerun()

    with b2:
        if st.button("🗑️ Clear Internal Session Matrix Array"):
            st.session_state.result_history = []
            st.session_state.period_history = []
            st.session_state.prediction_history = []
            st.session_state.actual_outcome_history = []
            st.success("System state arrays flushed safely.")
            st.rerun()

with col2:
    st.markdown("### 📊 Operational Time-Series Chain View")
    if st.session_state.result_history:
        st.write(f"**📝 Historical Numeric Chain Trace (Last 15):** `{st.session_state.result_history[-15:]}`")
        st.write(f"**⏳ Chronological Period ID Array Context:** `{st.session_state.period_history[-15:]}`")

        sizes_mapped = ["SMALL" if n <= 4 else "BIG" for n in st.session_state.result_history]
        big_counts = sum(1 for x in sizes_mapped if x == "BIG")
        small_counts = sum(1 for x in sizes_mapped if x == "SMALL")
        st.info(f"📈 Current Pipeline Distributions -> BIG elements: {big_counts} | SMALL elements: {small_counts}")
    else:
        st.info("Internal transaction trace database arrays currently stand uninitialized. Please append rolling numbers.")

# --- Helper Function for Core Prediction Engine Architecture ---
def execute_prediction_engine(results_slice):
    if len(results_slice) < 5:
        return "Neutral Trend", 50.0, 0.0, {}

    mapped_sizes = ["SMALL" if n <= 4 else "BIG" for n in results_slice]
    mapped_parity = ["EVEN" if n % 2 == 0 else "ODD" for n in results_slice]
    total_elements = len(results_slice)

    # A. Recent Weight System & Score
    weights = []
    for i in range(total_elements):
        if total_elements - i <= 10:
            weights.append(2.0)  # Double weight for last 10 rounds
        else:
            weights.append(1.0)
    
    total_w = sum(weights)
    weighted_big = sum(weights[i] for i in range(total_elements) if mapped_sizes[i] == "BIG")
    recent_trend_score = (weighted_big / total_w) * 100.0

    # B. Transition Matrix Calculation
    trans_counts = defaultdict(int)
    for i in range(len(mapped_sizes) - 1):
        trans_counts[f"{mapped_sizes[i]}→{mapped_sizes[i+1]}"] += 1
    
    big_exits = sum(1 for x in mapped_sizes[:-1] if x == "BIG")
    small_exits = sum(1 for x in mapped_sizes[:-1] if x == "SMALL")
    
    p_bb = (trans_counts["BIG→BIG"] / big_exits * 100) if big_exits > 0 else 50.0
    p_bs = (trans_counts["BIG→SMALL"] / big_exits * 100) if big_exits > 0 else 50.0
    p_sb = (trans_counts["SMALL→BIG"] / small_exits * 100) if small_exits > 0 else 50.0
    p_ss = (trans_counts["SMALL→SMALL"] / small_exits * 100) if small_exits > 0 else 50.0
    
    trans_matrix_pct = {"BB": p_bb, "BS": p_bs, "SB": p_sb, "SS": p_ss}

    # C. Existing Advanced Indicator Pre-calculations
    dragon_streak = 1
    for i in range(len(mapped_sizes) - 1, 0, -1):
        if mapped_sizes[i] == mapped_sizes[i-1]:
            dragon_streak += 1
        else:
            break
    is_dragon_active = dragon_streak >= 4

    zigzag_alternations = 0
    for i in range(len(mapped_sizes) - 1, max(0, len(mapped_sizes) - 6), -1):
        if mapped_sizes[i] != mapped_sizes[i-1]:
            zigzag_alternations += 1
        else:
            break
    is_zigzag_active = zigzag_alternations >= 3

    volatilities = [abs(results_slice[i] - results_slice[i-1]) for i in range(1, len(results_slice))]
    mean_volatility = float(np.mean(volatilities)) if volatilities else 0.0
    volatility_score = min(100.0, (mean_volatility / 4.5) * 100.0)

    # D. Ensemble Voting Engine Infrastructure
    votes = []
    
    # Vote 1: Ratio Engine Vote
    if recent_trend_score > 53.0:
        votes.append("BIG")
    elif recent_trend_score < 47.0:
        votes.append("SMALL")
    else:
        votes.append("NEUTRAL")

    # Vote 2: Transition Engine Vote
    last_state = mapped_sizes[-1]
    if last_state == "BIG":
        votes.append("BIG" if p_bb > p_bs else "SMALL" if p_bs > p_bb else "NEUTRAL")
    else:
        votes.append("BIG" if p_sb > p_ss else "SMALL" if p_ss > p_sb else "NEUTRAL")

    # Vote 3: Pattern Engine Vote (Convolution Engine Mapping)
    pattern_vote = "NEUTRAL"
    if len(results_slice) >= 5:
        target_seq = results_slice[-3:]
        match_indices = []
        for i in range(len(results_slice) - 4):
            if results_slice[i:i+3] == target_seq:
                match_indices.append(i + 3)
        if match_indices:
            next_elements = [results_slice[idx] for idx in match_indices if idx < len(results_slice)]
            if next_elements:
                big_match_count = sum(1 for x in next_elements if x >= 5)
                pattern_vote = "BIG" if big_match_count / len(next_elements) > 0.5 else "SMALL"
    votes.append(pattern_vote)

    # Vote 4: Momentum Engine Vote (Dragon/ZigZag Analysis)
    momentum_vote = "NEUTRAL"
    if is_dragon_active:
        momentum_vote = mapped_sizes[-1]
    elif is_zigzag_active:
        momentum_vote = "SMALL" if mapped_sizes[-1] == "BIG" else "BIG"
    votes.append(momentum_vote)

    # Majority Voting Resolution Layer
    vote_counts = Counter(votes)
    winner, win_count = vote_counts.most_common(1)[0]
    
    # Confidence Score Calculation Algorithm
    base_confidence = (win_count / 4.0) * 100.0
    if winner == "BIG":
        skew_bonus = max(0.0, (recent_trend_score - 50.0) * 0.4)
        confidence_score = min(98.5, base_confidence + skew_bonus)
        calculated_signal = "BIG Trend"
    elif winner == "SMALL":
        skew_bonus = max(0.0, (50.0 - recent_trend_score) * 0.4)
        confidence_score = min(98.5, base_confidence + skew_bonus)
        calculated_signal = "SMALL Trend"
    else:
        confidence_score = 50.0
        calculated_signal = "Neutral Trend"

    # Volatility Check Boundary Override Rules
    if volatility_score > 82.0 and not is_dragon_active:
        calculated_signal = "Skip Recommendation"
        confidence_score = 0.0

    return calculated_signal, confidence_score, recent_trend_score, trans_matrix_pct

# 5. Core Mathematical Processing Frame Trigger
if len(st.session_state.result_history) >= 5:
    st.write("---")
    st.markdown("## ⚙️ Advanced Pattern and Ensemble Voting Engine")

    results = st.session_state.result_history
    periods = st.session_state.period_history
    mapped_sizes = ["SMALL" if n <= 4 else "BIG" for n in results]
    mapped_parity = ["EVEN" if n % 2 == 0 else "ODD" for n in results]
    total_elements = len(results)

    # Run Active Core Engine Calculation Frame
    calculated_signal, confidence_score, recent_trend_score, trans_matrix_pct = execute_prediction_engine(results)

    # Append Generated Output Safely to Tracking Arrays
    if len(st.session_state.prediction_history) < len(st.session_state.actual_outcome_history) + 1:
        st.session_state.prediction_history.append(calculated_signal)

    # Module 1 & 2: Hot/Cold Distribution Matrices
    num_counts = Counter(results)
    sorted_by_freq = sorted(range(10), key=lambda x: num_counts[x], reverse=True)
    hot_numbers = sorted_by_freq[:3]
    cold_numbers = sorted_by_freq[-3:]

    # Module 3: Variance Gap Matrix Tracker
    gap_matrix = {}
    for target in range(10):
        occurrences = [i for i, x in enumerate(results) if x == target]
        if len(occurrences) >= 2:
            gap_matrix[target] = int(np.mean(np.diff(occurrences)))
        else:
            gap_matrix[target] = total_elements

    # Number Transition Matrix Analysis Calculation (0-9 Matrix Context)
    num_trans_matrix = defaultdict(lambda: defaultdict(int))
    for i in range(len(results) - 1):
        num_trans_matrix[results[i]][results[i+1]] += 1

    # Ratios for Display Metrics
    big_ratio100 = (sum(1 for x in mapped_sizes if x == "BIG") / total_elements) * 100.0
    small_ratio100 = 100.0 - big_ratio100
    odd_ratio100 = (sum(1 for x in mapped_parity if x == "ODD") / total_elements) * 100.0
    even_ratio100 = 100.0 - odd_ratio100

    # Dragon & ZigZag Streak Length Trackers for Display UI
    dragon_streak = 1
    for i in range(len(mapped_sizes) - 1, 0, -1):
        if mapped_sizes[i] == mapped_sizes[i-1]:
            dragon_streak += 1
        else:
            break
    volatilities = [abs(results[i] - results[i-1]) for i in range(1, len(results))]
    volatility_score = min(100.0, (float(np.mean(volatilities)) / 4.5) * 100.0) if volatilities else 0.0
    trend_strength = min(100.0, (abs(np.mean(results[-3:]) - np.mean(results[:-3])) / 4.5) * 100.0) if len(results) >= 6 else 0.0

    # 6. Visualization Render Layer Panels
    v_col1, v_col2 = st.columns(2)

    with v_col1:
        st.markdown("### 🔢 Comprehensive Historical Vector Distribution Data")
        hist_fig = go.Figure(data=[go.Bar(
            x=list(range(10)),
            y=[results.count(i) for i in range(10)],
            marker_color='#38bdf8',
            opacity=0.85
        )])
        hist_fig.update_layout(
            title="Total Frequency Footprint by Single Integer Node",
            xaxis_title="Observed Integer Result Value",
            yaxis_title="Statistical Sampling Frequency Count",
            template="plotly_dark",
            margin=dict(l=20, r=20, t=40, b=20),
            height=280
        )
        st.plotly_chart(hist_fig, width='stretch')

    with v_col2:
        st.markdown("### 📈 Time-Series Value Deviation Trace Graph")
        trend_fig = go.Figure(data=[go.Scatter(
            x=list(range(len(results))),
            y=results,
            mode='lines+markers',
            line=dict(color='#9b59b6', width=2),
            marker=dict(size=6, color='#f1c40f')
        )])
        trend_fig.update_layout(
            title="Time-Series Linear Node Value Trajectory",
            xaxis_title="Historical Sampling Sequence Index",
            yaxis_title="Recorded Variable Integer Output",
            template="plotly_dark",
            margin=dict(l=20, r=20, t=40, b=20),
            height=280
        )
        st.plotly_chart(trend_fig, width='stretch')

    # 7. Analytical Telemetry Gauge Metrics Rows
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    with m_col1:
        st.metric("🔥 Hot Elements Array", f"[{', '.join(map(str, hot_numbers))}]")
    with m_col2:
        st.metric("❄️ Cold Elements Array", f"[{', '.join(map(str, cold_numbers))}]")
    with m_col3:
        st.metric("⚡ Volatility Index Score", f"{volatility_score:.1f}%")
    with m_col4:
        st.metric("📈 Vector Velocity Strength", f"{trend_strength:.1f}%")

    m_col5, m_col6, m_col7, m_col8 = st.columns(4)
    with m_col5:
        st.metric("📦 BIG Saturation Ratio", f"{big_ratio100:.1f}%")
    with m_col6:
        st.metric("📉 SMALL Saturation Ratio", f"{small_ratio100:.1f}%")
    with m_col7:
        st.metric("⚖️ ODD/EVEN Divergence", f"{odd_ratio100:.0f}/{even_ratio100:.0f}%")
    with m_col8:
        st.metric("🧬 Recent Trend Score", f"{recent_trend_score:.1f}%")

    # 8. Core Strategy Resolution Display Frame
    st.write("---")
    st.markdown("### 🎯 System Analysis Resolution Strategy Output")

    sig_color = "#38bdf8" if "BIG" in calculated_signal else "#e74c3c" if "SMALL" in calculated_signal else "#f1c40f" if "Neutral" in calculated_signal else "#95a5a6"
    display_string = f"{calculated_signal.upper()} (Confidence: {confidence_score:.1f}%)" if confidence_score > 0 else calculated_signal.upper()

    st.markdown(f"""
    <div style="padding:25px; border-radius:5px; background-color:{sig_color}22; border-left:5px solid {sig_color};">
        <h4>STRATEGY EVALUATION: [ {display_string} ]</h4>
        <p><strong>Ensemble Voting Resolution Parameters Locked.</strong> Run historical verification metrics downstream for validation checks.</p>
    </div>
    """, unsafe_allow_html=True)

    # 9. Transition Analytics Visual Displays Layout Matrix
    st.write("---")
    st.markdown("### 📊 Advanced Matrix Transition Analytics Loop")
    trans_col1, trans_col2 = st.columns(2)
    
    with trans_col1:
        st.markdown("#### 🔄 Size Structural Transition Probability Matrix")
        matrix_df = pd.DataFrame({
            "Target Next State (→)": ["BIG Next", "SMALL Next"],
            "BIG Prev (↓)": [f"{trans_matrix_pct['BB']:.1f}%", f"{trans_matrix_pct['BS']:.1f}%"],
            "SMALL Prev (↓)": [f"{trans_matrix_pct['SB']:.1f}%", f"{trans_matrix_pct['SS']:.1f}%"]
        })
        st.table(matrix_df)

    with trans_col2:
        st.markdown("#### 🔢 Number Transition Cluster Trailing Log (0-9)")
        num_logs = []
        for source_num in range(10):
            if source_num in num_trans_matrix:
                targets = num_trans_matrix[source_num]
                top_target = max(targets, key=targets.get)
                num_logs.append(f"Number `[{source_num}]` triggers pattern shift towards → `[{top_target}]` most frequently.")
        if num_logs:
            st.write("<br>".join(num_logs[:5]), unsafe_allow_html=True)
        else:
            st.caption("Insufficient chronological variance data array lengths to process integer mappings.")

    # 10. Real-Engine Prediction Verification & Backtesting Architecture Panels
    st.write("---")
    st.markdown("### 📌 Empirical Validation Verification & Historical Performance Reports")
    val_col1, val_col2 = st.columns(2)

    with val_col1:
        st.markdown("#### 🔍 Historical Real-Engine Accuracy Audit Ledger")
        
        big_hits, big_total = 0, 0
        small_hits, small_total = 0, 0
        neutral_count = 0
        audit_records = []

        if st.session_state.actual_outcome_history and len(st.session_state.prediction_history) > 1:
            total_verifications = min(len(st.session_state.actual_outcome_history), len(st.session_state.prediction_history) - 1)
            
            for i in range(total_verifications):
                pred_raw = st.session_state.prediction_history[i]
                actual_state = st.session_state.actual_outcome_history[i]
                
                is_hit = False
                if "BIG" in pred_raw:
                    big_total += 1
                    if actual_state == "BIG":
                        is_hit = True
                        big_hits += 1
                elif "SMALL" in pred_raw:
                    small_total += 1
                    if actual_state == "SMALL":
                        is_hit = True
                        small_hits += 1
                else:
                    neutral_count += 1

                audit_records.append({
                    "Index Position": i + 1,
                    "Forecast Sign": pred_raw,
                    "Actual Node": actual_state,
                    "Resolution": "SUCCESSFUL" if is_hit else "MISMATCH" if "Neutral" not in pred_raw else "NEUTRAL SKIP"
                })

            b_acc = (big_hits / big_total * 100) if big_total > 0 else 0.0
            s_acc = (small_hits / small_total * 100) if small_total > 0 else 0.0
            
            st.write(f"🟢 **BIG Prediction Accuracy:** `{b_acc:.1f}%` (Total: {big_total})")
            st.write(f"🔴 **SMALL Prediction Accuracy:** `{s_acc:.1f}%` (Total: {small_total})")
            st.write(f"⚪ **Neutral Prediction Counts:** `{neutral_count}`")
            
            st.dataframe(pd.DataFrame(audit_records).tail(8), width='stretch')
        else:
            st.info("System validation telemetry requires additional node elements to construct matching comparative loops.")

    with val_col2:
        st.markdown("#### 📋 Real-Engine Matrix Variance Backtesting Simulator")
        if len(results) >= 6:
            backtest_records = []
            profitable_simulations = 0
            total_simulations = 0

            # Step through time chronologically applying the ACTUAL engine logic retrospectively
            for step in range(4, len(results) - 1):
                subset_results = results[:step + 1]
                sim_signal, _, _, _ = execute_prediction_engine(subset_results)
                
                actual_next_value = results[step + 1]
                actual_next_size = "BIG" if actual_next_value >= 5 else "SMALL"

                if "Skip" in sim_signal or "Neutral" in sim_signal:
                    sim_res = "SKIP STRUCTURAL BOUNDS"
                elif ("BIG" in sim_signal and actual_next_size == "BIG") or ("SMALL" in sim_signal and actual_next_size == "SMALL"):
                    sim_res = "PROFIT ALIGNED"
                    profitable_simulations += 1
                    total_simulations += 1
                else:
                    sim_res = "DRAWDOWN MAXIMUM"
                    total_simulations += 1

                backtest_records.append({
                    "Backtest Node Index": step + 1,
                    "Engine Forecast": sim_signal,
                    "True Next Node": actual_next_value,
                    "Validation Resolution": sim_res
                })

            st.dataframe(pd.DataFrame(backtest_records).tail(8), width='stretch')
            sim_yield = (profitable_simulations / total_simulations) * 100.0 if total_simulations > 0 else 0
