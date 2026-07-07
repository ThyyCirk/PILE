import os, json

class FileManager:
    _cache = {}
    _loaded_files = set()

    @staticmethod
    def _load(file):
        if file in FileManager._loaded_files:
            return
        FileManager._cache[file] = {}
        try:
            with open(file) as f:
                for line in f:
                    line = line.strip()
                    if not line or "=" not in line:
                        continue
                    k, v = line.split("=", 1)
                    FileManager._cache[file][k.strip()] = v.strip()
        except OSError:
            pass  # file doesn't exist yet
        FileManager._loaded_files.add(file)

    @staticmethod
    def search(name, file="/flash/libs/data.txt"):
        FileManager._load(file)
        return FileManager._cache[file].get(name)

    @staticmethod
    def write(name, new_value, file="/flash/libs/data.txt"):
        FileManager._load(file)
        FileManager._cache[file][name] = str(new_value)
        FileManager._flush(file)

    @staticmethod
    def _flush(file):
        tmp_name = file + ".tmp"
        with open(tmp_name, "w") as f:
            for k, v in FileManager._cache[file].items():
                f.write(f"{k}={v}\n")
        try:
            os.remove(file)
        except OSError:
            pass
        os.rename(tmp_name, file)