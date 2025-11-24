import json
import os

BASE_RATE = 12.35
OVERTIME_MULTIPLIER = 1.5
REGULAR_HOURS = 80

HISTORY_FILE = os.path.join(os.path.dirname(__file__), "deduction_history.json")


def load_history():
    """Load deduction history from JSON."""
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []


def save_history(history):
    """Write deduction history to JSON."""
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f)


def parse_hours(hours_input: str) -> float:
    """
    Convert HH.MM or HH:MM into decimal hours.
    - "42:30" → 42.5
    - "37.25" → 37.25 (interpreting .25 as minutes * 100)
    """
    if ":" in hours_input:
        h, m = hours_input.split(":")
        hours = int(h)
        minutes = int(m)
    else:
        total = float(hours_input)
        hours = int(total)
        minutes = round((total - hours) * 100)

    return hours + (minutes / 60)


def calculate_pay(hours_input: str, history=None, actual_net=None):
    """
    Core calculation engine. Returns a dict with all computed values.
    """

    history = history or load_history()

    # Deduction multiplier (rolling average)
    deduction = (
        sum(history) / len(history)
        if history else
        0.8858  # Default calibration value
    )

    total_hours = parse_hours(hours_input)
    regular_hours = min(total_hours, REGULAR_HOURS)
    overtime_hours = max(total_hours - REGULAR_HOURS, 0)

    gross = (regular_hours * BASE_RATE) + (
        overtime_hours * BASE_RATE * OVERTIME_MULTIPLIER
    )

    net = gross * deduction
    eff_rate = net / total_hours if total_hours > 0 else 0

    result = {
        "hours_input": hours_input,
        "total_hours": total_hours,
        "regular_hours": regular_hours,
        "overtime_hours": overtime_hours,
        "gross": gross,
        "net": net,
        "deduction": deduction,
        "effective_rate": eff_rate,
        "updated_history": history[:],  # copy
    }

    # Update history if actual paycheck provided
    if actual_net:
        actual_multiplier = actual_net / gross if gross > 0 else deduction
        result["actual_multiplier"] = actual_multiplier

        history.append(actual_multiplier)
        save_history(history)

        result["updated_history"] = history

    return result
