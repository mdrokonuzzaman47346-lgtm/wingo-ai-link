import streamlit as st
import pandas as pd

st.set_page_config(page_title="Wingo Quantum AI Link", page_icon="🎯", layout="centered")
st.title("🎯 Wingo 1m Quantum AI Prediction Link")
st.subheader("Developed for my Best Friend | Active Mode ⚡")

@st.cache_data
def load_matrix():
    df = pd.read_csv('wingo_billion_data.csv')
    return df

try:
    df = load_matrix()
    st.success("🤖 High-Quality Server Matrix: 1 Billion Data Loaded Successfully!")
except:
    st.error("❌ Database Error: 'wingo_billion_data.csv' missing in this folder!")
    st.stop()

st.write("---")
st.markdown("### 🔍 Enter Live Running Numbers (Old to New)")
old_num = st.number_input("Enter 1-Minute Before OLD Number (0-9):", min_value=0, max_value=9, value=6, step=1)
new_num = st.number_input("Enter Just Arrived NEW Number (0-9):", min_value=0, max_value=9, value=4, step=1)

if st.button("🚀 ACTIVATE BILLION DATA SCAN"):
    matches = []
    for i in range(len(df) - 2):
        if df['result_number'].iloc[i] == old_num and df['result_number'].iloc[i+1] == new_num:
            next_round_result = df['result_number'].iloc[i+2]
            matches.append(next_round_result)
            
    total_cases = len(matches)
    
    if total_cases == 0:
        st.warning(f"No historical sequence found for pair {old_num}/{new_num}.")
    else:
        big_count = sum(1 for num in matches if num >= 5)
        small_count = sum(1 for num in matches if num <= 4)
        
        big_pct = round((big_count / total_cases) * 100, 2)
        small_pct = round((small_count / total_cases) * 100, 2)
        
        st.write("---")
        st.markdown(f"#### 📊 Total Matches Found in History: **{total_cases} Cases**")
        st.info(f"🔵 BIG Probability: **{big_pct}%** | 🔴 SMALL Probability: **{small_pct}%**")
        
        if big_pct > small_pct:
            st.markdown(f"### 🔥 STRATEGY SIGNAL: <span style='color:blue'>[ BIG ]</span> | CONFIDENCE: **{big_pct}%**", unsafe_allow_html=True)
        else:
            st.markdown(f"### 🔥 STRATEGY SIGNAL: <span style='color:red'>[ SMALL ]</span> | CONFIDENCE: **{small_pct}%**", unsafe_allow_html=True)
          
