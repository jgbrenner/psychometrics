# Psychometrics Project

## Overview

This project replicates Hudson Golino's workflow for generating psychometric test items using AI and performing Exploratory Graph Analysis (EGA) with R. It integrates both Python and R to create, analyze, and validate psychometric scales.

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Setup](#setup)
- [Usage](#usage)
- [Environment Variables](#environment-variables)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Project Structure

PsychometricsC9/ │
 ├── data/ 
 │└── rigid_perfectionism_items.csv # Generated test items 
 │
 ├── scripts/ 
 │ └── main.py # Main Python script 
 │ 
 ├── notebooks/ 
 │ └── analysis.ipynb # Jupyter Notebook for analysis 
 │ 
 ├── .env # Environment variables 
 ├── .gitignore # Specifies files to ignore in Git 
 ├── environment.yml # Conda environment configuration 
 ├── requirements.txt # Python dependencies 
 └── README.md # Project documentation


## Features

- **AI-Generated Test Items:** Utilizes Groq and OpenAI APIs to generate psychometric test items.
- **Embeddings:** Obtains embeddings for generated items using OpenAI's API.
- **Exploratory Graph Analysis (EGA):** Performs EGA using R's `EGAnet` package to validate psychometric scales.
- **Python and R Integration:** Seamlessly integrates Python and R using `rpy2`.
- **Secure API Key Management:** API keys are managed securely using environment variables.

## Prerequisites

- **Operating System:** Windows 10 or later
- **Software:**
  - [Anaconda](https://www.anaconda.com/products/distribution) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
  - [Visual Studio Code](https://code.visualstudio.com/)
  - [Rtools 4.4](https://cran.r-project.org/bin/windows/Rtools/) (for Windows users)
- **API Keys:**
  - [OpenAI API Key](https://platform.openai.com/account/api-keys)
  - [Groq API Key](https://groq.com/)

## Installation

### 1. Clone the Repository


git clone https://github.com/yourusername/PsychometricsC9.git
cd PsychometricsC9

conda env create -f environment.yml
conda activate psychometrics_env

pip install -r requirements.txt

R
# Install devtools if not already installed
if (!requireNamespace("devtools", quietly = TRUE)) {
    install.packages("devtools")
}

# Install EGAnet from GitHub
devtools::install_github("hfgolino/EGA")

# Install any other required packages
install.packages("EGAnet")



conda activate psychometrics_env
python scripts/main.py

## What the Script Does:

Generates Test Items: Uses Groq and OpenAI APIs to create psychometric test items.
Saves Items to CSV: Stores the generated items in data/rigid_perfectionism_items.csv.
Obtains Embeddings: Fetches embeddings for each item using OpenAI's API.
Performs EGA: Conducts Exploratory Graph Analysis using R's EGAnet package and prints the results.


### License
This project is licensed under the MIT License.