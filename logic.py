from data_models import (
    GRADE_RANGES_OPERATIVES, 
    GRADE_RANGES_ADMIN, 
    GRADE_RANGES_RF_OPERATIVES, 
    GRADE_RANGES_RF_ADMIN
)

def calculate_total_points(selected_levels):
    """
    selected_levels: dict of {factor_name: points}
    Returns: total points (float/int)
    """
    return sum(selected_levels.values())

def determine_grade(points, category, system):
    """
    points: total score
    category: "Operatives" or "Administrator"
    system: "MSS" or "Rank and File"
    Returns: grade string (e.g., "O 01")
    """
    if "Rank and File" in system:
        if category == "Operatives":
            ranges = GRADE_RANGES_RF_OPERATIVES
        else:
            ranges = GRADE_RANGES_RF_ADMIN
    else:
        ranges = GRADE_RANGES_OPERATIVES if category == "Operatives" else GRADE_RANGES_ADMIN
    
    for r in ranges:
        if r["min"] <= points <= r["max"]:
            return r["grade"]
    
    return "Unknown"

def get_job_clustering_info(category):
    if category == "Operatives":
        return "Highest (538.75) - Lowest (153.25) / 5 = Interval (77.1)"
    else:
        return "Highest (482.95) - Lowest (237.25) / 5 = Interval (81.90)" # Preserving user text
