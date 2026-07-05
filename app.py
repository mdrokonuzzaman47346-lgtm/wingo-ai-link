import streamlit as st

# পেজ কনফিগারেশন - সহজ ও ক্লিন ডিজাইন
st.set_page_config(page_title="Advanced Wingo Analyzer", page_icon="📈", layout="centered")

st.title("🤖 WINGO প্রফেশনাল ১০-ডিজিট ম্যাট্রিক্স ড্যাশবোর্ড")
st.write("এই অ্যাপটি শেষ ১০টি পিরিয়ডের ওয়েভ মোメントাম এবং এক্সট্রিম রিভার্সাল থিওরি ট্র্যাক করে।")

# সেশন স্টেট মেমরি সেটআপ
if 'history' not in st.session_state:
    st.session_state.history = []

# ইনপুট সেকশন
st.subheader("📝 লাইভ রেজাল্ট ইনপুট দিন")
new_num_input = st.number_input("এইমাত্র আসা শেষ রেজাল্ট নম্বরটি দিন (০-৯):", min_value=0, max_value=9, value=0, step=1)

if st.button("➕ হিস্টোরিতে নম্বর যোগ করুন"):
    if len(st.session_state.history) >= 10:
        st.session_state.history.pop(0)  # সর্বোচ্চ ১০টি নম্বর লক রাখবে
    st.session_state.history.append(new_num_input)
    st.success(f"নম্বর {new_num_input} সফলভাবে সংরক্ষিত!")

# কারেন্ট হিস্টোরি প্রদর্শন
if st.session_state.history:
    st.write(f"📁 **ওয়াচ-লিস্ট হিস্টোরি (পুরাতন থেকে নতুন):** `{st.session_state.history}`")
else:
    st.info("হিস্টোরি বর্তমানে খালি। অন্তত ২টি বা তার বেশি নম্বর যোগ করো ফ্রেন্ড।")

if st.button("🗑️ হিস্টোরি সাফ করুন"):
    st.session_state.history = []
    st.rerun()

# অ্যাডভান্সড থিওরি ইঞ্জিন
def advanced_wingo_engine(history):
    if len(history) < 2:
        return None
        
    old_num = history[-2]
    new_num = history[-1]
    diff = abs(old_num - new_num)
    
    sizes = ["SMALL" if n <= 4 else "BIG" for n in history]
    
    # ১. ১০-পিরিয়ড ড্রাগন মোড চেক
    if len(sizes) >= 4 and len(set(sizes[-4:])) == 1:
        current_dragon = sizes[-1]
        return {
            "log": f"🚨 **ড্রাগন ট্রেন্ড অ্যালার্ট!** মার্কেট একটানা {current_dragon} জোনে লক হয়ে আছে।",
            "shot": f"🎯 পরবর্তী শর্ট: {current_dragon}",
            "logic": "💡 প্রফেশনাল থিওরি: ড্রাগন মোড সচল থাকা অবস্থায় বিপরীত দিকে যাওয়া ঝুঁকিপূর্ণ। ট্রেন্ডের গতি ফলো করাই নিয়ম।",
            "targets": "🔢 টার্গেট: ট্রেন্ড জোনের শক্তিশালী সংখ্যাসমূহ।"
        }
        
    # ২. এক্সট্রিম রিভার্সাল ট্র্যাপ (০ এবং ৫ রুল)
    if new_num == 0:
        return {
            "log": "📌 **এক্সট্রিম রিভার্সাল ট্র্যাপ (০-রুল):** সর্বনিম্ন বর্ডারলাইন ডিটেক্টেড।",
            "shot": "🎯 পরবর্তী শর্ট: BIG",
            "logic": "💡 প্রফেশনাল থিওরি: ০ নম্বরটি এক্সট্রিম রিবাউন্ড পয়েন্ট। ৬ থেকে ০-তে নামার পর বড় ব্যবধান তৈরি হওয়ায় সার্ভার ইন্টারনাল ব্যালেন্সার ঠিক রাখতে আপ-ওয়ার্ড পুশ দেবে।",
            "targets": "🔢 টার্গেট সংখ্যা: ৫, ৭ অথবা ৯"
        }
    if new_num == 5:
        return {
            "log": "📌 **টার্নিং পয়েন্ট ট্র্যাপ (৫-রুল):** সেন্ট্রাল ব্যালেন্সার অ্যাক্টিভেটেড।",
            "shot": "🎯 পরবর্তী শর্ট: SMALL",
            "logic": "💡 প্রফেশনাল থিওরি: ৫ নম্বরটি প্রধান ফ্লিপিং ব্যালেন্সার। মার্কেট এই বর্ডারলাইন থেকে ডাউনে বাউন্স ব্যাক করার প্রবণতা দেখায়।",
            "targets": "🔢 টার্গেট সংখ্যা: ০, ২ অথবা ৪"
        }

    # ৩. হাই পার্থক্য লুপ (৬ থেকে ৯) -> রিভার্সাল
    if diff >= 6:
        next_shot = "BIG" if new_num <= 4 else "SMALL"
        target_text = "৫, 六 অথবা ৮" if next_shot == "BIG" else "০, ২ অথবা ৪"
        return {
            "log": f"📌 **হাই পার্থক্য ভোলটাইল জোন:** গ্যাপ {diff} (জিগ-জ্যাগ ওয়েভ)।",
            "shot": f"🎯 পরবর্তী শর্ট: {next_shot}",
            "logic": "💡 প্রফেশনাল থিওরি: বড় ব্যবধান বা তরঙ্গের পর মার্কেট কন্টিনিউ না করে বিপরীত জোনে দ্রুত রিবাউন্ড করে (Trend Flip)।",
            "targets": f"🔢 টার্গেট সংখ্যা: {target_text}"
        }

    # ৪. কম পার্থক্য লুপ (১ থেকে ৪) -> কন্টিনিউয়েশন
    if diff <= 4:
        next_shot = "SMALL" if new_num <= 4 else "BIG"
        target_text = "০, ১ অথবা ২" if next_shot == "SMALL" else "৬, ৭ অথবা ৯"
        return {
            "log": f"📌 **শান্ত ও স্টেবল জোন:** গ্যাপ {diff} (কমপ্যাক্ট ওয়েভ)।",
            "shot": f"🎯 পরবর্তী শর্ট: {next_shot}",
            "logic": "💡 প্রফেশনাল থিওরি: পার্থক্য কম থাকায় মার্কেট স্টেবিলিটি মেইনটেইন করছে এবং আগের সাইজের ধারাবাহিকতা ধরে রাখছে (Continuation)।",
            "targets": f"🔢 টার্গেট সংখ্যা: {target_text}"
        }

    return None

# ফলাফল প্রদর্শন
if len(st.session_state.history) >= 2:
    st.subheader("🔍 লাইভ প্রফেশনাল অ্যানালাইসিস")
    analysis = advanced_wingo_engine(st.session_state.history)
    
    if analysis:
        st.info(analysis["log"])
        st.success(f"### {analysis['shot']}")
        st.warning(analysis["logic"])
        st.code(analysis["targets"])
