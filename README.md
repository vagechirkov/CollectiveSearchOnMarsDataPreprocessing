## Example Trace Plot (time is 3x faster than real time)

![Example Trace Plot](docs/fast_e210f5fb3b144b9e9044ea524ea0f75a_traces.gif)

The corresponding csv file is [here](docs/e210f5fb3b144b9e9044ea524ea0f75a_traces.csv).

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


## .env File

```dotenv
API_KEY=<PlayFab API key>
TITLE_ID=<PlayFab title ID>
SEGMENT_ID=<PlayFab segment ID>
```