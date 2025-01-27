# REPL Recorder

A cross-platform Python REPL wrapper that generates executable scripts reproducing your interactive session with perfect fidelity.

## Features

- **Session Preservation**: Create executable scripts from REPL sessions  
- **Cross-Platform**: Works on Windows, macOS, and Linux  
- **AST-Powered Parsing**: Handle complex syntax edge cases  
- **Smart Error Handling**: Comment out problematic lines while preserving valid code  
- **Multi-Statement Support**: Perfect semicolon handling with context awareness  

## Installation

```bash
pip install repl-recorder
```

## Usage

```bash
repl [-o OUTPUT_FILE]
```

## Examples

### Basic Session Capture
**REPL Input:**
```
>>> 5 + 5
10
>>> message = "Hello World"
>>> message[::-1]
'dlroW olleH'
```

**Generated Script (`session.py`):**
```python
print(repr(5 + 5))
message = "Hello World"
print(repr(message[::-1]))
```

**Script Output:**
```
10
'dlroW olleH'
```

### Advanced Error Handling
**REPL Input:**
```
>>> valid = 5; valid ** 2; invalid * 3
25
Traceback (most recent call last):
  File "<stdin>", line 1
    invalid * 3
NameError: name 'invalid' is not defined
```

**Generated Script:**
```python
valid = 5; print(repr(valid ** 2)); # invalid * 3
```

### Complex Code Blocks
**REPL Input:**
```
>>> def factorial(n):
...     return 1 if n <=1 else n*factorial(n-1)
>>> factorial(5)
120
```

**Generated Script:**
```python
def factorial(n):
    return 1 if n <=1 else n*factorial(n-1)
print(repr(factorial(5)))
```

## Edge Cases

### Semicolons in Strings
**REPL Input:**
```
>>> print("A;B;C"); {'k1;v1': 'k2;v2'}
A;B;C
{'k1;v1': 'k2;v2'}
```

**Generated Script:**
```python
print(repr(print("A;B;C"))); print(repr({'k1;v1': 'k2;v2'}))
```

## How It Works

1. Uses Python's AST module to parse input
2. Detects standalone expressions vs statements
3. Wraps expressions in `print(repr(...))` 
4. Preserves original code structure
5. Comments lines causing errors

## License

Mozilla Public License 2.0 - See [LICENSE](LICENSE)
