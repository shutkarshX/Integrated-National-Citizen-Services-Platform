"""Educational loading, linking, relocation and address-binding simulations."""
from collections.abc import Mapping, Sequence


def bind_address(relative_address: int, load_base: int, segment_size: int) -> int:
    """Translate a valid module-relative address to an absolute address."""
    values = (relative_address, load_base, segment_size)
    if any(not isinstance(v, int) or isinstance(v, bool) for v in values):
        raise ValueError("address and size values must be integers")
    if relative_address < 0 or load_base < 0 or segment_size <= 0:
        raise ValueError("addresses must be non-negative and segment_size positive")
    if relative_address >= segment_size:
        raise ValueError("relative address is outside the module")
    return load_base + relative_address


def link_modules(modules: Sequence[Mapping[str, object]]) -> dict[str, object]:
    """Build a global symbol table and resolve each module external reference.

    Each module supplies a name, a mapping of exported symbol to relative
    address, and a sequence of required external symbol names.
    """
    symbol_table = {}
    for module in modules:
        name = module.get("name")
        exports = module.get("exports", {})
        if not isinstance(name, str) or not name:
            raise ValueError("each module must have a non-empty name")
        if not isinstance(exports, Mapping):
            raise ValueError("module exports must be a mapping")
        for symbol, address in exports.items():
            if not isinstance(symbol, str) or not symbol:
                raise ValueError("exported symbol names must be non-empty strings")
            if not isinstance(address, int) or isinstance(address, bool) or address < 0:
                raise ValueError("exported symbol addresses must be non-negative integers")
            if symbol in symbol_table:
                raise ValueError(f"duplicate symbol: {symbol}")
            symbol_table[symbol] = {"module": name, "relative_address": address}

    resolutions = {}
    for module in modules:
        name = module["name"]
        required = module.get("requires", [])
        if not isinstance(required, Sequence) or isinstance(required, (str, bytes)):
            raise ValueError("module requires must be a sequence of symbol names")
        for symbol in required:
            if symbol not in symbol_table:
                raise ValueError(f"unresolved external symbol: {symbol}")
            resolutions[f"{name}:{symbol}"] = dict(symbol_table[symbol])
    return {"symbol_table": symbol_table, "resolutions": resolutions,
            "linked": True, "modules": [module["name"] for module in modules]}


def load_modules(modules: Sequence[Mapping[str, object]], start_address: int = 4096) -> dict[str, object]:
    """Assign consecutive load addresses to modules and relocate their exports."""
    if not isinstance(start_address, int) or isinstance(start_address, bool) or start_address < 0:
        raise ValueError("start_address must be a non-negative integer")
    cursor = start_address
    placements, relocated_symbols = {}, {}
    for module in modules:
        name, size = module.get("name"), module.get("size")
        exports = module.get("exports", {})
        if not isinstance(name, str) or not name:
            raise ValueError("each module must have a non-empty name")
        if not isinstance(size, int) or isinstance(size, bool) or size <= 0:
            raise ValueError("module size must be a positive integer")
        if not isinstance(exports, Mapping):
            raise ValueError("module exports must be a mapping")
        placements[name] = {"load_base": cursor, "size": size}
        for symbol, relative in exports.items():
            if not isinstance(relative, int) or isinstance(relative, bool) or not 0 <= relative < size:
                raise ValueError(f"export {symbol} is outside module {name}")
            if symbol in relocated_symbols:
                raise ValueError(f"duplicate symbol: {symbol}")
            relocated_symbols[symbol] = cursor + relative
        cursor += size
    return {"placements": placements, "relocated_symbols": relocated_symbols,
            "next_free_address": cursor}


def run_loading_linking_demo() -> dict[str, object]:
    modules = [
        {"name": "application", "size": 256, "exports": {"main": 0}, "requires": ["calculate_tax"]},
        {"name": "tax_library", "size": 128, "exports": {"calculate_tax": 32}, "requires": []},
    ]
    linked = link_modules(modules)
    loaded = load_modules(modules, start_address=4096)
    return {
        "linking": linked,
        "loading": loaded,
        "address_binding_example": {
            "relative_address": 32, "load_base": loaded["placements"]["tax_library"]["load_base"],
            "absolute_address": bind_address(32, loaded["placements"]["tax_library"]["load_base"], 128),
        },
        "concepts": {
            "compile_time_binding": "Absolute addresses are fixed when the program is compiled; relocation is limited.",
            "load_time_binding": "The loader chooses a load base and adjusts relocatable addresses before execution.",
            "execution_time_binding": "Address translation is deferred while the process runs, typically using hardware support.",
            "linking": "The linker resolves external symbol references between separately compiled modules.",
            "loading": "The loader places the executable modules into memory and prepares them for execution.",
        },
        "scope": "A user-space model of symbol resolution, module placement and relocation; not an actual executable loader or MMU.",
    }