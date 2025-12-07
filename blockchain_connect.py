from web3 import Web3
import json
from datetime import datetime

# ===========================================
#   Blockchain Configuration
# ===========================================
GANACHE_URL = "http://127.0.0.1:8545"  # Local Ganache RPC
CHAIN_ID = 1337  # Default Ganache chain ID
MY_ADDRESS = "0xE104AF514e60Eb2eeF60d5f3c55a590c4b32911D"
PRIVATE_KEY = "0xb73503a5b37446658598559cff5cd95eb13ab3175a3a1d0a1cef5313604202e6"

# ===========================================
#   Connect to Blockchain
# ===========================================
w3 = Web3(Web3.HTTPProvider(GANACHE_URL))
if not w3.is_connected():
    raise Exception("❌ Failed to connect to Ganache at 127.0.0.1:8545")

# Load ABI and contract address
with open("contract_abi.json") as f:
    ABI = json.load(f)
with open("contract_address.txt") as f:
    CONTRACT_ADDRESS = f.read().strip()

contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)


# ===========================================
#   Blockchain Utility Functions
# ===========================================
def log_alert_to_blockchain(session_id: str, detected: bool):
    """Log a detection event to the blockchain."""
    try:
        nonce = w3.eth.get_transaction_count(MY_ADDRESS)
        tx = contract.functions.logAlert(session_id, detected).build_transaction({
            "chainId": CHAIN_ID,
            "from": MY_ADDRESS,
            "nonce": nonce,
            "gas": 300000,
            "maxFeePerGas": w3.to_wei("60", "gwei"),
            "maxPriorityFeePerGas": w3.to_wei("2", "gwei"),
        })

        signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        raw_tx = getattr(signed_tx, "raw_transaction", None) or getattr(signed_tx, "rawTransaction", None)
        tx_hash = w3.eth.send_raw_transaction(raw_tx)
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        return receipt.transactionHash.hex()

    except Exception as e:
        print(f"⚠️ Blockchain Logging Failed: {e}")
        return None


def get_alert_count():
    """Return total number of alerts logged on blockchain."""
    try:
        return contract.functions.getAlertCount().call()
    except Exception as e:
        print(f"⚠️ Could not fetch alert count: {e}")
        return 0


def get_alert(index: int):
    """Fetch and format a specific alert by index."""
    try:
        sid, detected, ts = contract.functions.getAlert(index).call()
        # ✅ Convert timestamp (UNIX) to human-readable format
        readable_time = datetime.fromtimestamp(ts).strftime("%b %d, %Y %I:%M %p")
        return sid, detected, readable_time
    except Exception as e:
        print(f"⚠️ Could not fetch alert: {e}")
        return None, None, None
