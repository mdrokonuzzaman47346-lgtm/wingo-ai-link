import streamlit as st
import pandas as pd

# পেজ কনফিগারেশন
st.set_page_config(page_title="Professional Wingo Dashboard", page_icon="📈", layout="centered")

st.title("📈 WINGO প্রফেশনাল রিস্ক ও ট্রেন্ড ড্যাশবোর্ড")
st.write("মেমরি লুপ, মার্টিনগেল প্রোটেকশন এবং লাইভ রিস্ক ম্যানেজমেন্ট ড্যাশবোর্ড।")

# সেশন স্টেট মেমরি সেটআপ
if 'history' not in st.session_state:
    st.session_state.history = []
if 'level' not in st.session_state:
    st.session_state.level = 1

# রিস্ক ম্যানেজমেন্ট প্যানেল (Sidebar)
st.sidebar.header("🛡️ ক্যাপিটাল শিল্ড কন্ট্রোল")
base_bet = st.sidebar.number_input("বেস বেট অ্যামাউন্ট (BDT):", min_value=10, value=10, step=10)

# মার্টিনগেল হিসাব
level_multipliers = [1, 3, 9, 27, 81]
current_bet = base_bet * level_multipliers[st.session_state.level - 1]

st.sidebar.metric(label="🔄 কারেন্ট রিকভারি লেভেল", value=f"Level {st.session_state.level}")
st.sidebar.metric(label="💰 অনুমিত বেট অ্যামাউন্ট", value=f"{current_bet} BDT")

# ইনপুট সেকশন
st.subheader("📝 লাইভ পিরিয়ড রেজাল্ট")
new_num_input = st.number_input("শেষ রেজাল্ট নম্বরটি দাও (০-৯):", min_value=0, max_value=9, value=0, step=1)

col1, col2 = st.columns(2)
with col1:
    if st.button("➕ নম্বর যোগ করুন"):
        if len(st.session_state.history) >= 10:
            st.session_state.history.pop(0)
        st.session_state.history.append(new_num_input)
        st.success(f"নম্বর {new_num_input} লগে সংরক্ষিত!")
with col2:
    if st.button("🗑️ ড্যাশবোর্ড রিসেট"):
        st.session_state.history = []
        st.session_state.level = 1
        st.rerun()

# লাইভ ডাটা ও গ্রাফ প্রদর্শন
if st.session_state.history:
    st.write(f"📁 **ওয়াচ-লিস্ট লগ (পুরাতন ➔ নতুন):** {st.session_state.history}")
    
    # ভিজুয়াল চার্ট তৈরি
    chart_data = pd.DataFrame({"নম্বর": st.session_state.history})
    st.line_chart(chart_data)
else:
    st.info("হিস্টোরি খালি। ডাটা ইনপুট দেওয়া শুরু করো ফ্রেন্ড।")

# মূল প্রফেশনাল লজিক
def professional_analysis(history):
    if len(history) < 2:
        return "⚠️ অন্তত ২টি নম্বর ইনপুট দাও।", "", "", ""
        
    old_num = history[-2]
    new_num = history[-1]
    diff = abs(old_num - new_num)
    sizes = ["SMALL" if n <= 4 else "BIG" for n in history]
    
    # ১. ড্রাগন মোড প্রোটেকশন
    if len(sizes) >= 4 and len(set(sizes[-4:])) == 1:
        return (
            f"🚨 **সতর্কতা: ড্রাগন ট্রেন্ড চলমান!**",
            f"🎯 পরবর্তী শর্ট: {sizes[-1]}",
            "💡 প্রফেশনাল রুল: ড্রাগন ট্রেন্ডের বিপরীতে বাজি ধরা সম্পূর্ণ নিষিদ্ধ। ট্রেন্ড ফলো করাই নিয়ম।",
            "🔢 টার্গেট সংখ্যা: ট্রেন্ড জোনের শক্তিশালী সংখ্যাগুলো।"
        )
        
    # ২. ০ এবং ৫ স্পেশাল রিবাউন্ড
    if new_num == 0:
        return "📌 ০-বর্ডার রিবাউন্ড সিগন্যাল।", "🎯 পরবর্তী শর্ট: BIG", "💡 লজিক: এক্সট্রিম ডাউন জোন থেকে মার্কেট আপ-জোনে বাউন্স ব্যাক করে।", "🔢 টার্গেট সংখ্যা: ৫, ৭ অথবা ৯"
    if new_num == 5:
        return "📌 ৫-টার্নিং পয়েন্ট সিগন্যাল।", "🎯 পরবর্তী শর্ট: SMALL", "💡 লজিক: ৫ নম্বরটি অ্যালগরিদমের অন্যতম প্রধান ফ্লিপিং ব্যালেন্সার।", "🔢 টার্গেট সংখ্যা: ০, ২ অথবা ৪"

    # ৩. হাই পার্থক্য লুপ (রিভার্সাল)
    if diff >= 6:
        next_shot = "BIG" if new_num <= 4 else "SMALL"
        targets = "৫, ৬ অথবা ৮" if next_shot == "BIG" else "০, ২ অথবা ৪"
        return "📌 হাই পার্থক্য (ভোলটাইল মার্কেট)।", f"🎯 পরবর্তী শর্ট: {next_shot}", "💡 লজিক: বড় গ্যাপ তৈরি হওয়ার পর সার্ভার দ্রুত বিপরীত জোনে শিফট করে।", f"🔢 টার্গেট সংখ্যা: {targets}"

    # ৪. কম পার্থক্য লুপ (কন্টিনিউয়েশন)
    if diff <= 4:
        next_shot = "SMALL" if new_num <= 4 else "BIG"
        targets = "০, ১ অথবা ২" if next_shot == "SMALL" else "৬, ৭ অথবা ৯"
        return "📌 কম পার্থক্য (স্টেবল মার্কেট)।", f"🎯 পরবর্তী শর্ট: {next_shot}", "💡 লজিক: মার্কেট শান্ত থাকায় আগের পিরিয়ডের সাইজ ধারাবাহিকতা বজায় রাখছে।", f"🔢 টার্গেট সংখ্যা: {targets}"

    return "⚠️ মার্কেট পর্যবেক্ষণ মোড।", "স্কিপ করুন।", "", ""

# ফলাফল ও লেভেল কন্ট্রোল বাটন
if len(st.session_state.history) >= 2:
    st.subheader("🔍 লাইভ অ্যানালাইসিস ফলাফল")
    status, shot, logic, targets = professional_analysis(st.session_state.history)
    
    st.info(status)
    if shot:
        st.success(f"### {shot}")
        st.warning(logic)
        st.code(targets)
        
        # লেভেল আপ/ডাউন বাটন
        st.write("📊 **এই শটের ফলাফল কী এলো?**")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("✅ WIN (লেভেল ১ রিসেট)"):
                st.session_state.level = 1
                st.rerun()
        with c2:
            if st.button("❌ MISS (পরবর্তী লেভেল)"):
                if st.session_state.level < 5:
                    st.session_state.level += 1
                else:
                    st.error("🚨 লেভেল ৫ ডেফিসিট! ৩ পিরিয়ড স্কিপ করে রিসেট করো।")
                    st.session_state.level = 1
                st.rerun()
