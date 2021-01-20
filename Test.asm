TestRegs  LOAD  R0,$0   Just testing all registers
          LOAD  R1,$1 
          LOAD  R2,$2 
          LOAD  R3,$3 
          LOAD  R4,$4 
          LOAD  R5,$5 
          LOAD  R6,$6 
          LOAD  R7,$7 
          LOAD  R8,$8 
          LOAD  R9,$9 
          LOAD  RA,$A  
          LOAD  RB,$B 
          LOAD  RC,$C 
          LOAD  RD,$D 
          LOAD  RE,$E 
          LOAD  RF,$F 
          SKE   RE,$E   Test SKE
          JUMP  ERROR 
          ADDR  R5,R5    
          SKRE  R5,RA   Test SKRE
          JUMP  ERROR 
          MOVE  R0,R5   Test MOVE 
          SKRE  R0,R5 
          JUMP  ERROR 
          LOAD  RC,$AA  
          LOAD  R0,$00  
          OR    RC,R0   Test OR 
          SKE   RC,$AA  
          JUMP  ERROR 
          LOAD  R0,$0A 
          AND   RA,R0   Test AND 
          SKE   RA,$0A  
          JUMP  ERROR  
          LOAD  RA,$3C 
          XOR   RA,R0   Test XOR 
          SKE   RA,$36  00110110
          JUMP  ERROR 
          LOAD  R0,$1 
          LOAD  R1,$3 
          SUB   R1,R0   Test SUB 
          SKE   RF,$1   
          JUMP  ERROR 
          SKE   R1,$2 
          JUMP  ERROR 
          SHR   R1,R1   Test SHR
          SKE   RF,$0 
          JUMP  ERROR 
          SKE   R1,$1 
          JUMP  ERROR
          LOAD  R2,$84 
          SHL   R2,R2   Test SHL
          SKE   RF,$1   
          JUMP  ERROR 
          SKE   R2,$08 
          JUMP  ERROR 
          LOAD  R4,FF   
          SKRNE R2,R4   Test SKRNE
          JUMP  ERROR 
          LOAD  R0,$0 
          JUMPI SUCCESS Test JUMPI
          JUMP  ERROR 
SUCCESS   RAND  R0,$FE  Test RAND
          SKNE  R0,$FF  
          JUMP  ERROR 
          LOAD  R0,$7   PRESS KEY 7
          SKPR  R0      Test SKPR 
          JUMP  ERROR   
          LOAD  R0,$7   RELEASE KEY 0
          SKUP  R0      Test SKPR 
          JUMP  ERROR 
          LOAD  R9,$FF 
          LOADD R9      Test LOADD 
          MOVED R4      Test MOVED 
          SKNE  R4,$0 
          JUMP  ERROR
          LOADS R9 
          KEYD  R5      Test KEYD PRESS KEY 
          LOAD  R2,$17  
          LOADI $B00    
          ADDI  R2      Test ADDI 
          STOR  RF 
PASS      LOAD  RF,$AA 
          JUMP  PASS 
ERROR     LOAD  RF,$EE 
          JUMP  ERROR 
