import os
from google import genai

# تهيئة عميل Gemini باستخدام مفتاح الأمان
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def run_academic_check():
    print("جاري فحص منصة الجامعة بحثاً عن تحديثات جديدة...")
    
    # مثال توضيحي لتحليل إعلان عبر الذكاء الاصطناعي
    sample_announcement = "تم تحديد موعد امتحان الذكاء الاصطناعي الأسبوع القادم يشمل الفصول من 1 إلى 4."
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=f"لخّص هذا الإعلان واستخرج المهام المطلوبة بالعربية والإنجليزية: {sample_announcement}"
    )
    print("نتيجة تحليل Gemini:")
    print(response.text)

if __name__ == "__main__":
    run_academic_check()
