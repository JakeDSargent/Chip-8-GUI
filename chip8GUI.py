from chip8 import *
import os
import tkinter as tk

DEBUG_MODE = True

class ByteDisplay:
  def __init__(self, master, data_byte, title, bg, fg, border=0):
    self.text_var = tk.StringVar()
    self.data = data_byte
    self.frame = tk.Frame(master, bg=bg, relief=tk.GROOVE, border=border)
    self.title = tk.Label(self.frame, text=title, bg=bg, fg=fg, font=("Courier", 12))
    self.display = tk.Label(self.frame, textvariable=self.text_var, bg=bg, fg=fg, font=("Courier", 12))
    self.title.pack()
    self.display.pack()
    self.update()
  
  def update(self):
    self.text_var.set(self.data.hex_str)

class WordDisplay:
  def __init__(self, master, data_word, title, bg, fg, border=0):
    self.text_var = tk.StringVar()
    self.data = data_word
    self.frame = tk.Frame(master, bg=bg, relief=tk.GROOVE, border=border)
    self.title = tk.Label(self.frame, text=title, bg=bg, fg=fg, font=("Courier", 10))
    self.display = tk.Label(self.frame, textvariable=self.text_var, bg=bg, fg=fg, font=("Courier", 10))
    self.title.pack(side=tk.LEFT)
    self.display.pack(side=tk.LEFT)
    self.update()
  
  def update(self):
    self.text_var.set(self.data.hex_str)

