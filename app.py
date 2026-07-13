import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from collections import Counter, defaultdict
import datetime

# ==================================================================================
# 1. PAGE CONFIGURATION & SETUP
# ==================================================================================
st.set_page_config(page_title="Wingo Trend Matrix Omni-Engine v2", page_icon="📈", layout="wide")
st.title("📈 Wingo Trend Matrix Omni-Engine v2")
st.subheader("Advanced Weighted Ensemble Voting & Real-Time Predictive Architecture")

# ==================================================================================
# 2. ROBUST SESSION STATE MANAGEMENT
# ==================================================================================
if 'result_history' not in st.session_state:
    st.session_state.result_history = []
if 'period_history' not in st.session_state:
    st.session_state.period_history = []
if 'prediction_ledger' not in st.session_state:
    st.session_state.prediction_ledger = []

MAX_HISTORY = 50

# Telemetry Overview Banner
st.markdown("### 🌐 Operational Telemetry Status")
t_col1, t_col2, t_col3 = st.columns(3)
with t_col1:
    st.success(f"📊 Historical Vector Database: {len(st.session_state.result_history)} / {MAX_HISTORY} Rounds")
with t_col2:
    st.info("🧬 Core Engine: 15-Module Deterministic Ensemble Voting Active")
with t_col3:
    st.warning("⚖️ Performance Analyzer: Live Verification Dynamic Pipeline Active")

st.write("---")

# ==================================================================================
# 3. MANUAL DATA LOGGING & CONTROL SECTION
# ==================================================================================
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📥 Manual Parametric Input Control Panel")
    log_result = st.number_input("Last Active Result Number (0-9):", min_value=0, max_value=9, value=0, step=1, key="res_in")
    log_period = st.number_input("Target/Next Period ID (Last 3 Digits, e.g., 101):", min_value=0, max_value=999, value=101, step=1, key="per_in")

    b1, b2 = st.columns(2)
    with b1:
        if st.button("🚀 Push Parameters to State"):
            if len(st.session_state.result_history) >= MAX_HISTORY:
                st.session_state.result_history.pop(0)
                st.session_state.period_history.pop(0)

            st.session_state.result_history.append(log_result)
            st.session_state.period_history.append(log_period)
            st.success(f"✔️ Appended Node: Result {log_result} for Period Context {log_period}")
            st.rerun()

    with b2:
        if st.button("🗑️ Flush System Session Arrays"):
            st.session_state.result_history = []
            st.session_state.period_history = []
            st.session_state.prediction_ledger = []
            st.success("Internal pipeline database flushed safely.")
            st.rerun()

with col2:
    st.markdown("### 📊 Operational Time-Series Chain View")
    if st.session_state.result_history:
        st.write(f"**📝 Numeric Sequence (Last 15):** `{st.session_state.result_history[-15:]}`")
        st.write(f"**⏳ Period ID Context Context:** `{st.session_state.period_history[-15:]}`")
        
        sizes_mapped = ["SMALL" if n <= 4 else "BIG" for n in st.session_state.result_history]
        st.info(f"📈 Window Distribution -> BIG: {sizes_mapped.count('BIG')} | SMALL: {sizes_mapped.count('SMALL')}")
    else:
        st.info("System arrays currently stand uninitialized. Please input sequential rolling numbers above.")

