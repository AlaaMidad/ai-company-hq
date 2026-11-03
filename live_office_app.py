import streamlit as st
from database import load_data, save_data
from github_upskilling import upskill_employee

st.set_page_config(page_title="Nadrai AI HQ - Live Office", layout="wide")

st.title("🏢 Nadrai HQ - Live Office (مكتب الشركة الحي)")
st.markdown("لوحة التحكم المركزية لإدارة وتطوير وكلاء الذكاء الاصطناعي.")

data = load_data()

if data:
    st.sidebar.header("⚙️ لوحة تحكم المدير التنفيذي")
    st.sidebar.text(f"حالة المديرة: {data.get('ceo_status', 'Active')}")
    
    if st.sidebar.button("🔄 إجراء جولة بحث وتطوير (GitHub Upskill)"):
        msg1 = upskill_employee(2)
        msg2 = upskill_employee(3)
        st.sidebar.success("تم تحديث مهارات الموظفين بنجاح!")
        st.rerun()

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
    st.subheader("📋 سجل المهام والأحداث")
    
    # نموذج إضافة مهمة جديدة مباشرة من الواجهة
    with st.form("new_task_form"):
        new_prompt = st.text_input("أمر أو مهمة جديدة للمدير التنفيذي:")
        submitted = st.form_submit_button("إرسال المهمة للمديرة")
        if submitted and new_prompt:
            from datetime import datetime
            new_task = {
                "task_id": len(data.get("tasks", [])) + 1,
                "prompt": new_prompt,
                "assigned_to": "Backend Python Agent",
                "status": "In Progress",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            data.setdefault("tasks", []).append(new_task)
            save_data(data)
            st.success("تم إرسال المهمة للـ CEO وتوزيعها بنجاح!")
            st.rerun()

    if data.get("tasks"):
        for t in reversed(data["tasks"]):
            st.info(f"مهمة #{t['task_id']}: {t['prompt']} — **المسؤول:** {t['assigned_to']} [{t['status']}] ({t['timestamp']})")
    else:
        st.write("لا توجد مهام نشطة حالياً.")
else:
    st.warning("جاري تحميل بيانات النظام...")