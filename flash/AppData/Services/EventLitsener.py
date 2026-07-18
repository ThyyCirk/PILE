import ustruct as struct
import uctypes
import GlobalVars

# Globally stored listeners: [[address, value_type, last_value, event_callback], ...]
listeners = []

type_map = {
    'char':   ('b', 1), # Signed 1-byte integer / char
    'uchar':  ('B', 1), # Unsigned 1-byte
    'short':  ('h', 2), # Signed 2-byte integer
    'ushort': ('H', 2), # Unsigned 2-byte
    'int':    ('i', 4), # Signed 4-byte integer
    'uint':   ('I', 4), # Unsigned 4-byte integer
    'float':  ('f', 4), # 4-byte Float
    'double': ('d', 8), # 8-byte Double precision float
}

def _read_memory(address, value_type):
    """Helper to read raw memory at an address and unpack it."""
    fmt, size = type_map[value_type]
    raw_bytes = uctypes.bytearray_at(address, size)
    return struct.unpack(f'<{fmt}', raw_bytes)[0]

def addListener(address=None, value_type=None, event=None, current_page_module=None):
    """
    Registers a memory address to be watched.
    """
    if address is None or value_type is None or event is None or current_page_module is None:
        return
    if not callable(event):
        raise ValueError("Event must be a callable function.")
    if value_type not in type_map:
        raise ValueError(f"Unsupported type. Choose from: {list(type_map.keys())}")
    
    # Read the initial value at the address to establish a baseline
    initial_value = _read_memory(address, value_type)
    
    # Store the tracking data
    listeners.append({
        "address": address,
        "type": value_type,
        "last_value": initial_value,
        "event": event
    })

def Listen():
    """
    Call this in your main loop. It checks all registered addresses,
    detects changes, updates the baseline, and triggers the events.
    """
    for item in listeners:
        current_value = _read_memory(item["address"], item["type"])
        
        # If the value changed in memory, trigger the callback
        if current_value != item["last_value"]:
            old_val = item["last_value"]
            item["last_value"] = current_value  # Update baseline
            
            # Fire the event, passing the new and old values
            item["event"](current_value, old_val)
            
def check_delete():
    pass