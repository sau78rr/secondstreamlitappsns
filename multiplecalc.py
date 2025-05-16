import streamlit as st
import pandas as pd
from io import BytesIO
import time

# --- Page config and theme tip ---
st.set_page_config(
    page_title="Multi-Calculator App",
    page_icon="🧮",
    layout="wide"
)

# --- Sidebar enhancements ---
st.sidebar.image("https://img.icons8.com/color/96/000000/calculator.png", width=80)
st.sidebar.title("🔢 Navigation")
page = st.sidebar.radio("Choose Calculator", [
    "💧 Water Requirement Calculator",
    "➕ Simple Addition Calculator"
])
st.sidebar.markdown("---")
st.sidebar.info(
    "Made with ❤️ using [Streamlit](https://streamlit.io/)\n\n"
    "💡 *Tip: Use the ⋮ menu (top right) to switch between 🌙 dark and ☀️ light mode!*"
)

# --- Main header with animation ---
st.markdown(
    "<h1 style='text-align: center; color: #4F8BF9;'>Multi-Calculator App</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align: center;'>Switch calculators using the sidebar. Enjoy a modern, interactive experience! ✨</p>",
    unsafe_allow_html=True
)

# --- Water Requirement Calculator ---
if page == "💧 Water Requirement Calculator":
    st.header("💧 Water Requirement Calculator")
    st.markdown("Upload your Excel file and get instant water requirement calculations with downloadable results.")

    uploaded_file = st.file_uploader("📤 Upload Book1.xlsx", type=["xlsx"])

    if uploaded_file:
        with st.spinner("Reading your file..."):
            df = pd.read_excel(uploaded_file)
            time.sleep(0.5)
        st.success("File uploaded! Preview below:")
        st.dataframe(df.head(), use_container_width=True)

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
            with st.expander("🔍 See Calculation Results", expanded=True):
                st.dataframe(df.head(), use_container_width=True)

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
    st.markdown("Enter two numbers and see their sum instantly, with a little celebration!")

    col1, col2 = st.columns(2)
    with col1:
        a = st.number_input("Enter first number", value=0, key="num1")
    with col2:
        b = st.number_input("Enter second number", value=0, key="num2")

    if st.button("Calculate Sum", use_container_width=True):
        with st.spinner("Calculating..."):
            time.sleep(0.5)
        st.success(f"🎉 The sum is: {a + b}")
        st.balloons()
