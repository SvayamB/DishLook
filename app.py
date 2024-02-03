# app.py

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
    dining_halls = request.form.getlist('diningHalls[]')  # Updated to 'diningHalls'

    error_message = ""

    try:
        # Pass the diningHalls as additional arguments to the subprocess
        result = subprocess.run(['python', 'hacky.py', user_input, *dining_halls],
                                capture_output=True, text=True, check=True)
        output = result.stdout
    except subprocess.CalledProcessError as e:
        error_message = e.stderr.decode('utf-8') if e.stderr else str(e)
        output = f"Error: {error_message}"

    return render_template('index.html', user_input=user_input, another_input=another_input,
                           dining_halls=dining_halls, output=output, error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)
