import streamlit as st

# পেজ কনফিগারেশন
st.set_page_config(page_title="Smart Wingo Analyzer", page_icon="🤖", layout="centered")

st.title("🤖 WINGO প্রফেশনাল ট্রেন্ড ও মেমরি অ্যানালাইজার")
st.write("এই অ্যাপটি শেষ কয়েকটি পিরিয়ডের ট্রেন্ড মনে রেখে লজিক্যাল অ্যানালাইসিস তৈরি করে।")

# স্ট্রিমলিট সেশন স্টেট ব্যবহার করে ব্যাকএন্ড মেমরি তৈরি
if 'history' not in st.session_state:
    st.session_state.history = []

# ইনপুট সেকশন
st.subheader("📝 লাইভ রেজাল্ট ইনপুট দিন")
new_num_input = st.number_input("এইমাত্র আসা শেষ রেজাল্ট নম্বরটি দিন (০-৯):", min_value=0, max_value=9, value=0, step=1)

if st.button("➕ হিস্টোরিতে নম্বর যোগ করুন"):
    if len(st.session_state.history) >= 6:
        st.session_state.history.pop(0)  # সর্বোচ্চ ৬টি নম্বর মনে রাখবে
    st.session_state.history.append(new_num_input)
    st.success(f"নম্বর {new_num_input} হিস্টোরিতে সফলভাবে যোগ হয়েছে!")

# কারেন্ট হিস্টোরি প্রদর্শন
if st.session_state.history:
    st.write(f"📁 **তোমার ওয়াচ-লিস্ট হিস্টোরি (পুরাতন থেকে নতুন):** {st.session_state.history}")
else:
    st.info("হিস্টোরি বর্তমানে খালি। অন্তত ২টি বা তার বেশি নম্বর যোগ করো।")

if st.button("🗑️ হিস্টোরি সাফ করুন"):
    st.session_state.history = []
    st.experimental_rerun()

# মূল অ্যানালাইসিস লজিক
def advanced_analysis(history):
    if len(history) < 2:
        return "⚠️ অ্যানালাইসিস শুরু করতে অন্তত ২টি নম্বর হিস্টোরিতে যোগ করো।", "", "", ""
        
    old_num = history[-2]
    new_num = history[-1]
    diff = abs(old_num - new_num)
    
    # সাইজ ডিটেকশন
    sizes = ["SMALL" if n <= 4 else "BIG" for n in history]
    
    # ১. ড্রাগন ট্রেন্ড ট্র্যাকার (টানা একই সাইড আসলে)
    if len(sizes) >= 4 and len(set(sizes[-4:])) == 1:
        current_dragon = sizes[-1]
        opposite_dragon = "BIG" if current_dragon == "SMALL" else "SMALL"
        return (
            f"🚨 **ড্রাগন ট্রেন্ড অ্যালার্ট!** টানা ৪ বা তার বেশি পিরিয়ড ধরে মার্কেট {current_dragon} জোনে লক হয়ে আছে।",
            f"🎯 পরবর্তী শর্ট: {current_dragon} (ট্রেন্ড ফলো)",
            "💡 লজিক: ড্রাগন মোড সচল থাকা অবস্থায় বিপরীত দিকে যাওয়া ঝুঁকিপূর্ণ। ট্রেন্ডের গতি ফলো করাই নিরাপদ।",
            "🔢 টার্গেট সংখ্যা: ট্রেন্ডের ভেতরের যেকোনো ৩টি স্ট্রং নম্বর।"
        )

    # ২. ০ এবং ৫ স্পেশাল বর্ডারলাইন রুল
    if new_num == 0:
        return "📌 বর্ডারলাইন ডিটেক্টেড।", "🎯 পরবর্তী শর্ট: BIG", "💡 লজিক: আলটিমেট ০-রুল বর্ডার রিবাউন্ড জোন।", "🔢 টার্গেট সংখ্যা: ৫, ৭ অথবা ৯"
    if new_num == 5:
        return "📌 টার্নিং পয়েন্ট ডিটেক্টেড।", "🎯 পরবর্তী শর্ট: SMALL", "💡 লজিক: ৫-রুল আলটিমেট ফ্লিপিং ব্যালেন্সার।", "🔢 টার্গেট সংখ্যা: ০, ২ অথবা ৪"

    # ৩. সিমেট্রিক মিরর (ডাবল রিপিট)
    if diff == 0:
        next_shot = "BIG" if new_num <= 4 else "SMALL"
        logic_text = "জিরো-ডিফারেন্স ব্রেকআউট (Trend Flip)।"
        target_text = "৬, ۷ অথবা ৮" if next_shot == "BIG" else "১, ২ অথবা ৪"
        return "📌 ডাবল রিপিট লুপ ডিটেক্টেড।", f"🎯 পরবর্তী শর্ট: {next_shot}", f"💡 লজিক: {logic_text}", f"🔢 টার্গেট সংখ্যা: {target_text}"

    # ৪. হাই পার্থক্য লুপ (৬ থেকে ৯) -> রিভার্সাল
    if diff >= 6:
        next_shot = "BIG" if new_num <= 4 else "SMALL"
        target_text = "৫, ৬ অথবা ৮" if next_shot == "BIG" else "০, ২ अथवा ৪"
        return "📌 হাই পার্থক্য ভোলটাইল জอน।", f"🎯 পরবর্তী শর্ট: {next_shot}", "💡 লজিক: বড় ব্যবধানের পর মার্কেট বিপরীত জোনে রিবাউন্ড করে।", f"🔢 টার্গেট সংখ্যা: {target_text}"

    # ৫. কম পার্থক্য লুপ (১ থেকে ৪) -> কন্টিনিউয়েশন
    if diff <= 4:
        next_shot = "SMALL" if new_num <= 4 else "BIG"
        target_text = "০, ১ অথবা ২" if next_shot == "SMALL" else "৬, ৭ अथवा ৯"
        return "📌 শান্ত ও স্টেবল মার্কেট জোন।", f"🎯 পরবর্তী শর্ট: {next_shot}", "💡 লজিক: কম পার্থক্যের কারণে মার্কেট আগের ধারাবাহিকতা বজায় রাখছে।", f"🔢 টার্গেট সংখ্যা: {target_text}"

    return "⚠️ অ্যালগরিদম রিফ্রেশ মোড।", "অবজারভেশনে রাখুন।", "", ""

# ফলাফল প্রদর্শন
if len(st.session_state.history) >= 2:
    st.subheader("🔍 লাইভ অ্যানালাইসিস ফলাফল")
    status, shot, logic, targets = advanced_analysis(st.session_state.history)
    
    st.info(status)
    if shot:
        st.success(f"### {shot}")
        st.warning(logic)
        st.code(targets)
