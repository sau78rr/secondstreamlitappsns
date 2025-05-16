import streamlit as st
import pandas as pd
from io import BytesIO
import time
import altair as alt

# --- Page config with icon ---
st.set_page_config(
    page_title="Multi-Calculator App",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for styling ---
st.markdown("""
    <style>
    /* Background gradient */
    .stApp {
        background: linear-gradient(135deg, #f0f4f8, #d9e2ec);
        color: #0f172a;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    /* Header style */
    .header {
        font-size: 3rem;
        font-weight: 700;
        color: #2563eb;
        text-align: center;
        margin-bottom: 0.1rem;
    }
    /* Section divider */
    .divider {
        height: 3px;
        background: #2563eb;
        margin: 1rem 0 2rem 0;
        border-radius: 5px;
    }
    /* Button style */
    div.stButton > button {
        background-color: #2563eb;
        color: white;
        height: 3rem;
        width: 100%;
        border-radius: 10px;
        font-size: 1.1rem;
        font-weight: 600;
        transition: background-color 0.3s ease;
    }
    div.stButton > button:hover {
        background-color: #1e40af;
        color: #f0f4f8;
    }
    /* File uploader box */
    .stFileUploader > div {
        border: 2px dashed #2563eb;
        border-radius: 10px;
        padding: 1rem;
        background-color: #e0e7ff;
    }
    /* Dataframe container */
    .dataframe-container {
        box-shadow: 0 0 10px rgba(37, 99, 235, 0.3);
        border-radius: 10px;
        padding: 1rem;
        background-color: white;
    }
    </style>
""", unsafe_allow_html=True)

# --- App Header ---
st.markdown('<div class="header">🧮 Multi-Calculator App</div>', unsafe_allow_html=True)
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown("Use the sidebar to switch between calculators. Enjoy a clean, interactive experience! 🚀")

# --- Sidebar ---
st.sidebar.image("https://img.icons8.com/color/96/000000/calculator.png", width=70)
st.sidebar.title("Navigation")
page = st.sidebar.radio("Choose Calculator", [
    "💧 Water Requirement Calculator",
    "➕ Simple Addition Calculator"
])
st.sidebar.markdown("---")
st.sidebar.info(
    "Made with ❤️ using [Streamlit](https://streamlit.io/)\n\n"
    "💡 *Tip: Use the ⋮ menu (top right) to switch between 🌙 dark and ☀️ light mode!*"
)

# --- Water Requirement Calculator ---
if page == "💧 Water Requirement Calculator":
    st.header("💧 Water Requirement Calculator")
    st.markdown("Upload your Excel file to calculate water requirements. Results include a downloadable Excel file and interactive charts.")

    uploaded_file = st.file_uploader("📤 Upload your Excel file (.xlsx)", type=["xlsx"])

    if uploaded_file:
        with st.spinner("Reading your file..."):
            df = pd.read_excel(uploaded_file)
            time.sleep(0.5)

        st.success("File uploaded successfully! Preview below:")
        st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
        st.dataframe(df.head(), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        required_columns = [
            'Ab Rh @ Achivable Temp & 80% Rh (gm/m3)',
            'Absolute Humidity (gm/m3)'
        ]

        if all(col in df.columns for col in required_columns):
            with st.spinner("Calculating water requirements..."):
                df['Moisture to add(ml/m3)'] = df['Ab Rh @ Achivable Temp & 80% Rh (gm/m3)'] - df['Absolute Humidity (gm/m3)']
                df['Water Required'] = df['Moisture to add(ml/m3)'] * 69340.64 * 0.4 / 1000 * 60
                df['WaterRequired'] = df['Water Required'] * 11
                df['Requirement Ltr/SqM/Day'] = df['WaterRequired'] / 9216
                time.sleep(0.5)

            st.balloons()

            # Tabs for results and charts
            tabs = st.tabs(["📊 Data Preview", "📈 Visualization"])

            with tabs[0]:
                st.subheader("Calculation Results Preview")
                st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
                st.dataframe(df.head(), use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

            with tabs[1]:
                st.subheader("Water Requirement Chart")
                chart_data = df[['Moisture to add(ml/m3)', 'Requirement Ltr/SqM/Day']].reset_index()
                chart = alt.Chart(chart_data).mark_line(point=True).encode(
                    x='index',
                    y='Moisture to add(ml/m3)',
                    tooltip=['Moisture to add(ml/m3)', 'Requirement Ltr/SqM/Day']
                ).interactive()
                st.altair_chart(chart, use_container_width=True)

            # Download button
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)
            output.seek(0)

            st.download_button(
                label="⬇️ Download Result Excel File",
                data=output,
                file_name="finalresult.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.error(f"❗ Your file must contain the columns: {', '.join(required_columns)}")
    else:
        st.info("Please upload an Excel file to begin.")

# --- Simple Addition Calculator ---
elif page == "➕ Simple Addition Calculator":
    st.header("➕ Simple Addition Calculator")
    st.markdown("Enter two numbers and see their sum instantly, with a fun progress bar!")

    col1, col2 = st.columns(2)
    with col1:
        a = st.number_input("Enter first number", value=0, key="num1")
    with col2:
        b = st.number_input("Enter second number", value=0, key="num2")

    if st.button("Calculate Sum", use_container_width=True):
        with st.spinner("Calculating..."):
            for percent_complete in range(101):
                time.sleep(0.01)
                st.progress(percent_complete)
        st.success(f"🎉 The sum is: {a + b}")
        st.balloons()
