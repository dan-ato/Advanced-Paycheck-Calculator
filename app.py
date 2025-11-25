import streamlit as st
from estimator.core import load_history, calculate_pay
import os

# --- 1. Page Setup ---
st.set_page_config(
    page_title="Advanced Paycheck Estimator",
    page_icon="💰",
    layout="centered"
)

# --- 2. Header with Visual Pizazz ---
st.markdown(
    """
    <div style='background-color:#f0f2f6;padding:15px;border-radius:10px'>
        <h2 style='color:#0f4c75;text-align:center'>💰 Advanced Paycheck Estimator</h2>
        <p style='text-align:center;font-size:14px;color:#333333'>
            Rolling deduction model with calibration memory
        </p>
    </div>
    """, unsafe_allow_html=True
)

st.markdown("<br>", unsafe_allow_html=True)  # spacing

# --- 3. Sidebar Info ---
st.sidebar.header("About")
st.sidebar.info(
    """
    This tool estimates your paycheck using a rolling deduction multiplier based on your
    actual net pay entries. Enter your hours and optional actual net pay to improve
    accuracy over time. 💡
    """
)

# --- 4. Input Section ---
with st.container():
    st.subheader("Enter Your Work Data")
    hours_input = st.text_input("Hours (HH.MM or HH:MM):")
    actual_net_input = st.text_input("Actual Net Pay (optional):")
    calculate = st.button("Calculate")

if calculate:
    # Parse actual net
    actual_net = float(actual_net_input) if actual_net_input.strip() else None

    # Load history from estimator
    history = load_history()
    result = calculate_pay(hours_input, history=history, actual_net=actual_net)

    # --- 5. Output Section with Metrics ---
    st.markdown("---")
    st.subheader("📊 Paycheck Results")
    st.metric(label="Converted Hours", value=f"{result['total_hours']:.3f}")
    st.metric(label="Regular Hours", value=f"{result['regular_hours']:.2f}")
    st.metric(label="Overtime Hours", value=f"{result['overtime_hours']:.2f}")
    st.metric(label="Gross Pay", value=f"${result['gross']:.2f}")
    st.metric(label="Estimated Net Pay", value=f"${result['net']:.2f}")
    st.metric(label="Effective Hourly Rate", value=f"${result['effective_rate']:.2f}/hr")

    st.markdown("---")
    st.write(f"Current Deduction Multiplier: **{result['deduction']:.4f}**")

    # Calibration update
    if actual_net:
        st.write("### Calibration Update")
        st.write(f"Actual Multiplier: **{result['actual_multiplier']:.4f}**")
        st.success("History Updated ✔️")
