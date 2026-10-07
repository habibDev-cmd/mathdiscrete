<div align="center">

# MathDiscrete

### A modular Python workspace for discrete mathematics

[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![SymPy](https://img.shields.io/badge/symbolic%20math-SymPy-3B5526)](https://www.sympy.org/)
[![NetworkX](https://img.shields.io/badge/graphs-NetworkX-4B8BBE)](https://networkx.org/)
[![Docker](https://img.shields.io/badge/deploy-Docker-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)

**MathDiscrete** is an academic-oriented application for exploring and solving selected problems in discrete mathematics. A modular Python core keeps mathematical operations separate from the Streamlit interface, making solvers straightforward to test, extend, and reuse.

</div>

## Overview

The application currently provides deterministic tools for selected problem types:

- **Propositional logic:** safe parsing of Boolean expressions, truth tables, and tautology, contradiction, or contingency classification.
- **Set theory:** union, intersection, difference, symmetric difference, and Cartesian product.
- **Combinatorics:** permutations, combinations, factorials, enumeration helpers, and a Pigeonhole Principle bound.
- **Graph theory:** weighted and unweighted graph input, adjacency matrices, Dijkstra shortest paths, tree checks, and graph visualization.

The Streamlit interface currently includes views for propositional logic, set theory, and graph theory. The combinatorics solver is available in the core package; its dedicated UI view is not yet implemented. This is a focused solver application, not a general natural-language proof system, and results are limited to the documented input grammars.

## Technology Stack

| Area | Technology | Purpose |
| --- | --- | --- |
| Language | Python 3.11+ | Application and mathematical core |
| User interface | Streamlit | Interactive academic web interface |
| Symbolic logic | SymPy | Boolean expressions and logical analysis |
| Graph algorithms | NetworkX | Graph construction, matrices, and shortest paths |
| Graph rendering | Matplotlib | Static graph visualization in Streamlit |
| Numerical arrays | NumPy | Matrix representation and numerical support |
| Deployment | Docker Compose | Reproducible containerized runtime |
| Testing | pytest | Automated solver and view tests |

## Architecture

Mathematical logic lives in `core/`; Streamlit presentation and navigation live in `ui/`. Tests exercise both layers independently where practical.

```text
mathdiscrete/
├── core/
│   ├── __init__.py
│   ├── combinatorics.py
│   ├── graphs.py
│   ├── logic.py
│   └── sets_theory.py
├── ui/
│   ├── __init__.py
│   ├── app.py
│   └── views/
│       ├── __init__.py
│       ├── graphs_view.py
│       ├── logic_view.py
│       └── sets_view.py
├── tests/
│   ├── test_combinatorics.py
│   ├── test_graphs.py
│   ├── test_graphs_view.py
│   ├── test_logic.py
│   └── test_sets_theory.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

The repository also retains root-level files from an earlier prototype. The current modular application and Docker image use `ui/app.py` as their entry point.

## Local Installation

### 1. Prerequisites

- Python 3.11 or newer
- `venv` and `pip` (included with standard Python installations)

### 2. Clone the repository

```bash
git clone https://github.com/habibDev-cmd/mathdiscrete.git
cd mathdiscrete
```

### 3. Create and activate a virtual environment

**Linux / macOS**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows PowerShell**

```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
```

### 4. Install runtime dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 5. Start the application

```bash
python -m streamlit run ui/app.py
```

Open the local URL printed by Streamlit, typically <http://localhost:8501>.

### 6. Run the tests

Install pytest in the active virtual environment, then run the suite:

```bash
python -m pip install pytest
python -m pytest -q
```

## Docker Deployment

Docker Compose builds the lightweight `python:3.11-slim` image, installs `requirements.txt`, copies the `core/` and `ui/` packages, and publishes Streamlit on port `8501`.

From the repository root, build and start the service:

```bash
docker compose up --build
```

Open <http://localhost:8501> to use the application. Stop the service with `Ctrl+C`; to stop and remove the Compose container and network, run:

```bash
docker compose down
```

To build the image without starting the service:

```bash
docker compose build
```

## Development Notes

- Keep mathematical calculations in `core/` and Streamlit rendering in `ui/`.
- Prefer typed solver interfaces and deterministic results that can be verified with tests.
- Add new views under `ui/views/` and connect them through the navigation map in `ui/app.py`.
- The standard runtime dependencies are listed in `requirements.txt`; test tooling is installed separately for development.

## Scope and Limitations

MathDiscrete is being built incrementally. It does not currently cover every area of discrete mathematics, interpret arbitrary problem statements, or guarantee correctness for inputs outside each solver's supported grammar. Review the relevant solver and its tests when using results in coursework or research.