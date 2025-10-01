import streamlit as st
import pandas as pd
import sys

sys.path.append(r"D:\PythonPackages")

# ---------------- Page Config ----------------
st.set_page_config(page_title="Faculty Search", page_icon="🎓", layout="wide")

# ---------------- Fixed Search Bar CSS ----------------
st.markdown(
    """
    <style>
    .fixed-search {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        background-color: #ffffff;
        padding: 15px 20px;
        z-index: 9999;
        border-bottom: 2px solid #ddd;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
    }
    .search-spacer {
        height: 70px; /* same height as the search bar */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- Centered Title ----------------
st.markdown(
    """
    <div style='text-align: center; margin-top: 0px;'>
        <h1>🎓 Faculty Search</h1>
        <p>Search for faculty details including cabin and email information.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------- Sticky Search Input ----------------
st.markdown('<div class="fixed-search">', unsafe_allow_html=True)
search_input = st.text_input("🔍 Search Faculty (Name, Designation, Cabin, Email)", key="search")
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div class="search-spacer"></div>', unsafe_allow_html=True)  # pushes content down

# ---------------- Load Data ----------------
@st.cache_data
def load_data(file_path="faculty details.xlsx"):
    df = pd.read_excel(file_path)
    column_map = {
        'Name of the Faculty': 'name',
        'Dept': 'department',
        'Designation': 'designation',
        'Cabin Details': 'cabin',
        'Email ID': 'email'
    }
    df.rename(columns=column_map, inplace=True)
    df.columns = [col.strip().lower() for col in df.columns]
    return df

df = load_data()

# ---------------- Sidebar Options ----------------
st.sidebar.header("Options")
available_columns = [col for col in df.columns if col in ['name', 'department', 'designation', 'cabin', 'email']]
selected_columns = st.sidebar.multiselect(
    "Select columns to display",
    options=available_columns,
    default=available_columns
)
if 'cabin' in available_columns and 'cabin' not in selected_columns:
    selected_columns.insert(0, 'cabin')

# ---------------- Search Function ----------------
def search_faculty(data, search_term):
    if not search_term:
        return pd.DataFrame()
    search_term = search_term.lower()
    mask = pd.Series(False, index=data.index)
    for col in ['name', 'designation', 'cabin', 'email']:
        if col in data.columns:
            mask = mask | data[col].astype(str).str.lower().str.contains(search_term)
    return data[mask]

filtered_df = search_faculty(df, search_input)

# ---------------- Display Results as Cards ----------------
def render_card(row):
    st.markdown(
        f"""
        <div style='border:1px solid #ccc; padding:15px; margin-bottom:10px; 
                    border-radius:12px; background-color:#f0f8ff; color:#000; 
                    font-size:14px; box-shadow: 2px 2px 8px rgba(0,0,0,0.1);'>
            <strong style="font-size:16px;">Name:</strong> {row.get('name', '')} <br>
            <strong>Designation:</strong> {row.get('designation', '')} <br>
            <strong>Cabin:</strong> {row.get('cabin', '')} <br>
            <strong>Email:</strong> <a href="mailto:{row.get('email', '')}" style="color:#1a73e8;">{row.get('email', '')}</a>
        </div>
        """,
        unsafe_allow_html=True
    )

# ---------------- Display Logic ----------------
if not filtered_df.empty:
    st.write(f"### Found {len(filtered_df)} faculty member(s)")
    for index, row in filtered_df[selected_columns].iterrows():
        render_card(row)

    
elif search_input:
    st.warning("No faculty found with the given search criteria.")
else:
    st.info("Please enter a search term above to find faculty details.")
