"""Explicit lock-variable and process-type teaching material for Module 3."""

def simulate_lock_variable_race() -> dict[str, object]:
    """Show why a shared Boolean lock variable alone is not mutual exclusion.

    This is a deterministic interleaving model, not a threaded Python lock.
    Both processes read False before either writes True, so both enter.
    """
    lock = False
    trace: list[dict[str, object]] = []
    p1_observed = lock
    trace.append({"process": "P1", "action": "check", "observed_locked": p1_observed})
    p2_observed = lock
    trace.append({"process": "P2", "action": "check", "observed_locked": p2_observed})
    p1_enters = not p1_observed
    if p1_enters:
        lock = True
        trace.append({"process": "P1", "action": "set_lock_and_enter"})
    p2_enters = not p2_observed
    if p2_enters:
        lock = True
        trace.append({"process": "P2", "action": "set_lock_and_enter"})
    return {"initial_lock": False, "trace": trace,
            "processes_entered_critical_section": [p for p, entered in (("P1", p1_enters), ("P2", p2_enters)) if entered],
            "mutual_exclusion_violated": p1_enters and p2_enters,
            "lesson": "Check-then-set is not atomic; a lock variable alone cannot guarantee mutual exclusion."}

def explain_process_types() -> dict[str, object]:
    """Summarize common process classifications; course terminology may vary."""
    return {
        "independent_process": "A process that does not directly share data or depend on another process state.",
        "cooperating_process": "A process that can affect or be affected by other processes, commonly through shared data or IPC.",
        "cpu_bound_process": "Spends a relatively large portion of its execution doing computation.",
        "io_bound_process": "Spends a relatively large portion of its execution waiting for input/output operations.",
        "note": "These are common OS classifications. Confirm the exact classification expected by the instructor lecture notes.",
    }

def run_lock_variable_demo() -> dict[str, object]:
    return simulate_lock_variable_race()
