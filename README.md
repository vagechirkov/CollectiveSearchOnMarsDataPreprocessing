# Virtual Environment

To create a virtual environment and install the required packages, follow these steps:

1. Open a command line interface and navigate to the directory where you want to create the virtual environment.

2. Use the `venv` command to create the virtual environment, specifying the name of the environment (e.g. `myenv`):

    ```
    python -m venv myenv
    ```

3. Activate the virtual environment by running the `activate` script in the environment's `bin` directory:

    ```
    myenv/bin/activate
    ```

4. Use the `pip` command to install the required packages from the `requirements.txt` file:

    ```
    pip install -r requirements.txt
    ```

5. When you are finished working with the virtual environment, deactivate it by running the `deactivate` command.
