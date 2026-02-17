# Factor Scores for Managerial, Supervisory, and Specialist Positions
# Based on Screenshot 3
FACTOR_SCORES_MSS = {
    "Education": {1: 11, 2: 36, 3: 61, 4: 85, 5: 110},
    "Experience": {1: 12, 2: 39, 3: 66, 4: 93, 5: 120},
    "Complexity": {1: 14, 2: 46, 3: 77, 4: 109, 5: 140},
    "Effect of Errors": {1: 10, 2: 33, 3: 55, 4: 78, 5: 100},
    "Relevance to Core Mission": {1: 7, 2: 39, 3: 70}, # Only 3 levels shown
    "Extent of Line or Functional Supervision": {1: 8, 2: 26, 3: 44, 4: 62, 5: 80},
    "Scope of Supervision": {1: 6, 2: 17, 3: 28, 4: 38, 5: 49, 6: 60},
    "Responsibility for Confidence": {1: 7, 2: 23, 3: 39, 4: 54, 5: 70},
    "Contact with Others": {1: 25, 2: 41, 3: 58, 4: 74, 5: 90}, # Assuming 6 levels in table, but only 5 increments shown clearly or maybe 6th is N/A. Screenshot shows 6 columns but "90" is under Col 6. Let's re-verify. 
    # Row 12: Col 1=25, Col 2=41, Col 3=58, Col 4=74, Col 5=90. Col 6 header exists but cell is empty/N/A? No, looked closer. Col 6 has 90. Col 5 has 74.
    # Corrections below based on visual re-check of columns:
    # Col 1 | Col 2 | Col 3 | Col 4 | Col 5 | Col 6 | Col 7
    # 25    | 41    | 58    | 74    | 90    | N/A   | N/A
    # Wait. Row 12. "9" is percent. "25" is Col 1.
    # Col 1: 25. Col 2: 41. Col 3: 58. Col 4: 74. Col 5: 90.
    # Level 6 is blank/N/A.
    
    "Ingenuity": {1: 11, 2: 36, 3: 61, 4: 85, 5: 110},
    "Work Area": {1: 5, 2: 28, 3: 50} # Only 3 levels
}

# Fix Contact with Others based on reasoning:
FACTOR_SCORES_MSS["Contact with Others"] = {1: 25, 2: 41, 3: 58, 4: 74, 5: 90}

# Job Grade Ranges
# Operatives Level
GRADE_RANGES_OPERATIVES = [
    {"grade": "O 01", "min": 0, "max": 230},
    {"grade": "O 02", "min": 231, "max": 307},
    {"grade": "O 03", "min": 308, "max": 385},
    {"grade": "O 04", "min": 386, "max": 462},
    {"grade": "O 05", "min": 463, "max": 9999}, # "463 upwards"
]

# Administrator Level (Managerial, Supervisory, Specialist)
GRADE_RANGES_ADMIN = [
    {"grade": "MS 01", "min": 0, "max": 319},
    {"grade": "MS 02", "min": 320, "max": 401},
    {"grade": "MS 03", "min": 402, "max": 9999}, # "402 upwards"
]

# Factor Weights (for display purposes, already baked into scores)
FACTOR_WEIGHTS = {
    "Education": 11,
    "Experience": 12,
    "Complexity": 14,
    "Effect of Errors": 10,
    "Relevance to Core Mission": 7,
    "Extent of Line or Functional Supervision": 8,
    "Scope of Supervision": 6,
    "Responsibility for Confidence": 7,
    "Contact with Others": 9,
    "Ingenuity": 11,
    "Work Area": 5
}

# Reference Position Rankings (as per provided data)
REFERENCE_POSITIONS_OPERATIVES = [
    {"Position": "Canteen Aide", "Rating": 153.25},
    {"Position": "Teacher’s Aide", "Rating": 169.00},
    {"Position": "Bookstore Aide", "Rating": 172.00},
    {"Position": "Cashiering Assistant", "Rating": 185.50},
    {"Position": "Canteen Cook", "Rating": 209.50},
    {"Position": "Maintenance Aide", "Rating": 235.00},
    {"Position": "Computer Technician", "Rating": 238.75},
    {"Position": "Cashier", "Rating": 239.50},
    {"Position": "Driver", "Rating": 240.25},
    {"Position": "Office Assistant", "Rating": 244.00},
    {"Position": "Property Custodian", "Rating": 250.75},
    {"Position": "Bookkeeper", "Rating": 284.50},
    {"Position": "Instructional Media Assistant", "Rating": 310.00},
    {"Position": "Science Laboratory Assistant", "Rating": 315.25},
    {"Position": "School Nurse", "Rating": 331.00},
    {"Position": "Librarian", "Rating": 383.50},
    {"Position": "Faculty Member", "Rating": 508.75},
    {"Position": "Guidance Counselor", "Rating": 538.75}
]

