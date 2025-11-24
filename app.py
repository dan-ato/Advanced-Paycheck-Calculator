import streamlit as st
from estimator.core import load_history, calculate_pay

st.title("Advanced Paycheck Estimator")
st.caption("Rolling deduction model with calibration memory")

hours_input = st.text_input("Hours (HH.MM or HH:MM)")
actual_net_input = st.text_input("Actual Net Pay (optional)")

if st.button("Calculate"):
    actual_net = float(actual_net_input) if actual_net_input.strip() else None

    history = load_history()
    result = calculate_pay(hours_input, history=history, actual_net=actual_net)

    st.subheader("Results")
    st.write(f"Converted Hours: **{result['total_hours']:.3f}**")
    st.write(f"Regular: **{result['regular_hours']:.2f}** hours")
    st.write(f"Overtime: **{result['overtime_hours']:.2f}** hours")
    st.write(f"Gross Pay: **${result['gross']:.2f}**")
    st.write(f"Estimated Net: **${result['net']:.2f}**")
    st.write(f"Effective Rate: **${result['effective_rate']:.2f}/hr**")

    st.write("---")
    st.write(f"Current Deduction Multiplier: **{result['deduction']:.4f}**")

    if actual_net:
        st.write("### Calibration Update")
        st.write(f"Actual Multiplier: **{result['actual_multiplier']:.4f}**")
        st.write("History Updated ✔️")

