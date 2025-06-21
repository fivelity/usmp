---
trigger: model_decision
description: Svelte 5 reminder
---

# 08-troubleshooting

## Troubleshooting - How to fix potential issues that may arise during development.

SVELTE 5 (WITH RUNES) HELP:
- In Svelte 5, we can't export and reassign state variables. 
Instead, we need to either:
  1. Export a function that returns the state value, or
  2. Only mutate properties of the state object without reassigning it.

JavaScript property descriptor rules, you cannot have both a getter/setter and a value/writable attribute in the same descriptor. 