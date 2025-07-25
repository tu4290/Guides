# Advanced Python Quantitative and Mathematical Programming Techniques

## Mathematical Optimization Fundamentals

Mathematical optimization is a powerful domain that deals with finding numerically
minimums (or maximums or zeros) of a function. In `Python`, advanced optimization
techniques can be implemented using specialized `libraries` that provide sophisticated
`algorithms` for various types of optimization problems.

### Understanding Optimization Problem Types

Before applying optimization techniques, it's crucial to understand the nature of your
problem:

```python
import numpy as np
from scipy import optimize

# Different problem types require different approaches
def convex_function(x):
    """A simple convex function (has one global minimum)"""
    return (x - 2) ** 2 + 1

def non_convex_function(x):
    """A non-convex function (has multiple local minima)"""
    return np.sin(x) + 0.1 * x**2
```

---

## Advanced `SciPy` Optimization Techniques

`SciPy`'s `optimize` module provides powerful tools for black-box optimization where we
don't rely on the mathematical expression of the function:

```python
import numpy as np
from scipy import optimize

# Advanced multidimensional optimization
def rosenbrock(x):
    """The Rosenbrock function - a classic optimization test problem"""
    return sum(100.0 * (x[1:] - x[:-1]**2.0)**2.0 + (1 - x[:-1])**2.0)

# Gradient of the Rosenbrock function
def rosenbrock_gradient(x):
    grad = np.zeros_like(x)
    grad[0] = -400 * x[0] * (x[1] - x[0]**2) - 2 * (1 - x[0])
    grad[1:-1] = 200 * (x[1:-1] - x[:-2]**2) - 400 * x[1:-1] * (x[2:] - x[1:-1]**2) - 2 * (1 - x[1:-1])
    grad[-1] = 200 * (x[-1] - x[-2]**2)
    return grad

# Using BFGS algorithm with analytical gradient for efficiency
result = optimize.minimize(
    rosenbrock,
    x0=np.array([-1.2, 1.0]),
    method='BFGS',
    jac=rosenbrock_gradient,
    options={'gtol': 1e-8, 'disp': True}
)
```

---

## Constrained Optimization Superpower Techniques

For problems with `constraints`, advanced techniques can be applied:

```python
import numpy as np
from scipy import optimize

# Objective function to minimize
def objective(x):
    return x[0]**2 + x[1]**2

# Constraint: x[0]**2 + x[1] - 1 >= 0
def constraint1(x):
    return x[0]**2 + x[1] - 1

# Constraint: x[0] + x[1]**2 >= 0
def constraint2(x):
    return x[0] + x[1]**2

# Constraints must be formulated as dictionaries
constraints = [
    {'type': 'ineq', 'fun': constraint1},
    {'type': 'ineq', 'fun': constraint2}
]

# Bounds for variables
bounds = [(-2, 2), (-2, 2)]

# Initial guess
x0 = [0, 0]

# SLSQP is powerful for constrained optimization
result = optimize.minimize(
    objective,
    x0,
    method='SLSQP',
    bounds=bounds,
    constraints=constraints,
    options={'ftol': 1e-9, 'disp': True, 'maxiter': 1000}
)
```

---

## Advanced Linear Algebra with `NumPy`

`NumPy` provides sophisticated linear `algebra` capabilities essential for quantitative
computing:

```python
import numpy as np

# Advanced matrix decompositions
def advanced_matrix_operations(matrix):
    # Singular Value Decomposition - powerful for dimensionality reduction
    U, S, Vh = np.linalg.svd(matrix, full_matrices=False)

    # Eigendecomposition - essential for PCA and other techniques
    eigenvalues, eigenvectors = np.linalg.eig(matrix)

    # QR decomposition - useful for solving linear systems
    Q, R = np.linalg.qr(matrix)

    # Cholesky decomposition - efficient for positive definite matrices
    try:
        L = np.linalg.cholesky(matrix @ matrix.T) # Ensure positive definite
    except np.linalg.LinAlgError:
        L = None

    # Compute matrix condition number - important for numerical stability
    cond = np.linalg.cond(matrix)

    return {
        'svd': (U, S, Vh),
        'eigen': (eigenvalues, eigenvectors),
        'qr': (Q, R),
        'cholesky': L,
        'condition_number': cond
    }

# Create a test matrix
A = np.array([[4, 2, 1], [2, 5, 3], [1, 3, 6]])
results = advanced_matrix_operations(A)
```

