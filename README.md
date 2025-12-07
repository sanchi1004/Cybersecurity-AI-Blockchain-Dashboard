# Cybersecurity AI + Blockchain Dashboard

This project combines a lightweight machine‑learning model for cyberattack detection with an Ethereum smart contract to immutably log alerts. A Streamlit web app provides an interactive dashboard for predictions, model insights, and blockchain alert history.

## Overview

- AI: Trains a `RandomForestClassifier` on `cyber_dataset.csv` to predict `attack_detected` from network/session features.
- App: `app.py` collects session inputs, runs the model, and logs detection results to the blockchain.
- Blockchain: `CyberLog.sol` defines a contract with functions to record and read alerts; `blockchain_connect.py` handles Web3 interactions.
- Artifacts: Model and metadata saved via `joblib` (`*.pkl`) for inference and display in the app.

## Repo Structure

- `train_cyber_model.py`: Train, evaluate, and persist model, scaler, label encoders, and metrics.
- `cyber_dataset.csv`: Input dataset. Includes categorical fields (protocol, encryption, browser) and numerical features.
- `app.py`: Streamlit dashboard with three tabs: Prediction, Model Insights (accuracy, confusion matrix, feature importances), and Blockchain Logs.
- `CyberLog.sol`: Solidity contract storing alerts: `sessionId`, `detected`, `timestamp`.
- `blockchain_connect.py`: Web3 client, reads `contract_abi.json` and `contract_address.txt`, and exposes helpers: `log_alert_to_blockchain`, `get_alert_count`, `get_alert`.
- `contract_abi.json`: Compiled ABI of the deployed `CyberLog` contract.
- `contract_address.txt`: Address of the deployed contract.
- `README.md`: Project documentation.

## Prerequisites

- Python 3.11+ recommended.
- Node/Ganache or any Ethereum JSON‑RPC node (local at `http://127.0.0.1:8545`).
- Packages: `streamlit`, `pandas`, `numpy`, `scikit-learn`, `joblib`, `matplotlib`, `seaborn`, `web3`.

## Steps to Run Locally

### Install Dependencies

Create a virtual environment and install packages:

```zsh
python3 -m venv .venv
source .venv/bin/activate
pip install streamlit pandas numpy scikit-learn joblib matplotlib seaborn web3
```

### Train the Model

Generates the required artifacts (`*.pkl`) used by the app.

```zsh
python train_cyber_model.py
```

Outputs:

- `cyber_ai_model.pkl`: trained classifier
- `scaler.pkl`: feature scaler
- `label_encoders.pkl`: encoders for categorical fields
- `metrics.pkl`: accuracy, confusion matrix, feature importances

### Run Ganache RPC Server Locally

```zsh
"ganache"
```

Run on local terminal and save the "Available Accounts" and "Private Keys" generated

### Deploy the Smart Contract

- Open Remix, create `CyberLog.sol`, compile with Solidity `^0.8.0`.

> *Note: IT WONT WORK WITH THE LATEST COMPILER OF SOLIDITY.*

- Connect Remix to your local Ganache server and then deploy.
- Copy the deployed contract address into `contract_address.txt`.
- Export ABI from Remix and save as `contract_abi.json`.

### Configure Blockchain Connection

In `blockchain_connect.py`:

- `GANACHE_URL`: JSON‑RPC endpoint (default `http://127.0.0.1:8545`).
- `CHAIN_ID`: network chain ID (`1337` for Ganache by default).
- `MY_ADDRESS` and `PRIVATE_KEY`: Paste one of the accounts and keys from your ganache server.

Security note: For local dev, keys are in code as they are re-generated everytime new server started. For production, move keys, addresses and accounts to env or a secure store.

### Run the Dashboard Locally

```zsh
streamlit run app.py
```

Tabs:

- Prediction: enter session details, click Analyze to see prediction; result is logged to blockchain with a tx hash.
- Model Insights: view accuracy, confusion matrix, and feature importances.
- Blockchain Logs: fetch recent alerts via contract `getAlertCount`/`getAlert`.