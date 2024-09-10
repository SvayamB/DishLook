
# app.py
from dining import get_menu
from dining import location_id_to_name
from difflib import SequenceMatcher
import datetime
import pytz
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_script', methods=['POST'])
def run_script():
    user_input = request.form.get('user_input', '')
    another_input = request.form.get('another_input', '')
    counties = request.form.getlist('diningHalls[]')
      # Updated to 'diningHalls'
    days=int(request.form.get('days',''))
    print(days)
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
    output=getNextDay(user_input, days, dining_halls)
    return render_template('index.html', user_input=user_input, another_input=another_input,
                           dining_halls=dining_halls, output=output, error_message=error_message)

def isSubstring(s1, s2):
    s1=s1.lower()
    s2=s2.lower()
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
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def getNextDay(Foodname, days, diningHalls):
    ny_timezone = pytz.timezone('America/New_York')
    ny_time = datetime.datetime.now(ny_timezone)
    date = ny_time.date()  
    for _ in range(days):
        for dinHall in diningHalls:
            menu = get_menu(dinHall, date)
            for item in menu:
                similarity = similar(Foodname, item['dish-name'])
                if similarity >= 0.7 or isSubstring(Foodname, item['dish-name']) != -1:
                    return f"{item['dish-name']} At {location_id_to_name(dinHall)} on {date.strftime('%m/%d/%Y')} during {item['meal-name']}"
        date += datetime.timedelta(days=1)
    
    return f"no {Foodname} found in the next {days} days."

if __name__ == '__main__':
    app.run(debug=True)




