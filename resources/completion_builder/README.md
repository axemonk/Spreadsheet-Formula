# Function completion builder

## Dependencies
- `openpyxl`
- `pandas`
- `argparse`

## Scripts

General operations performed by the scripts found in this directory:

### *main.py* Main
Runner script

### *js.py* JSON
Convert the function data found in `func_data_list.txt` to JSON, where each has:
- `func_name` (String)
- `req_param` (Array)
- `opt_param` (Array)
- `ellipsis` (Boolean)

### *cb.py* Completion Builder
Build out completion strings for param-having functions

### *ld.py* Load
Convert the function metadata found in *\*\_funcs\_ref.xlsx* to JSON

### *mg.py* Merge

1. Match completion strings to descriptions, categories, and function names.

2. Build out completion strings for nullary functions.
    (Nullary functions are not included during the OCR which creates the
    *\*\_data\_list\_raw.txt* file. Nullary functions are however included in
    the *\*\_funcs\_ref.xlsx* file, so this is where they are managed.)

3. Remove `TRUE()` and `FALSE()` from consideration if present in
    *\*\_funcs\_ref.xlsx*

4. Run all subscripts (if `toggle_rerun` is enabled) and build out entire
    *.sublime-completions* file.


## Comments

- NOTE: Not all `ellipsis == True` functions follow the same format.

    ```
    COUNTA~value1,[value2],...
    COUNTIFS~criteria_range1,criteria1,...
    ```

    Before running this script, clean formulas in *\*\_funcs\_data\_list.txt*
    that look like the second line to look like the first, using your best
    judgement. Find them using: `[^\]],\.{3}`
