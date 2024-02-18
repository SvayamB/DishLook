# UMass DishLookup

Welcome to UMass DishLookup! This is a brief guide to help you get started.

## Getting Started

1. **Clone the Repository**: First, navigate to the directory (on your terminal) where you want to clone the repository (store this file).
    ```bash
    git clone https://github.com/SvayamB/DishLook.git
    ```

2. **Navigate to the Project Directory**: Move into the project directory.
    ```bash
    cd DishLook
    ```

## Installation

After navigating to the project directory, install the necessary dependencies using `pip` and the provided `requirements.txt` file.

```bash
pip install -r requirements.txt
```
## Usage

To run the application, execute the respective command:
### MacOS
```bash
gunicorn app:app
```

### Windows
```bash
waitress-serve app:app
```

