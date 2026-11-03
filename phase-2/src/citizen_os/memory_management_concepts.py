"""Conceptual overview of operating-system memory-management functions."""

def explain_memory_management_functions() -> dict[str, str]:
    """Return concise explanations of the OS memory manager responsibilities."""
    return {
        "tracking": "Keeps records of which memory regions and frames are free, allocated, or assigned to processes.",
        "allocation": "Assigns memory to processes when needed and reclaims it when processes release memory or terminate.",
        "address_translation": "Maps a process virtual/logical addresses to physical memory using mechanisms such as page tables or segment tables.",
        "protection": "Enforces access permissions so a process cannot access memory it is not authorized to read, write, or execute.",
        "sharing": "Allows controlled sharing of memory regions between processes when appropriate, while preserving protection boundaries.",
        "virtual_memory": "Maintains the illusion of a large, private address space and brings required pages into RAM when they are needed.",
        "fragmentation_management": "Tracks and helps manage wasted space caused by internal or external fragmentation, depending on the allocation scheme.",
        "note": "These are conceptual OS responsibilities. This project demonstrates selected ideas in user-space simulations; it does not implement a kernel memory manager.",
    }
