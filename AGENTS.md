# Guidance for Codex Agents

This repository contains Python and R code for exploring GWAS hits and eQTL effects. The project was recently refactored to follow a modular layout:

- **src/** – importable Python modules under `src/gwas` and R scripts under `src/r_scripts`.
- **scripts/** – command line entry points that call the modules.
- **data/raw** and **data/processed** – input and output data (ignored by git).
- **tests/** – Python unit tests executed with `pytest`.

## How to work with this repository

1. **Keep code modular.** Place reusable Python functions in `src/gwas` and keep CLI wrappers in `scripts`. Avoid hard coded paths or `os.chdir` calls.
2. **R scripts.** Scripts in `src/r_scripts` take the analysis directory as their first argument. Do not rely on interactive working directories.
3. **Dependencies.** Record Python packages in `requirements.txt` and mirror them in `environment.yml` when relevant.
4. **Testing.** After modifying any Python code, run `pytest` from the repository root. Ensure all tests pass before committing.
5. **Data.** Do not commit large data files. The `data/` directory is for local use only and is already listed in `.gitignore`.
6. **Legacy scripts.** Older scripts live in `python_scripts/` for reference. Avoid editing them unless a task explicitly requires it.

Following these guidelines keeps the project consistent with the refactoring plan and ensures reproducibility across environments.
