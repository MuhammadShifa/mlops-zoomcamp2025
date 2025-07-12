## 🧼 Code Quality: Linting and Formatting

In this lesson, we focus on improving **code quality** from a **style and maintainability** perspective. While previous topics emphasized testing and correctness, this section ensures that our code also looks clean, readable, and consistent — following established style conventions.

### 🔍 What is Linting?

One key aspect of code quality is **linting** — the process of automatically analyzing code to detect potential errors, stylistic issues, or deviations from best practices. This is done using tools called **linters**.

**Linters** are tools that analyze your code without running it (static analysis) and report issues related to:
- Style violations (e.g., spacing, naming)
- Code smells (e.g., unused imports, reassigning built-ins)
- Potential bugs
  
There are several linters available in the Python ecosystem such as:
- `pylint` – comprehensive static analysis and style checking
- `flake8` – lightweight linter with plugin support
- `pyflakes` – focused on logic errors without stylistic rules
- `ruff` – ultra-fast linter combining functionality of others

In this module, we'll focus on `pylint` for its strong rule set and ability to detect both stylistic issues and code bugs.

---

### 🛠 Tool: `pylint`

We'll use `pylint` for linting. It not only checks for PEP8 compliance but also detects deeper issues like:
- Use of global variables
- Missing docstrings
- Unused arguments or imports

#### 🔧 Installation & Setup

```bash
pipenv install --dev pylint
pipenv shell
```

Run `pylint` on a single file:
```bash
pylint model.py
```

Run on the entire project recursively:
```bash
pylint --recursive=y .
```

This command will show warnings such as missing docstrings, extra whitespaces, or unused variables.

---

### 🧪 Example Warning and Fix

Example warning: `missing-function-docstring`

To fix it:

```python
def get_model_location(run_id):
    """Method to get the model location from S3 or locally."""
    model_location = os.getenv('MODEL_LOCATION')
    if model_location is not None:
        return model_location
```

---

### ⚠️ Suppressing Warnings

#### Option 1: Inline Comment
```python
# pylint: disable=unused-argument
```

#### Option 2: `.pylintrc` Configuration File

Create a `.pylintrc` file in your project directory:

```ini
[MESSAGES CONTROL]
disable=missing-function-docstring, missing-class-docstring, missing-final-newline
```

This disables repeated warnings across the codebase.

---

### 📦 Central Config with `pyproject.toml`

Instead of using multiple config files, modern Python tools prefer a central config file: `pyproject.toml`.

Example for `pylint`, `black`, and `isort`:

```toml
[tool.black]
line-length = 88
target-version = ['py39']
skip-string-normalization = true

[tool.isort]
multi_line_output = 3
length_sort = true
```

---

### 🎨 Code Formatting with `black`

**Black** is an uncompromising Python code formatter. It formats code automatically to follow PEP8. Unlike linters, it changes the code directly.

#### 🔧 Install and Run

```bash
pipenv install --dev black

black --diff . | less                 # Show diff only
black -S --diff . | less              # Keep single quotes
black .                               # Apply formatting to all files
```

Use the `-S` or `--skip-string-normalization` flag if you want to avoid auto-converting quotes to double quotes.

---

### 📚 Import Sorting with `isort`

**isort** organizes imports alphabetically and by group. This keeps imports tidy and consistent.

#### 🔧 Install and Run

```bash
pipenv install --dev isort

isort --diff . | less                 # Show what changes would be made
isort .                               # Apply sorting
```

Add configuration to `pyproject.toml`:

```toml
[tool.isort]
multi_line_output = 3
length_sort = true
```

---

### ✅ Pre-Push Code Checks

Before pushing code, make sure:
1. All linter and formatter checks pass
2. All tests pass
3. Exit code is zero

Run:

```bash
isort .
black .
pylint --recursive=y .
pytest tests/
echo $?   # Should return 0
```

If `echo $?` returns a non-zero code, Git hooks or CI might block the push.

---

### ✅ Summary

- ✅ `pylint` checks code for issues and style problems
- ✅ `black` formats code automatically
- ✅ `isort` sorts import statements
- ✅ `pyproject.toml` can be used to configure all tools in one place
- ✅ Run all tools and tests before pushing code

By combining linting, formatting, and testing, we ensure our code is not just working — but clean, readable, and ready for production!

---

### Reference
- [Pylint Configuration](https://www.codeac.io/documentation/pylint-configuration.html#:~:text=fail%2Don%3D-,%5BMESSAGES%20CONTROL%5D,-%23%20Only%20show%20warnings)
- [Pep 8](https://peps.python.org/pep-0008/)
- [pyproject.toml](https://packaging.python.org/en/latest/specifications/pyproject-toml/)
- [Black Configuration](https://black.readthedocs.io/en/stable/usage_and_configuration/the_basics.html#:~:text=%5Btool.black%5D%0Aline%2Dlength%20%3D%2088%0Atarget%2Dversion%20%3D%20%5B%27py37%27%5D)
- [isort configuration](https://pycqa.github.io/isort/docs/configuration/config_files.html#:~:text=%5Bisort%5D%0Aprofile%20%3D%20black%0Amulti_line_output%20%3D%203)
