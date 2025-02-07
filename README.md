# Project Name

## Setup Instructions

It is recommended to use a Python virtual environment to manage dependencies and avoid conflicts.

### 1. Create and Activate a Virtual Environment (Optional but recommended)

#### On macOS/Linux:
```sh
python -m venv venv
source venv/bin/activate
```

#### On Windows:
Execute this <span style="color:red;">**ONLY**</span> if you are using powershell terminal.
```powershell
Set-ExecutionPolicy AllSigned
OR
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

```sh
python -m venv venv
venv\Scripts\activate
```

### 2. Upgrade Essential Packages

Ensure `pip`, `setuptools`, and `wheel` are up to date:
```sh
python -m pip install --upgrade pip
pip install --upgrade setuptools wheel
```

### 3. Install Project Dependencies

Run the following command to install the project:
```sh
pip install -e .
```
### 4. Adding Embeddings
Add the embeddings to the program:
1. Download the embeddings from the releases page (embeddings.zip).
2. Extract the embeddings
3. Place it in the following directory structure inside `src/`:
```sh
./
├─ src/
│  ├─ utils/
│  │  ├─ embeddings/
│  │  │  ├─ occupations_embedding.pkl
│  │  │  ├─ skills_embedding.pkl
```
Now, your environment is set up and ready to use!
## Using Prepared Data (Optional)
### Using Pre-Trained Model
To use pre-trained models, follow these steps:

1. Download the pre-trained model from the releases page (model.zip).
2. Extract the model.
3. Place it in the following directory structure inside `src/`:

```sh
./
├─ src/
│  ├─ model/
│  │  ├─ model-best/
```

### Using Prepared Datasets
To use prepared datasets, follow these steps:
1. Download the prepared datasets from the releases page (datasets.zip).
2. Extract the datasets
3. Place it in the following directory structure inside `src/`:

```sh
./
├─ src/
│  ├─ datasets/
│  │  ├─ [The datasets to use]
```

Available datasets provided:
- Training Data
    - job_desc.csv
        - Contains raw data of job listings
        - Intended to be used for Google Gemini auto labelling
    - job_desc_with_skills.csv
        - Contains annotated data from Google Gemini
        - Intended to be used starting from the Data Cleaning step
- Processing Data
    - job_listing.csv
        - Contains scraped data from MyCareersFuture website
        - Intended to be used by model for processing
- Out-of-the-box Data
    - job_listing_normalized.csv
        - Contains normalized scraped data that the model processed
        - Intended to be directly used by the web server  


## Usage

Run the following command to use the project:
```sh
python main.py <Mode>
```

### Modes:
- `Train`: Perform model training
- `Scrape`: Perform scraping on MyCareersFuture
- `Process`: Use the trained model
