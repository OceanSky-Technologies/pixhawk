# mavlink scripts

## Setup

Install [MAVSDK](https://github.com/mavlink/mavsdk/releases) for your operating system.
If you're on Windows extract the zip file to a folder of your choice and 

Set up a virtual environment and enter it:

```bash
python -m venv ./.venv

# Linux
source ./.venv/bin/activate

# Windows
# first allow virtual environments: start a terminal with admin permissions and run
Set-ExecutionPolicy Unrestricted -Force

# afterwards you can launch the venv with
.\.venv\Scripts\activate
```

Install necessary libraries inside this venv:

```bash
python -m pip install -r requirements.txt
```

If you require more python packages inside this venv, you can add them using `pip install ...` and save them to the venv using

```bash
pip freeze > requirements.txt
``````

You can leave the venv any time using

```bash
deactivate
```

In `vscode` you can create or use the existing venv with `Ctrl+Shift+P` -> `Python: Create Environment`.

## Usage

Run scripts with

```bash
python ./mavlink-scripts/orbit.py
```
