import streamlit as st
import json
from database import load_data, save_data
from github_upskilling import upskill_employee
from datetime import datetime

st.set_page_config(page_title="Nadrai AI HQ - Interactive Office", layout="wide")

st.title("🏢 Nadrai HQ - نظام إدارة وكلاء الذكاء الاصطناعي")
st.markdown("مكتب الإدارة الذكي، غرفة الحوار، وتتبع تقدم المهام الفريقي.")

# تحميل البيانات من قاعدة البيانات السحابية (Supabase) أو المحلية
data = load_data()

if data:
    # --- الشريط الجانبي لإدارة الشركة ---
    st.sidebar.header("⚙️ لوحة تحكم الإدارة")
    st.sidebar.text(f"حالة المديرة: {data.get('ceo_status', 'Active 🟢')}")
    
    if st.sidebar.button("🔄 جولة بحث وتطوير (GitHub Upskill)"):
        upskill_employee(2)
        upskill_employee(3)
        st.sidebar.success("تم تحديث مهارات الموظفين عبر GitHub!")
        st.rerun()

    # --- التنقل بين الأقسام الرئيسية ---
    tab1, tab2 = st.tabs(["💬 غرفة الحوار مع CEO", "📊 لوحة متابعة المهام وتفاصيل الموظفين"])

    with tab1:
        st.subheader("💬 العصف الذهني ومناقشة المهام مع المدير التنفيذي")
        st.markdown("ناقش الأفكار بحرية. عندما تصلون لاتفاق، اطلب منها اعتماد المهمة لتسجيلها وإرسالها للفريق.")

        # تهيئة سجل المحادثة
        if "ceo_messages" not in st.session_state:
            st.session_state.ceo_messages = [
                {"role": "assistant", "content": "مرحباً بك! أنا جاهزة لمناقشة أفكارك وتوزيع المهام البرمجية على الفريق. ما الذي سنعمل عليه اليوم؟"}
            ]

        # عرض الرسائل بطريقة آمنة
        for message in st.session_state.ceo_messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # استخدام st.chat_input بشكل مباشر وصحيح لتجنب أخطاء الاستيراد الديناميكي
        user_input = st.chat_input("اطرح فكرتك أو ناقش استراتيجية العمل هنا...")
        if user_input:
            st.session_state.ceo_messages.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.markdown(user_input)

            # صياغة رد المديرة الذكي
            if any(word in user_input for word in ["اعتمد", "نفذ", "هات", "سوي", "ابدأ"]):
                ceo_reply = "👩‍💼 [المدير التنفيذي]: ممتاز! تم الاتفاق على هذه الخطة. قمت باعتماد المهمة، تسجيلها في السجل السحابي، وتوزيع الأدوار على الموظفين المختصين."
                
                # تجميع سياق المحادثة الأخيرة لتخزينها كمرجع للمهمة
                chat_history_snippet = " \n".join([f"{m['role']}: {m['content']}" for m in st.session_state.ceo_messages[-4:]])
                
                new_task = {
                    "task_id": len(data.get("tasks", [])) + 1,
                    "prompt": user_input,
                    "discussion_context": chat_history_snippet,
                    "assigned_to": "Backend Python Agent & Code Reviewer",
                    "status": "قيد التنفيذ (In Progress)",
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "employee_logs": [
                        {"agent": "CEO Agent", "action": "تخطيط وتحليل المتطلبات واعتماد الفكرة."},
                        {"agent": "Backend Python Agent", "action": "كتابة الأكواد وتجهيز الهيكل البرمجي."},
                        {"agent": "Code Reviewer Agent", "action": "مراجعة الأمان وجودة الكود بانتظار الاختبار النهائي."}
                    ]
                }
                data.setdefault("tasks", []).append(new_task)
                save_data(data)
            else:
                ceo_reply = "👩‍💼 [المدير التنفيذي]: فكرة رائعة ودقيقة. دعنا نحلل الجوانب التقنية أكثر: ما هي المكتبات أو الجداول التي سنحتاج إليها؟ بمجرد أن نتفق نهائياً، قل لي (اعتمد المهمة) لأقوم بتدوينها وتوجيه فريق العمل فوراً."

            st.session_state.ceo_messages.append({"role": "assistant", "content": ceo_reply})
            with st.chat_message("assistant"):
                st.markdown(ceo_reply)

    with tab2:
        st.subheader("📊 لوحة تفاصيل المهام وسجل إنجاز الموظفين")
        st.markdown("تتبع حالة المهام المتفق عليها، المحادثة التي أنتجتها، وماذا عمل كل موظف فيها.")

        tasks = data.get("tasks", [])
        if tasks:
            for t in reversed(tasks):
                with st.expander(f"📌 مهمة #{t['task_id']}: {t['prompt']} — الحالة: [{t['status']}]"):
                    st.markdown(f"**⏰ وقت الإنشاء:** {t.get('timestamp', 'غير محدد')}")
                    st.markdown(f"**👤 المسؤول الرئيسي:** {t.get('assigned_to', 'غير محدد')}")
                    
                    st.markdown("---")
                    st.markdown("#### 💬 المحادثة والنقاش الذي أدى إلى هذه المهمة:")
                    st.info(t.get('discussion_context', 'لا توجد تفاصيل محادثة مسجلة.'))
                    
                    st.markdown("---")
                    st.markdown("#### 🛠️ ما ماذا عمل كل موظف في هذه المهمة؟")
                    logs = t.get('employee_logs', [
                        {"agent": "CEO Agent", "action": "استلام الطلب وتوجيهه."},
                        {"agent": "Backend Python Agent", "action": "جاري المعالجة والبرمجة."}
                    ])
                    for log in logs:
                        st.markdown(f"* **{log['agent']}:** {log['action']}")
        else:
            st.info("لا توجد مهام مسجلة حتى الآن. ابدأ الحوار مع المديرة التنفيذية في التبويب الأول وأنشئ مهمتك الأولى!")

        st.markdown("---")
        st.subheader("👥 مستويات الموظفين ونقاط الخبرة (XP & Levels)")
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
else:
    st.warning("جاري تحميل بيانات النظام والاتصال بقاعدة البيانات السحابية...")
