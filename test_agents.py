import json
from database import load_data, save_data

def evaluate_agent_performance(employee_id, test_passed: bool):
    """
    يقوم باختبار الموظف: إذا نجح في الاختبار يحصل على XP وترتفع ثقته،
    وإذا فشل ينخفض رصيده ليعكس مستواه الحقيقي.
    """
    data = load_data()
    if not data:
        return "بيانات الشركة غير موجودة."
        
    target_emp = None
    for emp in data.get("employees", []):
        if emp["id"] == employee_id:
            target_emp = emp
            break
            
    if not target_emp:
        return "الموظف غير موجود."
        
    current_xp = target_emp.get("xp", 0)
    
    if test_passed:
        xp_change = 40
        result_msg = f"✅ اجتاز الموظف ({target_emp['name']}) اختبار الأداء بنجاح! تم إضافة {xp_change} XP."
    else:
        xp_change = -20
        result_msg = f"❌ فشل الموظف ({target_emp['name']}) في اختبار الأداء. تم خصم {abs(xp_change)} XP."
        
    # تحديث النقاط وضمان عدم نزولها تحت الصفر
    target_emp["xp"] = max(0, current_xp + xp_change)
    
    # تحديث المستوى بناءً على الـ XP الجديد (كل 100 نقطة مستوى)
    target_emp["level"] = min(10, max(1, 1 + (target_emp["xp"] // 100)))
    
    save_data(data)
    return result_msg

if __name__ == "__main__":
    # مثال: اختبار الموظف رقم 2 (مطور البايثون) واجتيازه للاختبار
    print(evaluate_agent_performance(2, test_passed=True))