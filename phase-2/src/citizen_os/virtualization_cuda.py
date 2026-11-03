"""Educational virtualization, hypervisor and GPU/CUDA execution models."""

HYPERVISOR_TYPES = ("type-1", "type-2")


def create_virtual_machine(name: str, vcpus: int, memory_gb: int,
                           host_cpus: int, host_memory_gb: int,
                           hypervisor_type: str = "type-1") -> dict[str, object]:
    """Validate a VM resource request against host capacity."""
    if not isinstance(name, str) or not name.strip():
        raise ValueError("VM name must be a non-empty string")
    if hypervisor_type not in HYPERVISOR_TYPES:
        raise ValueError("hypervisor_type must be type-1 or type-2")
    values = (vcpus, memory_gb, host_cpus, host_memory_gb)
    if any(not isinstance(value, int) or isinstance(value, bool) for value in values):
        raise ValueError("CPU and memory capacities must be integers")
    if vcpus <= 0 or memory_gb <= 0 or host_cpus <= 0 or host_memory_gb <= 0:
        raise ValueError("CPU and memory capacities must be positive")
    if vcpus > host_cpus or memory_gb > host_memory_gb:
        raise ValueError("VM resource request exceeds host capacity")
    return {
        "name": name.strip(), "state": "configured",
        "virtual_cpus": vcpus, "memory_gb": memory_gb,
        "host_cpus": host_cpus, "host_memory_gb": host_memory_gb,
        "hypervisor_type": hypervisor_type,
        "cpu_utilization_of_host_capacity_percent": round(vcpus / host_cpus * 100, 2),
        "memory_utilization_of_host_capacity_percent": round(memory_gb / host_memory_gb * 100, 2),
        "scope": "Resource configuration model; it does not boot a guest operating system.",
    }


def compare_hypervisors() -> dict[str, object]:
    """Summarize the hosted and bare-metal hypervisor architectures."""
    return {
        "type-1": {
            "name": "Bare-metal hypervisor",
            "placement": "Runs directly on the physical hardware.",
            "examples": ["VMware ESXi", "Microsoft Hyper-V", "Xen"],
            "typical_context": "Data centres and server virtualization.",
        },
        "type-2": {
            "name": "Hosted hypervisor",
            "placement": "Runs as an application on a host operating system.",
            "examples": ["Oracle VirtualBox", "VMware Workstation"],
            "typical_context": "Desktop labs, development and learning.",
        },
        "note": "Examples identify products/platforms; this function does not install or run them.",
    }


def simulate_cuda_vector_add(a: list[int | float], b: list[int | float],
                             threads_per_block: int = 4) -> dict[str, object]:
    """Simulate CUDA grid/block/thread indexing for element-wise vector addition."""
    if len(a) != len(b):
        raise ValueError("input vectors must have equal lengths")
    if not isinstance(threads_per_block, int) or isinstance(threads_per_block, bool) or threads_per_block <= 0:
        raise ValueError("threads_per_block must be a positive integer")
    if any(not isinstance(value, (int, float)) or isinstance(value, bool) for value in a + b):
        raise ValueError("vector elements must be numeric")
    n = len(a)
    blocks = (n + threads_per_block - 1) // threads_per_block
    output: list[int | float | None] = [None] * n
    launched_threads = blocks * threads_per_block
    active_threads = 0
    trace = []
    for block_id in range(blocks):
        for thread_id in range(threads_per_block):
            global_id = block_id * threads_per_block + thread_id
            if global_id < n:
                output[global_id] = a[global_id] + b[global_id]
                active_threads += 1
                trace.append({"block_id": block_id, "thread_id": thread_id,
                              "global_id": global_id, "output": output[global_id]})
    return {
        "input_a": a[:], "input_b": b[:], "output": output,
        "elements": n, "threads_per_block": threads_per_block,
        "blocks_in_grid": blocks, "launched_threads": launched_threads,
        "active_threads": active_threads, "inactive_threads_due_to_bounds": launched_threads - active_threads,
        "thread_trace": trace,
        "scope": "CPU simulation of CUDA indexing; no GPU or CUDA runtime is used.",
    }


def explain_cuda_execution_model() -> dict[str, object]:
    """Return the basic CUDA host/device and grid/block/thread model."""
    return {
        "host": "CPU code allocates/copies data and launches a kernel.",
        "device": "GPU executes many kernel instances in parallel.",
        "hierarchy": {
            "grid": "Collection of thread blocks launched for one kernel.",
            "block": "Group of threads that can cooperate and share block-level resources.",
            "thread": "One execution instance identified by its indices.",
        },
        "common_global_index": "blockIdx.x * blockDim.x + threadIdx.x",
        "bounds_check": "if (global_id < number_of_elements) before accessing arrays.",
        "note": "Conceptual CUDA explanation; actual kernel execution requires CUDA-capable hardware and a CUDA toolchain.",
    }


def run_virtualization_demo() -> dict[str, object]:
    return {
        "vm": create_virtual_machine("OS-Lab-VM", 2, 4, 8, 16, "type-2"),
        "hypervisors": compare_hypervisors(),
    }


def run_cuda_demo() -> dict[str, object]:
    return {
        "execution_model": explain_cuda_execution_model(),
        "vector_addition": simulate_cuda_vector_add([1, 2, 3, 4, 5, 6, 7],
                                                     [10, 20, 30, 40, 50, 60, 70], 4),
    }