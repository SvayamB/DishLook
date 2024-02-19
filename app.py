# app.py
from dining import getDay
from flask import Flask, render_template, request

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
    output=getDay(user_input, 15, dining_halls)
    return render_template('index.html', user_input=user_input, another_input=another_input,
                           dining_halls=dining_halls, output=output, error_message=error_message)





if __name__ == '__main__':
    app.run(debug=True)



