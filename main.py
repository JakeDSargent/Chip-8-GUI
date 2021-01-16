from chip8GUI import *

if __name__ == "__main__":
  
  chippy = Chip8GUI(DEBUG_MODE=True)
  chippy.chip8.load("Fibonacci.ch8")
  while(1):
    chippy.run()