# =========================
# ADVANCED ANALYSIS PANEL
# =========================

st.write("---")
st.markdown("## 📈 Advanced Statistical Analysis")

res_hist = st.session_state.result_history

if len(res_hist) > 0:

    # Frequency Table
    freq_df = pd.DataFrame({
        "Number": range(10),
        "Count": [res_hist.count(i) for i in range(10)]
    })

    st.markdown("### 🔢 Number Frequency Table")
    st.dataframe(freq_df, use_container_width=True)

    # Result Trend Chart
    st.markdown("### 📊 Result Trend Chart")

    chart_df = pd.DataFrame({
        "Result": res_hist
    })

    st.line_chart(chart_df)

    # Odd Even Analysis
    odd_count = sum(1 for x in res_hist if x % 2 == 1)
    even_count = len(res_hist) - odd_count

    col_a, col_b = st.columns(2)

    with col_a:
        st.metric("ODD Count", odd_count)

    with col_b:
        st.metric("EVEN Count", even_count)

    # Big Small Percentage
    big_count = sum(1 for x in res_hist if x >= 5)
    small_count = len(res_hist) - big_count

    big_percent = round(
        (big_count / len(res_hist)) * 100,
        2
    )

    small_percent = round(
        (small_count / len(res_hist)) * 100,
        2
    )

    col_c, col_d = st.columns(2)

    with col_c:
        st.metric("BIG %", f"{big_percent}%")

    with col_d:
        st.metric("SMALL %", f"{small_percent}%")

    # Hot Numbers
    hot_numbers = sorted(
        range(10),
        key=lambda x: res_hist.count(x),
        reverse=True
    )[:3]

    st.success(
        f"🔥 Hot Numbers: {hot_numbers}"
    )

    # Cold Numbers
    cold_numbers = sorted(
        range(10),
        key=lambda x: res_hist.count(x)
    )[:3]

    st.info(
        f"❄️ Cold Numbers: {cold_numbers}"
    )

    # Current Streak
    sizes = [
        "SMALL" if x <= 4 else "BIG"
        for x in res_hist
    ]

    streak = 1

    for i in range(
        len(sizes)-1,
        0,
        -1
    ):
        if sizes[i] == sizes[i-1]:
            streak += 1
        else:
            break

    st.warning(
        f"⚡ Current Streak: {streak} {sizes[-1]}"
    )

    # Historical Accuracy
    if (
        len(st.session_state.signal_history) > 1
        and len(sizes) > 1
    ):

        wins = 0

        compare_len = min(
            len(st.session_state.signal_history)-1,
            len(sizes)-1
        )

        for i in range(compare_len):

            prediction = st.session_state.signal_history[i]
            actual = sizes[i+1]

            if prediction == actual:
                wins += 1

        accuracy = round(
            (wins / compare_len) * 100,
            2
        ) if compare_len > 0 else 0

        st.metric(
            "📌 Historical Accuracy",
            f"{accuracy}%"
        )
