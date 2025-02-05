# Project Name

## Setup Instructions

It is recommended to use a Python virtual environment to manage dependencies and avoid conflicts.

### 1. Create and Activate a Virtual Environment (Optional but recommended)

#### On macOS/Linux:
```sh
python3 -m venv venv
source venv/bin/activate
```

#### On Windows:
Execute this <span style="color:red;">**ONLY**</span> if you are using powershell terminal.
```powershell
Set-ExecutionPolicy AllSigned
```

```sh
python -m venv venv
venv\Scripts\activate
```

### 2. Upgrade Essential Packages

Ensure `pip`, `setuptools`, and `wheel` are up to date:
```sh
python3 -m pip install --upgrade pip
pip install --upgrade setuptools wheel
```

### 3. Install Project Dependencies

Run the following command to install the project:
```sh
pip install -e .
```

### 4. Adding Pre-Trained Model and Embeddings
To use pre-trained models and embeddings, follow these steps:

1. Download the pre-trained model and embeddings from the releases page.
2. Extract the downloaded files.
3. Place them in the following directory structure inside `src/`:

```sh
./
├─ src/
│  ├─ model/
│  │  ├─ model-best/
│  ├─ utils/
│  │  ├─ embeddings/
│  │  │  ├─ occupations_embedding.pkl
│  │  │  ├─ skills_embedding.pkl
```

Ensuring the correct directory structure will allow the program to load the model and embeddings seamlessly.

Now, your environment is set up and ready to use!

## Usage

Run the following command to use the project:
```sh
python main.py <Mode>
```

### Modes:
- `Train`: Perform model training
- `Scrape`: Perform scraping on MyCareersFuture
- `Process`: Use the trained model
