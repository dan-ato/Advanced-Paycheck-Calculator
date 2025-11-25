import streamlit as st
from estimator.core import load_history, calculate_pay

# --- 1️⃣ Page Setup ---
st.set_page_config(
    page_title="Advanced Paycheck Estimator",
    page_icon="💰",
    layout="centered"
)

# Theme-based colors
theme_base = st.get_option("theme.base")

if theme_base == "light":
    container_bg = "#f9f9f9ad"       # light gray container
    header_color = "#0a3d62"       # darker blue for better contrast
    subtitle_color = "#333333"     # dark gray
else:
    container_bg = "#1e1e1e"       # dark gray container
    header_color = "#2f73fa"       # soft cyan
    subtitle_color = "#cccccc"     # light gray

# Header container
st.markdown(
    f"""
    <div style='background-color:{container_bg};padding:20px;border-radius:15px;text-align:center'>
        <h2 style='color:{header_color}'>💰 Advanced Paycheck Estimator</h2>
        <p style='color:{subtitle_color};font-size:14px'>Rolling deduction model with calibration memory</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("<br>", unsafe_allow_html=True)

# --- 4️⃣ Sidebar Extras ---
st.sidebar.header("About & Tips")
st.sidebar.info(
    """
    Enter your hours worked (HH.MM or HH:MM). Optionally enter your actual net pay to calibrate the rolling deduction model.
    
    This tool becomes more accurate over time as you input actual net pay.
    """
)
st.sidebar.write("**Version:** 1.0.0")

# --- 5️⃣ Input Section with subtle background ---
with st.container():
    st.subheader("Enter Your Work Data")
    hours_input = st.text_input("Hours (HH.MM or HH:MM):")
    actual_net_input = st.text_input("Actual Net Pay (optional):")
    calculate = st.button("Calculate")

# --- 6️⃣ Process Calculation ---
if calculate:
    actual_net = float(actual_net_input) if actual_net_input.strip() else None
    history = load_history()
    result = calculate_pay(hours_input, history=history, actual_net=actual_net)

    st.markdown("---")
    st.subheader("📊 Paycheck Results")

    # Conditional color for Effective Rate
    eff_rate = result['effective_rate']
    if eff_rate >= 12.35:
        eff_color = metric_good
    elif 11 <= eff_rate < 12.35:
        eff_color = metric_warning
    else:
        eff_color = metric_bad

    # Display metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Gross Pay", f"${result['gross']:.2f}")
    col2.metric("Estimated Net", f"${result['net']:.2f}")
    col3.metric("Effective Rate", f"${eff_rate:.2f}/hr", delta=None)

    st.write(f"Converted Hours: **{result['total_hours']:.3f}**")
    st.write(f"Regular Hours: **{result['regular_hours']:.2f}**")
    st.write(f"Overtime Hours: **{result['overtime_hours']:.2f}**")
    st.markdown(
        f"<p style='color:{eff_color}'>Effective Hourly Rate Status</p>",
        unsafe_allow_html=True
    )

    st.markdown("---")
    st.write(f"Current Deduction Multiplier: **{result['deduction']:.4f}**")

    if actual_net:
        st.write("### Calibration Update")
        st.write(f"Actual Multiplier: **{result['actual_multiplier']:.4f}**")
        st.success("History Updated ✔️")
