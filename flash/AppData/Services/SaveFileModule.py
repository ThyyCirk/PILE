## IMPORTANT SEARCH SAVE FILE MODULE, DONT DELETE

import os, sys
saveFile = "/flash/libs/data.txt"

class FileManager:
    def search(Name, file=saveFile):
        inside_block = False
        result = []

        with open(file) as f:
            for line in f:
                line = line.strip()

                # Start of block
                if line == Name + "=[":
                    inside_block = True
                    continue

                # Normal key=value (only if not in a block)
                if not inside_block and line.startswith(Name + "="):
                    return line.split("=", 1)[1]

                # Inside block
                if inside_block:
                    if line == "]":
                        return result
                    if "=" in line:
                        k, v = line.split("=", 1)
                        result.append((k.strip(), v.strip()))

        return None
    
    def write(Name, new_value, File=saveFile):
        tmp_name = File + ".tmp"
        found = False

        is_block = isinstance(new_value, dict)

        with open(File, "r") as src, open(tmp_name, "w") as tmp:
            inside_block = False

            for line in src:
                stripped = line.strip()

                # Check if we're entering a block
                if stripped == f"{Name}=[":
                    found = True
                    inside_block = True
                    tmp.write(f"{Name}=[\n")

                    # Write the new block content
                    if is_block:
                        for k, v in new_value.items():
                            tmp.write(f"{k}={v}\n")
                    else:
                        tmp.write(f"value={new_value}\n")

                    # Skip old block lines
                    continue

                # Skip old block lines
                if inside_block:
                    if stripped == "]":
                        inside_block = False
                    continue

                # Handle normal key=value lines
                if not inside_block and stripped.startswith(Name + "="):
                    found = True
                    if not is_block:
                        tmp.write(f"{Name}={new_value}\n")
                    else:
                        tmp.write(f"{Name}=[\n")
                        for k, v in new_value.items():
                            tmp.write(f"{k}={v}\n")
                        tmp.write("]\n")
                    continue

                # Otherwise, copy line as-is
                tmp.write(line)

            # If not found, append at the end
            if not found:
                if is_block:
                    tmp.write(f"{Name}=[\n")
                    for k, v in new_value.items():
                        tmp.write(f"{k}={v}\n")
                    tmp.write("]\n")
                else:
                    tmp.write(f"{Name}={new_value}\n")

        # Replace old file safely (MicroPython-compatible)
        try:
            os.remove(File)
        except OSError:
            pass
        os.rename(tmp_name, File)
