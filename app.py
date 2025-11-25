import streamlit as st
from estimator.core import load_history, calculate_pay

# --- 1️⃣ Page Setup ---
st.set_page_config(
    page_title="Advanced Paycheck Estimator",
    page_icon="💰",
    layout="centered"
)

# --- 2️⃣ Color & Visual Theme ---
theme_base = st.get_option("theme.base")

# Container background & shadow
if theme_base == "light":
    container_bg = "#f5f5f5"  # softer light gray
    subtitle_color = "#555555"
else:
    container_bg = "#1e1e1e"  # darker gray
    subtitle_color = "#cccccc"

header_color = "#111111" if theme_base == "light" else "#ffffff"
container_shadow = "0 4px 6px rgba(0,0,0,0.1)"  # subtle shadow

# Header container
st.markdown(
    f"""
    <div style='background-color:{container_bg};
                padding:20px;
                border-radius:15px;
                text-align:center;
                box-shadow:{container_shadow}'>
        <h2 style='color:{header_color}; margin-bottom:5px;'>💰 Advanced Paycheck Estimator</h2>
        <p style='color:{subtitle_color}; font-size:14px; margin-top:0;'>Rolling deduction model with calibration memory</p>
    </div>
    """,
    unsafe_allow_html=True
)
st.markdown("<br>", unsafe_allow_html=True)

# --- 3️⃣ Sidebar Extras ---
st.sidebar.header("About & Tips")
st.sidebar.info(
    """
    Enter your hours worked (HH.MM or HH:MM). Optionally enter your actual net pay to calibrate the rolling deduction model.
    
    This tool becomes more accurate over time as you input actual net pay.
    """
)
st.sidebar.write("**Version:** 1.0.0")

# --- 4️⃣ Input Section ---
with st.container():
    st.subheader("Enter Your Work Data")
    hours_input = st.text_input("Hours (HH.MM or HH:MM):")
    actual_net_input = st.text_input("Actual Net Pay (optional):")
    calculate = st.button("Calculate")

# --- 5️⃣ Process Calculation ---
if calculate:
    actual_net = float(actual_net_input) if actual_net_input.strip() else None
    history = load_history()
    result = calculate_pay(hours_input, history=history, actual_net=actual_net)

    st.markdown("---")
    st.subheader("📊 Paycheck Results")

    # Conditional colors for Effective Rate
    metric_good = "#2ecc71"    # green
    metric_warning = "#f1c40f" # yellow
    metric_bad = "#e74c3c"     # red

    eff_rate = result['effective_rate']
    if eff_rate >= 12.35:
        eff_color = metric_good
    elif 11 <= eff_rate < 12.35:
        eff_color = metric_warning
    else:
        eff_color = metric_bad

    # Display metrics in columns
    col1, col2, col3 = st.columns(3)
    col1.metric("Gross Pay", f"${result['gross']:.2f}")
    col2.metric("Estimated Net", f"${result['net']:.2f}")
    col3.metric("Effective Rate", f"${eff_rate:.2f}/hr", delta=None)

    # Additional info
    st.write(f"Converted Hours: **{result['total_hours']:.3f}**")
    st.write(f"Regular Hours: **{result['regular_hours']:.2f}**")
    st.write(f"Overtime Hours: **{result['overtime_hours']:.2f}**")
    st.markdown(
        f"<p style='color:{eff_color}; font-weight:bold'>Effective Hourly Rate Status</p>",
        unsafe_allow_html=True
    )

    st.markdown("---")
    st.write(f"Current Deduction Multiplier: **{result['deduction']:.4f}**")

    if actual_net:
        st.write("### Calibration Update")
        st.write(f"Actual Multiplier: **{result['actual_multiplier']:.4f}**")
        st.success("History Updated ✔️")
