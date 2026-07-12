import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO

# -----------------------------------------------------------------------------
# 1. STREAMLIT PAGE CONFIGURATION & THEME
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Professional Wingo Analysis Engine",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling for visual scannability and structure
st.markdown("""
<style>
    .metric-card {
        background-color: #1e222b;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #4a90e2;
        margin-bottom: 10px;
    }
    .signal-card {
        background-color: #14171f;
        padding: 25px;
        border-radius: 10px;
        border: 2px solid #28a745;
        text-align: center;
    }
    .reason-box {
        background-color: #1a1e24;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #343a40;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. CORE MATHEMATICAL ANALYSIS ENGINE
# -----------------------------------------------------------------------------
def analyze_wingo_data(df):
    """
    Performs pure deterministic calculations across all requested modules.
    DataFrame must be sorted with Top = Most Recent (Current Period).
    """
    if df.empty:
        return {}

    total_records = len(df)
    
    # Fundamental column mappings
    df['Size'] = df['Number'].apply(lambda x: 'BIG' if x >= 5 else 'SMALL')
    df['Parity'] = df['Number'].apply(lambda x: 'ODD' if x % 2 != 0 else 'EVEN')
    
    # Temporal order inversion for sequential tracking (Oldest -> Newest)
    df_chrono = df.iloc[::-1].copy().reset_index(drop=True)
    chrono_len = len(df_chrono)

    # MODULE 1 & 2: Transition Matrix & Number-to-Number Probability Table
    num_transition_matrix = np.zeros((10, 10))
    for i in range(chrono_len - 1):
        current_num = df_chrono.loc[i, 'Number']
        next_num = df_chrono.loc[i + 1, 'Number']
        if 0 <= current_num <= 9 and 0 <= next_num <= 9:
            num_transition_matrix[current_num][next_num] += 1
            
    num_prob_matrix = np.zeros((10, 10))
    for r in range(10):
        row_sum = num_transition_matrix[r].sum()
        if row_sum > 0:
            num_prob_matrix[r] = (num_transition_matrix[r] / row_sum) * 100

    # MODULE 3: Big-Small Transition Statistics
    bs_states = ['BIG', 'SMALL']
    bs_matrix = pd.DataFrame(0, index=bs_states, columns=bs_states)
    for i in range(chrono_len - 1):
        curr_state = df_chrono.loc[i, 'Size']
        next_state = df_chrono.loc[i + 1, 'Size']
        if curr_state in bs_states and next_state in bs_states:
            bs_matrix.loc[curr_state, next_state] += 1
            
    bs_prob_matrix = bs_matrix.copy().astype(float)
    for state in bs_states:
        r_sum = bs_matrix.loc[state].sum()
        if r_sum > 0:
            bs_prob_matrix.loc[state] = (bs_matrix.loc[state] / r_sum) * 100

    # MODULE 6: Last 20 Round Statistics
    df_last_20 = df.head(20).copy()
    l20_total = len(df_last_20)
    l20_big = int((df_last_20['Size'] == 'BIG').sum())
    l20_small = int((df_last_20['Size'] == 'SMALL').sum())
    l20_odd = int((df_last_20['Parity'] == 'ODD').sum())
    l20_even = int((df_last_20['Parity'] == 'EVEN').sum())

    # MODULE 11 & 7: Trend Strength & Trend Score Breakdown
    recent_15 = df['Size'].head(15)
    len_r15 = len(recent_15)
    r15_big_count = (recent_15 == 'BIG').sum()
    r15_small_count = len_r15 - r15_big_count
    big_ratio = r15_big_count / len_r15 if len_r15 > 0 else 0.5
    trend_strength = abs(big_ratio - 0.5) * 200
    
    trend_breakdown = {
        "Micro Window (Size 15) Total": len_r15,
        "BIG Appearances": r15_big_count,
        "SMALL Appearances": r15_small_count,
        "Raw Distribution Deviation": abs(r15_big_count - r15_small_count)
    }

    # Core Original System Features
    df['Size_Match'] = df['Size'] == df['Size'].shift(-1)
    win_rate_size = (df['Size_Match'].sum() / (total_records - 1)) * 100 if total_records > 1 else 50.0

    # Streak Detector
    current_streak_len = 0
    current_streak_type = None
    if total_records > 0:
        sizes = df['Size'].tolist()
        current_streak_type = sizes[0]
        for s in sizes:
            if s == current_streak_type:
                current_streak_len += 1
            else:
                break

    dragon_active = current_streak_len >= 5
    
    # Zig Zag Detector
    zig_zag_count = 0
    if total_records > 2:
        for i in range(min(10, total_records - 2)):
            if df['Size'].iloc[i] != df['Size'].iloc[i+1] and df['Size'].iloc[i+1] != df['Size'].iloc[i+2]:
                zig_zag_count += 1
    zig_zag_active = zig_zag_count >= 3

    # Number Frequencies & Hot/Cold
    num_counts = df['Number'].value_counts().reindex(range(10), fill_value=0)
    num_freq_pct = (num_counts / total_records) * 100
    hot_numbers = num_counts.nlargest(3).index.tolist()
    cold_numbers = num_counts.nsmallest(3).index.tolist()

    # Volatility
    recent_10 = df['Number'].head(10)
    volatility_score = float(np.std(recent_10)) if len(recent_10) > 1 else 0.0

    # Gap Analysis
    gap_dict = {}
    for n in range(10):
        found_indices = df[df['Number'] == n].index
        gap_dict[n] = int(found_indices[0]) if len(found_indices) > 0 else total_records

    # Odd/Even
    odd_count = (df['Parity'] == 'ODD').sum()
    even_count = total_records - odd_count
    odd_even_ratio = f"{odd_count}:{even_count}"

    # Skip Recommendation
    should_skip = volatility_score > 3.2 or (45 <= trend_strength <= 55 and current_streak_len < 2)

    return {
        "win_rate_size": win_rate_size,
        "current_streak_len": current_streak_len,
        "current_streak_type": current_streak_type,
        "dragon_active": dragon_active,
        "zig_zag_active": zig_zag_active,
        "num_freq_pct": num_freq_pct,
        "hot_numbers": hot_numbers,
        "cold_numbers": cold_numbers,
        "volatility_score": volatility_score,
        "gap_dict": gap_dict,
        "odd_even_ratio": odd_even_ratio,
        "trend_strength": trend_strength,
        "should_skip": should_skip,
        "total_records": total_records,
        "num_prob_matrix": num_prob_matrix,
        "bs_prob_matrix": bs_prob_matrix,
        "l20_stats": {"total": l20_total, "big": l20_big, "small": l20_small, "odd": l20_odd, "even": l20_even},
        "trend_breakdown": trend_breakdown,
        "df_chrono": df_chrono
    }

# -----------------------------------------------------------------------------
# 3. RULE-BASED TRANSPARENT SIGNAL ENGINE
# -----------------------------------------------------------------------------
def generate_logical_signal(metrics, df):
    """
    Calculates rule-based signals strictly from properties of the dataset.
    """
    if not metrics or df.empty:
        return "NO SIGNAL", "Weak", ["Insufficient rows."]

    reasons = []
    scores = 0
    recent_size = df['Size'].iloc[0]
    opposing_size = "SMALL" if recent_size == "BIG" else "BIG"
    
    # 1. Trend Rule Calculation
    if metrics['dragon_active']:
        predicted_size = recent_size
        reasons.append(f"Trend: Active 'Dragon Pattern' discovered. Riding current streak ({metrics['current_streak_len']}x {recent_size}).")
        scores += 3
    elif metrics['zig_zag_active']:
        predicted_size = opposing_size
        reasons.append(f"Trend: Clear alternating 'Zig-Zag' sequence flagged. Anticipating structural flip to {opposing_size}.")
        scores += 2
    else:
        predicted_size = recent_size if metrics['trend_strength'] > 60 else opposing_size
        reasons.append(f"Trend: Distribution strength calculated at {metrics['trend_strength']:.1f}%.")
        scores += 1

    # 2. Frequency Rule Calculation
    recent_5 = df['Size'].head(5).tolist()
    big_freq = recent_5.count('BIG')
    if big_freq >= 4:
        if predicted_size == 'BIG': scores += 2
        reasons.append(f"Frequency: Heavy volume skew towards BIG ({big_freq}/5 periods) in recent micro-window.")
    elif big_freq <= 1:
        if predicted_size == 'SMALL': scores += 2
        reasons.append(f"Frequency: Heavy volume skew towards SMALL ({(5 - big_freq)}/5 periods) in recent micro-window.")
    else:
        scores += 1
        reasons.append("Frequency: Distribution metrics normalized across short-term sample sets.")

    # 3. Volatility Rule Calculation
    if metrics['volatility_score'] > 3.0:
        reasons.append(f"Volatility: High variance observed ({metrics['volatility_score']:.2f}). Sequence breaks likely.")
        scores -= 1
    else:
        reasons.append(f"Volatility: Low variance detected ({metrics['volatility_score']:.2f}). Stable conditions persist.")
        scores += 2

    # 4. Win Rate Rule Calculation
    if metrics['win_rate_size'] > 54.0:
        scores += 2
        reasons.append(f"Win Rate: Local dataset yields historical back-to-back persistence rate of {metrics['win_rate_size']:.1f}%.")
    else:
        scores += 1
        reasons.append(f"Win Rate: Historical baseline trends match standard model thresholds ({metrics['win_rate_size']:.1f}%).")

    # Final Strength Translation Matrix
    if scores >= 7:
        strength = "Strong"
    elif scores >= 4:
        strength = "Medium"
    else:
        strength = "Weak"

    if metrics['should_skip']:
        return "SKIP RECOMMENDATION", "N/A", ["Skip Engine triggered. Trend ambiguity or high volatility violates safety thresholds."]

    return predicted_size, strength, reasons

# -----------------------------------------------------------------------------
