# PODCAST AUDIO TRANSCRIPTION

## Environment Setup

Depending on your environment, install the required packages by running the following command

```bash
pip install -r requirements.txt
or
conda install --file requirements.txt
```

To make your virtual environment recognized as a Jupyter kernel in VS Code, follow these steps:

1. Ensure Jupyter is installed in the virtual environment by running the following command

    ```bash
    python -m jupyter --version
    or
    pip show jupyter
    ```

    If not found, you can install it using the command below

    ```bash
    pip install jupyter
    ```

2. Run the following command to add your virtual environment as a Jupyter kernel

    ```bash
    python -m ipykernel install --user --name=your_virtual_env_name --display-name "Python (my_env)"
    ```

    Replace `your_virtual_env_name` with the actual name of your virtual environment. The `--display-name` is what will appear in Jupyter Notebook.

3. Open VS Code and select the kernel you just created. Click on the kernel name at the top right (it might default to the system Python).

## Issues

When trying to install the `llama-cpp-python` package, you might encounter the error `ERROR: Could not find a version that satisfies the requirement llama-cpp-python`. This is due to the fact that the package is not available in the default PyPI repository. To fix this, you need to install the package from a custom index URL.

Run the following command to install the `llama-cpp-python` package from the custom index URL

```bash
pip install --no-cache-dir llama-cpp-python==0.2.77 --extra-index-url <https://abetlen.github.io/llama-cpp-python/whl/cu124>
```
