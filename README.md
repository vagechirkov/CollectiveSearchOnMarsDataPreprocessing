## Example Traces Plot

![docs/2F3BA89351BC480A_689DD7AEB301A55E_CF40933BA34EDB9_traces.gif](docs/2F3BA89351BC480A_689DD7AEB301A55E_CF40933BA34EDB9_traces.gif)

## Virtual Environment

To create a virtual environment and install the required packages, follow these steps:

1. Open a command line interface and navigate to the directory where you want to create the virtual environment.

2. Use the `venv` command to create the virtual environment, specifying the name of the environment (e.g. `myenv`):

    ```
    python3 -m venv myenv
    ```

3. Activate the virtual environment by running the `activate` script in the environment's `bin` directory:

    ```
    source myenv/bin/activate
    ```

4. Use the `pip` command to install the required packages from the `requirements.txt` file:

    ```
    pip install -r requirements.txt
    ```

5. When you are finished working with the virtual environment, deactivate it by running the `deactivate` command.
