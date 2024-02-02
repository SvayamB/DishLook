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
    error_message = ""  # Initialize the variable here

    try:
        result = subprocess.run(['python', 'hacky.py', user_input],
                                capture_output=True, text=True, check=True)
        output = result.stdout
    except subprocess.CalledProcessError as e:
        error_message = e.stderr.decode('utf-8') if e.stderr else str(e)
        output = f"Error: {error_message}"

    return render_template('index.html', user_input=user_input, output=output, error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)