# ==================================================================================
# 4. CORE DETERMINISTIC PREDICTION ENGINE ARCHITECTURE (15-Module Ensemble Engine)
# ==================================================================================
def run_ensemble_prediction_engine(results_slice, periods_slice):
    total_len = len(results_slice)
    if total_len < 5:
        return "BIG", 50.0, ["Insufficient Historical Vector Data Context"], {}

    window_size = min(total_len, 25)
    res_w = results_slice[-window_size:]
    per_w = periods_slice[-window_size:]
    w_len = len(res_w)

    sizes_w = ["SMALL" if n <= 4 else "BIG" for n in res_w]
    parity_w = ["EVEN" if n % 2 == 0 else "ODD" for n in res_w]

    votes = {"BIG": 0.0, "SMALL": 0.0}
    supporting_factors = []
    engine_details = {}

    def apply_vote(side, weight, label):
        votes[side] += weight
        supporting_factors.append(f"✓ {label} -> {side}")

    # MODULE 1: Recent Trend Analysis (Sub-windows: Last 5, Last 10, Last 20)
    for sub_size, w_val in [(5, 1.2), (10, 1.0), (20, 0.8)]:
        if w_len >= sub_size:
            sub_sizes = sizes_w[-sub_size:]
            sub_b = sub_sizes.count("BIG")
            sub_s = sub_sizes.count("SMALL")
            side = "BIG" if sub_b >= sub_s else "SMALL"
            apply_vote(side, w_val, f"Trend Window (Last {sub_size})")

    # MODULE 2 & 3: Size & Parity Base Ratio Distribution Analysis
    b_ratio = sizes_w.count("BIG") / w_len
    apply_vote("SMALL" if b_ratio >= 0.5 else "BIG", 1.0, "Reversion Size Ratio Engine")

    even_ratio = parity_w.count("EVEN") / w_len
    apply_vote("BIG" if even_ratio >= 0.5 else "SMALL", 0.7, "Parity Correlation Analysis")

    # MODULE 4: Dragon Streak Detection Logic Array
    dragon_streak = 1
    for i in range(w_len - 1, 0, -1):
        if sizes_w[i] == sizes_w[i-1]:
            dragon_streak += 1
        else:
            break
    if dragon_streak >= 4:
        apply_vote(sizes_w[-1], 1.5, f"Dragon Continuity Tracker ({dragon_streak} Rnds)")
    else:
        apply_vote("BIG" if sizes_w[-1] == "SMALL" else "SMALL", 0.5, "Standard Momentum Reversion")

    # MODULE 5: ZigZag Anti-Alternation Micro-Engine Analysis
    zigzag_count = 0
    for i in range(w_len - 1, max(0, w_len - 6), -1):
        if sizes_w[i] != sizes_w[i-1]:
            zigzag_count += 1
        else:
            break
    if zigzag_count >= 3:
        next_zigzag = "SMALL" if sizes_w[-1] == "BIG" else "BIG"
        apply_vote(next_zigzag, 1.4, f"ZigZag Sequence Continuation ({zigzag_count} Osc)")

    # MODULE 6: Classical Step-1 Transition Probability Matrix Array Map
    t_counts = defaultdict(int)
    for i in range(w_len - 1):
        t_counts[f"{sizes_w[i]}→{sizes_w[i+1]}"] += 1
    
    b_exits = sum(1 for x in sizes_w[:-1] if x == "BIG")
    s_exits = sum(1 for x in sizes_w[:-1] if x == "SMALL")
    
    p_bb = (t_counts["BIG→BIG"] / b_exits * 100) if b_exits > 0 else 50.0
    p_bs = (t_counts["BIG→SMALL"] / b_exits * 100) if b_exits > 0 else 50.0
    p_sb = (t_counts["SMALL→BIG"] / s_exits * 100) if s_exits > 0 else 50.0
    p_ss = (t_counts["SMALL→SMALL"] / s_exits * 100) if s_exits > 0 else 50.0
    
    engine_details["transitions"] = {"BB": p_bb, "BS": p_bs, "SB": p_sb, "SS": p_ss}
    
    if sizes_w[-1] == "BIG":
        apply_vote("BIG" if p_bb >= p_bs else "SMALL", 1.2, "Transition Matrix Solver")
    else:
        apply_vote("BIG" if p_sb >= p_ss else "SMALL", 1.2, "Transition Matrix Solver")

    # MODULE 7: 2-State Markov Chain Stochastic Analysis Framework
    state_matrix = np.zeros((2, 2))
    state_matrix[0, 0] = p_bb / 100.0
    state_matrix[0, 1] = p_bs / 100.0
    state_matrix[1, 0] = p_sb / 100.0
    state_matrix[1, 1] = p_ss / 100.0
    
    try:
        S = np.dot(state_matrix, state_matrix)
        stationary_big_bias = S[0, 0] / (S[0, 0] + S[1, 0]) if (S[0, 0] + S[1, 0]) > 0 else 0.5
        apply_vote("BIG" if stationary_big_bias >= 0.5 else "SMALL", 1.1, "Markov Stationary Driver")
    except:
        apply_vote("BIG", 0.1, "Markov Chain Fallback Default")

    # MODULE 8: Convolution Pattern Matching Engine Framework (Depth 2, 3, 4 Arrays)
    pattern_side = "NEUTRAL"
    for d in [4, 3, 2]:
        if w_len > d:
            target_p = res_w[-d:]
            matches = []
            for i in range(w_len - d - 1):
                if res_w[i:i+d] == target_p:
                    matches.append(res_w[i+d])
            if matches:
                b_m = sum(1 for x in matches if x >= 5)
                pattern_side = "BIG" if b_m >= (len(matches) - b_m) else "SMALL"
                break
    if pattern_side != "NEUTRAL":
        apply_vote(pattern_side, 1.3, f"Historical Convolution Matching (Depth {d})")

    # MODULE 9: Period ID Sequence Delta Vector Tracking Analysis
    if w_len >= 3:
        p_deltas = np.diff(per_w)
        mean_p_delta = float(np.mean(p_deltas)) if len(p_deltas) > 0 else 1.0
        p_factor = int(abs(per_w[-1] + mean_p_delta)) % 2
        apply_vote("BIG" if p_factor == 0 else "SMALL", 0.6, "Period Sequencing Vector Engine")

    # MODULE 10, 11 & 12: Frequency Variance Gap / Hot & Cold Index Metrics
    counts = Counter(res_w)
    hot_sorted = sorted(range(10), key=lambda x: counts[x], reverse=True)
    
    gaps = {}
    for target in range(10):
        pos = [idx for idx, val in enumerate(res_w) if val == target]
        gaps[target] = (w_len - 1 - pos[-1]) if pos else w_len

    engine_details["hot_numbers"] = hot_sorted[:3]
    engine_details["cold_numbers"] = hot_sorted[-3:]
    engine_details["gaps"] = gaps

    big_hot_strength = sum(counts[n] for n in hot_sorted[:3] if n >= 5)
    small_hot_strength = sum(counts[n] for n in hot_sorted[:3] if n <= 4)
    apply_vote("BIG" if big_hot_strength >= small_hot_strength else "SMALL", 0.9, "Numerical Hot-Spot Vector")

    # MODULE 13 & 14: Recent Velocity Momentum / Trend Reversal Trackers
    if w_len >= 6:
        m_recent = np.mean(res_w[-3:])
        m_prior = np.mean(res_w[-6:-3])
        m_delta = m_recent - m_prior
        
        apply_vote("BIG" if m_delta >= 0 else "SMALL", 0.8, "Velocity Momentum Tracker")
        
        if m_recent > 7.2:
            apply_vote("SMALL", 1.1, "Trend Reversal Overbought Detector")
        elif m_recent < 1.8:
            apply_vote("BIG", 1.1, "Trend Reversal Oversold Detector")

    # MODULE 15: Deep Weighted Recency Index Score Frame
    r_weights = np.linspace(1.0, 3.0, w_len)
    w_sum = sum(r_weights)
    weighted_big_score = sum(r_weights[i] for i in range(w_len) if sizes_w[i] == "BIG")
    recency_percentage = (weighted_big_score / w_sum) * 100.0
    
    apply_vote("BIG" if recency_percentage >= 50.0 else "SMALL", 1.5, "Deep Linear Recency Scalar")

    # RESOLUTION & CONFIDENCE EVALUATION LAYER
    total_votes_cast = votes["BIG"] + votes["SMALL"]
    if votes["BIG"] >= votes["SMALL"]:
        final_prediction = "BIG"
        agreement_ratio = votes["BIG"] / total_votes_cast if total_votes_cast > 0 else 0.5
    else:
        final_prediction = "SMALL"
        agreement_ratio = votes["SMALL"] / total_votes_cast if total_votes_cast > 0 else 0.5

    raw_conf = 50.0 + (agreement_ratio - 0.5) * 97.0
    final_confidence = min(98.5, max(50.0, raw_conf))

    return final_prediction, final_confidence, supporting_factors, engine_details

