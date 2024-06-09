from flask import Flask, render_template, request
import re


# Create a Flask application
app = Flask(__name__)


# Function to evaluate postfix expression
def evaluate_postfix(expression):
    # Initialize a stack to store operands
    stack = []

    # Iterate over each token in the postfix expression
    for token in expression.split():
        
        # Check if the token is a digit or a floating-point number
        if token.isdigit() or re.match(r'^\d+\.\d+$', token):
            stack.append(float(token))  # Push operand onto the stack
            
        else:
            # Pop two operands from the stack
            operand2 = stack.pop()
            operand1 = stack.pop()
            
            # Perform the operation based on the operator
            if token == '+':
                stack.append(operand1 + operand2)
            elif token == '-':
                stack.append(operand1 - operand2)
            elif token == '*':
                stack.append(operand1 * operand2)
            elif token == '/':
                stack.append(operand1 / operand2)
                
    # The final result is the only element left in the stack
    return stack.pop()


# Function to convert infix expression to postfix
def infix_to_postfix(infix):
    
    # Define operator precedence
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
    
    # Initialize an empty list to store the postfix expression
    postfix = []
    
    # Initialize a stack to hold operators
    stack = []

    # Tokenize the infix expression
    tokens = re.findall(r'\d+\.\d+|\d+|[+\-*/()]', infix)

    # Iterate over each token in the infix expression
    for token in tokens:
        
        # If the token is a digit or a floating-point number, append it to the postfix expression
        if token.isdigit() or re.match(r'^\d+\.\d+$', token):
            postfix.append(token)
            
        elif token == '(':
            stack.append(token)  # Push opening parenthesis onto the stack
            
        elif token == ')':
            # Pop operators from the stack and append them to the postfix expression
            # until an opening parenthesis is encountered            
            while stack and stack[-1] != '(':
                postfix.append(stack.pop())
                
            stack.pop()  # Discard the opening parenthesis
            
        else:
            # Pop operators with higher precedence from the stack and append them to the postfix expression
            # until an operator with lower precedence is encountered or the stack is empty
            while stack and precedence.get(stack[-1], 0) >= precedence.get(token, 0):
                postfix.append(stack.pop())
                
            stack.append(token)  # Push the current operator onto the stack

    # Append any remaining operators from the stack to the postfix expression
    while stack:
        postfix.append(stack.pop())

    # Join the elements of the postfix expression list into a single string
    return ' '.join(postfix)


# Define a route for the calculator application
@app.route('/', methods=['GET', 'POST'])
def calculator():
    
    result = None
    expression = ''
    
    # if request method is 'post'
    if request.method == 'POST':
        expression = request.form['expression']
        
        # Convert the infix expression to postfix
        postfix_expr = infix_to_postfix(expression)
        
        # Evaluate the postfix expression to obtain the result
        result = evaluate_postfix(postfix_expr)
        
        # Check if the result is an integer or a floating-point number
        # If it's an integer, convert it to an integer type
        if result % 1 == 0:
            result = int(result)

        # Render the calculator template
        return render_template('calculator.html', expression=expression, result=result)
    
    # if request method is 'get'
    return render_template('calculator.html')


# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
