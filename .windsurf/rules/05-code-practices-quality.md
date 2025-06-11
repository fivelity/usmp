---
trigger: always_on
description: 
globs: 
---
# 05-code-practices-quality
## Code Practices & Quality
### General coding standards (readability, comments, type hinting, linting, error handling).
STRICT REQUIREMENT:
- Readability & Maintainability: Use clear, concise, well-commented code.
- Type Hinting: Use Python type hints and TypeScript interfaces extensively.
- Linting & Formatting: Follow `flake8` and `black` for Python; `eslint` and `prettier` for TypeScript/Svelte.
- Error Handling: Implement try/catch for JavaScript and try/except for Python.
- Avoid Early Returns: Print error messages instead of exiting early.
- Firestore Querying: Avoid `orderBy()`—fetch and sort in memory.