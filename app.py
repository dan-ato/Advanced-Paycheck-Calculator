import streamlit as st
from estimator.core import load_history, calculate_pay

# --- 1️⃣ Page Setup ---
st.set_page_config(
    page_title="Paycheck Estimator",
    page_icon="💰",
    layout="centered"
)

# --- 2️⃣ Theme-based colors ---
theme_base = st.get_option("theme.base")

header_color = "#0f4c75" if theme_base == "light" else "#90e0ef"
metric_good = "#0f9d58"
metric_warning = "#f4b400"
metric_bad = "#db4437"

# --- 3️⃣ Header ---
st.markdown(
    f"""
    <div style="
        background-color:#f0f2f6;
        padding:24px;
        border-radius:15px;
        text-align:center;
        margin-bottom:20px;
    ">
        <h1 style="
            color:{header_color};
            margin-bottom:5px;
        ">
            💰 Paycheck Estimator
        </h1>

        <p style="
            color:#555;
            font-size:15px;
            margin-bottom:0px;
        ">
            Estimate your take-home pay from hours worked.
        </p>

        <p style="
            color:#888;
            font-size:12px;
            margin-top:6px;
        ">
            Rolling deduction model • Calibrated with your actual pay
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# --- 4️⃣ Sidebar ---
st.sidebar.header("About & Tips")

st.sidebar.info(
    """
    Enter your hours worked using:

    **HH.MM** or **HH:MM**

    Example:
    `42:30` = 42 hours 30 minutes

    You can optionally enter your actual net paycheck to improve the calculator's future estimates.
    """
)

st.sidebar.divider()

st.sidebar.caption("Personal paycheck estimator")
st.sidebar.caption("Version 1.1")

# --- 5️⃣ Input Section ---
st.subheader("Enter Your Work Data")

col1, col2 = st.columns(2)

with col1:
    hours_input = st.text_input(
        "Hours Worked",
        placeholder="e.g. 84:30"
    )

with col2:
    actual_net_input = st.text_input(
        "Actual Net Pay",
        placeholder="Optional"
    )

calculate = st.button(
    "Calculate Paycheck",
    type="primary",
    use_container_width=True
)

# --- 6️⃣ Process Calculation ---
if calculate:

    # Validate hours input
    if not hours_input.strip():
        st.warning("Enter your hours worked first.")
        st.stop()

    # Validate actual net input
    try:
        actual_net = (
            float(actual_net_input)
            if actual_net_input.strip()
            else None
        )
    except ValueError:
        st.error("Actual net pay must be a number.")
        st.stop()

    # Load history and calculate
    history = load_history()

    try:
        result = calculate_pay(
            hours_input,
            history=history,
            actual_net=actual_net
        )
    except (ValueError, TypeError):
        st.error(
            "I couldn't interpret those hours. "
            "Try something like `84:30` or `84.30`."
        )
        st.stop()

    # --- Results ---
    st.divider()

    st.subheader("📊 Paycheck Results")

    # Main paycheck metrics
    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Gross Pay",
        f"${result['gross']:,.2f}"
    )

    col2.metric(
        "Estimated Net",
        f"${result['net']:,.2f}"
    )

    col3.metric(
        "Effective Rate",
        f"${result['effective_rate']:.2f}/hr"
    )

    # --- Take-home ratio ---
    st.write("### Take-Home Ratio")

    deduction_percent = result["deduction"]

    st.progress(
        min(max(deduction_percent, 0.0), 1.0),
        text=f"{deduction_percent:.1%} of gross pay"
    )

    st.caption(
        f"Your current model estimates that you keep "
        f"{deduction_percent:.1%} of gross earnings after deductions."
    )

    # --- Hours breakdown ---
    st.divider()

    st.subheader("⏱️ Hours Breakdown")

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

    # --- Effective hourly rate status ---
    eff_rate = result["effective_rate"]

    if eff_rate >= 13.35:
        eff_color = metric_good
        rate_message = "Your estimated take-home rate is above your base hourly rate."
    elif eff_rate >= 11:
        eff_color = metric_warning
        rate_message = "Your estimated take-home rate reflects normal payroll deductions."
    else:
        eff_color = metric_bad
        rate_message = "Your estimated take-home rate is significantly below your base rate."

    st.markdown(
        f"""
        <div style="
            padding:12px 16px;
            border-radius:10px;
            background-color:#f8f9fa;
            border-left:5px solid {eff_color};
            margin-top:10px;
        ">
            <strong>Effective Hourly Rate</strong><br>
            <span style="color:{eff_color};">
                ${eff_rate:.2f}/hr
            </span>
            <br>
            <small>{rate_message}</small>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --- Marginal hour insight ---
    if result["total_hours"] > 0:

        next_hour_result = calculate_pay(
            str(result["total_hours"] + 1),
            history=history
        )

        marginal_net = (
            next_hour_result["net"] - result["net"]
        )

        st.divider()

        st.success(
            f"💰 **One additional hour** would add approximately "
            f"**${marginal_net:.2f}** to your take-home pay."
        )

    # --- Calibration information ---
    st.divider()

    st.subheader("🧠 Model Calibration")

    col1, col2 = st.columns(2)

    col1.metric(
        "Deduction Multiplier",
        f"{result['deduction']:.4f}"
    )

    col2.metric(
        "Paychecks Recorded",
        f"{len(result['updated_history'])}"
    )

    st.caption(
        "The calculator uses your historical net-to-gross ratios "
        "to make future estimates more personalized."
    )

    # --- Actual paycheck calibration ---
    if actual_net:

        st.divider()

        st.subheader("✅ Calibration Update")

        col1, col2 = st.columns(2)

        col1.metric(
            "Actual Net Pay",
            f"${actual_net:,.2f}"
        )

        col2.metric(
            "Actual Multiplier",
            f"{result['actual_multiplier']:.4f}"
        )

        difference = actual_net - result["net"]

        if difference >= 0:
            st.success(
                f"Actual paycheck was ${abs(difference):.2f} "
                f"higher than the original estimate."
            )
        else:
            st.info(
                f"Actual paycheck was ${abs(difference):.2f} "
                f"lower than the original estimate."
            )

        st.success(
            "History updated. Future estimates will use this paycheck."
        )

    # --- Calculation details ---
    with st.expander("🔍 Calculation Details"):

        st.write(
            f"**Base hourly rate:** ${13.35:.2f}"
        )

        st.write(
            f"**Overtime multiplier:** 1.5×"
        )

        st.write(
            f"**Overtime rate:** ${13.35 * 1.5:.2f}/hr"
        )

        st.write(
            f"**Deduction multiplier:** "
            f"{result['deduction']:.4f}"
        )

        st.write(
            f"**Gross pay:** "
            f"${result['gross']:,.2f}"
        )

        st.write(
            f"**Estimated net pay:** "
            f"${result['net']:,.2f}"
        )

# --- Footer ---
st.divider()

st.caption(
    "Personal paycheck estimator • "
    "Calibrated against your actual pay history"
)
