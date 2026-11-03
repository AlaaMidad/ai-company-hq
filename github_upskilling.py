import requests
from database import load_data, save_data

def search_github_for_skills(agent_role):
    query_map = {
        "Development": "python streamlit automation framework",
        "QA & Security": "python security code review static analysis",
        "R&D": "github trending AI agents tools"
    }
    search_query = query_map.get(agent_role, "python developer tools")
    url = f"https://api.github.com/search/repositories?q={search_query}&sort=stars&order=desc"
    
    try:
        response = requests.get(url, headers={"Accept": "application/vnd.github.v3+json"}, timeout=10)
        if response.status_code == 200:
            items = response.json().get("items", [])
            if items:
                top_repo = items[0]
                return {
                    "skill_name": top_repo["name"],
                    "xp_gained": 50
                }
    except Exception:
        pass
        
    return {
        "skill_name": "Advanced-Python-Patterns",
        "xp_gained": 30
    }

def upskill_employee(employee_id):
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
        
    new_skill = search_github_for_skills(target_emp["role"])
    target_emp["xp"] = target_emp.get("xp", 0) + new_skill["xp_gained"]
    
    old_level = target_emp["level"]
    new_level = min(10, 1 + (target_emp["xp"] // 100))
    target_emp["level"] = new_level
    
    status_msg = f"🚀 [تطوير ذاتي]: الموظف ({target_emp['name']}) زار مكتبة GitHub وتعلم: '{new_skill['skill_name']}'."
    if new_level > old_level:
        status_msg += f" 🏆 **LEVEL UP!** مستوى جديد: {new_level}!"
        
    save_data(data)
    return status_msg

if __name__ == "__main__":
    print(upskill_employee(2))