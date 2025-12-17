import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px  # Optional: For nice charts if installed, otherwise uses st.bar_chart

# --------------------------
# Database Functions
# --------------------------
DB_NAME = "employees.db"

def init_db():
    """Initialize the database table."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            department TEXT,
            position TEXT,
            salary REAL
        )
        """)
        conn.commit()

def run_query(query, params=(), fetch=False):
    """Helper function to run queries safely."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        if fetch:
            return cursor.fetchall()
        conn.commit()

# --------------------------
# Page Configuration
# --------------------------
st.set_page_config(
    page_title="HR Dashboard",
    page_icon="👥",
    layout="wide"
)

# Initialize DB on first run
init_db()

# --------------------------
# Sidebar & Navigation
# --------------------------
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/912/912314.png", width=100)
st.sidebar.title("Navigation")
menu = ["Dashboard", "Add Employee", "Update Employee", "Delete Employee"]
choice = st.sidebar.radio("Go to", menu)

# --------------------------
# 1. Dashboard (View)
# --------------------------
if choice == "Dashboard":
    st.title("📊 HR Dashboard")

    # Fetch Data
    rows = run_query("SELECT * FROM employees", fetch=True)
    df = pd.DataFrame(rows, columns=["ID", "Name", "Email", "Phone", "Department", "Position", "Salary"])

    if not df.empty:
        # Top Metrics
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Employees", len(df))
        c2.metric("Average Salary", f"${df['Salary'].mean():,.2f}")
        c3.metric("Total Departments", df['Department'].nunique())

        st.markdown("---")

        # Search Bar
        search_term = st.text_input("🔍 Search by Name, Dept, or Position")
        
        if search_term:
            # Filter dataframe based on search
            mask = df.apply(lambda x: x.astype(str).str.contains(search_term, case=False).any(), axis=1)
            display_df = df[mask]
        else:
            display_df = df

        st.dataframe(display_df, use_container_width=True)
        
        # Simple Visualization
        st.subheader("Department Distribution")
        dept_counts = display_df['Department'].value_counts()
        st.bar_chart(dept_counts)
        
    else:
        st.info("No employees found. Go to 'Add Employee' to get started.")

# --------------------------
# 2. Add Employee
# --------------------------
elif choice == "Add Employee":
    st.title("➕ Add New Employee")
    
    with st.form("add_form"):
        c1, c2 = st.columns(2)
        name = c1.text_input("Name*")
        email = c2.text_input("Email")
        
        c3, c4 = st.columns(2)
        phone = c3.text_input("Phone")
        department = c4.selectbox("Department", ["HR", "Finance", "IT", "Sales", "Marketing", "Operations"])
        
        c5, c6 = st.columns(2)
        position = c5.text_input("Position")
        salary = c6.number_input("Salary", min_value=0.0, step=1000.0)

        submitted = st.form_submit_button("Save Employee")

        if submitted:
            if name:
                run_query(
                    "INSERT INTO employees(name,email,phone,department,position,salary) VALUES(?,?,?,?,?,?)",
                    (name, email, phone, department, position, salary)
                )
                st.success(f"✅ Employee **{name}** added successfully!")
            else:
                st.error("Name is required!")

# --------------------------
# 3. Update Employee
# --------------------------
elif choice == "Update Employee":
    st.title("✏️ Update Details")

    # Fetch list of employees to select from
    rows = run_query("SELECT id, name FROM employees", fetch=True)
    
    if rows:
        # Create a dictionary for the dropdown: "ID - Name" -> ID
        employee_dict = {f"{row[0]} - {row[1]}": row[0] for row in rows}
        selected_emp = st.selectbox("Select Employee to Update", list(employee_dict.keys()))
        selected_id = employee_dict[selected_emp]

        # Fetch current details of selected user
        data = run_query("SELECT * FROM employees WHERE id=?", (selected_id,), fetch=True)[0]
        
        # Unpack data
        # Data structure: (id, name, email, phone, dept, pos, salary)
        curr_name, curr_email, curr_phone, curr_dept, curr_pos, curr_salary = data[1], data[2], data[3], data[4], data[5], data[6]

        with st.form("update_form"):
            c1, c2 = st.columns(2)
            new_name = c1.text_input("Name", value=curr_name)
            new_email = c2.text_input("Email", value=curr_email)
            
            c3, c4 = st.columns(2)
            new_phone = c3.text_input("Phone", value=curr_phone)
            
            # handle default index for department selectbox
            dept_options = ["HR", "Finance", "IT", "Sales", "Marketing", "Operations"]
            try:
                dept_index = dept_options.index(curr_dept)
            except ValueError:
                dept_index = 0
                
            new_dept = c4.selectbox("Department", dept_options, index=dept_index)
            
            c5, c6 = st.columns(2)
            new_pos = c5.text_input("Position", value=curr_pos)
            new_salary = c6.number_input("Salary", min_value=0.0, value=float(curr_salary), step=1000.0)

            updated = st.form_submit_button("Update Details")

            if updated:
                run_query("""
                    UPDATE employees 
                    SET name=?, email=?, phone=?, department=?, position=?, salary=? 
                    WHERE id=?
                """, (new_name, new_email, new_phone, new_dept, new_pos, new_salary, selected_id))
                st.success(f"✅ Employee **{new_name}** updated successfully!")
                
    else:
        st.warning("No employees found to update.")

# --------------------------
# 4. Delete Employee
# --------------------------
elif choice == "Delete Employee":
    st.title("🗑️ Delete Employee")

    rows = run_query("SELECT id, name, department FROM employees", fetch=True)
    
    if rows:
        # Dictionary for selectbox
        employee_dict = {f"{row[0]} - {row[1]} ({row[2]})": row[0] for row in rows}
        selected_emp = st.selectbox("Select Employee to Delete", list(employee_dict.keys()))
        selected_id = employee_dict[selected_emp]

        st.warning(f"Are you sure you want to delete **{selected_emp}**?")
        
        if st.button("Confirm Delete", type="primary"):
            run_query("DELETE FROM employees WHERE id=?", (selected_id,))
            st.success("Employee deleted successfully!")
            st.rerun() # Rerun to update the list immediately
    else:
        st.info("No employees to delete.")
