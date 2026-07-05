import streamlit as st

# পেজ কনফিগারেশন
st.set_page_config(page_title="Wingo Analyzer", page_icon="🤖", layout="centered")

st.title("🤖 WINGO ১-মিনিট অ্যালগরিদম অ্যানালাইজার")
st.write("তোমার ওল্ড এবং নিউ নম্বর দুটি বসিয়ে নিচের অ্যানালাইসিস বাটনে ক্লিক করো।")

def analyze_wingo(old_num, new_num):
    old_type = "Even" if old_num % 2 == 0 else "Odd"
    new_type = "Even" if new_num % 2 == 0 else "Odd"
    diff = abs(old_num - new_num)
    
    analysis_details = f"""
    📊 **কারেন্ট ম্যাট্রিক্স লগ:**
    * ওল্ড নম্বর: **{old_num}** ({old_type})
    * নিউ নম্বর: **{new_num}** ({new_type})
    * গাণিতিক পার্থক্য: **{diff}**
    """
    
    # ১. সিমেট্রিক মিরর লুপ (ডাবল রিপিট রুল)
    if diff == 0:
        if new_num in:
            return analysis_details, "🎯 পরবর্তী শট: BIG", "💡 লজিক: জিরো-ডিফারেন্স ব্রেকআউট (Trend Flip)।", "🔢 টার্গেট সংখ্যা: ৬, ৭ অথবা ৮"
        else:
            return analysis_details, "🎯 পরবর্তী শট: SMALL", "💡 লজিক: সিমেট্রিক মিরর ট্রেন্ড ফ্লিপ (Trend Flip)।", "🔢 টার্গেট সংখ্যা: ১, ২ অথবা ৪"
            
    # ২. ০ এবং ৫-এর স্পেশাল টার্নিং পয়েন্ট রুল
    if new_num == 0:
        return analysis_details, "🎯 পরবর্তী শট: BIG", "💡 লজিক: আলটিমেট ০-রুল বর্ডার রিবাউন্ড।", "🔢 টার্গেট সংখ্যা: ৫, ৭ অথবা ৯"
    if new_num == 5:
        return analysis_details, "🎯 পরবর্তী শট: SMALL", "💡 লজিক: ৫-রুল আলটিমেট ফ্লিপিং পয়েন্ট।", "🔢 টার্গেট সংখ্যা: ০, ২ অথবা ৪"

    # ৩. হাই পার্থক্য লুপ (৬, ۷, ৮, ৯) -> ফ্লিপ/রিভার্সাল ট্রেন্ড
    if diff >= 6:
        if new_num in:
            return analysis_details, "🎯 পরবর্তী শট: BIG", "💡 লজিক: হাই পার্থক্য রিভার্সাল সাইকেল।", "🔢 টার্গেট সংখ্যা: ৫, ৬ অথবা ৮"
        else:
            return analysis_details, "🎯 পরবর্তী শট: SMALL", "💡 লজিক: হাই পার্থক্য ভোলটাইল জোন ফ্লিপ।", "🔢 টার্গেট সংখ্যা: ০, ২ অথবা ৪"

    # ৪. কম পার্থক্য লুপ (১, ২, ৩, ৪) -> কন্টিনিউয়েশন ট্রেন্ড
    if diff <= 4:
        if new_num in:
            if old_type == "Even" and new_type == "Even":
                return analysis_details, "🎯 পরবর্তী শট: SMALL", "💡 লজিক: [Even + Even] লুপে বিজোড় স্মল কন্টিনিউয়েশন।", "🔢 টার্গেট সংখ্যা: ১ অথবা ৩"
            return analysis_details, "🎯 পরবর্তী শট: SMALL", "💡 লজিক: কম পার্থক্য স্মল জোন ধারাবাহিকতা (Continuation)।", "🔢 টার্গেট সংখ্যা: ০, ১ অথবা ২"
        else:
            if old_type == "Even" and new_type == "Even":
                return analysis_details, "🎯 পরবর্তী শট: BIG", "💡 লজিক: [Even + Even] লুপে বিজোড় বিগ কন্টিনিউয়েশন।", "🔢 টার্গেট সংখ্যা: ৭ অথবা ৯"
            return analysis_details, "🎯 পরবর্তী শট: BIG", "💡 লজিক: কম পার্থক্য বিগ জোন ধারাবাহিকতা (Continuation)।", "🔢 টার্গেট সংখ্যা: ৬, ৭ অথবা ৯"

    return analysis_details, "⚠️ অ্যালগরিদম রিফ্রেশ মোড।", "অবজারভেশনে রাখুন।", ""

# ইউজার ইনপুট ইন্টারফেস
old_input = st.number_input("➡️ ওল্ড নম্বরটি দাও (০-৯):", min_value=0, max_value=9, value=0, step=1)
new_input = st.number_input("➡️ নিউ নম্বরটি দাও (০-৯):", min_value=0, max_value=9, value=0, step=1)

if st.button("🔍 রান অ্যানালাইসিস"):
    log_data, shot, logic, targets = analyze_wingo(old_input, new_input)
    
    st.info(log_data)
    st.success(f"### {shot}")
    st.warning(logic)
    st.code(targets)
    
