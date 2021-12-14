import random
import commandAction

# TODO: better comments on code; should probably clean up the code in other areas too

def main():
  running=0
  while running==0:
    a=input("Press enter to begin.\nType \"help\" for a game tutorial.\nType \"example\" for an example game.\nType \"exit\" at any time to exit program: ")
    if a=="help":
      tutorial()
    elif a=="example":
      example()
    elif a != "exit":
      values=begin_game()
      if values == []:
        print("ERROR: You must enter at least 1 valid value. Please try again.\n")
      else:
        run_game(values)
    else:
      running=1
  return


def begin_game():
  values = []
  gameType=input("\nr = random set\nc = custom set\nd = default set\nSpecify a game type: ")

  if gameType=="r":
    amount = input("\nPlease specify how many numbers to play with: ").split()
    minValue = 1
    maxValue = input("Please give the maximum value for the puzzle numbers: ").split()
    if (commandAction.bArgExists(amount, 0) and commandAction.bArgExists(maxValue, 0)) and (commandAction.bArgIsInt(amount, 0) and commandAction.bArgIsInt(maxValue, 0)):
      for i in range(0,int(amount[0])):
        n=random.randint(minValue,int(maxValue[0]))
        values.append({"value":n})

  elif gameType=="c":
    customRow = input("Enter values separated by a space: ")
    if customRow=="exit":
      endProgram()
    # get only ints from custom val string and append to values list
    # no error for non-ints
    tempValues = customRow.split()
    for val in tempValues:
      try:
        int(val)
        if int(val) != 0:
          values.append({"value":int(val)})
      except ValueError:
        pass

  elif gameType == "d":
    for i in range(0, 5):
      n=random.randint(1,50)
      values.append({"value":n})

  elif gameType=="exit":
    endProgram()
  else:
    print("Enter a valid command.")

  # Here, we generate a random ID for each value in the bottom row
  # if that ID already exists, we just generate a new one -- brute force works here but it's elegant
  for x in values:
    commandAction.generateID(values, [], x) # must use empty list for arg 2

  return values