# Execute calculations live
engine_ready = len(st.session_state.result_history) >= 5

if engine_ready:
    f_pred, f_conf, f_factors, f_details = run_ensemble_prediction_engine(
        st.session_state.result_history, st.session_state.period_history
    )
    
    next_expected_period = st.session_state.period_history[-1] + 1 if st.session_state.period_history else 100
    
    if st.session_state.prediction_ledger:
        last_logged_p = st.session_state.prediction_ledger[-1]["period_id"]
    else:
        last_logged_p = None

    if next_expected_period != last_logged_p:
        st.session_state.prediction_ledger.append({
            "period_id": next_expected_period,
            "prediction": f_pred,
            "confidence": f_conf,
            "timestamp": datetime.datetime.now().strftime("%H:%M:%S")
        })

    # ==================================================================================
    # 5. NEXT PREDICTION TERMINAL PANEL
    # ==================================================================================
    st.markdown("## 🎯 Next Prediction Focus Engine Matrix Terminal")
    
    p_bg = "#38bdf8" if f_pred == "BIG" else "#e74c3c"
    st.markdown(f"""
    <div style="padding:25px; border-radius:10px; background-color:{p_bg}18; border:2px solid {p_bg}; text-align:center;">
        <h1 style="color:{p_bg}; margin:0; font-size:45px;">🚀 NEXT PREDICTION: {f_pred}</h1>
        <h3 style="margin:10px 0 0 0;">CONFIDENCE SCORE: {f_conf:.1f}%</h3>
    </div>
    """, unsafe_allow_html=True)
    
    if f_conf < 55.0:
        st.markdown("""
        <div style="padding:10px; margin-top:10px; background-color:#f1c40f22; border-left:5px solid #f1c40f; text-align:center; font-weight:bold; color:#f1c40f;">
            ⚠️ ATTENTION WARNING: LOW CONFIDENCE MATRIX SIGNALS IDENTIFIED
        </div>
        """, unsafe_allow_html=True)

    st.markdown("#### 🔍 Active Core Engine Supporting Verification Factors Matrix:")
    fact_cols = st.columns(3)
    for idx, factor in enumerate(f_factors[:12]):
        fact_cols[idx % 3].markdown(f"<span style='color:#10b981;'>{factor}</span>", unsafe_allow_html=True)

