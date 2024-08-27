import requests
from tabulate import tabulate
from colorama import Fore, Style

# Function to read all authorization tokens from query.txt
def get_authorization_tokens():
    with open('query.txt', 'r') as file:
        return [line.strip() for line in file if line.strip()]

# Function to set headers with the provided token
def get_headers(token):
    return {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "authorization": f"tma {token}",
        "content-type": "application/json",
        "priority": "u=1, i",
        "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Microsoft Edge\";v=\"127\", \"Chromium\";v=\"127\", \"Microsoft Edge WebView2\";v=\"127\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "Referer": "https://cats-frontend.tgapps.store/",
        "Referrer-Policy": "strict-origin-when-cross-origin"
    }

def fetch_tasks(headers):
    url = "https://cats-backend-wkejfn-production.up.railway.app/tasks/user?group=cats"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

def clear_task(task_id, headers):
    url = f"https://cats-backend-wkejfn-production.up.railway.app/tasks/{task_id}/complete"
    response = requests.post(url, headers=headers, json={})
    
    if response.status_code == 200:
        print(Fore.GREEN + f"Task {task_id} successfully marked as completed.")
        return response.json()
    else:
        print(Fore.RED + f"Failed to mark task {task_id} as completed.")
        response.raise_for_status()
        
def print_welcome_message():
    print(Fore.WHITE + r"""
          
█▀▀ █░█ ▄▀█ █░░ █ █▄▄ █ █▀▀
█▄█ █▀█ █▀█ █▄▄ █ █▄█ █ ██▄
          """)
    print(Fore.GREEN + Style.BRIGHT + "CATS BOT")
    print(Fore.YELLOW + Style.BRIGHT + "Free Konsultasi Join Telegram Channel: https://t.me/ghalibie")
    print(Fore.BLUE + Style.BRIGHT + "Buy me a coffee :) 0823 2367 3487 GOPAY / DANA")
    print(Fore.RED + Style.BRIGHT + "NOT FOR SALE ! Ngotak dikit bang. Ngoding susah2 kau tinggal rename :)\n\n")        

def complete_all_tasks():
    tokens = get_authorization_tokens()
    
    confirmation = input(Fore.WHITE + f"Apakah Anda ingin menyelesaikan semua task? (y/n): ").strip().lower()
    if confirmation != 'y':
        return
    
    for token in tokens:
        headers = get_headers(token)
        tasks = fetch_tasks(headers).get('tasks', [])
        
        for task in tasks:
            if not task['completed']:
                try:
                    clear_task(task['id'], headers)
                except requests.RequestException:
                    # Handle any request exception and move on to the next task
                    print(Fore.WHITE + f"Skipping task {task['id']} due to an error.")

def user():
    tokens = get_authorization_tokens()
    all_user_data = []
    total_rewards_sum = 0
    
    for token in tokens:
        headers = get_headers(token)
        url = "https://cats-backend-wkejfn-production.up.railway.app/user"
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            # Extract required fields
            first_name = data.get('firstName')
            last_name = data.get('lastName')
            telegram_age = data.get('telegramAge')
            total_rewards = data.get('totalRewards')
            
            # Collect user data
            all_user_data.append([first_name, last_name, telegram_age, total_rewards])
            total_rewards_sum += total_rewards  # Accumulate total rewards
        else:
            print(Fore.RED + f"Failed to fetch user data for token {token}.")
            response.raise_for_status()
    
    # Prepare data for tabulate
    table_data = [
        ["First Name", "Last Name", "Telegram Age", "Total Rewards"]
    ]
    table_data.extend(all_user_data)
    
    # Print table
    print(tabulate(table_data, headers='firstrow', tablefmt='grid'))
    
    # Print total rewards sum with color
    print(Fore.GREEN + f"\nTotal Rewards: " + Fore.WHITE + f"{total_rewards_sum}" + Style.RESET_ALL)

def main():
    print_welcome_message()
    complete_all_tasks()
    print(Fore.WHITE + f"\nDisplaying user information...")
    user()

# Example usage
if __name__ == "__main__":
    main()