# must rewrite to account for values of each array val
def run_game(bottom_row):
  top_row=[]
  run = 0
  turnCount=0
  originalPuzzle = []
  for val in bottom_row:
    originalPuzzle.append(val["value"])
  while run == 0:
    # first set up arrays with only the int values to be printed on screen
    printTopRow = []
    printBottomRow = []
    for x in top_row:
      printTopRow.append(x['value'])
    for x in bottom_row:
      printBottomRow.append(x['value'])

    # then start loop by checking for win condition
    if ((len(bottom_row) <= 1) and (bottom_row == [] or bottom_row[0]['value']==1) and (top_row == [])):
      run=1
      print("\n"+separator)
      print(printTopRow)
      print(printBottomRow)
      print(separator)
      print("\n" + separator)
      print("SOLVED")
      print("Original puzzle:",originalPuzzle)
      print("Solved in "+str(turnCount)+" turns.")
      print(separator+"\n")
      return
    
    # not sure if this is needed anymore
    topRowLength=0
    for vals in top_row:
      topRowLength+=1
    bottomRowLength=0
    for vals in bottom_row:
      bottomRowLength+=1

    print("\n"+separator)
    print(printTopRow)
    print(printBottomRow)
    print(separator)
    command=str(input("\nEnter a command: \nType \"help\" for a list of commands: "))


    # index 0 == type of commnand
    # index 1 is number to execute command on
    commandArgs = command.split()
    
     # prevent error if command has no contents
    try:
      commandArgs[0]
    except IndexError:
      commandArgs.append("")

    if commandArgs[0] == "help":
      commandAction.help()


    # splits specified bottom number
    elif commandArgs[0]=="split":
      bArgOneExists = False
      bArgOneIsInt = False
      bArgTwoExists = False
      bArgTwoIsInt = False

      bArgOneExists = commandAction.bArgExists(commandArgs, 1)
      if not bArgOneExists:
        print("\nSpecify the number to be split.\n")
      else:  
        bArgOneIsInt = commandAction.bArgIsInt(commandArgs, 1)
        if not bArgOneIsInt:
          print("ERROR: " + commandArgs[1] + " is not a valid number.\n")
      bArgTwoExists = commandAction.bArgExists(commandArgs, 2)
      if bArgTwoExists:
        bArgTwoIsInt = commandAction.bArgIsInt(commandArgs, 2)

      if bArgOneExists and bArgOneIsInt:
        splitArgOne = int(commandArgs[1])
        splitNum = commandAction.findNumInRow(bottom_row, splitArgOne)
        if splitNum == []:
          print("ERROR: " + str(commandArgs[1] + " doesn't exist in the bottom row."))
        else:
          if bArgTwoExists and bArgTwoIsInt:
            splitArgTwo = int(commandArgs[2])
            if (splitArgTwo >= bottom_row[splitNum[0]]['value']) and (splitArgOne%2 == 1):
              print("ERROR: Cannot remove more than original value.")
            else:
              commandAction.split(bottom_row,top_row, splitNum[0], splitArgTwo)
              turnCount+=1
          else:
            if splitArgOne%2 == 0:
              commandAction.split(bottom_row,top_row, splitNum[0], -1)
              turnCount+=1
            else:
              lSplitOut = input("How much should be removed from " + str(commandArgs[1]) + "? ").split()
              if commandAction.bArgIsInt(lSplitOut, 0):
                splitOut = int(lSplitOut[0])
                if splitOut >= splitArgOne:
                  print("ERROR: Cannot remove more than original value.")
                else:
                  commandAction.split(bottom_row,top_row,splitNum[0], splitOut)
              else:
                print("ERROR: " + lSplitOut[1] + " is not a valid number.\n")
    

    # merges all instances of specified number in bottom row
    elif commandArgs[0]=="merge":
      bArgOneExists = False
      bArgOneIsInt = False

      bArgOneExists = commandAction.bArgExists(commandArgs, 1)
      if not bArgOneExists:
        print("\nSpecify the number to be merged.\n")
      else:
        bArgOneIsInt = commandAction.bArgIsInt(commandArgs, 1)
        if not bArgOneIsInt:
          print("ERROR: " + commandArgs[1] + " is not a valid number.\n")

      if bArgOneExists and bArgOneIsInt:
          mergeNum = commandAction.findNumInRow(bottom_row, int(commandArgs[1]))
          mergeNum = bottom_row[mergeNum[0]]
          mergeRow = commandAction.merge(bottom_row, top_row, mergeNum)
          if mergeRow == bottom_row:
            print("ERROR: No merge was done. Must be at least two matching numbers in the bottom row.")
          else:
            bottom_row = mergeRow # is this wrong?
            turnCount += 1

    
    # cancels numbers
    elif commandArgs[0] == "cancel":
      bArgOneExists = False
      bArgOneIsInt = False
      bArgTwoExists = False
      bArgTwoIsInt = False

      bArgOneExists = commandAction.bArgExists(commandArgs, 1)
      if not bArgOneExists:
        print("\nSpecify the number to be canceled.\n")
      else:
        bArgOneIsInt = commandAction.bArgIsInt(commandArgs, 1)
        if not bArgOneIsInt:
          print("ERROR: " + commandArgs[1] + " is not a valid number.\n")
        else:
          bArgTwoExists = commandAction.bArgExists(commandArgs, 2)
          if not bArgTwoExists:
            print("\nSpecify the number to be canceled.\n")
          else:
            bArgTwoIsInt = commandAction.bArgIsInt(commandArgs, 2)
            if not bArgTwoIsInt:
              print("ERROR: " + commandArgs[2] + " is not a valid number.\n")
      
      if (bArgOneExists and bArgOneIsInt) and (bArgTwoExists and bArgTwoIsInt):
        bCanCancel = True
        topCancel = int(commandArgs[1])
        bottomCancel = int(commandArgs[2])
        
        # cancelTop and cancelBottom specify the indeces of the items to be canceled
        cancelTop = commandAction.findNumInRow(top_row, topCancel)
        cancelBottom = commandAction.findNumInRow(bottom_row, bottomCancel)
        findDigitInfo = commandAction.findDigitInNum(bottomCancel, topCancel)
        cancelDigit = 0
        if findDigitInfo[0] == 0:
          print("ERROR: No cancelation done. Digits must match exactly.")
        elif findDigitInfo[0] == 1:
          cancelDigit = findDigitInfo[1]
        else:
          cancelDigit = input("Which digit should be canceled?: ")
          try:
            int(cancelDigit)
            cancelDigit = int(cancelDigit)
          except ValueError:
            print("Enter a valid number")

        if cancelTop == []:
          print("ERROR: The specified top row number does not exist.")
          bCanCancel=False
        if cancelBottom == []:
          print("ERROR: The specified bottom row number does not exist.")
          bCanCancel=False
        if bCanCancel:
          cancelInfo = commandAction.cancel(top_row,bottom_row,cancelTop,cancelBottom,cancelDigit)
          if cancelInfo[0] == 1:
            print("ERROR: No cancelation done. Digits must match exactly.")
          elif cancelInfo[0] == 2:
            print("ERROR: No cancelation done. Top numbers cannot cancel with their source bottom number until the bottom number is modified in some way.")
          else:
            del top_row[cancelInfo[1]]
            turnCount+=1

    elif commandArgs[0]=="exit":
      endProgram()

    elif commandArgs[0]=="restart":
      run=1
      print("\n"+separator)
      print("GAME OVER")
      print("Original puzzle:",originalPuzzle)
      print("Puzzle quit after "+str(turnCount)+" turns.")
      print(separator+"\n")

    else:
      print("\n\nEnter a valid command.")
  return


