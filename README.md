# Chip-8 Discrepency Resolution
- SHR and SHL require two operands
-- Shift Ry by 1 and store in Rx
-- Use two identical operands for default behavior
- MOVE 8xy0 stores Ry in Rx

# To assemble a new program:
- In the repl.it terminal in the main directory (check with an `ls` if you're not sure)
> bash Assemble.sh <yourProgram>.<anything_but_ch8> 

- edit the main.py to load your `"*.ch8"` filename
-- soon I will just add a load button

# Changelog
- Fixed bug forcing screen redraws every frame
-- Greatly increased speed if debug_mode is off
- Edited statement.py to expect two operands for SHR and SHL
- Changed GUI to only update on changes, huge performance boost