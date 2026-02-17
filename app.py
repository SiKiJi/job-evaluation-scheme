import streamlit as st
import pandas as pd
from data_models import (
    FACTOR_SCORES_MSS, 
    FACTOR_SCORES_RF,
    GRADE_RANGES_OPERATIVES, 
    GRADE_RANGES_ADMIN, 
    FACTOR_WEIGHTS,
    FACTOR_WEIGHTS_RF,
    REFERENCE_POSITIONS_OPERATIVES,
    REFERENCE_POSITIONS_ADMIN,
    REFERENCE_POSITIONS_RF_OPERATIVES,
    REFERENCE_POSITIONS_RF_ADMIN
)
from logic import calculate_total_points, determine_grade, get_job_clustering_info

st.set_page_config(page_title="Job Evaluation Automation", layout="wide")

# --- Modern UI CSS Injection ---
st.markdown("""
    <style>
    /* Global Styles */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: #1f2937; /* Gray-800 */
    }
    
    /* App Background */
    .stApp {
        background-color: #f3f4f6; /* Gray-100 */
    }
    
    /* Navigation Bar Styling */
    div[data-testid="stVerticalBlock"] > div:first-child {
        padding-top: 0;
    }
    
    /* Unified Nav Styling */
    [data-testid="stVerticalBlockBorderWrapper"]:has(.nav-unified) {
        background-color: #1e3a8a !important; /* Blue-900 */
        padding: 1.5rem 2rem !important;
        border-radius: 0.75rem !important;
        margin-bottom: 2rem !important;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05) !important;
        border: none !important;
    }
    
    /* Ensure the inner block has no extra padding/background */
    [data-testid="stVerticalBlockBorderWrapper"]:has(.nav-unified) > div {
        background-color: transparent !important;
    }
    
    /* Nav Button Overrides */
    .nav-btn button {
        background-color: transparent !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
    }
    .nav-btn button:hover {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border-color: white !important;
    }
    .nav-btn-active button {
        background-color: white !important;
        color: #1e3a8a !important; /* Match Blue-900 */
        border: none !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    /* Card Container Styling for Content Sections */
    .content-card {
        background-color: white;
        padding: 2rem;
        border-radius: 0.75rem; /* 12px */
        border: 1px solid #e5e7eb;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        margin-bottom: 1.5rem;
    }
    
    /* Input Field Styling */
    .stTextInput > div > div > input {
        border-radius: 0.5rem;
        border-color: #d1d5db;
    }
    .stSelectbox > div > div > div {
        border-radius: 0.5rem;
        border-color: #d1d5db;
    }
    
    /* Button Styling */
    .stButton > button {
        border-radius: 0.5rem;
        font-weight: 600;
        transition: all 0.2s ease-in-out;
    }
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    /* Metric Styling */
    [data-testid="stMetricValue"] {
        font-size: 2.25rem;
        font-weight: 700;
        color: #2563eb; /* Blue-600 */
    }
    
    /* Table Styling */
    [data-testid="stDataFrame"] {
        border-radius: 0.5rem;
        overflow: hidden;
        border: 1px solid #e5e7eb;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #111827; /* Gray-900 */
        font-weight: 700;
        letter-spacing: -0.025em;
    }
    
    /* Print Styles */
    @media print {
        body * { visibility: hidden; }
        .stApp { visibility: hidden; }
        #printable-area, #printable-area * { visibility: visible; }
        #printable-area {
            position: absolute;
            left: 0;
            top: 0;
            width: 100%;
            background-color: white !important;
            color: black !important;
            padding: 20px;
            z-index: 9999;
        }
        table { width: 100%; border-collapse: collapse; font-family: 'Inter', sans-serif; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; color: black; }
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Session State for Navigation
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = "Job Evaluation"

# --- Helper Functions for Persistence ---
CSV_FILE = "ratings_history.csv"

def reset_evaluation_form():
    """Resets all factor selections and input fields in the evaluation form."""
    # Reset all MSS factors
    for factor in FACTOR_SCORES_MSS.keys():
        if factor in st.session_state:
            del st.session_state[factor]
    
    # Reset all RF factors
    for factor in FACTOR_SCORES_RF.keys():
        if factor in st.session_state:
            del st.session_state[factor]
    
    # Reset input fields
    if 'employee_name' in st.session_state:
        del st.session_state['employee_name']
    if 'position_selection' in st.session_state:
        del st.session_state['position_selection']
    if 'custom_position' in st.session_state:
        del st.session_state['custom_position']

def save_rating(name, position, category, system, total_points, grade, details_json):
    """Saves the rating to a CSV file."""
    timestamp = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
    new_data = {
        "Date": timestamp,
        "Employee Name": name,
        "Position": position,
        "Category": category,
        "System": system,
        "Total Points": total_points,
        "Grade": grade,
    }
    
    try:
        df = pd.read_csv(CSV_FILE)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Date", "Employee Name", "Position", "Category", "System", "Total Points", "Grade"])
        
    # Append new data using concat
    df_new = pd.DataFrame([new_data])
    df = pd.concat([df, df_new], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)

def delete_rating(index):
    """Deletes a rating record by index."""
    try:
        df = pd.read_csv(CSV_FILE)
        df = df.drop(index)
        df.to_csv(CSV_FILE, index=False)
        return True
    except Exception as e:
        return False

def update_rating(index, updated_row):
    """Updates a rating record by index."""
    try:
        df = pd.read_csv(CSV_FILE)
        # We ensure the columns match
        for col in updated_row:
            if col in df.columns:
                df.at[index, col] = updated_row[col]
        df.to_csv(CSV_FILE, index=False)
        return True
    except Exception as e:
        return False

def get_history():
    """Reads the history CSV."""
    try:
        df = pd.read_csv(CSV_FILE)
        # Ensure "System" column exists for legacy data
        if "System" not in df.columns:
            df["System"] = "MSS (Legacy)" 
        return df
    except FileNotFoundError:
        return pd.DataFrame(columns=["Date", "Employee Name", "Position", "Category", "System", "Total Points", "Grade"])

# --- Custom Navigation Bar (Styled) ---

# CSS for the unified navbar
# CSS for the unified navbar
st.markdown("""
<style>
    /* Target ONLY the specific container with our anchor */
    div[data-testid="stVerticalBlockBorderWrapper"]:has(div#main-nav) {
        background-color: white; /* Revert to white/transparent */
        padding: 1.5rem 2rem;
        border-radius: 0.75rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        gap: 1rem;
        border: 1px solid #e5e7eb; /* Add subtle border back */
    }
    
    /* Ensure the inner block has no extra padding/background */
    div[data-testid="stVerticalBlockBorderWrapper"]:has(div#main-nav) > div {
        background-color: transparent;
    }
    
    /* Reset button styling for light background */
    div[data-testid="stVerticalBlockBorderWrapper"]:has(div#main-nav) button {
        /* Default Streamlit style usually works, but we can ensure standard look */
    }
    
    /* Override primary button in nav to be standard blue on white */
    div[data-testid="stVerticalBlockBorderWrapper"]:has(div#main-nav) button[kind="primary"] {
        background-color: #2563eb !important; /* Blue-600 */
        color: white !important;
        border: none;
    }
</style>
""", unsafe_allow_html=True)

with st.container(border=True):
    # Anchor for CSS targeting
    st.markdown('<div id="main-nav"></div>', unsafe_allow_html=True)
    
    # Layout: Title on Left, Buttons on Right
    col_title, col_btns = st.columns([1.5, 2.5])
    
    with col_title:
        # Revert text color to dark
        st.markdown('<h2 style="color: #111827; margin: 0; padding: 0; font-size: 1.5rem; font-weight: 700;">Job Evaluation Scheme</h2>', unsafe_allow_html=True)
        st.markdown('<p style="color: #6b7280; margin: 0; font-size: 0.85rem;">Automated Rating System</p>', unsafe_allow_html=True)
        
    with col_btns:
        # Nested columns for buttons to align them
        b1, b2, b3, b4 = st.columns(4)
        
        with b1:
            if st.button("📝 Evaluation", use_container_width=True, type="primary" if st.session_state.active_tab == "Job Evaluation" else "secondary", key="nav_eval"):
                st.session_state.active_tab = "Job Evaluation"
                st.rerun()
                
        with b2:
            if st.button("📚 References", use_container_width=True, type="primary" if st.session_state.active_tab == "Reference Rankings" else "secondary", key="nav_ref"):
                st.session_state.active_tab = "Reference Rankings"
                st.rerun()
        
        with b3:
            if st.button("📁 Records", use_container_width=True, type="primary" if st.session_state.active_tab == "Records" else "secondary", key="nav_rec"):
                st.session_state.active_tab = "Records"
                st.rerun()
                
        with b4:
            if st.button("📊 Analytics", use_container_width=True, type="primary" if st.session_state.active_tab == "Analytics" else "secondary", key="nav_ana"):
                st.session_state.active_tab = "Analytics"
                st.rerun()

# Spacing
st.write("")

# --- Printable Report Content (Hidden on Screen, Visible on Print) ---
# ... (Logic remains, just ensuring variables are caught safely if switching tabs)
if st.session_state.active_tab == "Job Evaluation":
    # Logic placeholder for print variables
    pass

# --- Content Rendering with Modern Layout ---

if st.session_state.active_tab == "Job Evaluation":
    
    # Grid Layout using Streamlit containers as 'Cards'
    
    # 1. Job Details Card
    with st.container(border=True):
        st.subheader("1. Job Details")
        st.markdown("Enter the employee and position information below.")
        
        # Add System Selector
        evaluation_system = st.radio("Evaluation System", 
                                     ["Managerial/Supervisory/Specialist (MSS)", "Rank and File"], 
                                     horizontal=True)
        
        st.divider()
        
        col_details_1, col_details_2, col_details_3 = st.columns([1, 0.8, 1.2])
        
        with col_details_1:
            name = st.text_input("Employee Name", placeholder="e.g. John Doe", key="employee_name")
            
        with col_details_2:
            # Category is now relevant for BOTH systems
            category = st.radio("Job Category", ["Operatives", "Administrator"], horizontal=True)

        with col_details_3:
            # Dropdown logic based on System AND Category
            pos_options = []
            
            if evaluation_system == "Managerial/Supervisory/Specialist (MSS)":
                if category == "Operatives":
                    pos_options = [p["Position"] for p in REFERENCE_POSITIONS_OPERATIVES]
                else:
                    pos_options = [p["Position"] for p in REFERENCE_POSITIONS_ADMIN]
            else: # Rank and File
                if category == "Operatives":
                    pos_options = [p["Position"] for p in REFERENCE_POSITIONS_RF_OPERATIVES]
                else:
                    pos_options = [p["Position"] for p in REFERENCE_POSITIONS_RF_ADMIN]
            
            pos_options.append("Other (Enter Custom)")
            
            position_selection = st.selectbox("Position Title", pos_options, key="position_selection")
            
            if position_selection == "Other (Enter Custom)":
                position = st.text_input("Enter Position Title", placeholder="e.g. Utility Worker", key="custom_position")
            else:
                position = position_selection

    st.write("") # Spacing

    # 2. Main Content Grid: Factors (Left) & Results (Right)
    col_input, col_result = st.columns([1.6, 1])

    result_scores = {}
    selected_levels_display = []
    
    # Determine which data to use
    if evaluation_system == "Managerial/Supervisory/Specialist (MSS)":
        current_factor_scores = FACTOR_SCORES_MSS
        current_factor_weights = FACTOR_WEIGHTS
    else:
        current_factor_scores = FACTOR_SCORES_RF
        current_factor_weights = FACTOR_WEIGHTS_RF

    with col_input:
        with st.container(border=True):
            st.subheader("2. Rating Factors")
            st.markdown(f"Select levels for **{evaluation_system}** factors.")
            
            for factor, levels_data in current_factor_scores.items():
                st.markdown(f"**{factor}**")
                
                # Initialize factor state to None (unselected) if not exists
                if factor not in st.session_state:
                    st.session_state[factor] = None

                # Create columns for buttons
                cols = st.columns(len(levels_data))
                
                selected_lvl_key = None
                selected_pts = 0
                
                for idx, (lvl, pts) in enumerate(levels_data.items()):
                    lvl_key = f"Level {lvl}"
                    
                    with cols[idx]:
                        # Determine button type based on selection state
                        is_selected = st.session_state[factor] == lvl_key
                        btn_type = "primary" if is_selected else "secondary"
                        
                        # Button label
                        if st.button(f"Level {lvl}\n({pts} pts)", key=f"btn_{factor}_{lvl}", type=btn_type, use_container_width=True):
                            st.session_state[factor] = lvl_key
                            st.rerun()
                    
                    # Capture the points for the currently selected level to use in calculation
                    if st.session_state.get(factor) == lvl_key:
                        selected_lvl_key = lvl
                        selected_pts = pts

                # Logic to use the selected value (only if something is selected)
                if selected_lvl_key is not None:
                    result_scores[factor] = selected_pts
                    
                    selected_levels_display.append({
                        "Factor": factor,
                        "Level": selected_lvl_key,
                        "Points": selected_pts,
                        "Weight (%)": current_factor_weights.get(factor, 0)
                    })
                
                st.write("") # Spacing
                st.write("---") # Separator between factors

    with col_result:
        with st.container(border=True):
            st.subheader("3. Results Summary")
            
            # Only calculate and display if at least one factor is selected
            if result_scores:
                total_points = calculate_total_points(result_scores)
                grade = determine_grade(total_points, category, evaluation_system)
                
                # Use columns for metrics to look like dashboard stats
                m_col1, m_col2 = st.columns(2)
                m_col1.metric("Total Points", total_points, delta_color="normal")
                m_col2.metric("Job Grade", grade, delta_color="inverse")
                
                st.markdown("#### Rating Breakdown")
                df_breakdown = pd.DataFrame(selected_levels_display)
                st.dataframe(df_breakdown, use_container_width=True, hide_index=True)
                
                st.info(f"**Clustering Info:** {get_job_clustering_info(category)}")
                
                st.write("")
                if st.button("💾 Save to Records", type="primary", use_container_width=True):
                    if name and position:
                        save_rating(name, position, category, evaluation_system, total_points, grade, selected_levels_display)
                        st.success(f"Record saved for **{name}**!")
                        # Reset the form and refresh
                        reset_evaluation_form()
                        st.rerun()
                    else:
                        st.error("Missing Name or Position.")
            else:
                # Show placeholder when no factors are selected
                st.info("👆 Please select rating levels for each factor above to see the results.")
                
                # Show empty metrics
                m_col1, m_col2 = st.columns(2)
                m_col1.metric("Total Points", "-")
                m_col2.metric("Job Grade", "-")



elif st.session_state.active_tab == "Records":
    st.header("Records of Rating Sheets")
    st.markdown("Historical data of saved job evaluations. Use the buttons to manage records.")
    
    # Initialize session state for editing
    if "edit_index" not in st.session_state:
        st.session_state.edit_index = None
    
    df_history = get_history()
    
    if not df_history.empty:
        # Sort by index descending (latest first) to keep original indices consistent during single-session edits
        # However, indices are from CSV, so we should be careful. 
        # Better: work with the DataFrame index and use it as ID.
        df_display = df_history.copy()
        
        # Edit Mode
        if st.session_state.edit_index is not None:
            idx = st.session_state.edit_index
            if idx in df_display.index:
                row = df_display.loc[idx]
                with st.container(border=True):
                    st.subheader(f"✏️ Editing Record #{idx}")
                    col_e1, col_e2 = st.columns(2)
                    with col_e1:
                        new_name = st.text_input("Employee Name", row["Employee Name"])
                        new_pos = st.text_input("Position", row["Position"])
                        new_cat = st.radio("Category", ["Operatives", "Administrator"], 
                                          index=0 if row["Category"] == "Operatives" else 1, horizontal=True)
                    with col_e2:
                        new_sys = st.selectbox("System", ["Managerial/Supervisory/Specialist (MSS)", "Rank and File"],
                                              index=0 if "MSS" in row["System"] else 1)
                        new_pts = st.number_input("Total Points", value=float(row["Total Points"]))
                        new_grade = st.text_input("Grade", row["Grade"])
                        
                    ec1, ec2 = st.columns(2)
                    if ec1.button("✅ Update Record", type="primary", use_container_width=True):
                        update_data = {
                            "Employee Name": new_name,
                            "Position": new_pos,
                            "Category": new_cat,
                            "System": new_sys,
                            "Total Points": new_pts,
                            "Grade": new_grade
                        }
                        if update_rating(idx, update_data):
                            st.success("Record updated successfully!")
                            st.session_state.edit_index = None
                            st.rerun()
                    if ec2.button("❌ Cancel", use_container_width=True):
                        st.session_state.edit_index = None
                        st.rerun()
            else:
                st.session_state.edit_index = None
                st.rerun()
        
        st.write("") # Spacing
        
        # Records Table Header
        h_col1, h_col2, h_col3, h_col4, h_col5, h_col6, h_col7, h_col8 = st.columns([1.5, 2, 2, 1.2, 1, 1, 1.5, 1.5])
        h_col1.markdown("**Date**")
        h_col2.markdown("**Name**")
        h_col3.markdown("**Position**")
        h_col4.markdown("**Category**")
        h_col5.markdown("**Points**")
        h_col6.markdown("**Grade**")
        h_col7.markdown("**System**")
        h_col8.markdown("**Actions**")
        st.divider()

        # Records Table Rows (Showing last 50 for performance if many)
        for idx, row in df_display.sort_index(ascending=False).iterrows():
            # Filter System string for brevity
            sys_disp = "MSS" if "MSS" in str(row["System"]) else "Rank/File"
            
            r_col1, r_col2, r_col3, r_col4, r_col5, r_col6, r_col7, r_col8 = st.columns([1.5, 2, 2, 1.2, 1, 1, 1.5, 1.5])
            
            r_col1.caption(str(row["Date"]).split(" ")[0]) # Show date only
            r_col2.write(row["Employee Name"])
            r_col3.write(row["Position"])
            r_col4.write(row["Category"])
            r_col5.write(str(row["Total Points"]))
            r_col6.write(f"**{row['Grade']}**")
            r_col7.caption(sys_disp)
            
            # Action Buttons
            btn_col1, btn_col2 = r_col8.columns(2)
            if btn_col1.button("✏️", key=f"edit_{idx}", help="Edit Record"):
                st.session_state.edit_index = idx
                st.rerun()
            if btn_col2.button("🗑️", key=f"del_{idx}", help="Delete Record"):
                if delete_rating(idx):
                    st.success(f"Deleted record for {row['Employee Name']}")
                    st.rerun()
            st.divider()

        # Download button for CSV remains at the bottom
        st.write("")
        csv = df_history.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Full History (CSV)",
            data=csv,
            file_name='job_evaluation_records.csv',
            mime='text/csv',
        )
    else:
        st.info("No records found. Rate a job and click 'Save to Records' to populate this list.")

elif st.session_state.active_tab == "Analytics":
    st.header("Analytics Dashboard")
    st.markdown("Insights and trends from historical job evaluation data.")
    
    df_history = get_history()
    
    if not df_history.empty:
        # Convert Date to datetime for time-series
        df_history['Date'] = pd.to_datetime(df_history['Date'])
        
        # --- Top Level Metrics ---
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Evaluations", len(df_history))
        m2.metric("Avg Points", f"{df_history['Total Points'].mean():.1f}")
        m3.metric("Highest Score", f"{df_history['Total Points'].max():.1f}")
        m4.metric("Lowest Score", f"{df_history['Total Points'].min():.1f}")
        
        st.write("") # Spacing
        
        # --- Distributions ---
        col_a1, col_a2 = st.columns(2)
        
        with col_a1:
            with st.container(border=True):
                st.subheader("📊 Grade Distribution")
                grade_counts = df_history['Grade'].value_counts().reset_index()
                grade_counts.columns = ['Grade', 'Count']
                st.bar_chart(grade_counts.set_index('Grade'))
        
        with col_a2:
            with st.container(border=True):
                st.subheader("🎯 System & Category Split")
                # Group by System and Category
                sys_cat_split = df_history.groupby(['System', 'Category']).size().reset_index(name='count')
                st.dataframe(sys_cat_split, use_container_width=True, hide_index=True)
                
                # Simple pie chart representation via bar chart (system count)
                sys_counts = df_history['System'].value_counts().reset_index()
                sys_counts.columns = ['System', 'Count']
                st.bar_chart(sys_counts.set_index('System'))

        st.write("") # Spacing
        
        # --- Trends ---
        with st.container(border=True):
            st.subheader("📈 Evaluation Trends over Time")
            # Group by Date (Day)
            df_history['DateOnly'] = df_history['Date'].dt.date
            trend_data = df_history.groupby('DateOnly').size().reset_index(name='Evaluations')
            st.line_chart(trend_data.set_index('DateOnly'))
            
            st.markdown("**Average Points over Time**")
            avg_trend = df_history.groupby('DateOnly')['Total Points'].mean().reset_index(name='Avg Points')
            st.line_chart(avg_trend.set_index('DateOnly'))

    else:
        st.info("No data available for analytics yet. Save some evaluations to see results.")

elif st.session_state.active_tab == "Reference Rankings":
    st.header("Reference Rankings & Categories")
    
    col_ref_1, col_ref_2 = st.columns(2)
    
    with col_ref_1:
        st.subheader("Job Categories")
        
        st.markdown("**Operatives Level**")
        st.table(pd.DataFrame([
            {"Grade": "O 01", "Range": "0 – 230"},
            {"Grade": "O 02", "Range": "231 – 307"},
            {"Grade": "O 03", "Range": "308 – 385"},
            {"Grade": "O 04", "Range": "386 – 462"},
            {"Grade": "O 05", "Range": "463+"},
        ]).set_index("Grade"))
        
        st.markdown("**Administrator Level**")
        st.table(pd.DataFrame([
            {"Grade": "MS 01", "Range": "0 – 319"},
            {"Grade": "MS 02", "Range": "320 – 401"},
            {"Grade": "MS 03", "Range": "402+"},
        ]).set_index("Grade"))

    with col_ref_2:
        st.subheader("Position Rankings (Reference)")
        
        st.markdown("#### Operatives")
        st.dataframe(pd.DataFrame(REFERENCE_POSITIONS_OPERATIVES), use_container_width=True)
        
        st.markdown("#### Administrator")
        st.dataframe(pd.DataFrame(REFERENCE_POSITIONS_ADMIN), use_container_width=True)