def tutorial():
  print("\n"+separator)
  print("Thanks for playing my game! I don't have a name for it yet, so i'll just call it the \"Number Game\".")
  print("\nThe game begins with two rows of numbers: the top row and the bottom row.")
  print("The end goal of the game is to get the top row to clear entirely, and the bottom row to equal 0 or 1.")
  print("\nWhen you begin, you'll have numbers in the bottom row, but the top row will be blank.")
  print("You move numbers into the top row by \"splitting\" an even number in half. Half of the number will go up to the top row, and the other half stays in the bottom row.")
  print("The number \"0\" does not move into the top row, nor does it exist as it's own number in the bottom row.")
  print("When you split an odd number, you can split it into any two numbers which add together to equal the original, but both numbers remain in the bottom row.")
  print("Splitting numbers is how you create a path to solve the puzzle.")
  print("\nYou can \"cancel\" digits in the top row with digits in the bottom row. This is how you will achieve the win condition.")
  print("ex. if the top row is [6] and the bottom row is [36, 65, 6], you can cancel the top 6 with any of the 6's in the bottom row, resulting in a blank top row and either [30, 65, 6], [36, 5, 6] or [36, 65] in the bottom row.")
  print("\nIf multiple numbers in the bottom row are equal, you can \"merge\" them together (if the bottom row is [5, 21, 5], a merge will result in [5, 21] remaining).")
  print("You cannot merge top row numbers.\n")
  print("Is it recommended to start with 5 numbers, ranging from 1-50. This is the setting for default puzzles. Adding more numbers and increasing the max size increases puzzle difficulty.")
  print("\nIMPORTANT: It is also  not allowed to split an even number, then cancel it with itself. The bottom number must be modified in some way first.")
  print("When the game ends, it will return the number of turns you took to solve the puzzle. Try to solve puzzles as effieicnetly as you can!")
  print(separator+"\n")

def example():
  print("\n"+separator)
  print("Example Game:")
  print(separator)
  print("[]")
  print("[4, 3]")
  print("~this is the start of the puzzle.")
  print(separator+"\n")
  print(separator)
  print("[]")
  print("[4, 2, 1]")
  print("~3 is split to 2 and 1.")
  print(separator+"\n")
  print(separator)
  print("[2]")
  print("[2, 2, 1]")
  print("~4 is split.")
  print(separator+"\n")
  print(separator)
  print("[2]")
  print("[2, 1]")
  print("~the 2's are merged.")
  print(separator+"\n")
  print(separator)
  print("[]")
  print("[1]")
  print("the 2's are canceled.")
  print("~top row is blank, and bottom row is 1, so the puzzle is solved.")
  print(separator+"\n")


def endProgram():
  print(endMessage)
  exit()


separator="-----------------------------------"
endMessage="Program ended. ggs"
main()
endProgram()
