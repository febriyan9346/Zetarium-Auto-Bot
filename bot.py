import os
import time
import random
from datetime import datetime
import pytz
from colorama import Fore, Style, init
import requests
from typing import Optional, Dict, List
from eth_account import Account
from eth_account.messages import encode_defunct
from web3 import Web3

os.system('clear' if os.name == 'posix' else 'cls')

import warnings
warnings.filterwarnings('ignore')

import sys
if not sys.warnoptions:
    os.environ["PYTHONWARNINGS"] = "ignore"

init(autoreset=True)

RPC_URL = "https://data-seed-prebsc-1-s1.binance.org:8545"
TOKEN_ADDRESS = "0x2186fc0e8404eCF9F63cCBf1C75d5fAF6B843786"
MARKET_CONTRACT_ADDRESS = "0x852a5C778034e0776181955536528347Aa901d24"
FAUCET_CONTRACT_ADDRESS = "0xc9e16209Ed6B2A4f41b751788FE74F5c0B7F8E1c"

class ZetariumBot:
    def __init__(self):
        self.base_url = "https://airdrop-data.zetarium.world"
        self.api_url = "https://api.zetarium.world"
        self.prediction_url = "https://prediction-market-api.zetarium.world"
        self.w3 = Web3(Web3.HTTPProvider(RPC_URL))
        self.trade_count_per_account = 1
        
        self.token_abi = [
            {"constant":False,"inputs":[{"name":"spender","type":"address"},{"name":"amount","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"payable":False,"stateMutability":"nonpayable","type":"function"},
            {"constant":True,"inputs":[{"name":"account","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},
            {"constant":True,"inputs":[{"name":"owner","type":"address"},{"name":"spender","type":"address"}],"name":"allowance","outputs":[{"name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"}
        ]
        
        self.market_abi = [
            {
                "constant": False,
                "inputs": [
                    {"name": "marketId", "type": "uint256"},
                    {"name": "outcome", "type": "uint8"},
                    {"name": "amount", "type": "uint256"}
                ],
                "name": "makePrediction",
                "outputs": [],
                "payable": False,
                "stateMutability": "nonpayable",
                "type": "function"
            }
        ]

        self.faucet_abi = [
            {
                "constant": False,
                "inputs": [],
                "name": "claim",
                "outputs": [],
                "payable": False,
                "stateMutability": "nonpayable",
                "type": "function"
            }
        ]

    def get_wib_time(self):
        wib = pytz.timezone('Asia/Jakarta')
        return datetime.now(wib).strftime('%H:%M:%S')
    
    def print_banner(self):
        banner = f"""
{Fore.CYAN}ZETARIUM AUTO BOT{Style.RESET_ALL}
{Fore.WHITE}By: FEBRIYAN{Style.RESET_ALL}
{Fore.CYAN}============================================================{Style.RESET_ALL}
"""
        print(banner)
    
    def log(self, message, level="INFO"):
        time_str = self.get_wib_time()
        
        if level == "INFO":
            color = Fore.CYAN
            symbol = "[INFO]"
        elif level == "SUCCESS":
            color = Fore.GREEN
            symbol = "[SUCCESS]"
        elif level == "ERROR":
            color = Fore.RED
            symbol = "[ERROR]"
        elif level == "WARNING":
            color = Fore.YELLOW
            symbol = "[WARNING]"
        elif level == "CYCLE":
            color = Fore.MAGENTA
            symbol = "[CYCLE]"
        elif level == "BET":
            color = Fore.MAGENTA
            symbol = "[BET]"
        else:
            color = Fore.WHITE
            symbol = "[LOG]"
        
        print(f"[{time_str}] {color}{symbol} {message}{Style.RESET_ALL}")
    
    def random_delay(self, min_sec=2, max_sec=5):
        delay = random.randint(min_sec, max_sec)
        time.sleep(delay)
    
    def show_proxy_menu(self):
        print(f"{Fore.CYAN}Select Mode:{Style.RESET_ALL}")
        print(f"{Fore.GREEN}1. Run with proxy")
        print(f"2. Run without proxy{Style.RESET_ALL}")
        print(f"{Fore.CYAN}============================================================{Style.RESET_ALL}")
        while True:
            try:
                choice = input(f"{Fore.GREEN}Enter your choice (1/2): {Style.RESET_ALL}").strip()
                if choice in ['1', '2']:
                    return choice == '1'
                else:
                    print(f"{Fore.RED}Invalid choice! Please enter 1 or 2.{Style.RESET_ALL}")
            except KeyboardInterrupt:
                exit(0)

    def show_action_menu(self):
        print(f"{Fore.CYAN}============================================================{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Select Mode:{Style.RESET_ALL}")
        print(f"{Fore.GREEN}1. Run Daily Checkin")
        print(f"2. Run Faucet + Trades")
        print(f"3. Run All{Style.RESET_ALL}")
        print(f"{Fore.CYAN}============================================================{Style.RESET_ALL}")
        while True:
            try:
                choice = input(f"{Fore.GREEN}Enter your choice (1/2/3): {Style.RESET_ALL}").strip()
                if choice in ['1', '2', '3']:
                    if choice in ['2', '3']:
                        try:
                            count = int(input(f"{Fore.GREEN}How many times do you want to trade : {Style.RESET_ALL}"))
                            self.trade_count_per_account = count
                        except ValueError:
                            self.trade_count_per_account = 1
                    return choice
                else:
                    print(f"{Fore.RED}Invalid choice! Please enter 1, 2 or 3.{Style.RESET_ALL}")
            except KeyboardInterrupt:
                exit(0)
    
    def countdown(self, seconds):
        for i in range(seconds, 0, -1):
            hours = i // 3600
            minutes = (i % 3600) // 60
            secs = i % 60
            print(f"\r{Fore.CYAN}[COUNTDOWN]{Style.RESET_ALL} Next cycle in: {hours:02d}:{minutes:02d}:{secs:02d} ", end="", flush=True)
            time.sleep(1)
        print("\r" + " " * 60 + "\r", end="", flush=True)

    def check_balance(self, private_key):
        try:
            account = self.w3.eth.account.from_key(private_key)
            wallet = account.address
            token_contract = self.w3.eth.contract(address=Web3.to_checksum_address(TOKEN_ADDRESS), abi=self.token_abi)
            balance = token_contract.functions.balanceOf(wallet).call()
            balance_usdc = self.w3.from_wei(balance, 'ether')
            return float(balance_usdc)
        except Exception as e:
            self.log(f"Balance check failed: {e}", "ERROR")
            return 0

    def check_and_approve(self, private_key, amount_wei):
        try:
            account = self.w3.eth.account.from_key(private_key)
            wallet = account.address
            token_contract = self.w3.eth.contract(address=Web3.to_checksum_address(TOKEN_ADDRESS), abi=self.token_abi)
            spender = Web3.to_checksum_address(MARKET_CONTRACT_ADDRESS)

            allowance = token_contract.functions.allowance(wallet, spender).call()
            
            if allowance < amount_wei:
                self.log("Approving USDC...", "INFO")
                max_amount = 115792089237316195423570985008687907853269984665640564039457584007913129639935
                tx = token_contract.functions.approve(spender, max_amount).build_transaction({
                    'from': wallet,
                    'nonce': self.w3.eth.get_transaction_count(wallet),
                    'gas': 100000,
                    'gasPrice': self.w3.eth.gas_price
                })
                signed_tx = self.w3.eth.account.sign_transaction(tx, private_key)
                tx_hash = self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
                self.w3.eth.wait_for_transaction_receipt(tx_hash)
                
                time_str = self.get_wib_time()
                print(f"[{time_str}] {Fore.GREEN}[SUCCESS] USDC Approved! Hash: {tx_hash.hex()[:10]}...{Style.RESET_ALL}")
                time.sleep(3)
            return True
        except Exception as e:
            self.log(f"Approve Failed: {e}", "ERROR")
            return False

    def claim_faucet(self, private_key):
        try:
            account = self.w3.eth.account.from_key(private_key)
            wallet = account.address
            
            contract = self.w3.eth.contract(address=Web3.to_checksum_address(FAUCET_CONTRACT_ADDRESS), abi=self.faucet_abi)
            contract_func = contract.functions.claim()

            try:
                gas_estimate = contract_func.estimate_gas({'from': wallet})
                gas_limit = int(gas_estimate * 1.2)
            except Exception as e:
                self.log("Faucet Already Claimed", "WARNING")
                return False

            tx = contract_func.build_transaction({
                'from': wallet,
                'nonce': self.w3.eth.get_transaction_count(wallet),
                'gas': gas_limit,
                'gasPrice': self.w3.eth.gas_price
            })

            signed_tx = self.w3.eth.account.sign_transaction(tx, private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
            
            self.log(f"Faucet Tx Sent! Explorer: https://testnet.bscscan.com/tx/{tx_hash.hex()}", "INFO")

            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=60)

            if receipt.status == 1:
                time_str = self.get_wib_time()
                print(f"[{time_str}] {Fore.GREEN}[SUCCESS] Faucet Claimed Successfully!{Style.RESET_ALL}")
                return True
            else:
                self.log("Transaction Failed on Blockchain", "ERROR")
                return False

        except Exception as e:
            self.log(f"Faucet Error: {str(e)}", "ERROR")
            return False

    def buy_prediction(self, private_key, market_id, outcome, token_amount):
        try:
            account = self.w3.eth.account.from_key(private_key)
            wallet = account.address
            amount_wei = self.w3.to_wei(token_amount, 'ether')

            token_contract = self.w3.eth.contract(address=Web3.to_checksum_address(TOKEN_ADDRESS), abi=self.token_abi)
            balance = token_contract.functions.balanceOf(wallet).call()
            
            if balance < amount_wei:
                self.log(f"Insufficient USDC Balance! Has: {self.w3.from_wei(balance, 'ether')}", "ERROR")
                return False

            if not self.check_and_approve(private_key, amount_wei):
                return False

            market_contract = self.w3.eth.contract(address=Web3.to_checksum_address(MARKET_CONTRACT_ADDRESS), abi=self.market_abi)
            
            outcome_str = "YES" if outcome == 1 else "NO"
            self.log(f"Placing Bet... ID: {market_id} | Pick: {outcome_str} | Amt: {token_amount} USDC", "BET")
            
            contract_func = market_contract.functions.makePrediction(
                int(market_id), 
                int(outcome), 
                amount_wei
            )

            try:
                gas_estimate = contract_func.estimate_gas({'from': wallet})
                gas_limit = int(gas_estimate * 1.2)
            except Exception as e:
                self.log(f"Betting Rejected (Market Closed/Error). Retrying...", "WARNING")
                return False

            nonce = self.w3.eth.get_transaction_count(wallet, 'pending')
            
            tx = contract_func.build_transaction({
                'from': wallet,
                'nonce': nonce,
                'gas': gas_limit, 
                'gasPrice': self.w3.eth.gas_price
            })
            
            signed_tx = self.w3.eth.account.sign_transaction(tx, private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
            
            self.log(f"Tx Sent! Explorer: https://testnet.bscscan.com/tx/{tx_hash.hex()}", "INFO")
            
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
            
            if receipt.status == 1:
                time_str = self.get_wib_time()
                print(f"[{time_str}] {Fore.GREEN}[SUCCESS] Bet Placed Successfully!{Style.RESET_ALL}")
                return True
            else:
                self.log("Transaction Failed on Blockchain", "ERROR")
                return False

        except Exception as e:
            self.log(f"Buy Error: {str(e)}", "ERROR")
            return False

    def get_prediction_markets(self, proxy: Optional[str] = None) -> Optional[Dict]:
        headers = {
            "accept": "*/*", "user-agent": "Mozilla/5.0",
            "origin": "https://prediction.zetarium.world"
        }
        proxies = {"http": proxy, "https": proxy} if proxy else None
        try:
            response = requests.get(f"{self.prediction_url}/markets?limit=200", headers=headers, proxies=proxies, timeout=30)
            return response.json() if response.status_code == 200 else None
        except: return None

    def get_user_info(self, token, proxy=None):
        headers = {"authorization": f"Bearer {token}", "user-agent": "Mozilla/5.0"}
        proxies = {"http": proxy, "https": proxy} if proxy else None
        try:
            res = requests.get(f"{self.base_url}/auth/me", headers=headers, proxies=proxies, timeout=30)
            return res.json() if res.status_code == 200 else None
        except: return None

    def sign_message(self, private_key: str, message: str) -> Optional[str]:
        try:
            account = Account.from_key(private_key)
            message_hash = encode_defunct(text=message)
            signed = account.sign_message(message_hash)
            return "0x" + signed.signature.hex()
        except: return None

    def get_wallet_address(self, private_key: str) -> Optional[str]:
        try:
            account = Account.from_key(private_key)
            return account.address
        except Exception as e:
            self.log(f"Invalid private key: {str(e)}", "ERROR")
            return None

    def claim_daily_gm(self, token, private_key, wallet, proxy=None):
        headers = {"authorization": f"Bearer {token}", "content-type": "application/json", "user-agent": "Mozilla/5.0"}
        proxies = {"http": proxy, "https": proxy} if proxy else None
        try:
            account = Account.from_key(private_key)
            msg = f"GM! Claim daily points - {account.address.lower()}"
            sig = self.sign_message(private_key, msg)
            if not sig: return {"success": False}
            
            res = requests.post(f"{self.api_url}/api/profile/{account.address}/gm", json={"message": msg, "signature": sig}, headers=headers, proxies=proxies)
            if res.status_code == 200: return res.json()
            elif res.status_code == 400: return {"success": False, "already_claimed": True}
            return {"success": False, "error": res.text}
        except Exception as e: return {"success": False, "error": str(e)}

    def load_accounts(self, filename: str = "accounts.txt") -> List[Dict[str, str]]:
        try:
            accounts = []
            with open(filename, 'r') as f:
                content = f.read().split('\n\n')
            for block in content:
                lines = block.strip().split('\n')
                acc = {}
                for line in lines:
                    if '=' in line:
                        k, v = line.split('=', 1)
                        acc[k.strip().lower()] = v.strip()
                if 'token' in acc: accounts.append(acc)
            return accounts
        except FileNotFoundError:
            self.log(f"File {filename} not found!", "ERROR")
            return []
        except Exception as e:
            self.log(f"Failed to read file: {str(e)}", "ERROR")
            return []

    def load_proxies(self, filename: str = "proxy.txt") -> List[str]:
        try:
            with open(filename, 'r') as f:
                proxies = [line.strip() for line in f if line.strip()]
            return proxies
        except FileNotFoundError:
            return []
        except Exception as e:
            self.log(f"Failed to read proxy file: {str(e)}", "ERROR")
            return []

    def process_account(self, idx, total, account, proxy, mode):
        token = account.get('token')
        pk = account.get('private_key')
        
        self.log(f"Account #{idx}/{total}", "INFO")
        if proxy:
            self.log(f"Proxy: {proxy[:30]}...", "INFO")
        else:
            self.log(f"Proxy: No Proxy", "INFO")

        self.random_delay(1, 3)
        user = self.get_user_info(token, proxy)
        if not user: 
            self.log("Login Failed / Token Expired", "ERROR")
            return
        
        username = user['user'].get('username', 'N/A')
        points = user['user'].get('points', 0)
        
        time_str = self.get_wib_time()
        print(f"[{time_str}] {Fore.GREEN}[SUCCESS] Login successful! Username: {username} | Points: {points}{Style.RESET_ALL}")
        
        if pk:
            self.random_delay(2, 4)
            wallet_address = self.get_wallet_address(pk)
            if not wallet_address:
                self.log("Invalid private key, skipping", "WARNING")
                return

            self.log(f"Wallet: {wallet_address[:6]}...{wallet_address[-4:]}", "INFO")
            
            current_balance = self.check_balance(pk)
            self.log(f"USDC Balance: {current_balance:.2f}", "INFO")
            
            self.log("Processing Daily GM...", "INFO")
            res = self.claim_daily_gm(token, pk, wallet_address, proxy)
            
            time_str = self.get_wib_time()
            if res.get('success'): 
                print(f"[{time_str}] {Fore.GREEN}[SUCCESS] GM Claimed Successfully!{Style.RESET_ALL}")
            elif res.get('already_claimed'): 
                print(f"[{time_str}] {Fore.GREEN}[SUCCESS] GM Already Claimed Today{Style.RESET_ALL}")
            
            if mode in ['2', '3']:
                self.random_delay(1, 2)
                self.log("Processing Faucet Claim...", "INFO")
                faucet_result = self.claim_faucet(pk)
                
                if faucet_result:
                    time.sleep(3)
                    current_balance = self.check_balance(pk)
                    self.log(f"Updated USDC Balance: {current_balance:.2f}", "INFO")

                self.log(f"Starting Prediction Loop ({self.trade_count_per_account} Trades)...", "INFO")
                
                markets = self.get_prediction_markets(proxy)
                
                if markets and "markets" in markets:
                    active_markets = [m for m in markets['markets'] if m.get('status') == 0]
                    random.shuffle(active_markets)
                    
                    if not active_markets:
                        self.log("No Active/Open Markets found! Skipping trades...", "WARNING")
                        return

                    successful_trades = 0
                    
                    for trade_num in range(1, self.trade_count_per_account + 1):
                        current_balance = self.check_balance(pk)
                        
                        if current_balance < 10:
                            self.log(f"Balance too low ({current_balance:.2f} USDC). Stopping trades.", "WARNING")
                            break
                        
                        if trade_num % 15 == 1 and trade_num > 1:
                            self.log(f"Auto-refresh at trade #{trade_num}. Fetching fresh market data...", "INFO")
                            markets = self.get_prediction_markets(proxy)
                            if markets and "markets" in markets:
                                active_markets = [m for m in markets['markets'] if m.get('status') == 0]
                                random.shuffle(active_markets)
                                self.log(f"Refreshed: {len(active_markets)} active markets available", "SUCCESS")
                                time.sleep(2)
                            else:
                                self.log("Failed to refresh market data", "ERROR")
                        
                        self.random_delay(3, 6)
                        print(f"{Fore.YELLOW}--- Trade #{trade_num}/{self.trade_count_per_account} ---{Style.RESET_ALL}")
                        
                        trade_success = False
                        attempts = 0
                        max_attempts = min(10, len(active_markets))
                        
                        while not trade_success and attempts < max_attempts:
                            if not active_markets or len(active_markets) < 3:
                                self.log("Low market count. Fetching fresh market data...", "INFO")
                                markets = self.get_prediction_markets(proxy)
                                if markets and "markets" in markets:
                                    active_markets = [m for m in markets['markets'] if m.get('status') == 0]
                                    random.shuffle(active_markets)
                                    if not active_markets:
                                        self.log("No active markets available", "ERROR")
                                        break
                                else:
                                    self.log("Failed to fetch market data", "ERROR")
                                    break
                            
                            target = active_markets.pop(0)
                            attempts += 1
                            
                            m_id = target['id']
                            question = target['question']
                            
                            yes_pool = int(target.get('yesPool', 0))
                            no_pool = int(target.get('noPool', 0))
                            
                            if yes_pool > no_pool:
                                outcome = 1 
                                reason = f"Following Majority (Yes Pool > No Pool)"
                            elif no_pool > yes_pool:
                                outcome = 2 
                                reason = f"Following Majority (No Pool > Yes Pool)"
                            else:
                                outcome = random.choice([1, 2])
                                reason = "Pools Equal, Random Pick"

                            bet_amount = random.randint(50, 100)
                            
                            if bet_amount > current_balance:
                                bet_amount = int(current_balance * 0.9)
                                if bet_amount < 10:
                                    self.log("Insufficient balance for minimum bet", "ERROR")
                                    break
                            
                            print(f"{Fore.MAGENTA}[MARKET] {question[:60]}... (ID: {m_id}){Style.RESET_ALL}")
                            print(f"{Fore.CYAN}Strategy: {reason} | Attempt: {attempts}/{max_attempts}{Style.RESET_ALL}")
                            
                            trade_success = self.buy_prediction(pk, m_id, outcome, bet_amount)
                            
                            if not trade_success:
                                if attempts < max_attempts:
                                    self.log(f"Trying next market...", "INFO")
                                time.sleep(2)
                        
                        if trade_success:
                            successful_trades += 1
                            current_balance = self.check_balance(pk)
                            self.log(f"Remaining Balance: {current_balance:.2f} USDC", "INFO")
                        else:
                            self.log(f"Could not place trade #{trade_num}. Refreshing market data...", "WARNING")
                            markets = self.get_prediction_markets(proxy)
                            if markets and "markets" in markets:
                                active_markets = [m for m in markets['markets'] if m.get('status') == 0]
                                random.shuffle(active_markets)
                                self.log(f"Refreshed: {len(active_markets)} active markets found", "INFO")
                            time.sleep(2)
                        
                        if trade_num < self.trade_count_per_account:
                            time.sleep(random.randint(4, 8))
                    
                    final_balance = self.check_balance(pk)
                    self.log(f"Trade Summary: {successful_trades}/{self.trade_count_per_account} successful | Final Balance: {final_balance:.2f} USDC", "INFO")
                else:
                    self.log("Failed to fetch market data, skipping trades...", "WARNING")

        else:
            self.log("No Private Key found for this account", "WARNING")
        
    def run(self):
        self.print_banner()
        
        use_proxy = self.show_proxy_menu()
        mode = self.show_action_menu()
        
        accounts = self.load_accounts()
        if not accounts: 
            self.log("No accounts found in accounts.txt!", "ERROR")
            return
        
        proxies = []
        if use_proxy:
            proxies = self.load_proxies()
            if proxies:
                self.log(f"Loaded {len(proxies)} proxies", "SUCCESS")
            else:
                self.log("No proxies found in proxy.txt, running without proxy", "WARNING")
        
        self.log(f"Loaded {len(accounts)} accounts successfully", "SUCCESS")

        cycle = 1
        while True:
            self.log(f"Cycle #{cycle} Started", "CYCLE")
            print(f"{Fore.CYAN}------------------------------------------------------------{Style.RESET_ALL}")
            
            for i, acc in enumerate(accounts):
                proxy = proxies[i % len(proxies)] if proxies else None
                self.process_account(i+1, len(accounts), acc, proxy, mode)
                print(f"{Fore.WHITE}............................................................{Style.RESET_ALL}")
                time.sleep(3)
            
            print(f"{Fore.CYAN}------------------------------------------------------------{Style.RESET_ALL}")
            self.log(f"Cycle #{cycle} Complete", "CYCLE")
            print(f"{Fore.CYAN}============================================================{Style.RESET_ALL}\n")
            
            cycle += 1
            self.countdown(86400)

if __name__ == "__main__":
    ZetariumBot().run()
