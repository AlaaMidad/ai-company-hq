import streamlit as st
import json
import os
from database import load_data, save_data
from github_upskilling import upskill_employee
from datetime import datetime
import psycopg2

st.set_page_config(page_title="Nadrai AI HQ - Interactive Office", layout="wide")

st.title("🏢 Nadrai HQ - نظام إدارة وكلاء الذكاء الاصطناعي")
st.markdown("مكتب الإدارة الذكي، غرفة الحوار، وتتبع تقدم المهام الفريقي.")

# --- دالة الأمان للتحقق من الاتصال وعرض الحالة ---
def verify_supabase_connection():
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        try:
            if "DATABASE_URL" in st.secrets:
                db_url = st.secrets["DATABASE_URL"]
        except Exception:
            pass
            
    if db_url:
        try:
            conn = psycopg2.connect(db_url)
            conn.close()
            return True, "✅ تم بنجاح الاتصال بقاعدة البيانات السحابية (Supabase)!"
        except Exception as e:
            return False, f"⚠️ خطأ في الاتصال بقاعدة البيانات: {e}"
    else:
        return False, "⚠️ رابط قاعدة البيانات غير معرف في الإعدادات."

is_connected, status_message = verify_supabase_connection()
if is_connected:
    st.success(status_message)
else:
    st.warning(status_message)

# تحميل البيانات مع حماية كاملة من الأخطاء لمنع ظهور الصفحة البيضاء
try:
    data = load_data()
except Exception as e:
    st.error(f"حدث خطأ أثناء تحميل بيانات النظام: {e}")
    data = None

if not data:
    data = {
        "ceo_status": "Active 🟢",
        "employees": [
            {"name": "Backend Python Agent", "role": "تطوير وبناء الأكواد", "xp": 120, "level": 2, "lamp": "🟢", "status": "متاح"},
            {"name": "Code Reviewer", "role": "مراجعة وأمان الكود", "xp": 90, "level": 1, "lamp": "🟢", "status": "متاح"},
            {"name": "R&D Agent", "role": "البحث والتطوير الذاتي", "xp": 150, "level": 2, "lamp": "🟢", "status": "متاح"}
        ],
        "tasks": []
    }

# --- الشريط الجانبي لإدارة الشركة ---
st.sidebar.header("⚙️ لوحة تحكم الإدارة")
st.sidebar.text(f"حالة المديرة: {data.get('ceo_status', 'Active 🟢')}")

if st.sidebar.button("🔄 جولة بحث وتطوير (GitHub Upskill)"):
    try:
        upskill_employee(2)
        upskill_employee(3)
        st.sidebar.success("تم تحديث مهارات الموظفين عبر GitHub!")
        st.rerun()
    except Exception as ex:
        st.sidebar.error(f"تعذر التحديث: {ex}")

# --- التنقل بين الأقسام الرئيسية ---
tab1, tab2 = st.tabs(["💬 غرفة الحوار مع CEO", "📊 لوحة متابعة المهام وتفاصيل الموظفين"])

with tab1:
    st.subheader("💬 العصف الذهني ومناقشة المهام مع المدير التنفيذي")
    st.markdown("ناقش الأفكار بحرية. عندما تصلون لاتفاق، اطلب منها اعتماد المهمة لتسجيلها وحفظها.")

    if "ceo_messages" not in st.session_state:
        st.session_state.ceo_messages = [
            {"role": "assistant", "content": "مرحباً بك! أنا جاهزة لمناقشة أفكارك وتوزيع المهام البرمجية على الفريق. ما الذي سنعمل عليه اليوم؟"}
        ]

    for message in st.session_state.ceo_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_input = st.chat_input("اطرح فكرتك أو ناقش استراتيجية العمل هنا...")
    if user_input:
        st.session_state.ceo_messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        if any(word in user_input for word in ["اعتمد", "نفذ", "هات", "سوي", "ابدأ"]):
            ceo_reply = "👩‍💼 [المدير التنفيذي]: ممتاز! تم الاتفاق على هذه الخطة. قمت باعتماد المهمة، تسجيلها في السجل، وتوزيع الأدوار."
            
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
            try:
                save_data(data)
            except Exception as e:
                st.error(f"تعذر الحفظ في قاعدة البيانات: {e}")
        else:
            ceo_reply = "👩‍💼 [المدير التنفيذي]: فكرة رائعة. دعنا نحلل الجوانب التقنية أكثر: ما هي المكتبات التي سنحتاج إليها؟ بمجرد أن نتفق نهائياً، قل لي (اعتمد المهمة) لأقوم بتدوينها وتوجيه فريق العمل."

        st.session_state.ceo_messages.append({"role": "assistant", "content": ceo_reply})
        with st.chat_message("assistant"):
            st.markdown(ceo_reply)

with tab2:
    st.subheader("📊 لوحة تفاصيل المهام وسجل إنجاز الموظفين")
    st.markdown("تتبع حالة المهام المتفق عليها، والمحادثة التي أنتجتها، وماذا عمل كل موظف.")

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
                logs = t.get('employee_logs', [])
                for log in logs:
                    st.markdown(f"* **{log['agent']}:** {log['action']}")
    else:
        st.info("لا توجد مهام مسجلة حتى الآن. ابدأ الحوار مع المديرة التنفيذية في التبويب الأول!")

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
