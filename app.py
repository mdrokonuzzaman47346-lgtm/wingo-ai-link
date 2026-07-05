def analyze_wingo(old_num, new_num):
    # সংখ্যা দুটি জোড় নাকি বিজোড় তা বের করা
    old_type = "Even" if old_num % 2 == 0 else "Odd"
    new_type = "Even" if new_num % 2 == 0 else "Odd"
    
    # ডিফারেন্স ট্র্যাপ (পার্থক্য বের করা)
    diff = abs(old_num - new_num)
    
    print("\n" + "="*40)
    print(f"📊 কারেন্ট ম্যাট্রিক্স লগ:")
    print(f"• ওল্ড নম্বর: {old_num} ({old_type})")
    print(f"• নিউ নম্বর: {new_num} ({new_type})")
    print(f"• গাণিতিক পার্থক্য: {diff}")
    print("="*40)
    
    # ১. সিমেট্রিক মিরর লুপ (ডাবল রিপিট রুল)
    if diff == 0:
        if new_num in:
            return "🎯 পরবর্তী শট: BIG \n💡 লজিক: জিরো-ডিফারেন্স ব্রেকআউট (Trend Flip)।\n🔢 টার্গেট সংখ্যা: ৬, ৭ অথবা ৮"
        else:
            return "🎯 পরবর্তী শট: SMALL \n💡 লজিক: সিমেট্রিক মিরর ট্রেন্ড ফ্লিপ (Trend Flip)।\n🔢 টার্গেট সংখ্যা: ১, ২ অথবা ৪"
            
    # ২. ০ এবং ৫-এর স্পেশাল টার্নিং পয়েন্ট রুল
    if new_num == 0:
        return "🎯 পরবর্তী শট: BIG \n💡 লজিক: আলটিমেট ০-রুল বর্ডার রিবাউন্ড।\n🔢 টার্গেট সংখ্যা: ৫, ৭ অথবা ৯"
    if new_num == 5:
        return "🎯 পরবর্তী শট: SMALL \n💡 লজিক: ৫-রুল আলটিমেট ফ্লিপিং পয়েন্ট।\n🔢 টার্গেট সংখ্যা: ০, ২ অথবা ৪"

    # ৩. হাই পার্থক্য লুপ (৬, ৭, ৮, ৯) -> ফ্লিপ/রিভার্সাল ট্রেন্ড
    if diff >= 6:
        if new_num in: # নিউ যদি স্মল হয়, তবে বিগে ফ্লিপ করবে
            target_nums = "৫, ৭ অথবা ৮" if diff == 7 else "০, ২ অথবা ৪"
            if old_num == 3 and new_num == Raw_Data: # কাস্টম ওড লুপ চেক
                target_nums = "০, ২ অথবা ৪"
            return f"🎯 পরবর্তী শট: BIG \n💡 লজিক: হাই পার্থক্য রিভার্সাল সাইকেল।\n🔢 টার্গেট সংখ্যা: ৫, ৬ অথবা ৮"
        else: # নিউ যদি বিগ হয়, তবে স্মলে ফ্লিপ করবে
            return f"🎯 পরবর্তী শট: SMALL \n💡 লজিক: হাই পার্থক্য ভোলটাইল জোন ফ্লিপ।\n🔢 টার্গেট সংখ্যা: ০, ২ অথবা ৪"

    # ৪. কম পার্থক্য লুপ (১, ২, ৩, ৪) -> কন্টিনিউয়েশন ট্রেন্ড
    if diff <= 4:
        if new_num in: # স্মল কন্টিনিউয়েশন
            if old_type == "Even" and new_type == "Even":
                return "🎯 পরবর্তী শট: SMALL \n💡 লজিক: [Even + Even] লুপে বিজোড় স্মল কন্টিনিউয়েশন।\n🔢 টার্গেট সংখ্যা: ১ অথবা ৩"
            return "🎯 পরবর্তী শট: SMALL \n💡 লজিক: কম পার্থক্য স্মল জোন ধারাবাহিকতা (Continuation)।\n🔢 টার্গেট সংখ্যা: ০, ১ অথবা ২"
        else: # বিগ কন্টিনিউয়েশন
            if old_type == "Even" and new_type == "Even":
                return "🎯 পরবর্তী শট: BIG \n💡 লজিক: [Even + Even] লুপে বিজোড় বিগ কন্টিনিউয়েশন।\n🔢 টার্গেট সংখ্যা: ৭ অথবা ৯"
            return "🎯 পরবর্তী শট: BIG \n💡 লজিক: কম পার্থক্য বিগ জোন ধারাবাহিকতা (Continuation)।\n🔢 টার্গেট সংখ্যা: ৬, ৭ অথবা ৯"

    return "⚠️ অ্যালগরিদম রিফ্রেশ মোড। অবজারভেশনে রাখুন।"

# লাইভ ইনপুট লুপ
if __name__ == "__main__":
    print("🤖 WINGO ১-মিনিট অ্যালগরিদম অ্যানালাইজার অনলাইন্ড...")
    while True:
        try:
            old_input = int(input("\n➡️ ওল্ড নম্বরটি দিন (০-৯) [অথবা বন্ধ করতে Ctrl+C চাপুন]: "))
            new_input = int(input("➡️ নিউ নম্বরটি দিন (০-৯): "))
            
            if old_input not in range(10) or new_input not in range(10):
                print("❌ ভুল ইনপুট! দয়া করে শুধু ০ থেকে <b style='color:red;'>৯</b> এর মধ্যে সংখ্যা দিন।")
                continue
                
            result = analyze_wingo(old_input, new_input)
            print(result)
            print("="*40)
        except KeyboardInterrupt:
            print("\n👋 অ্যানালাইজার বন্ধ করা হয়েছে। ভালো থাকো ফ্রেন্ড!")
            break
        except ValueError:
            print("❌ দয়া করে একটি সঠিক সংখ্যা ইনপুট দিন।")
            