class StackDisplay:
  rows_per_col = 8
  hex_dict = {0 : "0", 1 : "1", 2 : "2", 3 : "3", 4 : "4", 5 : "5", 6 : "6", 7 : "7",
              8 : "8", 9 : "9", 10: "A", 11: "B", 12: "C", 13: "D", 14: "E", 15: "F"}

  def __init__(self, master, stack, bg, fg):
    self.frame = tk.Frame(master, bg=bg, relief=tk.GROOVE, border=2)
    self.displays = []
    for i in range(len(stack)):
      display = WordDisplay(self.frame, stack[i], "Stack["+self.hex_dict[i]+"]", bg, fg)
      display.frame.grid(row=i%self.rows_per_col, column=i//self.rows_per_col)
      self.displays.append(display)
    self.update()

  def update(self):
    for display in self.displays:
      display.update()

class Chip8GUI:
  SCREEN_MULTIPLIER = 6
  MM_MULTIPLIER = SCREEN_MULTIPLIER // 2
  key_side = 48

  GREEN_GREY = "#262B27"
  GREEN = "#12c937"
  BLUE_GREY = "#222529"
  BLUE_WHITE = "#e3f1ff"

  def __init__(self, DEBUG_MODE=True):
    self.DEBUG_MODE = DEBUG_MODE
    os.system('xset r off')
    self.bg = self.BLUE_GREY
    self.fg = self.BLUE_WHITE
    self.root = tk.Tk()
    self.root.config(bg=self.bg)
    self.chip8 = Chip8()
    self.screen = tk.Canvas(self.root, bg=self.bg, width=self.chip8.SCREEN_WIDTH * self.SCREEN_MULTIPLIER, height=self.chip8.SCREEN_HEIGHT * self.SCREEN_MULTIPLIER)
    self.create_pixels()
    self.screen.grid(column=0, row=0, rowspan=2)
    if self.DEBUG_MODE:
      self.bytes_per_MM_col = 128
      self.MM_cols = 4096 // self.bytes_per_MM_col
      self.MM = tk.Canvas(self.root, bg=self.bg, width=8*self.MM_cols*self.MM_MULTIPLIER, height=self.bytes_per_MM_col*self.MM_MULTIPLIER)
      self.create_MM_pixels()
      self.MM.grid(column=0, row=2, rowspan=2)
      self.PC_color = "Red"
      self.I_color = "Cyan"
      self.Stack_Color = "Yellow"

    self.keypad = tk.Frame(self.root)
    self.keys = []
    self.key_frames = []
    self.create_keys()
    self.keypad.grid(column=1, row=0)

    if self.DEBUG_MODE:
      self.register_displays = []
      self.register_frame = tk.Frame(self.root, bg=self.bg, relief=tk.GROOVE, )
      for i in range(16):
        hex_i = self.chip8.V0.hex_dict[i]
        reg_display = ByteDisplay(self.register_frame, self.chip8.V[hex_i], "V"+hex_i, self.bg, self.fg)
        reg_display.frame.grid(row=i//6, column=i%6, sticky=tk.W+tk.E+tk.N+tk.S)
        self.register_displays.append(reg_display)
      
      delay_display = ByteDisplay(self.register_frame, self.chip8.delay, "DT", self.bg, self.fg)
      delay_display.frame.grid(row=2, column=4, sticky=tk.W+tk.E+tk.N+tk.S)
      self.register_displays.append(delay_display)

      sound_display = ByteDisplay(self.register_frame, self.chip8.sound, "ST", self.bg, self.fg)
      sound_display.frame.grid(row=2, column=5, sticky=tk.W+tk.E+tk.N+tk.S)
      self.register_displays.append(sound_display)

      self.pointer_frame = tk.Frame(self.register_frame, bg=self.bg)
      self.pointer_frame.grid(row=3, column=0, columnspan=6)

      sp_display = ByteDisplay(self.pointer_frame, self.chip8.SP, "SP", self.bg, self.Stack_Color)
      sp_display.frame.grid(row=0, column=0, rowspan=2, sticky=tk.W, ipadx=20)
      self.register_displays.append(sp_display)

      stack = StackDisplay(self.pointer_frame, self.chip8.Stack, self.bg, self.fg)
      stack.frame.grid(row=2, column=0, columnspan=2)
      self.register_displays.append(stack)

      i_display = WordDisplay(self.pointer_frame, self.chip8.I, "I", self.bg, self.I_color)
      i_display.frame.grid(row=0, column=1, sticky=tk.E, ipadx=10)
      self.register_displays.append(i_display)

      pc_display = WordDisplay(self.pointer_frame, self.chip8.PC, "PC", self.bg, self.PC_color)
      pc_display.frame.grid(row=1, column=1, sticky=tk.E, ipadx=10)
      self.register_displays.append(pc_display)
    
      self.register_frame.grid(column=1, row=1, rowspan=2, sticky=tk.W+tk.E+tk.N)

    self.chip8_running = False

    self.button_frame = tk.Frame(self.root, bg=self.bg)
    self.button_frame.grid(row=3, column=1, sticky=tk.S)
    self.step_button = tk.Button(self.button_frame, command=self.chip8.step, fg=self.fg, bg=self.bg, font=("Courier", 14), text="STEP")
    self.step_button.pack(side=tk.LEFT)
    self.run_stringvar = tk.StringVar()
    self.run_stringvar.set("RUN")
    self.run_button = tk.Button(self.button_frame, command=self.run_button_event, textvariabl=self.run_stringvar, fg=self.fg, bg=self.bg, font=("Courier", 14))
    self.run_button.pack(side=tk.RIGHT)

    for i in range(10):
      self.root.rowconfigure(i, weight=10)
    self.root.rowconfigure(0, weight=1)
    self.root.rowconfigure(3, weight=1)
    self.step_GUI()

  def run(self):
    if self.chip8_running:
      self.chip8.step()
    self.step_GUI()

  def run_button_event(self):
    if self.chip8_running:
      self.run_stringvar.set("RUN")
      self.chip8_running = False
      self.step_button["state"] = tk.NORMAL
    else:
      self.run_stringvar.set("STOP")
      self.chip8_running = True
      self.step_button["state"] = tk.DISABLED


  def create_pixels(self):
    for x in range(self.chip8.SCREEN_WIDTH):
      for y in range(self.chip8.SCREEN_HEIGHT):
        self.screen.create_rectangle(x*self.SCREEN_MULTIPLIER, 
                                     y*self.SCREEN_MULTIPLIER, 
                                     x*self.SCREEN_MULTIPLIER+self.SCREEN_MULTIPLIER, 
                                     y*self.SCREEN_MULTIPLIER+self.SCREEN_MULTIPLIER, 
                                     fill=self.fg, outline=self.fg)

  def create_MM_pixels(self):
    for x in range(self.MM_cols):
      for y in range(self.bytes_per_MM_col):
        for bit in range(8):
          self.MM.create_rectangle(x*8*self.MM_MULTIPLIER+bit*self.MM_MULTIPLIER, 
                                   y*self.MM_MULTIPLIER, 
                                   x*8*self.MM_MULTIPLIER+self.MM_MULTIPLIER+bit*self.MM_MULTIPLIER, 
                                   y*self.MM_MULTIPLIER+self.MM_MULTIPLIER, 
                                   fill=self.fg, outline=self.fg)    

  def press_key(self, index):
    self.keys[index].config(fg=self.bg, bg=self.fg)
    self.key_frames[index].config(bg=self.fg, relief=tk.SUNKEN)
    self.chip8.key_pressed[index] = True

  def release_key(self, index):
    self.keys[index].config(fg=self.fg, bg=self.bg)
    self.key_frames[index].config(bg=self.bg, relief=tk.RAISED)
    self.chip8.key_pressed[index] = False

  def create_keys(self):
      key_order=[1, 2, 3, 12, 4, 5, 6, 13, 7, 8, 9, 14, 10, 0, 11, 15]

      for i in range(16):
        frame = tk.Frame(self.keypad, bg=self.bg, width=self.key_side, height=self.key_side, border=5, relief=tk.RAISED)
        key = tk.Label(frame, border=0, text=self.chip8.V0.hex_dict[i], fg=self.fg, bg=self.bg, font=("Courier", 24))
        key.pack()
        self.keys.append(key)
        self.key_frames.append(frame)
        self.key_frames[i].bind("<Button-1>", lambda event, i=i: self.press_key(i))
        self.key_frames[i].bind("<ButtonRelease-1>", lambda event, i=i: self.release_key(i))
        self.keys[i].bind("<Button-1>", lambda event, i=i: self.press_key(i))
        self.keys[i].bind("<ButtonRelease-1>", lambda event, i=i: self.release_key(i))
        self.root.bind("<KeyPress-"+self.chip8.V0.hex_dict[i].lower()+">", lambda event, i=i: self.press_key(i))
        self.root.bind("<KeyRelease-"+self.chip8.V0.hex_dict[i].lower()+">", lambda event, i=i: self.release_key(i))
        
      for i in range(16):
        self.key_frames[key_order[i]].grid(column=i%4, row=i//4, sticky=tk.N+tk.S+tk.W+tk.E, ipadx=10)

      

  def draw_screen(self):
    if self.chip8.screen_needs_refreshed:
      pixel_id = 1
      for x in range(self.chip8.SCREEN_WIDTH):
        for y in range(self.chip8.SCREEN_HEIGHT):
          if self.chip8.screen[x][y]:
            self.screen.itemconfig(pixel_id, fill=self.fg, outline=self.fg)
          else:
            self.screen.itemconfig(pixel_id, fill=self.bg, outline=self.bg)
          pixel_id += 1

  def draw_MM(self):
    pixel_id = 1
    for x in range(self.MM_cols):
      for y in range(self.bytes_per_MM_col):
        index = x*self.bytes_per_MM_col+y
        temp_byte = self.chip8.MM[index].bin_str
        for bit in range(8):
          if index == self.chip8.I.value:
            if temp_byte[bit] == '1':
              self.MM.itemconfig(pixel_id, fill=self.fg, outline=self.I_color)
            else:
              self.MM.itemconfig(pixel_id, fill=self.bg, outline=self.I_color)
          elif index == self.chip8.PC.value or index == self.chip8.PC.value+1:
            if temp_byte[bit] == '1':
              self.MM.itemconfig(pixel_id, fill=self.fg, outline=self.PC_color)
            else:
              self.MM.itemconfig(pixel_id, fill=self.bg, outline=self.PC_color)
          elif index == self.chip8.Stack[self.chip8.SP.value].value or index == self.chip8.Stack[self.chip8.SP.value].value+1:
            if temp_byte[bit] == '1':
              self.MM.itemconfig(pixel_id, fill=self.fg, outline=self.Stack_Color)
            else:
              self.MM.itemconfig(pixel_id, fill=self.bg, outline=self.Stack_Color)
          else:
            if temp_byte[bit] == '1':
              self.MM.itemconfig(pixel_id, fill=self.fg, outline=self.fg)
            else:
              self.MM.itemconfig(pixel_id, fill=self.bg, outline=self.bg)
          pixel_id += 1

  def step_GUI(self):
    if self.DEBUG_MODE:
      self.draw_MM()
      for display in self.register_displays:
        display.update()

    self.draw_screen()

    self.root.update()
    self.root.update_idletasks()
    


if __name__ == "__main__":
  
  chippy = Chip8GUI()
  while(1):
    chippy.run()
