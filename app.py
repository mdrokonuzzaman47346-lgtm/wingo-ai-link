import datetime
import pandas as pd
import streamlit as st

# ============================================================
# 1. Page Configuration
# ============================================================
st.set_page_config(
    page_title="Result History Tracker", page_icon="📊", layout="wide"
)

st.markdown(
    """
<style>
    .glow-table {
        width: 100%;
        border-collapse: collapse;
        border: 2px solid #38bdf8;
        border-radius: 10px;
        overflow: hidden;
        margin-top: 15px;
        margin-bottom: 15px;
        background-color: #0b0f19;
    }
    .glow-table th {
        background-color: #1e293b;
        color: #ffffff;
        padding: 12px;
        text-align: center;
        font-weight: bold;
        font-size: 15px;
        border-bottom: 2px solid #38bdf8;
    }
    .glow-table td {
        padding: 10px;
        text-align: center;
        font-weight: bold;
        font-size: 15px;
        border-bottom: 1px solid #1e293b;
        color: #ffffff;
    }
    .txt-big { color: #3b82f6 !important; font-weight: bold; }
    .txt-small { color: #a855f7 !important; font-weight: bold; }
    .txt-green { color: #2ecc71 !important; font-weight: bold; }
    .txt-red { color: #ef4444 !important; font-weight: bold; }
</style>
""",
    unsafe_allow_html=True,
)

st.title("📊 Result History Tracker")
st.caption(
    "This tool logs and summarizes past results only. It does not, and cannot, "
    "predict future outcomes of a random draw. Any 'streak' or 'pattern' shown "
    "below is a description of history, not a forecast."
)

# ============================================================
# 2. Google Sheet Live Data Loader (fixed: real usage + safe errors)
# ============================================================
SHEET_ID = "1OwGoYO76mBvQpD8B5iclV3dfPwn4_sUiCHt8dMNuMqc"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"


@st.cache_data(ttl=60)
def load_google_sheet_data():
    """Fetch the full sheet. Returns (df, error_message)."""
    try:
        df_live = pd.read_csv(CSV_URL, dtype=str)
        if df_live is None or df_live.empty:
            return None, "Sheet returned no rows."
        return df_live, None
    except Exception as e:
        return None, f"{type(e).__name__}: {e}"


live_df, load_error = load_google_sheet_data()

with st.expander("🌐 Google Sheet Sync Status", expanded=False):
    if live_df is not None:
        st.success(f"Connected. {len(live_df):,} rows fetched just now (cache refreshes every 60s).")
        st.dataframe(live_df.tail(10), use_container_width=True)
    else:
        st.error(
            "Could not fetch the Google Sheet, so this session is running on "
            "manually logged data only. No fallback numbers are being invented."
        )
        if load_error:
            st.caption(f"Details: {load_error}")

# ============================================================
# 3. Session Memory Setup
# ============================================================
MAX_HISTORY = 100

