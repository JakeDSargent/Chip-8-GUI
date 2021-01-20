from random import randrange as rand
from datetime import datetime, timedelta
from time import sleep


class Byte:

  hex_dict = {0 : "0", 1 : "1", 2 : "2", 3 : "3", 4 : "4", 5 : "5", 6 : "6", 7 : "7",
              8 : "8", 9 : "9", 10: "A", 11: "B", 12: "C", 13: "D", 14: "E", 15: "F",
              "0" : 0, "1" : 1, "2" : 2, "3" : 3, "4" : 4, "5" : 5, "6" : 6, "7" : 7,
              "8" : 8, "9" : 9, "A" :10, "B" :11, "C" :12, "D" :13, "E" :14, "F" :15}

  bin_dict = {"0" : "0000", "1" : "0001", "2" : "0010", "3" : "0011", "4" : "0100", "5" : "0101", "6" : "0110", "7" : "0111",
              "8" : "1000", "9" : "1001", "A" : "1010", "B" : "1011", "C" : "1100", "D" : "1101", "E" : "1110", "F" : "1111",
              "0000" : 0, "0001" : 1, "0010" : 2, "0011" : 3, "0100" : 4, "0101" : 5, "0110" : 6, "0111" : 7,
              "1000" : 8, "1001" : 9, "1010" :10, "1011" :11, "1100" :12, "1101" :13, "1110" :14, "1111" :15}

  hex_length = 2
  max_value = 16**hex_length
  
  def __init__(self, in_value = 0):
    self.set(in_value)
  
  def __str__(self):
    return '{self.hex_str}'.format(self=self)

  @staticmethod
  def bitwise_AND(byte1, byte2):
    or_list = ["1" if byte1.bin_str[i] == "1" and byte2.bin_str[i] == "1" else "0" for i in range(len(byte1.bin_str))]
    return ''.join(or_list)

  @staticmethod
  def bitwise_OR(byte1, byte2):
    or_list = ["1" if byte1.bin_str[i] == "1" or byte2.bin_str[i] == "1" else "0" for i in range(len(byte1.bin_str))]
    return ''.join(or_list)

  @staticmethod
  def bitwise_XOR(byte1, byte2):
    or_list = ["1" if byte1.bin_str[i] != byte2.bin_str[i] else "0" for i in range(len(byte1.bin_str))]
    return ''.join(or_list)

  @staticmethod
  def sanitize(i):
    i = abs(i)
    while(i>=Byte.max_value):
      i -= Byte.max_value
    return i

  def set_from_int(self, in_value):
    negative = True if in_value < 0 else False
    
    in_value = self.sanitize(in_value)
    self.value = in_value
    self.hex_str = Byte.hex_dict[in_value//16] + Byte.hex_dict[in_value%16]
    
    if negative:
      self.set(Byte(Byte.bitwise_XOR(self, Byte("FF"))).value + 1)


  def set_from_hex_str(self, in_value):
    self.value = 16 * Byte.hex_dict[in_value[0]] + Byte.hex_dict[in_value[1]]
    self.hex_str = in_value

  def set_from_bin_str(self, in_value):
    self.set_from_hex_str(''.join([self.hex_dict[self.bin_dict[in_value[4*i:4*i+4]]] for i in range(self.hex_length)]))

  def set(self, in_value):
    if type(in_value) == int:
      self.set_from_int(in_value)

    elif type(in_value) == str:
      if len(in_value) == self.hex_length:
        self.set_from_hex_str(in_value)

      if len(in_value) == self.hex_length*4:
        self.set_from_bin_str(in_value)

    self.update_bin_str()

  def update_bin_str(self):
    self.bin_str = ''.join([self.bin_dict[c] for c in self.hex_str])

  
  def increment(self, n = 1):
    n = abs(n)
    for i in range(n):
      self.set(self.value + 1)

  def decrement(self, n = 1):
    n = abs(n)
    for i in range(n):
      self.set(self.value - 1)


class Word(Byte):
  hex_length = 4
  max_value = 16**hex_length

  @staticmethod
  def sanitize(i):
    i = abs(i)
    while(i>=Word.max_value):
      i -= Word.max_value
    return i

  @staticmethod
  def get_val(hex_str):
    temp_word = Word(hex_str)
    return temp_word.value

  def set_from_int(self, in_value):
    in_value = self.sanitize(in_value)
    self.value = in_value
    temp_value = in_value

    a = temp_value // 16**3
    temp_value %= 16**3

    b = temp_value // 16**2
    temp_value %= 16**2

    c = temp_value // 16**1
    d = temp_value % 16**1

    self.hex_str = Word.hex_dict[a] + Word.hex_dict[b] + Word.hex_dict[c] + Word.hex_dict[d]

  def set_from_hex_str(self, in_value):
    self.value = 16**3 * Word.hex_dict[in_value[0]] + 16**2 * Word.hex_dict[in_value[1]] + \
                 16 * Word.hex_dict[in_value[2]] + Word.hex_dict[in_value[3]]
    self.hex_str = in_value
  

class Chip8:
  SCREEN_WIDTH = 128
  SCREEN_HEIGHT = 64

  MICROSEC_60Hz = 16667

  # for 8xy[6/E
  IGNORE_SHIFT_Y = True 

  def __init__(self):

    self.V0 = Byte()
    self.V1 = Byte()
    self.V2 = Byte()
    self.V3 = Byte()
    self.V4 = Byte()
    self.V5 = Byte()
    self.V6 = Byte()
    self.V7 = Byte()
    self.V8 = Byte()
    self.V9 = Byte()
    self.VA = Byte()
    self.VB = Byte()
    self.VC = Byte()
    self.VD = Byte()
    self.VE = Byte()
    self.VF = Byte()

    self.I = Word()

    self.delay = Byte()
    self.sound = Byte()

    self.PC = Word("0200")
    self.MM = [Byte(0) for i in range(4096)]
    self.MM_updated = False

    self.SP = Byte("0F")
    self.Stack = [Word(0) for i in range(16)]
    
    self.default_registers()

    self.V = { "0" : self.V0, "1" : self.V1, "2" : self.V2, "3" : self.V3, 
               "4" : self.V4, "5" : self.V5, "6" : self.V6, "7" : self.V7,
               "8" : self.V8, "9" : self.V9, "A" : self.VA, "B" : self.VB, 
               "C" : self.VC, "D" : self.VD, "E" : self.VE, "F" : self.VF }

    self.screen = [[False for y in range(Chip8.SCREEN_HEIGHT)] for x in range(Chip8.SCREEN_WIDTH)]
    self.screen_needs_refreshed = True
    self.pixel_toggles = []


    self.key_pressed = [False] * 16

    self.last_timer_tick = datetime.now()


  def default_registers(self):
    self.V0.set(0)
    self.V1.set(0)
    self.V2.set(0)
    self.V3.set(0)
    self.V4.set(0)
    self.V5.set(0)
    self.V6.set(0)
    self.V7.set(0)
    self.V8.set(0)
    self.V9.set(0)
    self.VA.set(0)
    self.VB.set(0)
    self.VC.set(0)
    self.VD.set(0)
    self.VE.set(0)
    self.VF.set(0)

    self.I.set(0)

    self.delay.set(0)
    self.sound.set(0)

    self.PC.set("0200")
    for i in range(4096):
      self.MM[i].set(0) 

    self.SP = Byte("0F")

    self.MM[512].set("24")  # first instruction == call to 400
    self.MM[1024].set("14")  # jump to 400

    self.load_hex_chars()

  def load_hex_chars(self):
    self.MM[0].set("01100000")
    self.MM[1].set("10010000")
    self.MM[2].set("10010000")
    self.MM[3].set("10010000")
    self.MM[4].set("01100000")
    self.MM[5].set("00100000")
    self.MM[6].set("01100000")
    self.MM[7].set("00100000")
    self.MM[8].set("00100000")
    self.MM[9].set("01110000")
    self.MM[10].set("11100000")
    self.MM[11].set("00010000")
    self.MM[12].set("01100000")
    self.MM[13].set("10000000")
    self.MM[14].set("11110000")
    self.MM[15].set("11100000")
    self.MM[16].set("00010000")
    self.MM[17].set("01100000")
    self.MM[18].set("00010000")
    self.MM[19].set("11100000")
    self.MM[20].set("10010000")
    self.MM[21].set("10010000")
    self.MM[22].set("11110000")
    self.MM[23].set("00010000")
    self.MM[24].set("00010000")
    self.MM[25].set("11110000")
    self.MM[26].set("10000000")
    self.MM[27].set("11100000")
    self.MM[28].set("00010000")
    self.MM[29].set("11100000")
    self.MM[30].set("01100000")
    self.MM[31].set("10000000")
    self.MM[32].set("11100000")
    self.MM[33].set("10010000")
    self.MM[34].set("01100000")
    self.MM[35].set("11110000")
    self.MM[36].set("00010000")
    self.MM[37].set("00100000")
    self.MM[38].set("01000000")
    self.MM[39].set("01000000")
    self.MM[40].set("01100000")
    self.MM[41].set("10010000")
    self.MM[42].set("01100000")
    self.MM[43].set("10010000")
    self.MM[44].set("01100000")
    self.MM[45].set("01100000")
    self.MM[46].set("10010000")
    self.MM[47].set("01110000")
    self.MM[48].set("00010000")
    self.MM[49].set("01100000")
    self.MM[50].set("01100000")
    self.MM[51].set("10010000")
    self.MM[52].set("11110000")
    self.MM[53].set("10010000")
    self.MM[54].set("10010000")
    self.MM[55].set("11100000")
    self.MM[56].set("10010000")
    self.MM[57].set("11100000")
    self.MM[58].set("10010000")
    self.MM[59].set("11100000")
    self.MM[60].set("01110000")
    self.MM[61].set("10000000")
    self.MM[62].set("10000000")
    self.MM[63].set("10000000")
    self.MM[64].set("01110000")
    self.MM[65].set("11100000")
    self.MM[66].set("10010000")
    self.MM[67].set("10010000")
    self.MM[68].set("10010000")
    self.MM[69].set("11100000")
    self.MM[70].set("11110000")
    self.MM[71].set("10000000")
    self.MM[72].set("11100000")
    self.MM[73].set("10000000")
    self.MM[74].set("11110000")
    self.MM[75].set("11110000")
    self.MM[76].set("10000000")
    self.MM[77].set("11100000")
    self.MM[78].set("10000000")
    self.MM[79].set("10000000")
    self.MM[80].set("01100000")
    self.MM[81].set("11010000")
    self.MM[82].set("11110000")
    self.MM[83].set("10110000")
    self.MM[84].set("01100000")

  def load(self, filename):
    with open(filename, "r") as in_file:
      lines = in_file.readlines()

    for line in lines:
      if line[:2] == "0x":
        load_list = line.split()
        addr = Word.get_val(load_list[0][2:])
        instruction = load_list[1]
        self.MM[addr].set(instruction[:2])
        self.MM[addr+1].set(instruction[2:])

  def execute_current_instruction(self):
    self.MM_updated = False 

    instruction_str = str(self.MM[self.PC.value]) + str(self.MM[self.PC.value+1])
    self.PC.increment(2)

    print(instruction_str)
    addr = "0" + instruction_str[1:] 
    w = instruction_str[0]
    x = instruction_str[1]
    y = instruction_str[2]
    n = instruction_str[3]
    kk = Byte(y+n).value

    # 00E0 - CLS
    # Clear the display.
    if instruction_str == "00E0":
      self.screen = [[False for y in range(Chip8.SCREEN_HEIGHT)] for x in range(Chip8.SCREEN_WIDTH)]
      self.screen_needs_refreshed = True

    # 00EE - RET
    # Return from a subroutine.

    # The interpreter sets the program counter to the address at the top of the stack, then subtracts 1 from the stack pointer.
    elif instruction_str == "00EE":
          self.PC.set(self.Stack[self.SP.value].value)
          self.SP.decrement()
          if self.SP.value == 255:
            self.SP.set("0F")

    # 1nnn - JP addr
    # Jump to location nnn.

    # The interpreter sets the program counter to nnn.
    elif w == "1":
      self.PC.set(addr)


    # 2nnn - CALL addr
    # Call subroutine at nnn.

    # The interpreter increments the stack pointer, then puts the current PC on the top of the stack. The PC is then set to nnn.
    elif w == "2":
      self.SP.increment()
      if self.SP.value == 16:
        self.SP.set("00")
      self.Stack[self.SP.value].set(self.PC.value)
      self.PC.set(addr)

    # 3xkk - SE Vx, byte
    # Skip next instruction if Vx = kk.

    # The interpreter compares register Vx to kk, and if they are equal, increments the program counter by 2.
    elif w == "3":
      if self.V[x].value == kk:
        self.PC.increment(2)

    # 4xkk - SNE Vx, byte
    # Skip next instruction if Vx != kk.

    # The interpreter compares register Vx to kk, and if they are not equal, increments the program counter by 2.
    elif w == "4":
      if self.V[x].value != kk:
        self.PC.increment(2)

    # 5xy0 - SE Vx, Vy
    # Skip next instruction if Vx = Vy.

    # The interpreter compares register Vx to register Vy, and if they are equal, increments the program counter by 2.
    elif w == "5":
      if self.V[x].value == self.V[y].value:
        self.PC.increment(2)

    # 6xkk - LD Vx, byte
    # Set Vx = kk.

    # The interpreter puts the value kk into register Vx.
    elif w == "6":
      self.V[x].set(kk)

    # 7xkk - ADD Vx, byte
    # Set Vx = Vx + kk.

    # Adds the value kk to the value of register Vx, then stores the result in Vx.
    elif w == "7":
      self.V[x].set(self.V[x].value + kk)

    elif w == "8":

      # 8xy0 - LD Vx, Vy
      # Set Vx = Vy.

      # Stores the value of register Vy in register Vx.
      if n == "0":
        self.V[x].set(self.V[y].value)
    
      # 8xy1 - OR Vx, Vy
      # Set Vx = Vx OR Vy.

      # Performs a bitwise OR on the values of Vx and Vy, then stores the result in Vx. A bitwise OR compares the corrseponding bits from two values, and if either bit is 1, then the same bit in the result is also 1. Otherwise, it is 0.
      elif n == "1":
        self.V[x].set(Byte.bitwise_OR(self.V[x], self.V[y]))

      # 8xy2 - AND Vx, Vy
      # Set Vx = Vx AND Vy.

      # Performs a bitwise AND on the values of Vx and Vy, then stores the result in Vx. A bitwise AND compares the corrseponding bits from two values, and if both bits are 1, then the same bit in the result is also 1. Otherwise, it is 0.
      elif n == "2":
        self.V[x].set(Byte.bitwise_AND(self.V[x], self.V[y]))

      # 8xy3 - XOR Vx, Vy
      # Set Vx = Vx XOR Vy.

      # Performs a bitwise exclusive OR on the values of Vx and Vy, then stores the result in Vx. An exclusive OR compares the corrseponding bits from two values, and if the bits are not both the same, then the corresponding bit in the result is set to 1. Otherwise, it is 0.
      elif n == "3":
        self.V[x].set(Byte.bitwise_XOR(self.V[x], self.V[y]))

      # 8xy4 - ADD Vx, Vy
      # Set Vx = Vx + Vy, set VF = carry.

      # The values of Vx and Vy are added together. If the result is greater than 8 bits (i.e., > 255,) VF is set to 1, otherwise 0. Only the lowest 8 bits of the result are kept, and stored in Vx.
      elif n == "4":
        total = self.V[x].value + self.V[y].value

        if total > 255:
          self.VF.set(1)
        else:
          self.VF.set(0)
        
        self.V[x].set(total)  # Byte handles overlows

      # 8xy5 - SUB Vx, Vy
      # Set Vx = Vx - Vy, set VF = NOT borrow.

      # If Vx > Vy, then VF is set to 1, otherwise 0. Then Vy is subtracted from Vx, and the results stored in Vx.
      elif n == "5":
        total = self.V[x].value - self.V[y].value

        if self.V[x].value > self.V[y].value:
          self.VF.set(1)
        else:
          self.VF.set(0)
        
        self.V[x].set(total)  # Byte handles up to negative 255 (at least)

      # 8xy6 - SHR Vx {, Vy}
      # Set Vx = Vx SHR 1.

      # If the least-significant bit of Vx is 1, then VF is set to 1, otherwise 0. Then Vx is divided by 2.
      elif n == "6":
        if self.V[x].bin_str[7] == "1":
          self.VF.set(1)
        else:
          self.VF.set(0)
        self.V[x].set(self.V[y].value // 2)

      # 8xy7 - SUBN Vx, Vy
      # Set Vx = Vy - Vx, set VF = NOT borrow.

      # If Vy > Vx, then VF is set to 1, otherwise 0. Then Vx is subtracted from Vy, and the results stored in Vx.
      elif n == "7":
        total = self.V[y].value - self.V[x].value

        if self.V[y].value > self.V[x].value:
          self.VF.set(1)
        else:
          self.VF.set(0)
        
        self.V[x].set(total)  # Byte handles up to negative 255 (at least)

      # 8xyE - SHL Vx {, Vy}
      # Set Vx = Vx SHL 1.

      # If the most-significant bit of Vx is 1, then VF is set to 1, otherwise to 0. Then Vx is multiplied by 2.
      elif n == "E":
        if self.V[x].bin_str[0] == "1":
          self.VF.set(1)
        else:
          self.VF.set(0)
        self.V[y].set(self.V[x].value * 2)

    # 9xy0 - SNE Vx, Vy
    # Skip next instruction if Vx != Vy.

    # The values of Vx and Vy are compared, and if they are not equal, the program counter is increased by 2.
    elif w == "9":
      if self.V[x].value != self.V[y].value:
        self.PC.increment(2)

    # Annn - LD I, addr
    # Set I = nnn.

    # The value of register I is set to nnn.
    elif w == "A":
      self.I.set(addr)

    # Bnnn - JP V0, addr
    # Jump to location nnn + V0.

    # The program counter is set to nnn plus the value of V0.
    elif w == "B":
      self.PC.set(addr)
      self.PC.set(self.PC.value + self.V0.value)

    # Cxkk - RND Vx, byte
    # Set Vx = random byte AND kk.

    # The interpreter generates a random number from 0 to 255, which is then ANDed with the value kk. The results are stored in Vx. See instruction 8xy2 for more information on AND.
    elif w == "C":
      self.V[x].set(Byte.bitwise_AND(Byte(rand(256)), Byte(kk)))

    # Dxyn - DRW Vx, Vy, nibble
    # Display n-byte sprite starting at memory location I at (Vx, Vy), set VF = collision.

    # The interpreter reads n bytes from memory, starting at the address stored in I. These bytes are then displayed as sprites on screen at coordinates (Vx, Vy). Sprites are XORed onto the existing screen. If this causes any pixels to be erased, VF is set to 1, otherwise it is set to 0. If the sprite is positioned so part of it is outside the coordinates of the display, it wraps around to the opposite side of the screen. See instruction 8xy3 for more information on XOR, and section 2.4, Display, for more information on the Chip-8 screen and sprites.
    elif w == "D":
      collision = False
      x_pos = self.V[x].value
      y_pos = self.V[y].value
      for i in range(Byte.hex_dict[n]):
        for j in range(8):
          if self.MM[self.I.value + i].bin_str[j] == "1":  # toggle pixel
            
            if self.screen[x_pos+j][y_pos+i]:
              collision = True

            self.pixel_toggles.append((x_pos+j, y_pos+i))  # handled at GUI level for performance

      if collision:
        self.VF.set(1)
      else:
        self.VF.set(0)

    elif w == "E":
      # Ex9E - SKP Vx
      # Skip next instruction if key with the value of Vx is pressed.

      # Checks the keyboard, and if the key corresponding to the value of Vx is currently in the down position, PC is increased by 2.
      if y == "9":
        try:
          if self.key_pressed[self.V[x].value]:
            self.PC.increment(2)
        except IndexError:
          pass  # if Vx.value > 15 then we will never skip

      # ExA1 - SKNP Vx
      # Skip next instruction if key with the value of Vx is not pressed.

      # Checks the keyboard, and if the key corresponding to the value of Vx is currently in the up position, PC is increased by 2.
      elif y == "A":
        try:
          if not self.key_pressed[self.V[x].value]:
            self.PC.increment(2)
        except IndexError:
          self.PC.increment(2)  # if Vx.value > 15 then we will always skip


    elif w == "F":
      # Fx07 - LD Vx, DT
      # Set Vx = delay timer value.

      # The value of DT is placed into Vx.
      if kk == 7:
        self.V[x].set(self.delay.value)

      # Fx0A - LD Vx, K
      # Wait for a key press, store the value of the key in Vx.

      # All execution stops until a key is pressed, then the value of that key is stored in Vx.
      elif kk == 10:
        if (not any(self.key_pressed)):
          self.PC.decrement(2) 
        else:
          for i in range(16):
            if self.key_pressed[i]:
              self.V[x].set(i)

      # Fx15 - LD DT, Vx
      # Set delay timer = Vx.

      # DT is set equal to the value of Vx.
      elif kk == 16 + 5:
        self.delay.set(self.V[x].value)

      # Fx18 - LD ST, Vx
      # Set sound timer = Vx.

      # ST is set equal to the value of Vx.
      elif kk == 16 + 8:
        self.sound.set(self.V[x].value)

      # Fx1E - ADD I, Vx
      # Set I = I + Vx.

      # The values of I and Vx are added, and the results are stored in I.
      elif kk == 16 + 14:
        self.I.set(self.I.value + self.V[x].value)

      # Fx29 - LD F, Vx
      # Set I = location of sprite for digit Vx.

      # The value of I is set to the location for the hexadecimal sprite corresponding to the value of Vx. See section 2.4, Display, for more information on the Chip-8 hexadecimal font.
      elif kk == 2*16 + 9:
        self.I.set(self.V[x].value * 5 if self.V[x].value < 16 else 16 * 5)  # 16 is the Error Character

      # Fx33 - LD B, Vx
      # Store BCD representation of Vx in memory locations I, I+1, and I+2.

      # The interpreter takes the decimal value of Vx, and places the hundreds digit in memory at location in I, the tens digit at location I+1, and the ones digit at location I+2.
      elif kk == 3*16 + 3:
        self.MM_updated = True
        bcd = str(self.V[x].value).rjust(3, "0")
        print(bcd)
        self.MM[self.I.value + 0].set(int(bcd[0]))
        self.MM[self.I.value + 1].set(int(bcd[1]))
        self.MM[self.I.value + 2].set(int(bcd[2]))

      # Fx55 - LD [I], Vx
      # Store registers V0 through Vx in memory starting at location I.

      # The interpreter copies the values of registers V0 through Vx into memory, starting at the address in I.
      elif kk == 5*16 + 5:
        self.MM_updated = True
        for i in range(16):
          self.MM[self.I.value + i].set(self.V[Byte.hex_dict[i]])
          if Byte.hex_dict[i] == x:
            break;

      # Fx65 - LD Vx, [I]
      # Read registers V0 through Vx from memory starting at location I.

      # The interpreter reads values from memory starting at location I into registers V0 through Vx.
      elif kk == 6*16 + 5:
        for i in range(16):
          self.V[Byte.hex_dict[i]].set(self.MM[self.I.value + i].value)
          if Byte.hex_dict[i] == x:
            break;

  def step(self):
    self.execute_current_instruction()

    time_diff = datetime.now() - self.last_timer_tick
    if time_diff.microseconds >= Chip8.MICROSEC_60Hz:
      if self.delay.value > 0:
        self.delay.decrement()
      if self.sound.value > 0:
        self.sound.decrement()
      self.last_timer_tick += timedelta(microseconds=Chip8.MICROSEC_60Hz)
      if self.sound.value > 0:
        print("\a\r", end='')  # Bell character go brrr
        
    
    

if __name__ == "__main__":
  
  chip = Chip8()
  for i in range(3):
    chip.sound.set(120)
    while(chip.sound.value > 0):
      chip.step()
    chip.delay.set(60)
    while(chip.delay.value > 0):
      chip.step()


