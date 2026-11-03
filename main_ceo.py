from datetime import datetime
from database import load_data, save_data

def give_task_to_ceo(user_prompt):
    data = load_data()
    if not data:
        print("خطأ في تحميل بيانات الشركة.")
        return
        
    new_task = {
        "task_id": len(data.get("tasks", [])) + 1,
        "prompt": user_prompt,
        "assigned_to": "Backend Python Agent",
        "status": "In Progress",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    
    data["tasks"].append(new_task)
    
    for emp in data.get("employees", []):
        if emp["name"] == new_task["assigned_to"]:
            emp["status"] = "Working"
            emp["lamp"] = "🟢"

    save_data(data)
    print(f"👩‍💼 [المدير التنفيذي]: تم استلام المهمة بنجاح وتوجيهها إلى ({new_task['assigned_to']}).")

if __name__ == "__main__":
    task_input = input("أدخل المهمة البرمجية للمدير التنفيذي: ")
    give_task_to_ceo(task_input)