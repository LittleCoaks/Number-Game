# Number-Game

Thanks for playing my game! I don't have a name for it yet, so i'll just call it the "Number Game".

The game begins with two rows of numbers: the top row and the bottom row. The end goal of the game is to get the top row to clear entirely, and the bottom row to equal 0 or 1.
When you begin, you'll have numbers in the bottom row, but the top row will be blank.

You move numbers into the top row by "splitting" an even number in half. Half of the number will go up to the top row, and the other half stays in the bottom row. The number "0" does not move into the top row, nor does it exist as it's own number in the bottom row. When you split an odd number, you can split it into any two numbers which add together to equal the original, but both numbers remain in the bottom row. Splitting numbers is how you create a path to solve the puzzle.

You can "cancel" digits in the top row with digits in the bottom row. This is how you will achieve the win condition.
  ex. if the top row is [6] and the bottom row is [36, 65, 6], you can cancel the top 6 with any of the 6's in the bottom row, resulting in a blank top row and either [30, 65, 6], [36, 5, 6] or [36, 65] in the bottom row.
  
If multiple numbers in the bottom row are equal, you can "merge" them together (if the bottom row is [5, 21, 5], a merge will result in [5, 21] remaining). You cannot merge top row numbers.

Is it recommended to start with 5 numbers, ranging from 1-50. This is the setting for default puzzles. Adding more numbers and increasing the max size increases puzzle difficulty. It is also technically not allowed to split an even number then cancel it with itself. I haven't patched this out yet, so please don't do it lol.

When the game ends, it will return the number of turns you took to solve the puzzle. Try to solve puzzles as effieicnetly as you can!
Don't be a nerd and criticise me for (probably) coding this poorly. Just enjoy the game damnit.

Image tutorial below.
