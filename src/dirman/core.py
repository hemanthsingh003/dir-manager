import json
import os
from pathlib import Path
from typing import Optional


SENSITIVE_FILES = [
    ".env",
    ".env.local",
    ".env.production",
    ".env.development",
    "credentials.json",
    "secrets.json",
    "config/secrets.py",
    "secrets.txt",
    "api_keys.json",
    ".npmrc",
    ".pypirc",
    "id_rsa",
    "id_rsa.pub",
    "*.pem",
    "*.key",
]


class DirManager:
    def __init__(self, store_path: Optional[Path] = None):
        if store_path is None:
            store_path = Path.home() / ".dirman" / "data.json"
        self.store_path = store_path
        self._ensure_store()

    def _ensure_store(self):
        self.store_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.store_path.exists():
            self._save({})

    def _load(self) -> dict:
        with open(self.store_path) as f:
            return json.load(f)

    def _save(self, data: dict):
        with open(self.store_path, "w") as f:
            json.dump(data, f, indent=2)

    def _check_sensitive_files(self, path: Path) -> list[str]:
        found = []
        gitignore_path = path / ".gitignore"
        ignored_patterns = set()

        if gitignore_path.exists():
            with open(gitignore_path) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        ignored_patterns.add(line)

        for pattern in SENSITIVE_FILES:
            if "*" in pattern:
                import fnmatch

                for file in path.iterdir():
                    if file.is_file() and fnmatch.fnmatch(file.name, pattern):
                        if pattern not in ignored_patterns:
                            found.append(str(file.relative_to(path)))
            else:
                file_path = path / pattern
                if file_path.exists() and pattern not in ignored_patterns:
                    found.append(pattern)

        return found

    def init(self, name: str, path: str) -> str:
        data = self._load()
        abs_path = Path(path).resolve()
        if not abs_path.exists():
            return f"Error: Path '{abs_path}' does not exist"
        if name in data:
            return f"Directory '{name}' already tracked"

        sensitive = self._check_sensitive_files(abs_path)
        if sensitive:
            return f"Error: Sensitive files found and not in .gitignore: {', '.join(sensitive)}\nPlease add them to .gitignore before tracking"

        data[name] = {"path": str(abs_path)}
        self._save(data)
        return f"Initialized directory '{name}' at {abs_path}"

    def add(self, name: str, path: str) -> str:
        return self.init(name, path)

    def remove(self, name: str) -> str:
        data = self._load()
        if name not in data:
            return f"Directory '{name}' not found"
        del data[name]
        self._save(data)
        return f"Removed directory '{name}'"

    def list(self) -> list:
        data = self._load()
        return [(name, info["path"]) for name, info in data.items()]

    def status(self) -> list:
        data = self._load()
        result = []
        for name, info in data.items():
            path = Path(info["path"])
            exists = path.exists()
            result.append({"name": name, "path": info["path"], "exists": exists})
        return result

    def get(self, name: str) -> Optional[dict]:
        data = self._load()
        return data.get(name)
