# Chess
Studying Mates

As an enthusiastic on chess, I did this code too look deeper on one of the most difficult ending games: Bishop + Knight + King x Black King.
This case is always a victory for White, but many people failed to achieve the mate ending the game in a draw, inclusive some Grand Masters lost this victory opportunity. 
Computer analyses in chess almost always end in a computational challenge due to the huge number of possible board combinations, but when the number of pieces decreases, we can run through all the possible positions. 
The biggest challenge here is to mate Black in less than 50 moves to avoid a draw. The algorithm show that it is always possible to mate black in less than 35 moves, quite close to fifty! In other words, in some of the positions you shall play the best move 35 times in a row, any deviation will keep you closer and closer to the draw.
Before moving to the algorithm let´s make a definition: Let A by a valid position, if by making a single move we reach position B, then B is a destination of A. 
Here is the algorithm:
1.	Find all valid possible positions.

2.	Mark all the valid positions as “undefined”, i.e., they are not “draw” or “Mate in x moves”.

3.	Run through all “Black to play” positions. If the Black King has no valid square to move, we have two possibilities: 
a.	the king is not in check, and it´s a draw. 
b.	or the king is in check and it´s mate! I called these of “mate in 0 moves”.
Moreover, if the black king can capture the bishop or the knight, it is a draw.

4.	Run through all the “White to play” positions. 
a.	I any of the destination of this position is a “mate in n moves” (n is an integer greater than or equal to zero), this position is a “mate in n+1 moves”.
b.	If all destination of this position are draws, this position is a draw.  

5.	Run through all the “Black to play” positions. 

a.	I all destinations of this position are “mate in n moves”, this position is a “mate in x moves”. Considering that Black will try to postpone the mate as much as possible, x will be equal to the greatest n among all destinations. 
 
b.	If any of the destination of this position is a draw, this position is a draw.  

6.	After steps 5 and 6, some of the positions may remain “undefined”.

a.	If at least one position is “undefined” go back to step 4.

b.	Else, we are done.