# ==================================================================================
# 6. EMPIRICAL REAL-ENGINE PERFORMANCE & ACCURACY TRACKING LEDGER
# ==================================================================================
st.write("---")
st.markdown("### 📌 Empirical Real-Engine Accuracy & Telemetry Audit Reports")

if len(st.session_state.result_history) >= 6 and len(st.session_state.prediction_ledger) > 1:
    audit_records = []
    
    for i in range(1, len(st.session_state.result_history)):
        past_res = st.session_state.result_history[i]
        past_per = st.session_state.period_history[i]
        actual_size = "BIG" if past_res >= 5 else "SMALL"
        
        match = [p for p in st.session_state.prediction_ledger if p["period_id"] == past_per]
        if match:
            pred_item = match[0]
            is_correct = pred_item["prediction"] == actual_size
            audit_records.append({
                "Period ID": past_per,
                "Prediction": pred_item["prediction"],
                "Actual Outcome": actual_size,
                "Confidence": pred_item["confidence"],
                "Status": "SUCCESS" if is_correct else "FAIL",
                "Is_Low_Conf": pred_item["confidence"] < 55.0
            })
            
    if audit_records:
        df_audit = pd.DataFrame(audit_records)
        
        def calc_acc(df_sub):
            if df_sub.empty: return 0.0, 0
            success_count = sum(df_sub["Status"] == "SUCCESS")
            return (success_count / len(df_sub)) * 100.0, len(df_sub)

        df_high = df_audit[df_audit["Is_Low_Conf"] == False]

        acc_all, total_all = calc_acc(df_audit)
        acc_20, total_20 = calc_acc(df_audit.tail(20))
        acc_50, total_50 = calc_acc(df_audit.tail(50))
        acc_high, total_high = calc_acc(df_high)

        m_col1, m_col2, m_col3, m_col4 = st.columns(4)
        m_col1.metric("📊 Last 20 Rounds Accuracy", f"{acc_20:.1f}%", f"Samples: {total_20}")
        m_col2.metric("📈 Last 50 Rounds Accuracy", f"{acc_50:.1f}%", f"Samples: {total_50}")
        m_col3.metric("🎯 Total Overall Accuracy", f"{acc_all:.1f}%", f"Base Total: {total_all}")
        m_col4.metric("🛡️ High-Confidence Accuracy", f"{acc_high:.1f}%", f"Filter Base: {total_high}")
        
        st.markdown("#### 📋 Comprehensive Verification Matrix Archive Ledger")
        st.dataframe(df_audit.tail(10), width='stretch')
    else:
        st.info("Awaiting historical target synchronization bounds to lock performance calculations.")
