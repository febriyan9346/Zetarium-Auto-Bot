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

os.system('clear' if os.name == 'posix' else 'cls')

import warnings
warnings.filterwarnings('ignore')

import sys
if not sys.warnoptions:
    os.environ["PYTHONWARNINGS"] = "ignore"

init(autoreset=True)

class ZetariumBot:
    def __init__(self):
        self.base_url = "https://airdrop-data.zetarium.world"
        self.api_url = "https://api.zetarium.world"
        
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
        else:
            color = Fore.WHITE
            symbol = "[LOG]"
        
        print(f"[{time_str}] {color}{symbol} {message}{Style.RESET_ALL}")
    
    def random_delay(self, min_sec=1, max_sec=3):
        delay = random.randint(min_sec, max_sec)
        time.sleep(delay)
    
    def show_menu(self):
        print(f"{Fore.CYAN}============================================================{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Select Mode:{Style.RESET_ALL}")
        print(f"{Fore.GREEN}1. Run with proxy")
        print(f"2. Run without proxy{Style.RESET_ALL}")
        print(f"{Fore.CYAN}============================================================{Style.RESET_ALL}")
        
        while True:
            try:
                choice = input(f"{Fore.GREEN}Enter your choice (1/2): {Style.RESET_ALL}").strip()
                if choice in ['1', '2']:
                    return choice
                else:
                    print(f"{Fore.RED}Invalid choice! Please enter 1 or 2.{Style.RESET_ALL}")
            except KeyboardInterrupt:
                print(f"\n{Fore.RED}Program terminated by user.{Style.RESET_ALL}")
                exit(0)
    
    def countdown(self, seconds):
        for i in range(seconds, 0, -1):
            hours = i // 3600
            minutes = (i % 3600) // 60
            secs = i % 60
            print(f"\r{Fore.CYAN}[COUNTDOWN]{Style.RESET_ALL} Next cycle in: {hours:02d}:{minutes:02d}:{secs:02d} ", end="", flush=True)
            time.sleep(1)
        print("\r" + " " * 60 + "\r", end="", flush=True)
    
    def sign_message(self, private_key: str, message: str) -> Optional[str]:
        try:
            account = Account.from_key(private_key)
            message_hash = encode_defunct(text=message)
            signed = account.sign_message(message_hash)
            return signed.signature.hex()
        except Exception as e:
            self.log(f"Failed to sign message: {str(e)}", "ERROR")
            return None
    
    def get_wallet_address(self, private_key: str) -> Optional[str]:
        try:
            account = Account.from_key(private_key)
            return account.address
        except Exception as e:
            self.log(f"Invalid private key: {str(e)}", "ERROR")
            return None
    
    def get_user_info(self, token: str, proxy: Optional[str] = None) -> Optional[Dict]:
        headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-US,en;q=0.9",
            "authorization": f"Bearer {token}",
            "content-type": "application/json",
            "origin": "https://airdrop.zetarium.world",
            "referer": "https://airdrop.zetarium.world/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
        }
        
        proxies = None
        if proxy:
            proxies = {"http": proxy, "https": proxy}
        
        try:
            response = requests.get(
                f"{self.base_url}/auth/me",
                headers=headers,
                proxies=proxies,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                self.log(f"Status code: {response.status_code}", "ERROR")
                return None
                
        except Exception as e:
            self.log(f"Request failed: {str(e)}", "ERROR")
            return None
    
    def get_gm_info(self, wallet_address: str, proxy: Optional[str] = None) -> Optional[Dict]:
        headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-US,en;q=0.9",
            "origin": "https://airdrop.zetarium.world",
            "referer": "https://airdrop.zetarium.world/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
        }
        
        proxies = None
        if proxy:
            proxies = {"http": proxy, "https": proxy}
        
        try:
            url = f"{self.api_url}/api/profile/{wallet_address}"
            response = requests.get(
                url,
                headers=headers,
                proxies=proxies,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return None
                
        except Exception as e:
            return None
    
    def claim_daily_gm(self, token: str, private_key: str, wallet_address: str, proxy: Optional[str] = None) -> Dict:
        headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/json",
            "origin": "https://airdrop.zetarium.world",
            "priority": "u=1, i",
            "referer": "https://airdrop.zetarium.world/",
            "sec-ch-ua": '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
        }
        
        proxies = None
        if proxy:
            proxies = {"http": proxy, "https": proxy}
        
        try:
            account = Account.from_key(private_key)
            checksum_address = account.address
            
            message = f"GM! Claim daily points - {checksum_address.lower()}"
            
            signature = self.sign_message(private_key, message)
            if not signature:
                return {"success": False, "error": "Failed to sign message"}
            
            payload = {
                "message": message,
                "signature": signature
            }
            
            url = f"{self.api_url}/api/profile/{checksum_address}/gm"
            
            response = requests.post(
                url,
                headers=headers,
                json=payload,
                proxies=proxies,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 400:
                try:
                    error_data = response.json()
                    return {"success": False, "already_claimed": True, "error": error_data}
                except:
                    return {"success": False, "already_claimed": True, "error": "Already claimed today"}
            else:
                return {"success": False, "error": f"Status code: {response.status_code}"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def load_accounts(self, filename: str = "accounts.txt") -> List[Dict[str, str]]:
        try:
            accounts = []
            with open(filename, 'r') as f:
                current_account = {}
                
                for line in f:
                    line = line.strip()
                    
                    if not line:
                        if 'token' in current_account:
                            accounts.append(current_account)
                            current_account = {}
                        continue
                    
                    if '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip().lower()
                        value = value.strip()
                        
                        if key == 'token':
                            current_account['token'] = value
                        elif key == 'private_key':
                            current_account['private_key'] = value if value else None
                
                if 'token' in current_account:
                    accounts.append(current_account)
            
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
    
    def process_account(self, account_num: int, total_accounts: int, token: str, private_key: Optional[str], proxy: Optional[str]):
        self.log(f"Account #{account_num}/{total_accounts}", "INFO")
        
        if proxy:
            self.log(f"Proxy: {proxy[:30]}...", "INFO")
        else:
            self.log(f"Proxy: No Proxy", "INFO")
        
        self.random_delay(1, 3)
        
        user_data = self.get_user_info(token, proxy)
        
        if not user_data or "user" not in user_data:
            self.log("Failed to get user info", "ERROR")
            return False
        
        user = user_data["user"]
        username = user.get('username', 'N/A')
        points = user.get('points', 0)
        
        self.log(f"Login successful! Username: {username}", "SUCCESS")
        
        if private_key:
            self.random_delay(2, 4)
            
            wallet_address = self.get_wallet_address(private_key)
            if not wallet_address:
                self.log("Invalid private key, skipping claim", "WARNING")
                return True
            
            self.log(f"Wallet: {wallet_address[:6]}...{wallet_address[-4:]}", "INFO")
            self.log("Checking Daily GM Status...", "INFO")
            
            self.random_delay(2, 3)
            
            gm_result = self.claim_daily_gm(token, private_key, wallet_address, proxy)
            
            if gm_result.get('success'):
                points_earned = gm_result.get('pointsEarned', 0)
                total_points = gm_result.get('points', 0)
                streak = gm_result.get('streakDays', 0)
                multiplier = gm_result.get('multiplier', 1)
                gm_count = gm_result.get('gmCount', 0)
                last_gm = gm_result.get('lastGmTime', 'N/A')
                
                self.log(f"Daily GM Claimed Successfully! ✓", "SUCCESS")
                print(f"{Fore.CYAN}------------------------------------------------------------{Style.RESET_ALL}")
                print(f"Status           : Claim Success")
                print(f"Points Earned    : +{points_earned} Points (Multiplier: x{multiplier})")
                print(f"Total Points     : {total_points:,} Points")
                print(f"Streak Days      : {streak} days")
                print(f"GM Count         : {gm_count} times")
                print(f"Last GM Time     : {last_gm}")
            elif gm_result.get('already_claimed'):
                self.log("Daily GM: Already claimed today ✓", "WARNING")
                
                self.random_delay(1, 2)
                gm_info = self.get_gm_info(wallet_address, proxy)
                
                if gm_info:
                    total_points = gm_info.get('points', points)
                    streak = gm_info.get('streakDays', 0)
                    gm_count = gm_info.get('gmCount', 0)
                    last_gm = gm_info.get('lastGmTime', 'N/A')
                    
                    print(f"{Fore.CYAN}------------------------------------------------------------{Style.RESET_ALL}")
                    print(f"Status           : Already Claimed Today")
                    print(f"Total Points     : {total_points:,} Points")
                    print(f"Streak Days      : {streak} days")
                    print(f"GM Count         : {gm_count} times")
                    print(f"Last GM Time     : {last_gm}")
                else:
                    print(f"{Fore.CYAN}------------------------------------------------------------{Style.RESET_ALL}")
                    print(f"Status           : Already Claimed Today")
                    print(f"Total Points     : {points:,} Points")
            else:
                error_msg = gm_result.get('error', 'Unknown error')
                self.log(f"Daily GM: Failed to claim - {error_msg}", "ERROR")
        else:
            self.log("No private key, skipping claim", "WARNING")
        
        return True
    
    def run(self):
        self.print_banner()
        
        choice = self.show_menu()
        use_proxy = (choice == '1')
        
        if use_proxy:
            self.log("Running with proxy", "INFO")
        else:
            self.log("Running without proxy", "INFO")
        
        accounts = self.load_accounts()
        if not accounts:
            self.log("No accounts found in accounts.txt!", "ERROR")
            self.log("Format:", "INFO")
            print(f"{Fore.YELLOW}token=your_bearer_token_here")
            print(f"private_key=your_private_key_here")
            print(f"")
            print(f"token=another_token")
            print(f"private_key=another_private_key{Style.RESET_ALL}")
            return
        
        self.log(f"Loaded {len(accounts)} accounts successfully", "SUCCESS")
        
        proxies = []
        if use_proxy:
            proxies = self.load_proxies()
            if proxies:
                self.log(f"Loaded {len(proxies)} proxies", "SUCCESS")
            else:
                self.log("No proxies found, running without proxy", "WARNING")
        
        print(f"\n{Fore.CYAN}============================================================{Style.RESET_ALL}\n")
        
        cycle = 1
        while True:
            self.log(f"Cycle #{cycle} Started", "CYCLE")
            print(f"{Fore.CYAN}------------------------------------------------------------{Style.RESET_ALL}")
            
            success_count = 0
            total_accounts = len(accounts)
            
            for idx, account in enumerate(accounts, 1):
                proxy = None
                if use_proxy and proxies:
                    proxy = proxies[(idx - 1) % len(proxies)]
                
                success = self.process_account(
                    idx,
                    total_accounts,
                    account['token'],
                    account.get('private_key'),
                    proxy
                )
                
                if success:
                    success_count += 1
                
                if idx < total_accounts:
                    print(f"{Fore.WHITE}............................................................{Style.RESET_ALL}")
                    time.sleep(2)
            
            print(f"{Fore.CYAN}------------------------------------------------------------{Style.RESET_ALL}")
            self.log(f"Cycle #{cycle} Complete | Success: {success_count}/{total_accounts}", "CYCLE")
            print(f"{Fore.CYAN}============================================================{Style.RESET_ALL}\n")
            
            cycle += 1
            
            wait_time = 86400
            self.countdown(wait_time)

if __name__ == "__main__":
    bot = ZetariumBot()
    bot.run()
