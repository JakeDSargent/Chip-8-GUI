from chip8GUI import *

if __name__ == "__main__":
  
  chippy = Chip8GUI(DEBUG_MODE=False)
  chippy.chip8.load("Fibonacci.ch8")
  chippy.MM_uninitialized = True
  while(1):
    chippy.run()