import os, datetime

UPLOAD_FOLDER = os.path.abspath('static')
#creating a function that saves current date to a file
def saveDate():
    try:
        with open("date.txt", 'a') as f:
            dateNow = datetime.datetime.now().strftime("%m.%d")
            f.write(dateNow+',')
            f.close()
    except Exception as e:
        print('Could not open a file date.txt')
        print(e)
        quit()
#creating a function that calcuates all spendings and expenses
def calculateSum(exp):
    sum = 0
    for i in exp:
        if i.char == "+":
            sum+=i.price
        else:
            sum-=i.price
    return round(sum,2)
#saving the calculations from previous function to a file
def saveToFile(exp):
    try:
        with open('data.txt', 'a') as f:
            print(calculateSum(exp))
            f.write(str(calculateSum(exp))+",")
            f.close()
    except Exception as e:
        print('Could not open data.txt')
        print(e)
        quit()