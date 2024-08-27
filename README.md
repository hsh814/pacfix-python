# pacfix-python
Python re-implementation of [pacfix](https://github.com/pslhy/pacfix/tree/main).

## Usage
You can see examples in [examples](./examples/) directory.

```shell
cd examples/example01
python3 ../../src/main.py run -i ./mem -l live-variables.txt
```

## Inputs
### live variables file
File name given by `-l` or `--live-vars` [live-variables.txt](./examples/example01/live-variables.txt).

```
1 x int
2 y int
3 z bool
4 b int
5 c int
```
First column is variable id.
Second column is variable name.
Third column is variable type.

### Input directory
Input directory given by `-i` or `--input-dir` [input-dir](./examples/example01/mem).
Input directory contains `neg` and `pos` subdirectories.
Each of them contains valuation files.
```
[begin]
1 7
2 1
3 0
4 8
5 6
[end]
[begin]
1 1
2 7
3 1
4 8
5 -6
[end]
```
First column is variable id.
Second column is value.
For each iteration, write `[begin]` and `[end]`.

## Output
Output file name given by `-o` or `--output`. If not given, it will be standard out.
