---
description: Purpose: To systematically improve code structure, eliminate redundancies, and ensure maintainability while preserving functionality.
---

### **Steps & Prompt Presets:**

- **Code Audit & Metrics Review**  
    **Prompt:**
    
    > “Analyze the current code for [MODULE NAME]. Highlight any code smells, duplications, or complexity issues. Return a list of components prioritized by refactoring need.”  
    > **Rules:**
    
    - Include metrics such as cyclomatic complexity and code coverage mismatches.
    - Use clear, numbered observations to structure the audit.
- **Automated Refactoring Suggestions**  
    **Prompt:**
    
    > “Based on the audit findings, suggest refactoring improvements for [MODULE NAME]. Provide code examples that simplify logic, improve modularity, or enhance performance.”  
    > **Rules:**
    
    - Each suggestion should include before-and-after code snippets.
    - Ensure that suggestions are minimal and non-disruptive to existing functionality.
- **Iterative Refactoring Cycle**  
    **Prompt:**
    
    > “Execute a refactoring cycle on [MODULE NAME]. Generate a revised version incorporating suggestions, preserving functionality with inline tests to verify changes.”  
    > **Rules:**
    
    - Maintain a version control log with clear commit messages.
    - Use automated regression tests to validate that changes do not introduce bugs.