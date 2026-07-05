import streamlit as st

# পেজ কনফিগারেশন - একদম সহজ ও ক্লিন রাখার জন্য
st.set_page_config(page_title="Wingo Analyzer", page_icon="🤖", layout="centered")

st.title("🤖 WINGO ১-মিনিট অ্যালগরিদম অ্যানালাইজার")
st.write("তোমার ওল্ড এবং নিউ নম্বর দুটি বসিয়ে নিচের অ্যানালাইসিস বাটনে ক্লিক করো।")

# স্ট্রিমলিট সেশন স্টেট মেমরি - এবার এটি লাস্ট ১০টি রেজাল্ট মনে রাখবে
if 'history' not in st.session_state:
    st.session_state.history = []

# ইনপুট সেকশন
st.subheader("📝 লাইভ রেজাল্ট ইনপুট দিন")
new_num_input = st.number_input("এইমাত্র আসা শেষ রেজাল্ট নম্বরটি দিন (০-৯):", min_value=0, max_value=9, value=0, step=1)

if st.button("➕ হিস্টোরিতে নম্বর যোগ করুন"):
    if len(st.session_state.history) >= 10:
        st.session_state.history.pop(0)  # সর্বোচ্চ ১০টি নম্বর মনে রাখবে (৬টি থেকে বাড়িয়ে ১০টি করা হলো)
    st.session_state.history.append(new_num_input)
    st.success(f"নম্বর {new_num_input} হিস্টোরিতে সফলভাবে যোগ হয়েছে!")

# কারেন্ট হিস্টোরি প্রদর্শন
if st.session_state.history:
    st.write(f"📁 **তোমার ওয়াচ-লিস্ট হিস্টোরি (পুরাতন থেকে নতুন):** {st.session_state.history}")
else:
    st.info("হিস্টোরি বর্তমানে খালি। অন্তত ২টি বা তার বেশি নম্বর যোগ করো।")

if st.button("🗑️ হিস্টোরি সাফ করুন"):
    st.session_state.history = []
    st.rerun()

# মূল অ্যানালাইসিস লজিক (যা তুমি স্ক্রিনশটে চেয়েছ)
def analyze_wingo(history):
    if len(history) < 2:
        return "⚠️ অ্যানালাইসিস শুরু করতে অন্তত ২টি নম্বর হিস্টোরিতে যোগ করো।", "", "", ""
        
    old_num = history[-2]
    new_num = history[-1]
    diff = abs(old_num - new_num)
    
    # সাইজ ট্র্যাকার (SMALL = ০-৪, BIG = ৫-৯)
    sizes = ["SMALL" if n <= 4 else "BIG" for n in history]
    
    analysis_details = f"""
    📊 **কারেন্ট ম্যাট্রিক্স লগ:**
    * ওল্ড নম্বর: **{old_num}**
    * নিউ নম্বর: **{new_num}**
    * গাণিতিক পার্থক্য: **{diff}**
    """
    
    # ১. ড্রাগন ট্রেন্ড ট্র্যাকার (টানা একই সাইড আসলে)
    if len(sizes) >= 4 and len(set(sizes[-4:])) == 1:
        current_dragon = sizes[-1]
        return (
            analysis_details,
            f"🎯 পরবর্তী শর্ট: {current_dragon}",
            f"💡 লজিক: ড্রাগন ট্রেন্ড অ্যালার্ট! টানা ৪ বা তার বেশি পিরিয়ড ধরে মার্কেট {current_dragon} জোনে লক হয়ে আছে। ট্রেন্ড ফলো করাই নিরাপদ।",
            "🔢 টার্গেট সংখ্যা: ট্রেন্ড জোনের যেকোনো ৩টি স্ট্রং নম্বর।"
        )
    
    # ২. সিমেট্রিক মিরর লুপ (ডাবল রিপিট রুল)
    if diff == 0:
        if new_num == 5 or new_num == 6 or new_num == 7 or new_num == 8 or new_num == 9:
            return analysis_details, "🎯 পরবর্তী শর্ট: BIG", "💡 লজিক: জিরো-ডিফারেন্স ব্রেকআউট (Trend Flip)।", "🔢 টার্গেট সংখ্যা: ৬, ৭ অথবা ৮"
        else:
            return analysis_details, "🎯 পরবর্তী শর্ট: SMALL", "💡 লজিক: সিমেট্রিক মিরর ট্রেন্ড ফ্লিপ (Trend Flip)।", "🔢 টার্গেট সংখ্যা: ১, ২ অথবা ৪"
            
    # ৩. ০ এবং ৫-এর স্পেশাল টার্নিং পয়েন্ট রুল
    if new_num == 0:
        return analysis_details, "🎯 পরবর্তী শর্ট: BIG", "💡 লজিক: আলটিমেট ০-রুল বর্ডার রিবাউন্ড।", "🔢 টার্গেট সংখ্যা: ৫, ৭ অথবা ৯"
    if new_num == 5:
        return analysis_details, "🎯 পরবর্তী শর্ট: SMALL", "💡 লজিক: ৫-রুল আলটিমেট ফ্লিপিং পয়েন্ট।", "🔢 টার্গেট সংখ্যা: ০, ২ অথবা ৪"

    # ৪. হাই পার্থক্য লুপ (৬, ৭, ৮, ৯) -> ফ্লিপ/রিভার্সাল ট্রেন্ড
    if diff >= 6:
        if new_num == 0 or new_num == 1 or new_num == 2 or new_num == 3 or new_num == 4:
            return analysis_details, "🎯 পরবর্তী শর্ট: BIG", "💡 লজিক: বড় ব্যবধানের পর মার্কেট বিপরীত জোনে রিবাউন্ড করে (Reverse)।", "🔢 টার্গেট সংখ্যা: ৫, ৬ অথবা ৮"
        else:
            return analysis_details, "🎯 পরবর্তী শর্ট: SMALL", "💡 লজিক: হাই পার্থক্য ভোলটাইল জোন ফ্লিপ (Reverse)।", "🔢 টার্গেট সংখ্যা: ০, ২ অথবা ৪"

    # ৫. কম পার্থক্য লুপ (১, ২, ৩, ৪) -> কন্টিনিউয়েশন ট্রেন্ড
    if diff <= 4:
        if new_num == 0 or new_num == 1 or new_num == 2 or new_num == 3 or new_num == 4:
            return analysis_details, "🎯 পরবর্তী শর্ট: SMALL", "💡 লজিক: কম পার্থক্য হওয়ার কারণে মার্কেট আগের ধারাবাহিকতা বজায় রাখছে (Continuation)।", "🔢 টার্গেট সংখ্যা: ০, ১ অথবা ২"
        else:
            return analysis_details, "🎯 পরবর্তী শর্ট: BIG", "💡 লজিক: কম পার্থক্য হওয়ার কারণে মার্কেট আগের ধারাবাহিকতা বজায় রাখছে (Continuation)।", "🔢 টার্গেট সংখ্যা: ৬, ৭ অথবা ৯"

    return analysis_details, "⚠️ অ্যালগরিদম রিফ্রেশ মোড।", "অবজারভেশনে রাখুন।", ""

# ফলাফল প্রদর্শন সেকশন (তোমার স্ক্রিনশটের মতো সুন্দর বক্স ডিজাইন)
if len(st.session_state.history) >= 2:
    st.subheader("🔍 লাইভ অ্যানালাইসিস ফলাফল")
    log_data, shot, logic, targets = analyze_wingo(st.session_state.history)
    
    st.info(log_data)
    if shot:
        st.success(f"### {shot}")
        st.warning(logic)
        st.code(targets)