---

## Numerical Integration and Differential Equations

Advanced quantitative programming often requires solving differential `equations` and
performing numerical `integration`:

```python
import numpy as np
from scipy import integrate

# Advanced numerical integration techniques
def complex_function(x):
    return np.sin(x) / (1 + x**2)

# Adaptive quadrature for difficult integrals
result, error = integrate.quad(complex_function, 0, np.inf)

# Solving ordinary differential equations
def lorenz_system(t, state, sigma=10, beta=8/3, rho=28):
    """The Lorenz system of differential equations."""
    x, y, z = state
    dx_dt = sigma * (y - x)
    dy_dt = x * (rho - z) - y
    dz_dt = x * y - beta * z
    return [dx_dt, dy_dt, dz_dt]

# Initial conditions
initial_state = [1.0, 1.0, 1.0]
# Time points
t = np.linspace(0, 50, 10000)

# Solve the ODE system using an adaptive method
solution = integrate.solve_ivp(
    lorenz_system,
    [0, 50],
    initial_state,
    t_eval=t,
    method='RK45', # Runge-Kutta 4(5)
    rtol=1e-6,    # Relative tolerance
    atol=1e-9     # Absolute tolerance
)
```

---

## Symbolic Mathematics with `SymPy`

For advanced mathematical manipulations, `SymPy` provides symbolic computation
capabilities:

```python
import sympy as sp

# Define symbolic variables
x, y, z = sp.symbols('x y z')

# Define a complex expression
expression = sp.sin(x) * sp.exp(-(x**2 + y**2)) + sp.cos(y) * sp.log(1 + z**2)

# Symbolic differentiation
dx_expression = sp.diff(expression, x)
dy_expression = sp.diff(expression, y)
dz_expression = sp.diff(expression, z)

# Convert symbolic expressions to functions for numerical evaluation
f_numerical = sp.lambdify((x, y, z), expression, 'numpy')
df_dx_numerical = sp.lambdify((x, y, z), dx_expression, 'numpy')

# Symbolic integration
integral = sp.integrate(sp.sin(x) * sp.exp(-x**2), (x, -sp.oo, sp.oo))

# Solve equations symbolically
solution = sp.solve(sp.Eq(x**2 - 4, 0), x)
```

---

## Advanced Statistical Methods

Quantitative programming often requires sophisticated statistical techniques:

```python
import numpy as np
from scipy import stats
import pymc3 as pm # Added for the Bayesian inference part

# Generate synthetic data
np.random.seed(42)
data = np.random.normal(loc=5, scale=2, size=1000)

# Advanced statistical tests
# Shapiro-Wilk test for normality
normality_test = stats.shapiro(data)

# Bootstrap confidence intervals
def bootstrap_mean_ci(data, n_bootstrap=10000, ci=0.95):
    bootstrap_means = np.zeros(n_bootstrap)
    for i in range(n_bootstrap):
        bootstrap_sample = np.random.choice(data, size=len(data), replace=True)
        bootstrap_means[i] = np.mean(bootstrap_sample)

    # Calculate confidence interval
    alpha = (1 - ci) / 2
    lower_bound = np.percentile(bootstrap_means, 100 * alpha)
    upper_bound = np.percentile(bootstrap_means, 100 * (1 - alpha))
    return lower_bound, upper_bound

mean_ci = bootstrap_mean_ci(data)

# Bayesian inference with PyMC3
with pm.Model() as model:
    # Prior
    mu = pm.Normal('mu', mu=0, sigma=10)
    sigma = pm.HalfNormal('sigma', sigma=10)

    # Likelihood
    likelihood = pm.Normal('likelihood', mu=mu, sigma=sigma, observed=data)

    # Inference
    trace = pm.sample(2000, tune=1000, cores=2)

    # Extract posterior distribution
    posterior_mu = trace['mu']
    posterior_sigma = trace['sigma']
```

---

## Sources

*   Mathematical optimization: finding minima of functions — `Scipy` lecture notes
*   Optimization and root finding - `Numpy` and `Scipy` Documentation
*   A Gentle Introduction to Advanced Quantitative Finance with `Python`
