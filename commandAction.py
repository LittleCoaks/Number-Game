def help():
  print("\nCommands:")
  print("split [x] [y]")
  print("- [y] argument is optional.")
  print("- If an even number: splits the number [x] in half. Half stays on bottom row and half goes to top row.")
  print("- If an odd number: subtracts [y] from [x]. Both numbers stay on bottom row. If [y] is not provided, you will be promted to specify it.\n")
  print("merge [x]")
  print("- Combines all numbers equal to [x] to one term.\n")
  print("cancel [x] [y]")
  print("- Removes [x] and the digit of [y] where [x] is found, where [x] is a top row number and [y] is a bottom row number.")
  print("- If [x] appears more than once in [y], you will be prompted to specify which digit\n")
  print("restart")
  print("- Ends the game before the puzzle is solved\n")


# returns the first ndex where number exists
# if not exists, returns -1
def findNumInRow(row,num):
  index = -1
  for i in range(0, len(row)):
    if int(row[i]) == int(num):
      index = i
      return index
  return index

# index 0 is number of instances where digit was found in the number
# index 1 is the digit where it was found
def findDigitInNum(num,digit):
  num = str(num)
  numList = list(num)
  numListRev = []
  foundDigit = 0
  foundDigitNum = 0
  finalInfo = []
  for d in range(len(numList),0,-1):
    numListRev.append(int(numList[(d - 1)]))
  for i in range(len(numListRev)):
    if numListRev[i] == digit:
      foundDigit += 1
      foundDigitNum = i + 1
  finalInfo.append(foundDigit)
  finalInfo.append(foundDigitNum)
  return finalInfo

def bArgExists(lis, i):
  bExists = False
  try:
    lis[i]
    bExists = True
  except IndexError:
    pass
  return bExists

def bArgIsInt(lis, i):
  bIsInt = False
  try:
    int(lis[i])
    bIsInt = True
  except ValueError:
    pass
  return bIsInt

def split(bottom_row,top_row,num,splitOut):
  # operation for even numbers
  if bottom_row[num]%2 == 0:
    bottom_row[num]=int(bottom_row[num]/2)
    addTop(top_row,bottom_row[num])

  # operation for odd numbers
  else:
    if splitOut >= bottom_row[num]:
      print("Cannot remove more than the original value.")
      return
    bottom_row[num]-=splitOut
    bottom_row.append(splitOut)


def merge(bottom_row,num1):
  mergedRow=[]
  hasMerged=False
  for vals in bottom_row:
    if (vals != num1):
      mergedRow.append(vals)
    if (vals == num1 and hasMerged==False):
      mergedRow.append(vals)
      hasMerged=True
  if (hasMerged == False):
    return bottom_row
  if (hasMerged==True):
    return mergedRow


def cancel(topRow,bottomRow,top,bottom,digit):
  topDigit=topRow[top]
  bottomRowVal=bottomRow[bottom]
  bottomRowLen=len(str(bottomRowVal))
  revisedVal=int
  hasCanceled=False
  canceledBottom=[]
  for digits in range(1,bottomRowLen+1):
    y=bottomRowVal%(10**digits)
    y=y//(10**(digits-1))
    if digit==digits and topDigit==y:
      revisedVal=bottomRowVal-10**(digit-1)*y
      hasCanceled=True
  for vals in bottomRow:
    if vals == bottomRowVal and hasCanceled==True and revisedVal!=0:
      canceledBottom.append(revisedVal)
    elif not (vals == bottomRowVal and revisedVal==0):
      canceledBottom.append(vals)
  return canceledBottom


def addTop(topRow,topNum):
  digitLen=len(str(topNum))
  for digits in range(1,digitLen+1):
    y=topNum%(10**digits)
    y=y//(10**(digits-1))
    if y!=0:
      topRow.append(y)
  return topRow

