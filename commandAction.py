import random

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
  index = []
  for i in range(0, len(row)):
    if int(row[i]['value']) == int(num):
      index.append(i)
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

# num is the index here
def split(bottom_row,top_row,num,splitOut):
  # operation for even numbers
  if bottom_row[num]['value']%2 == 0:
    bottom_row[num]['value']=int(bottom_row[num]['value']/2)
    generateID(bottom_row, top_row, bottom_row[num])
    addTop(top_row,bottom_row[num])

  # operation for odd numbers
  else:
    if splitOut >= bottom_row[num]['value']:
      print("Cannot remove more than the original value.")
      return
    bottom_row[num]['value']-=splitOut
    generateID(bottom_row, top_row, bottom_row[num])
    bottom_row.append({'value':splitOut})
    generateID(bottom_row, top_row, bottom_row[-1]) # make ID for last item, which is the item just appended

# num1 is the value that the user wants to merge, not the index
def merge(bottom_row, top_row, num1):
  mergedRow=[]
  hasMerged=False
  for i in range(0, len(bottom_row)):
    if (bottom_row[i]['value'] != num1['value']):
      mergedRow.append(bottom_row[i])
    if (bottom_row[i]['value'] == num1['value'] and hasMerged==False):
      mergedRow.append(bottom_row[i])
      generateID(bottom_row, top_row, bottom_row[i])
      hasMerged=True
  if (hasMerged == False):
    return bottom_row
  if (hasMerged==True):
    return mergedRow

# top and bottom are arrays of possible indeces here
def cancel(topRow,bottomRow,top,bottom,digit):
  didCancel = [1,-1]
  
  # do this loop thing in case there's multiple nums with the same val but different ID's to avoid falsely claiming that they cannot cancel
  for iTop in top:
    for iBottom in bottom:

      topDigit=topRow[iTop]['value']
      bottomRowVal=bottomRow[iBottom]['value']
      bottomRowID = bottomRow[iBottom]['ID']
      topRowID = topRow[iTop]['ID']
      bottomRowLen=len(str(bottomRowVal))
      revisedVal=0
      hasCanceled=False

      # generate the new value after cancellation
      for digits in range(1,bottomRowLen+1):
        y=bottomRowVal%(10**digits)
        y=y//(10**(digits-1))
        if digit==digits and topDigit==y:
          if (bottomRowID != topRowID):
            revisedVal=bottomRowVal-10**(digit-1)*y
            didCancel[0] = 0
            hasCanceled=True
          else:
            didCancel[0] = 2

      if (didCancel[0] == 0):
        iCanceled = -1
        for i in range(0, len(bottomRow)):
          if bottomRow[i]['ID'] == bottomRowID and hasCanceled==True:
            iCanceled = i
            bottomRow[i]['value'] = revisedVal
            generateID(bottomRow, topRow, bottomRow[i])
        if iCanceled >= 0 and revisedVal == 0:
          del bottomRow[iCanceled]
          return didCancel
        
  return didCancel


def addTop(topRow,topNum):
  digitLen=len(str(topNum['value']))
  for digits in range(1,digitLen+1):
    y=topNum['value']%(10**digits)
    y=y//(10**(digits-1))
    if y!=0:
      topRow.append({'value':y,'ID':topNum['ID']})
  return topRow # idk if this is needed

# item is the dictionary in the bottom row
# values 1 and 2 are the bottom and top rows
# checks if any ID's have the random one, and assigns the ID of the dictionary item to that ID
def generateID(values1, values2, item):
  bInvalid = True
  xID = 0
  while (bInvalid):
    bInvalid = False
    xID = random.randint(1,0x7FFFFFFF)
    for y in values1:
      yID = y.get("ID",0)
      if xID == yID:
        bInvalid = True
    for y in values2:
      yID = y.get("ID",0)
      if xID == yID:
        bInvalid = True
    item["ID"] = xID
