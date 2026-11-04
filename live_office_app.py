import streamlit as st
import json
from database import load_data, save_data
from github_upskilling import upskill_employee
from datetime import datetime

st.set_page_config(page_title="Nadrai AI HQ - Interactive Office", layout="wide")

st.title("🏢 Nadrai HQ - مكتب الإدارة الذكي (Interactive CEO & Live Office)")
st.markdown("مكتبة الوكلاء الأذكياء: ناقش المدير التنفيذي، طوّر الأكواد، وتابع مهام فريقك على مدار الساعة.")

# تحميل البيانات الحالية من قاعدة البيانات السحابية أو المحلية
data = load_data()

if data:
    # --- الشريط الجانبي لإدارة الشركة والبحث الذاتي ---
    st.sidebar.header("⚙️ لوحة تحكم الإدارة")
    st.sidebar.text(f"حالة المديرة: {data.get('ceo_status', 'Active 🟢')}")
    
    if st.sidebar.button("🔄 جولة بحث وتطوير (GitHub Upskill)"):
        msg1 = upskill_employee(2)
        msg2 = upskill_employee(3)
        st.sidebar.success("تم تحديث مهارات الموظفين عبر GitHub!")
        st.rerun()

    # --- قسم محادثة النقاش والعصف الذهني مع المدير التنفيذي (CEO Chat) ---
    st.subheader("💬 غرفة اجتماعات ومحادثة المدير التنفيذي (CEO Brainstorming)")
    st.markdown("تحدث مع المديرة التنفيذية لمناقشة أفكار التطبيقات، هيكلة البرامج، واكتشاف الأخطاء قبل توزيعها على الفريق.")

    # تهيئة سجل المحادثة في جلسة Streamlit
    if "ceo_messages" not in st.session_state:
        st.session_state.ceo_messages = [
            {"role": "assistant", "content": "مرحباً بك يا سيد دمشق! أنا جاهزة معك اليوم لمناقشة مشاريعنا البرمجية، تحليل متطلبات الأنظمة، أو اعتماد خطط التطوير. ما الفكرة التي نعمل عليها اليوم؟"}
        ]

    # عرض رسائل المحادثة السابقة
    for message in st.session_state.ceo_messages:
        with st.chat_message(message["role"]):
        # With st.chat_message ensures proper rendering of user and assistant messages
            st.markdown(message["content"])

    # استقبال مدخلات المستخدم للمحادثة
    if user_input := st.chat_input("اطرح فكرتك، ناقش استراتيجية، أو اطلب مراجعة برمجية من المدير التنفيذي..."):
        # عرض رسالة المستخدم
        st.session_state.ceo_messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # توليد رد المديرة التنفيذية الذكي والموجه للنقاش والتنفيذ
        # يمكنك لاحقاً ربط هذا الرد بـ Claude API أو Anthropic لذكاء أصطناعي حقيقي
        if "تنفذ" in user_input or "اعتمد" in user_input or "هات" in user_input or "سوي" in user_input:
            ceo_reply = "👩‍💼 [المدير التنفيذي]: لقد استوعبت الفكرة تماماً وأتممت مناقشتها معك. بناءً على توجيهك، قمت بفتح مهمة جديدة وتوجيهها مباشرة إلى (Backend Python Agent) للتنفيذ الفوري وإضافتها لسجل الشركة!"
            
            # تسجيل المهمة أوتوماتيكياً في قاعدة البيانات
            new_task = {
                "task_id": len(data.get("tasks", [])) + 1,
                "prompt": user_input,
                "assigned_to": "Backend Python Agent",
                "status": "In Progress",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            data.setdefault("tasks", []).append(new_task)
            save_data(data)
        else:
            ceo_reply = f"👩‍💼 [المدير التنفيذي]: فكرة متميزة ورائعة! دعنا نفكر في الأبعاد التقنية لهذا الأمر: هل نعتمد استخدام قواعد بيانات Supabase أم ننشئ جداول محلية أولاً؟ ناقشني في التفاصيل، وبمجرد أن نتفق، قل لي (اعتمد المهمة) لأقوم بتوزيعها فوراً على فريق العمل."

        st.session_state.ceo_messages.append({"role": "assistant", "content": ceo_reply})
        with st.chat_message("assistant"):
            st.markdown(ceo_reply)

    st.markdown("---")

    # --- قسم حالة الموظفين والمستويات (XP & Levels) ---
    st.subheader("👥 حالة الموظفين والمستويات (XP & Levels)")
    cols = st.columns(3)
    
    def get_title(level):
        if level <= 2: return "🌱 متدرب (Trainee)"
        elif level <= 5: return "💻 موظف أول (Senior)"
        elif level <= 8: return "🛠️ خبير (Expert)"
        else: return "🔥 أسطورة (Legend)"

    for i, emp in enumerate(data.get("employees", [])):
        current_xp = emp.get("xp", 0)
        current_level = emp.get("level", 1)
        title = get_title(current_level)
        
        with cols[i % 3]:
            st.markdown(f"""
            ### {emp.get('lamp', '⚪')} {emp['name']}
            * **الدور:** {emp['role']}
            * **اللقب:** {title}
            * **المستوى:** Lv.{current_level} (XP: {current_xp})
            * **الحالة:** `{emp['status']}`
            """)
            st.progress(min(1.0, current_xp / 500.0))
            
    st.markdown("---")
    
    # --- قسم سجل المهام النشطة ---
    st.subheader("📋 سجل المهام والأحداث المسجلة في السحابة")
    if data.get("tasks"):
        for t in reversed(data["tasks"]):
            st.info(f"مهمة #{t['task_id']}: {t['prompt']} — **المسؤول:** {t['assigned_to']} [{t['status']}] ({t['timestamp']})")
    else:
        st.write("لا توجد مهام نشطة حالياً.")
else:
    st.warning("جاري تحميل بيانات النظام والاتصال بقاعدة البيانات...")
