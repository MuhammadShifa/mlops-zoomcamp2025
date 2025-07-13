# 🧱 Next Module: Makefiles and `make`

Welcome to the next step in your MLOps journey!

In the previous modules, we covered:
- ✅ Git pre-commit hooks
- ✅ Code linting and formatting
- ✅ Unit and integration testing

Now it’s time to automate all these tasks with one powerful tool: **`make` and Makefiles**.

---

## 🧠 What Is `make`?

`make` is a command-line tool used to automate repetitive tasks. It reads instructions from a file called `Makefile` and executes a sequence of commands — **automating testing, building, formatting, deployments, and more**.

We define our **targets** (e.g., `test`, `build`, `run`), and then simply call:

```bash
make test
make build
make run
```

> Think of it like your project’s mini-orchestrator 🚀

---

## 🧰 Installing `make`

### 🖥️ macOS
Already pre-installed (via Xcode Command Line Tools).

### 🐧 Ubuntu/Linux
```bash
sudo apt update && sudo apt install build-essential
```

### 🪟 Windows (via Chocolatey)
```bash
choco install make
```

Restart your terminal after installation.

---

## 🚀 First Makefile Example

Create a file named `Makefile` (no extension!) in your project directory — for example, inside `06-best-practices/code`.

### 📝 Basic Example

```makefile
run:
  echo 123
```

Run it with:

```bash
make run
```

**Output:**
```
echo 123
123
```

✅ `make` found the `run` target and executed the command inside.

---

## 🔗 Connecting Targets (Dependencies)

Targets can **depend on other targets**. For example:

```makefile
test:
	echo "Running tests"

run: test
	echo "Running main app"
```

When you run:

```bash
make run
```

Output:
```
echo "Running tests"
Running tests
echo "Running main app"
Running main app
```

🎯 `run` depends on `test`, so it runs `test` first.

You can add **multiple dependencies**:

```makefile
test:
	echo "Tests running"

other_things:
	echo "Doing other things"

run: test other_things
	echo "Running main"
```

```bash
make run
```

Output:
```
echo "Tests running"
Tests running
echo "Doing other things"
Doing other things
echo "Running main"
Running main
```

---

## 🧪 Real-World Project Automation

Let’s write a Makefile that automates testing, linting, Docker builds, integration tests, and publishing.

```makefile
LOCAL_TAG := $(shell date +"%Y-%m-%d-%H-%M")
LOCAL_IMAGE_NAME := stream-model-duration:$(LOCAL_TAG)

# 🔬 Unit tests
test:
	pytest tests/

# 🎨 Linting and formatting
quality_checks:
	isort .
	black .
	pylint --recursive=y .

# 🛠️ Build Docker image (depends on tests and code quality)
build: quality_checks test
	docker build -t $(LOCAL_IMAGE_NAME) .

# 🧪 Integration tests (depends on build)
integration_test: build
	LOCAL_IMAGE_NAME=$(LOCAL_IMAGE_NAME) bash integration-test/run.sh

# 🚀 Publish Docker image (depends on everything)
publish: build integration_test
	LOCAL_IMAGE_NAME=$(LOCAL_IMAGE_NAME) bash scripts/publish.sh

# ⚙️ Project setup
setup:
	pipenv install --dev
	pre-commit install
```

---

## 🧪 How to Use It

You can run each command like this:

### Install dependencies:
```bash
make setup
```

### Run tests:
```bash
make test
```

### Format and lint:
```bash
make quality_checks
```

### Build Docker image:
```bash
make build
```

### Run integration tests:
```bash
make integration_test
```

### Publish to container registry:
```bash
make publish
```

---

## 📦 Why Use Make?

✅ Saves time — no need to remember long CLI commands  
✅ Reduces human error — everything is version-controlled  
✅ Acts like a mini-orchestrator  
✅ Portable — works on Linux, macOS, Windows  
✅ Great for CI/CD pipelines and teamwork  

---

## ⚠️ Important Notes

- All commands under a target **must be indented with a TAB**, not spaces.
- The default file is `Makefile` (case-sensitive).
- Targets run **in order of dependency**.
- You can create **shortcuts for any complex logic** using Make.

---

## 💡 Pro Tips

- Use variables like `LOCAL_TAG` to avoid hardcoding.
- Group targets by type (e.g., test, lint, build).
- Integrate Make with Git hooks or CI tools like GitHub Actions, GitLab CI, or Jenkins.
- You can create a `help` target to document all commands!

```makefile
help:
	@echo "make test               # Run unit tests"
	@echo "make quality_checks     # Run code linters"
	@echo "make build              # Build Docker image"
	@echo "make integration_test   # Run integration tests"
	@echo "make publish            # Publish to registry"
	@echo "make setup              # Install dev dependencies"
```

Run:

```bash
make help
```

---

## 📚 Summary

Makefiles are powerful, flexible, and beginner-friendly. Once you start using `make`, you’ll wonder how you lived without it. Master it now — your future self (and team) will thank you!

Happy Automating! 🚀

---
