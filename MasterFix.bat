@echo off
echo 🛠️ প্রফেসর ফয়সাল, আপনার সিস্টেম পাথ ফিক্স করা হচ্ছে...

:: পাইথন এবং স্ক্রিপ্ট পাথ সেট করা
setx PATH "%PATH%;C:\Users\Admin\AppData\Local\Python\pythoncore-3.14-64\Scripts;C:\Users\Admin\AppData\Local\Python\pythoncore-3.14-64" /M

:: লাইব্রেরিগুলো আপডেট এবং ইন্সটল করা
C:\Users\Admin\AppData\Local\Python\pythoncore-3.14-64\python.exe -m pip install -U google-generativeai pandas streamlit cryptography

echo ✅ অভিনন্দন! আপনার সিস্টেম এখন রেডি। 
echo 🚀 এখন আপনি 'streamlit run note.py' দিয়ে অ্যাপটি চালাতে পারবেন।
pause