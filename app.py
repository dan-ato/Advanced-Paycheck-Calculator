import streamlit as st
from estimator.core import load_history, calculate_pay

# --- 1️⃣ Page Setup ---

st.set_page_config(
page_title="Advanced Paycheck Estimator",
page_icon="💰",
layout="centered"
)

# --- 2️⃣ Theme-based colors ---

theme_base = st.get_option("theme.base")
header_color = "#0f4c75" if theme_base == "light" else "#90e0ef"
metric_good = "#0f9d58"  # green
metric_warning = "#f4b400"  # yellow
metric_bad = "#db4437"  # red

# --- 3️⃣ Header with subtle visuals ---

st.markdown(
f""" <div style='background-color:#f0f2f6;padding:20px;border-radius:15px;text-align:center'> <h2 style='color:{header_color}'>💰 Advanced Paycheck Estimator</h2> <p style='color:#333;font-size:14px'>Rolling deduction model with calibration memory</p> </div>
""",
unsafe_allow_html=True
)
st.markdown("<br>", unsafe_allow_html=True)

# --- 4️⃣ Sidebar Extras ---

st.sidebar.header("About & Tips")
st.sidebar.info(
"""
Enter your hours worked (HH.MM or HH:MM). Optionally enter your actual net pay to calibrate the rolling deduction model.

```
This tool becomes more accurate over time as you input actual net pay.
"""
```

)
st.sidebar.write("**Version:** 1.0.2")

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

```
st.markdown("---")
st.subheader("📊 Paycheck Results")

# Conditional color for Effective Rate
eff_rate = result['effective_rate']
if eff_rate >= 13.35:
    eff_color = metric_good
elif 11 <= eff_rate < 13.35:
    eff_color = metric_warning
else:
    eff_color = metric_bad

# Display metrics
col1, col2, col3 = st.columns(3)
col1.metric("Gross Pay", f"${result['gross']:.2f}")
col2.metric("Estimated Net", f"${result['net']:.2f}")
col3.metric("Effective Rate", f"${eff_rate:.2f}/hr", delta=None)

# --- Take-home ratio ---
st.write("### Take-Home Ratio")

deduction_percent = result['deduction']

st.progress(
    min(max(deduction_percent, 0.0), 1.0),
    text=f"{deduction_percent:.1%} of gross pay"
)

st.caption(
    f"Estimated take-home pay is {deduction_percent:.1%} of gross earnings."
)

# --- Hours breakdown ---
st.write("### ⏱️ Hours Breakdown")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Hours",
    f"{result['total_hours']:.2f}"
)

col2.metric(
    "Regular",
    f"{result['regular_hours']:.2f}"
)

col3.metric(
    "Overtime",
    f"{result['overtime_hours']:.2f}"
)

st.markdown(
    f"<p style='color:{eff_color}'>Effective Hourly Rate Status</p>",
    unsafe_allow_html=True
)

# --- One additional hour insight ---
if result['total_hours'] > 0:
    next_result = calculate_pay(
        str(result['total_hours'] + 1),
        history=history
    )

    additional_net = next_result['net'] - result['net']

    st.info(
        f"💡 One additional hour would add approximately "
        f"**${additional_net:.2f}** to your estimated take-home pay."
    )

st.markdown("---")
st.write(f"Current Deduction Multiplier: **{result['deduction']:.4f}**")

if actual_net:
    st.write("### Calibration Update")
    st.write(f"Actual Multiplier: **{result['actual_multiplier']:.4f}**")
    st.success("History Updated ✔️")
```
