          CLR                       #Clear Screen
          LOAD        R7,$6         Initial xpos
          LOAD        R8,$2         Initial ypos
          LOAD        RA,$0         
          CALL        DrawNumA      Fibonacci(n=0)
          LOAD        RA,$1         
          CALL        DrawNumA      Fibonacci(n=1)
          CALL        DrawNumA      Fibonacci(n=2)
          LOAD        RA,$1         Dont start algorithm until
          LOAD        RB,$1         Fibonanni(n=3)
MainLoop  ADDR        RA,RB         A = B + A
          CALL        DrawNumA
          ADDR        RB,RA         B = A + B
          CALL        DrawNumB
          JUMP        MainLoop          

DrawNumA  LOADI       $B17          Random Far MM location
          BCD         RA
          READ        R2
          LDSPR       R0            Load Char Sprite for value RX
          DRAW        R7,R8,$5      Draw Sprite I at X, Y, Nbytes
          ADD         R7,$5         move x 4 width char + 1 space
          LDSPR       R1          
          DRAW        R7,R8,$5      Draw Sprite I at X, Y, Nbytes
          ADD         R7,$5         move x 4 width char + 1 space
          LDSPR       R2
          DRAW        R7,R8,$5      Draw Sprite I at X, Y, Nbytes
          ADD         R7,$A         move x 4 width char + 6 space
          SKNE        R7,$7E        X Position after 6 BCD writes
          CALL        NewLine
          RTS 

DrawNumB  LOADI       $B17          Random Far MM location
          BCD         RB
          READ        R2
          LDSPR       R0            Load Char Sprite for value RX
          DRAW        R7,R8,$5      Draw Sprite I at X, Y, Nbytes
          ADD         R7,$5         move x 4 width char + 1 space
          LDSPR       R1          
          DRAW        R7,R8,$5      Draw Sprite I at X, Y, Nbytes
          ADD         R7,$5         move x 4 width char + 1 space
          LDSPR       R2
          DRAW        R7,R8,$5      Draw Sprite I at X, Y, Nbytes
          ADD         R7,$A         move x 4 width char + 6 space
          SKNE        R7,7E         X Position after 6 BCD writes
          CALL        NewLine
          RTS 

NewLine   LOAD        R7,$6         Reset initial X position
          ADD         R8,$6         5 pixels tall 1 space
          SKNE        R8,$3E        Skip unless at bottom
          CLR
          SKNE		    R8,$3E        Skip unless at bottom
		      LOAD        R8,$2 
          RTS 
