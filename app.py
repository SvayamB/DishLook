# app.py
from umass_toolkit.dining import get_menu
from umass_toolkit.dining import location_id_to_name
from difflib import SequenceMatcher
import datetime
from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_script', methods=['POST'])
def run_script():
    user_input = request.form.get('user_input', '')
    another_input = request.form.get('another_input', '')
    counties = request.form.getlist('diningHalls[]')  # Updated to 'diningHalls'

    error_message = ""
    '''
    try:
        # Pass the diningHalls as additional arguments to the subprocess
        result = subprocess.run(['python', 'hacky.py', user_input, *dining_halls],
                                capture_output=True, text=True, check=True)
        output = result.stdout
    except subprocess.CalledProcessError as e:
        error_message = e.stderr.decode('utf-8') if e.stderr else str(e)
        output = f"Error: {error_message}"
    '''
    dining_halls=[]
    if 'worcester' in counties:
        dining_halls.append(1)
    if 'franklin' in counties:
        dining_halls.append(2)
    if 'hampshire' in counties:
        dining_halls.append(3)
    if 'berkshire' in counties:
        dining_halls.append(4)
    output=getFoodNuts(user_input, 15, dining_halls)
    return render_template('index.html', user_input=user_input, another_input=another_input,
                           dining_halls=dining_halls, output=output, error_message=error_message)

def isSubstring(s1, s2):
    M = len(s1.lower())
    N = len(s2.lower())

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
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

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



if __name__ == '__main__':
    app.run(debug=True)


