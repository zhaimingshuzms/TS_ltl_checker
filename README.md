### How to use
```pip install pyparsing```  
```python check.py```
Then type the ltl formula want to examine.
By default, the transition system is stored at TS.txt

### Arch
```AST.py``` is AST node and tree to parse ltl formula  
```ltl_parser.py``` is ltl_parser using pyparsing package  
```automaton.py``` is GNBA and NBA
```TS.py``` is transition system and the production transition system
```check.py``` is the main program

### Notice
This model checker currently doesn't support arbitary initial state for TS.
