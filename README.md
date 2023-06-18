### How to use
```pip install pyparsing```

#### interact mode
```python interact.py -i```  
Then type the ltl formula want to examine and TS filepath.


#### test mode
```python interact.py -l ltl_file_path -t TS_file_path```   
This command will run the ltl_formula in ltl_file with TS in TS_file.  
All files must store in required formats.

### Arch
```AST.py``` is AST node and tree to parse ltl formula  
```ltl_parser.py``` is ltl_parser using pyparsing package  
```automaton.py``` is GNBA and NBA  
```TS.py``` is transition system and the production transition system  
```check.py``` is the main program

### Notice