for key, default in {
    "result_history": [],
    "period_history": [],
    "history_records": [],
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ============================================================
# 4. Helpers
# ============================================================
def get_number_color(n: int) -> str:
    if n in (1, 3, 7, 9):
        return "GREEN"
    if n in (2, 4, 6, 8):
        return "RED"
    if n == 5:
        return "GREEN"  # adjust here if your game's rule differs
    return "UNKNOWN"


def bounded_append(lst: list, item, max_len: int = MAX_HISTORY):
    lst.append(item)
    if len(lst) > max_len:
        lst.pop(0)


# ============================================================
# 5. Logging Panel
# ============================================================
st.write("---")
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 📥 Log a Result")
    log_result = st.number_input(
        "Result number (0-9):", min_value=0, max_value=9, value=0, step=1, key="res_in"
    )
    log_period = st.number_input(
        "Last 3 digits of Period ID (000-999):",
        min_value=0, max_value=999, value=452, step=1, key="per_in",
    )

    b1, b2 = st.columns(2)
    with b1:
        if st.button("➕ Add to History", use_container_width=True):
            actual_bs = "BIG" if log_result >= 5 else "SMALL"
            actual_color = get_number_color(log_result)

            rec = {
                "period": log_period,
                "num": log_result,
                "bs_actual": actual_bs,
                "rg_actual": actual_color,
            }
            bounded_append(st.session_state.history_records, rec)
            bounded_append(st.session_state.result_history, log_result)
            bounded_append(st.session_state.period_history, log_period)
            st.rerun()

    with b2:
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.result_history = []
            st.session_state.period_history = []
            st.session_state.history_records = []
            st.rerun()

with col2:
    st.markdown("### 📊 Recent Stats (last 30 logged results)")
    if st.session_state.result_history:
        res_30 = st.session_state.result_history[-30:]
        per_30 = st.session_state.period_history[-30:]

        freq_dict = [res_30.count(i) for i in range(10)]
        big_count_30 = sum(1 for x in res_30 if x >= 5)
        small_count_30 = sum(1 for x in res_30 if x <= 4)

        st.markdown(f"📝 **Last {len(res_30)} results:** `{res_30}`")
        st.markdown(f"⏳ **Matching periods:** `{per_30}`")
        st.markdown(f"📊 **Frequency (0-9):** `{freq_dict}`")
        st.markdown(
            f"""
            <div style='background-color:#1c3144; padding:12px; border-radius:6px; border:1px solid #3498db; margin-top:10px;'>
                <span style='font-size:15px; font-weight:bold; color:#7efff5;'>
                    Last {len(res_30)} results ➔ BIG: {big_count_30} | SMALL: {small_count_30}
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.info("No data logged yet.")

# ============================================================
# 6. Descriptive Pattern Summary (NOT a prediction)
# ============================================================
st.write("---")
st.markdown("### 🔍 Descriptive Pattern Summary")
st.caption(
    "These labels describe what already happened in your logged data. "
    "They are not signals for what comes next — each draw is independent."
)

if st.session_state.result_history:
    res_hist = st.session_state.result_history
    sizes = ["SMALL" if n <= 4 else "BIG" for n in res_hist]

    last_3 = sizes[-3:]
    last_5 = sizes[-5:]
    last_30 = sizes[-30:]

    is_dragon_5 = len(last_5) == 5 and len(set(last_5)) == 1
    is_dragon_3 = len(last_3) == 3 and len(set(last_3)) == 1
    is_zigzag_3 = (
        len(last_3) == 3 and last_3[0] != last_3[1] and last_3[1] != last_3[2]
    )
    is_double_chain_4 = (
        len(sizes) >= 4
        and sizes[-1] == sizes[-2]
        and sizes[-3] == sizes[-4]
        and sizes[-2] != sizes[-3]
    )

    big_30 = sum(1 for x in last_30 if x == "BIG")
    small_30 = sum(1 for x in last_30 if x == "SMALL")

    # Priority order applied consistently: longest streak first, then
    # shorter patterns, then simple imbalance. Only ONE label is shown —
    # no contradictory overrides, because we stop at the first match.
    labels = []
    if is_dragon_5:
        labels.append(f"5-in-a-row streak of {sizes[-1]}")
    elif is_dragon_3:
        labels.append(f"3-in-a-row streak of {sizes[-1]}")
    elif is_zigzag_3:
        labels.append("Alternating (zig-zag) pattern in last 3")
    elif is_double_chain_4:
        labels.append("2-2 alternating pattern in last 4")
    elif len(last_30) == 30 and big_30 >= 22:
        labels.append(f"Last 30 skewed BIG ({big_30}/30)")
    elif len(last_30) == 30 and small_30 >= 22:
        labels.append(f"Last 30 skewed SMALL ({small_30}/30)")
    else:
        labels.append("No notable streak or skew in recent history")

    st.markdown(
        f"""
        <div style='background-color:#1e293b; padding:16px; border-left:6px solid #38bdf8; border-radius:6px;'>
            <h4 style='color:#f1c40f; margin-top:0px; margin-bottom:5px;'>{labels[0]}</h4>
            <p style='color:#ecf0f1; font-size:14px; margin:0px;'>
                This describes the last {len(sizes)} logged draws only. It carries no
                predictive weight for the next draw.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    st.info("Log at least 3 results to see a pattern summary.")

# ============================================================
# 7. History Table
# ============================================================
st.write("---")
st.markdown("### 📋 Logged History (most recent 7)")

if st.session_state.history_records:
    last_7 = st.session_state.history_records[-7:][::-1]

    rows_html = ""
    for idx, rec in enumerate(last_7, 1):
        bs_code = "B" if rec["bs_actual"] == "BIG" else "S"
        bs_class = "txt-big" if rec["bs_actual"] == "BIG" else "txt-small"
        rg_code = "G" if rec["rg_actual"] == "GREEN" else ("R" if rec["rg_actual"] == "RED" else "?")
        rg_class = "txt-green" if rec["rg_actual"] == "GREEN" else "txt-red"

        rows_html += (
            f"<tr><td>{idx}</td><td>{rec['period']}</td><td>{rec['num']}</td>"
            f"<td class='{bs_class}'>{bs_code}</td>"
            f"<td class='{rg_class}'>{rg_code}</td></tr>"
        )

    st.markdown(
        f"""
        <table class="glow-table">
            <thead>
                <tr><th>#</th><th>Period</th><th>Num</th><th>B/S</th><th>R/G</th></tr>
            </thead>
            <tbody>{rows_html}</tbody>
        </table>
        """,
        unsafe_allow_html=True,
    )
else:
    st.info("Log at least 1 result to see the history table.")

st.write("---")
st.caption(
    "⚠️ Reminder: outcomes in games like this are generated independently each "
    "round. No amount of historical pattern-tracking changes the odds of the "
    "next draw. If tracking results is starting to feel stressful or "
    "compulsive, consider taking a break."
)
