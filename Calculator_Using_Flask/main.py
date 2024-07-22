from flask import Flask, render_template, request
import math

app = Flask(__name__)
app.config.from_object(__name__)

# Store calculation history
history = []

@app.route('/')
def Return():
    return render_template('form.html', history=history)

@app.route('/', methods=['POST'])
def Answer():
    global history
    # Get Number1
    Number1 = request.form.get("Number1", type=float)
    # Get Number2 (can be None for unary operations)
    Number2 = request.form.get("Number2", type=float)
    # Get Operation
    operation = request.form.get("operation")

    # Validate input
    if Number1 is None and operation not in ['sqrt', 'log', 'ceil']:
        Value = 'Error: Invalid input'
    else:
        try:
            if operation == '+':
                Value = Number1 + Number2
            elif operation == '-':
                Value = Number1 - Number2
            elif operation == '*':
                Value = Number1 * Number2
            elif operation == '/':
                Value = Number1 / Number2
            elif operation == 'pow':
                Value = math.pow(Number1, Number2)
            elif operation == 'sqrt':
                Value = math.sqrt(Number1)
            elif operation == 'log':
                Value = math.log2(Number1)
            elif operation == 'ceil':
                Value = math.ceil(Number1)
            else:
                Value = 'Error: Invalid operation'
        except ZeroDivisionError:
            Value = 'Error: Division by zero'
        except Exception as e:
            Value = f'Error: {e}'

    # Format the value for display
    if isinstance(Value, (int, float)):
        Value = f'{Value:.2f}'

    # Save to history if valid
    if isinstance(Value, str) and 'Error' not in Value:
        if operation in ['sqrt', 'log', 'ceil']:
            history.append(f'{operation}({Number1}) = {Value}')
        else:
            history.append(f'{Number1} {operation} {Number2} = {Value}')

    # Clear history if requested
    if 'clear' in request.form:
        history = []

    # Return a page with values
    return render_template('form.html', Value=Value, num1=Number1, num2=Number2, op=operation, history=history)

if __name__ == '__main__':
    app.run(debug=True)

