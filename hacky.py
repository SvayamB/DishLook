from umass_toolkit.dining import get_menu
from umass_toolkit.dining import location_id_to_name
from difflib import SequenceMatcher
import datetime
def isSubstring(s1, s2):
    M = len(s1)
    N = len(s2)

    # A loop to slide pat[] one by one
    for i in range(N - M + 1):

        # For current index i,
        # check for pattern match
        for j in range(M):
            if (s2[i + j] != s1[j]):
                break

        if j + 1 == M:
            return i

    return -1


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def getFoodNuts(Foodname,days,diningHalls):
    indexes=diningHalls#1 wussy,2 frank,3 hamp, 4 berk
    found=0
    count=0
    date = datetime.date.today()
    while (found==0 and count<days):
        for dinHall in indexes:
            menu=get_menu(dinHall,date)
            for items in menu:
                if (similar(Foodname,items['dish-name'])==0.8 or items['dish-name'].__contains__(Foodname)):
                    found=items
                if found!=0:
                    return (items['dish-name']+" At "+location_id_to_name(dinHall)+str(dinHall)+" on "+ date.strftime("%m/%d/%Y")+" during "+ found['meal-name'])
        date=date + datetime.timedelta(days = 1)
        count=count+1
    return "not be any " + Foodname + " in the next 15 days"
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python hacky.py <user_input>")
        sys.exit(1)

    inp = sys.argv[1]
    counties = sys.argv[2:]
    diningHalls=[]
    if 'worcester' in counties:
        diningHalls.append(1)
    if 'franklin' in counties:
        diningHalls.append(2)
    if 'hampshire' in counties:
        diningHalls.append(3)
    if 'berkshire' in counties:
        diningHalls.append(4)
    # Your existing code that uses user_input goes here
    print(getFoodNuts(inp, 15, diningHalls))

if __name__ == "__main__":
    main()




