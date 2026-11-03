"""Effective-access-time calculations for demand-paging performance study."""

def effective_access_time(memory_access_time: float, page_fault_rate: float,
                          page_fault_service_time: float) -> dict[str, float]:
    """Calculate EAT = (1-p)*ma + p*(page_fault_service_time + ma).

    page_fault_service_time is the additional service cost of handling a fault,
    excluding the final memory access after the page is resident.
    """
    values = (memory_access_time, page_fault_rate, page_fault_service_time)
    if any(not isinstance(value, (int, float)) or isinstance(value, bool) for value in values):
        raise ValueError("all inputs must be numeric")
    if memory_access_time <= 0 or page_fault_service_time < 0:
        raise ValueError("memory access time must be positive and fault service time non-negative")
    if not 0 <= page_fault_rate <= 1:
        raise ValueError("page_fault_rate must be between 0 and 1")
    eat = (1 - page_fault_rate) * memory_access_time + page_fault_rate * (page_fault_service_time + memory_access_time)
    return {"memory_access_time": float(memory_access_time),
            "page_fault_rate": float(page_fault_rate),
            "page_fault_service_time": float(page_fault_service_time),
            "effective_access_time": eat,
            "slowdown_factor": eat / memory_access_time}

def compare_demand_paging_scenarios(memory_access_time: float = 100.0,
                                    page_fault_service_time: float = 8000000.0) -> dict[str, object]:
    """Compare EAT at illustrative fault rates; times use the same unit (ns)."""
    rates = (0.0, 0.000001, 0.0001, 0.001)
    return {"unit": "nanoseconds", "assumptions": {
                "memory_access_time_ns": memory_access_time,
                "page_fault_service_time_ns": page_fault_service_time,
                "meaning": "Illustrative assumptions, not measurements from the project machine."},
            "scenarios": [effective_access_time(memory_access_time, rate, page_fault_service_time)
                          for rate in rates]}