else:
    st.info("Telemetry tracking initialization holds for extra sequence elements to complete calculations.")

# ==================================================================================
# 7. PRODUCTION-READY REPLAY VALIDATION BACKTEST ENGINE
# ==================================================================================
st.write("---")
st.markdown("### 📋 Matrix Real-Engine Retrospective Backtesting Simulator")

if engine_ready:
    backtest_data = []
    
    for step in range(4, len(st.session_state.result_history) - 1):
        sub_res = st.session_state.result_history[:step + 1]
        sub_per = st.session_state.period_history[:step + 1]
        
        b_pred, b_conf, _, _ = run_ensemble_prediction_engine(sub_res, sub_per)
        
        true_next_val = st.session_state.result_history[step + 1]
        true_next_size = "BIG" if true_next_val >= 5 else "SMALL"
        
        status_res = "PROFIT WIN" if b_pred == true_next_size else "DRAWDOWN LOSS"
        
        backtest_data.append({
            "Backtest Index": step + 1,
            "Target Period": st.session_state.period_history[step + 1],
            "Engine Forecast": b_pred,
            "True Outcome": true_next_size,
            "Resolution": status_res,
            "Confidence": b_conf
        })
        
    if backtest_data:
        df_bt = pd.DataFrame(backtest_data)
        bt_samples = len(df_bt)
        win_count = sum(df_bt["Resolution"] == "PROFIT WIN")
        win_rate = (win_count / bt_samples) * 100.0 if bt_samples > 0 else 0.0
        
        bt_col1, bt_col2, bt_col3 = st.columns(3)
        bt_col1.metric("🎯 Backtest Win Rate Indicator", f"{win_rate:.2f}%")
        bt_col2.metric("📉 Drawdown Loss Rate Metric", f"{100.0 - win_rate:.2f}%")
        bt_col3.metric("🔬 Simulation Sample Depth Base", f"{bt_samples} Rounds Run")
        
        st.dataframe(df_bt.tail(10), width='stretch')
    else:
        st.info("The backtesting system requires a baseline historical trace array containing at least 6 rounds.")
else:
    st.info("Awaiting structural array allocations to clear backtesting simulation parameters.")

