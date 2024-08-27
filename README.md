# pacfix-python
Python re-implementation of pacfix.

## Usage
```python
python3 src/main.py run -l live-variables.txt -i input-dir -o output-dir

## Input
### live variables file
File name given by `-l` or `--live-vars`.

```
1 x
2 y
3 z.field
4 a->field
```
First column is variable id.
Second column is variable name.