REFERENCE_POSITIONS_ADMIN = [
    {"Position": "Registrar", "Rating": 237.25},
    {"Position": "Prefect of Student Formation", "Rating": 306.55},
    {"Position": "Student Affairs Coordinator", "Rating": 334.00},
    {"Position": "Subject Area Coordinator", "Rating": 337.60},
    {"Position": "Pastoral Affairs Coordinator", "Rating": 345.25},
    {"Position": "Human Resource Management Officer", "Rating": 372.25},
    {"Position": "Institutional Affairs Officer", "Rating": 408.25},
    {"Position": "Guidance Program Coordinator", "Rating": 432.55},
    {"Position": "Academic Coordinator", "Rating": 482.95}
]

# Rank and File Grade Ranges
GRADE_RANGES_RF_OPERATIVES = [
    {"grade": "O 01", "min": 0.0,   "max": 274.99},
    {"grade": "O 02", "min": 275.0, "max": 349.99},
    {"grade": "O 03", "min": 350.0, "max": 424.99},
    {"grade": "O 04", "min": 425.0, "max": 499.99},
    {"grade": "O 05", "min": 500.0, "max": 1000.0}
]

GRADE_RANGES_RF_ADMIN = [
    {"grade": "MS 01", "min": 0.0,   "max": 349.99},
    {"grade": "MS 02", "min": 350.0, "max": 499.99},
    {"grade": "MS 03", "min": 500.0, "max": 1000.0}
]

# --- Rank and File Reference Positions (Placeholders) ---
REFERENCE_POSITIONS_RF_OPERATIVES = [
    {"Position": "Utility Worker", "Rating": 0},
    {"Position": "Messenger", "Rating": 0},
    {"Position": "Security Guard", "Rating": 0},
    {"Position": "Driver (RF)", "Rating": 0},
    {"Position": "Maintenance Staff", "Rating": 0}
]

REFERENCE_POSITIONS_RF_ADMIN = [
    {"Position": "Clerk", "Rating": 0},
    {"Position": "Office Assistant (RF)", "Rating": 0},
    {"Position": "Secretary", "Rating": 0},
    {"Position": "Data Encoder", "Rating": 0},
    {"Position": "Receptionist", "Rating": 0}
]

# --- Rank and File System Data ---

FACTOR_SCORES_RF = {
    "Education and Knowledge": {1: 15, 2: 42, 3: 69, 4: 96, 5: 123, 6: 150},
    "Experience and Training": {1: 9, 2: 36, 3: 63, 4: 90},
    "Judgment and Initiative": {1: 13, 2: 42, 3: 72, 4: 101, 5: 130},
    "Effect of Errors": {1: 10, 2: 33, 3: 55, 4: 78, 5: 100},
    "Supervision Received": {1: 7, 2: 23, 3: 39, 4: 54, 5: 70},
    "Responsibility for Confidence": {1: 9, 2: 25, 3: 41, 4: 58, 5: 74, 6: 90},
    "Contact with Others": {1: 12, 2: 39, 3: 66, 4: 93, 5: 120},
    "Relevance to Core Mission": {1: 7, 2: 39, 3: 70},
    "Physical Demand": {1: 6, 2: 20, 3: 33, 4: 47, 5: 60},
    "Mental and Visual Demand": {1: 7, 2: 23, 3: 39, 4: 54, 5: 70},
    "Work Area": {1: 5, 2: 20, 3: 35, 4: 50}
}

FACTOR_WEIGHTS_RF = {
    "Education and Knowledge": 15,
    "Experience and Training": 9,
    "Judgment and Initiative": 13,
    "Effect of Errors": 10,
    "Supervision Received": 7,
    "Responsibility for Confidence": 9,
    "Contact with Others": 12,
    "Relevance to Core Mission": 7,
    "Physical Demand": 6,
    "Mental and Visual Demand": 7,
    "Work Area": 5
}
