from flask import Flask, request, render_template_string

# Flask app
app = Flask(__name__)

# Python implementation of the 4th Order Runge-Kutta Method
def runge_kutta(f, x0, y0, x_end, h):
    """
    Solves an ODE using the 4th order Runge-Kutta method.

    Parameters:
        f (function): The function f(x, y) that defines the ODE y' = f(x, y).
        x0 (float): Initial value of x.
        y0 (float): Initial value of y.
        x_end (float): The value of x at which to stop the calculation.
        h (float): Step size.

    Returns:
        list of tuple: A list of (x, y) values at each step.
    """
    steps = []  # To store the results

    x = x0
    y = y0
    steps.append((x, y))

    while x < x_end:
        # Ensure we do not go beyond x_end
        if x + h > x_end:
            h = x_end - x

        # Compute Runge-Kutta terms
        k1 = h * f(x, y)
        k2 = h * f(x + h / 2, y + k1 / 2)
        k3 = h * f(x + h / 2, y + k2 / 2)
        k4 = h * f(x + h, y + k3)

        # Update y and x
        y = y + (k1 + 2 * k2 + 2 * k3 + k4) / 6
        x = x + h

        # Store the current step
        steps.append((x, y))

    return steps

# HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Runge-Kutta Solver</title>
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background-color: #f8f9fa;
        }
        .container {
            margin-top: 50px;
        }
        .table {
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="text-center text-primary">Runge-Kutta Method Solver</h1>
        <form method="POST" class="mt-4">
            <div class="mb-3">
                <label for="x0" class="form-label">Initial x (x0):</label>
                <input type="number" step="any" class="form-control" id="x0" name="x0" required>
            </div>
            <div class="mb-3">
                <label for="y0" class="form-label">Initial y (y0):</label>
                <input type="number" step="any" class="form-control" id="y0" name="y0" required>
            </div>
            <div class="mb-3">
                <label for="x_end" class="form-label">Final x (x_end):</label>
                <input type="number" step="any" class="form-control" id="x_end" name="x_end" required>
            </div>
            <div class="mb-3">
                <label for="h" class="form-label">Step size (h):</label>
                <input type="number" step="any" class="form-control" id="h" name="h" required>
            </div>
            <div class="mb-3">
                <label for="function" class="form-label">ODE Function f(x, y):</label>
                <input type="text" class="form-control" id="function" name="function" required placeholder="e.g., x**2 + 2*y**3">
            </div>
            <button type="submit" class="btn btn-primary w-100">Solve</button>
        </form>
        {% if solution %}
        <h2 class="text-success mt-4">Solution:</h2>
        <table class="table table-bordered table-striped">
            <thead>
                <tr>
                    <th>Step</th>
                    <th>x</th>
                    <th>y</th>
                </tr>
            </thead>
            <tbody>
                {% for i, (x, y) in enumerate(solution) %}
                <tr>
                    <td>{{ i+1 }}</td>
                    <td>{{ x|round(4) }}</td>
                    <td>{{ y|round(4) }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
        {% endif %}
    </div>
    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    solution = None
    if request.method == 'POST':
        try:
            # Get input from the user
            x0 = float(request.form['x0'])
            y0 = float(request.form['y0'])
            x_end = float(request.form['x_end'])
            h = float(request.form['h'])
            function_input = request.form['function']

            # Define the ODE function
            def user_function(x, y):
                return eval(function_input, {"x": x, "y": y})

            # Solve the ODE
            solution = runge_kutta(user_function, x0, y0, x_end, h)
        except Exception as e:
            solution = [("Error", str(e))]

    return render_template_string(HTML_TEMPLATE, solution=solution, enumerate=enumerate)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