# ==================================================================================
# 8. ADVANCED ANALYTICAL VISUALIZATION PLOTS LAYER (PLOTLY ENGINE FIXED)
# ==================================================================================
if engine_ready:
    st.write("---")
    st.markdown("### 📊 Real-Time Matrix Visualization Panel Arrays")
    
    viz_row1_col1, viz_row1_col2 = st.columns(2)
    viz_row2_col1, viz_row2_col2 = st.columns(2)
    viz_row3_col1, viz_row3_col2 = st.columns(2)
    
    tm = f_details["transitions"]
    
    # Plot 1: Transition Matrix Heatmap
    with viz_row1_col1:
        z_matrix = [[tm["BB"], tm["BS"]], [tm["SB"], tm["SS"]]]
        hm_fig = px.imshow(
            z_matrix, 
            labels=dict(x="Next State Target", y="Previous State Source", color="Probability Ratio %"),
            x=["BIG Next", "SMALL Next"],
            y=["BIG Prev", "SMALL Prev"],
            text_auto=".1f",
            color_continuous_scale="Viridis",
            title="Structural Size Probability Transition Matrix Heatmap"
        )
        hm_fig.update_layout(template="plotly_dark", height=290, margin=dict(l=10, r=10, t=40, b=10))
        st.plotly_chart(hm_fig, width='stretch')

    # Plot 2: Markov State Diagram (FIXED textposition style)
    with viz_row1_col2:
        markov_fig = go.Figure()
        markov_fig.add_trace(go.Scatter(
            x=[1, 2], y=[1, 1], mode="markers+text",
            marker=dict(size=[70, 70], color=["#38bdf8", "#e74c3c"]),
            text=["BIG", "SMALL"], textposition="top center",
            textfont=dict(color="white", size=14)
        ))
        markov_fig.update_layout(
            title=f"Markov Stochastic State Matrix Distributions (BB: {tm['BB']:.0f}% | SS: {tm['SS']:.0f}%)",
            template="plotly_dark", height=290,
            xaxis=dict(visible=False, range=[0.5, 2.5]), yaxis=dict(visible=False, range=[0.5, 1.5])
        )
        st.plotly_chart(markov_fig, width='stretch')

    # Plot 3: Confidence Metrics (FIXED line properties)
    with viz_row2_col1:
        if st.session_state.prediction_ledger:
            df_ledger = pd.DataFrame(st.session_state.prediction_ledger)
            conf_fig = px.line(
                df_ledger, x="period_id", y="confidence", 
                title="Historical Optimization Trend Signal Variance Chain Plots",
                markers=True, line_shape="spline"
            )
            conf_fig.update_traces(line_color="#10b981", line_width=2)
            conf_fig.update_layout(template="plotly_dark", height=290, yaxis=dict(range=[45, 105]))
            st.plotly_chart(conf_fig, width='stretch')
        else:
            st.info("Awaiting tracking telemetry arrays.")

    # Plot 4: Accuracy Trend Chart
    with viz_row2_col2:
        if 'audit_records' in locals() and audit_records:
            acc_tracker = []
            running_hits = 0
            for idx, r in enumerate(audit_records):
                if r["Status"] == "SUCCESS": running_hits += 1
                acc_tracker.append({"index": idx + 1, "Running Accuracy %": (running_hits / (idx + 1)) * 100.0})
            
            acc_fig = px.area(
                pd.DataFrame(acc_tracker), x="index", y="Running Accuracy %",
                title="Dynamic System Convergence Optimization Curves", color_discrete_sequence=["#9b59b6"]
            )
            acc_fig.update_layout(template="plotly_dark", height=290, yaxis=dict(range=[0, 105]))
            st.plotly_chart(acc_fig, width='stretch')
        else:
            st.info("Awaiting transaction trace logging sequences to render performance tracking curves.")

    # Plot 5: Size Distribution Pie Matrix Chart
    with viz_row3_col1:
        sizes_pie = ["SMALL" if n <= 4 else "BIG" for n in st.session_state.result_history]
        pie_df = pd.DataFrame(Counter(sizes_pie).items(), columns=["Structural State Type", "Total Samples Tracking Count"])
        pie_fig = px.pie(
            pie_df, names="Structural State Type", values="Total Samples Tracking Count",
            title="Pipeline Database Saturation Metric Status",
            color="Structural State Type", color_discrete_map={"BIG": "#38bdf8", "SMALL": "#e74c3c"}
        )
        pie_fig.update_layout(template="plotly_dark", height=290, margin=dict(l=10, r=10, t=40, b=10))
        st.plotly_chart(pie_fig, width='stretch')

    # Plot 6: Frequency Gap Analysis
    with viz_row3_col2:
        gap_data = f_details["gaps"]
        gap_df = pd.DataFrame(list(gap_data.items()), columns=["Integer Result Value", "Rounds Elapsed Interval Gap"])
        gap_fig = px.bar(
            gap_df, x="Integer Result Value", y="Rounds Elapsed Interval Gap",
            title="Frequency Recency Core Numerical Footprint Gaps Metrics",
            color="Rounds Elapsed Interval Gap", color_continuous_scale="Burg"
        )
        gap_fig.update_layout(template="plotly_dark", height=290, margin=dict(l=10, r=10, t=40, b=10))
        st.plotly_chart(gap_fig, width='stretch')

else:
    st.write("---")
    st.info("📊 Processing modules waiting for data stream stabilization. Input data values to start visual engines.")
