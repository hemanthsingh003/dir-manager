# DirManager

A Git-like CLI tool for managing directories. Track and manage your project directories with simple commands.

## Features

- **Track directories** - Add directories by name and path
- **List directories** - View all tracked directories
- **Check status** - Verify if tracked directories exist
- **Get details** - View details of a specific directory
- **Remove tracking** - Remove directories from tracking

## Installation

### Quick Install (macOS/Linux/Windows)

```bash
pipx install git+https://github.com/hemanthsingh003/dir-manager.git
```

### Requirements

- Python 3.8 or higher
- [pipx](https://pipx.pypa.io/) (install via: `python -m pip install pipx`)

### Uninstall

```bash
pipx uninstall dirm
```

## Usage

### Initialize/Add a directory

```bash
dirm init <name> <path>
dirm add <name> <path>
```

Example:
```bash
dirm init projects ~/Projects
dirm add work ~/Documents/work
```

### List all tracked directories

```bash
dirm list
```

### Check status of directories

```bash
dirm status
```

Output shows ✓ for existing directories and ✗ for missing ones:
```
✓ projects: /Users/hemanth/Projects
✗ work: /Users/hemanth/Documents/work
```

### Get details of a directory

```bash
dirm get <name>
```

### Remove a directory from tracking

```bash
dirm remove <name>
```

## Command-Line Options

| Command | Description |
|---------|-------------|
| `init <name> <path>` | Initialize/add a directory |
| `add <name> <path>` | Add a directory (alias for init) |
| `remove <name>` | Remove a directory from tracking |
| `list` | List all tracked directories |
| `status` | Show status of tracked directories |
| `get <name>` | Get details of a tracked directory |

## Project Structure

```
dir-manager/
├── pyproject.toml          # Project metadata and dependencies
├── README.md               # This file
└── src/
    └── dirman/
        ├── __init__.py     # Package entry point
        ├── cli.py          # CLI logic
        └── core.py         # Core functionality
```

## License

MIT License
