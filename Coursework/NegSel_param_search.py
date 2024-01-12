import subprocess
import numpy
from sklearn.model_selection import ParameterGrid


def parameter_search(threshold, N, max_iterations, max_age, initialDecay, decay, k):
    param_grid = {
        "threshold": threshold,
        "N": N,
        "max_iterations": max_iterations,
        "max_age": max_age,
        "initialDecay": initialDecay,
        "decay": decay,
        "k": k,
    }
    grid = ParameterGrid(param_grid)
    results = []
    for params in grid:
        # Formulate the command to run NegSelTesting.py with the current parameters
        command1 = [
            "python",
            "NegSelTraining.py",
            f'{params["threshold"]}',
            f'{params["N"]}',
            f'{params["max_iterations"]}',
            f'{params["max_age"]}',
            f'{params["initialDecay"]}',
            f'{params["decay"]}',
            f'{params["k"]}',
        ]
        command2 = ["python", "NegSelTesting.py"]
        subprocess.run(command1)
        result = subprocess.run(command2, capture_output=True, text=True).stdout.strip()
        result = result.split("\n")
        results.append({"params": params, "result": result[5:]})
    for result in results:
        print(f"Parameters: {result['params']}, \nMetric: {result['result']}\n")
    print(f"best parameters:\n")


parameter_search(
    threshold=[0.05],
    N=[500, 1000, 1500, 2000],
    max_iterations=[20],
    max_age=[3],
    initialDecay=[0.1],
    decay=[0.5],
    k=[5],
)
