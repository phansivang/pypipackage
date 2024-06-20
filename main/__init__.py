from tkinter import *
from tkinter import messagebox
from forex_python.converter import CurrencyRates
import threading
import requests
from bs4 import BeautifulSoup
import subprocess

# Load API key from file
def load_api_key(filename='API_Key.txt'):
    with open(filename, 'r') as file:
        return file.readline().strip()

API_KEY = load_api_key()

# Get balance and convert to USD
def get_balance():
    c = CurrencyRates()
    response = requests.get(f'http://api.sms-man.com/stubs/handler_api.php?action=getBalance&api_key={API_KEY}')
    rub_balance = float(response.text.split(':')[1])
    usd_balance = c.convert('RUB', 'USD', rub_balance)
    result.insert(1.0, f"$ {usd_balance}\n")

# Get a new number
def get_number():
    try:
        with open('Numbers.txt', 'r') as file:
            existing_numbers = file.readlines()

        if existing_numbers and messagebox.askokcancel('WARNING', 'You will lose the previous number if you buy a new one!'):
            save_new_number()
        elif not existing_numbers:
            save_new_number()
    except IndexError:
        pass

# Save a new number to file
def save_new_number():
    response = requests.get(
        f'http://api.sms-man.com/stubs/handler_api.php?action=getNumber&api_key={API_KEY}&service={clicked.get()}&country=0&ref=$ref')
    parts = response.text.split(':')
    number_id, number = parts[1], parts[2]
    result.insert(1.0, f'+{number}\n')
    with open('Numbers.txt', 'w') as file:
        file.write(f'{number_id}\n{number}')
    with open('LOGS.txt', 'a') as log_file:
        log_file.write(response.text + '\n')

# Get SMS code for the current number
def get_sms():
    try:
        with open('Numbers.txt', 'r') as file:
            number_id = file.readline().strip()

        response = requests.get(
            f'http://api.sms-man.com/stubs/handler_api.php?action=getStatus&api_key={API_KEY}&id={number_id}')
        status = response.text

        if status == 'STATUS_WAIT_CODE':
            result.insert(1.0, "WAIT FOR CODE\n")
        elif status in ['NO_ACTIVATION', 'ACCESS_CANCEL']:
            result.insert(1.0, f"{status}\n")
            clear_numbers_file()
        else:
            code = status.split(':')[1]
            result.insert(1.0, f"CODE: {code}\n")
            update_logs(response.text)
            clear_numbers_file()
    except IndexError:
        result.insert(1.0, 'NO NUMBER IN LIST\n')
        clear_numbers_file()

# Clear the numbers file
def clear_numbers_file():
    with open('Numbers.txt', 'w') as file:
        file.write('')

# Update logs with status
def update_logs(status):
    with open('LOGS.txt', 'r') as log_file:
        if status in log_file.readlines():
            with open('LOGS.txt', 'a') as log_file_append:
                log_file_append.write(":OK\n")

# Delete the current number
def delete_number():
    try:
        with open('Numbers.txt', 'r') as file:
            number_id = file.readline().strip()

        requests.get(
            f'http://api.sms-man.com/stubs/handler_api.php?action=setStatus&api_key={API_KEY}&id={number_id}&status=-1')
        result.insert(1.0, 'NUMBER DELETED\n')
        clear_numbers_file()
    except IndexError:
        result.insert(1.0, 'NO NUMBER IN LIST\n')

# Run get_sms in a separate thread
def thread_for_code():
    threading.Thread(target=get_sms).start()

# Clear the result text box
def clear_result():
    result.delete(1.0, END)

# Initialize and run the Tkinter application
def start_tk_app():
    global result, clicked
    root = Tk()
    root.title('ICODE')
    root.resizable(False, False)
    root.config(bg='black')
    root.geometry('300x600')

    Label(root, text='ICODE', font=('', '50'), fg='white', bg='black').pack(pady=20)
    Button(root, text='BUY NUMBER', width=20, fg='white', bg='black', command=get_number).pack(pady=5)
    Button(root, text='DELETE NUMBER', width=20, fg='white', bg='black', command=delete_number).pack(pady=5)
    Button(root, text='GET CODE', width=20, fg='white', bg='black', command=thread_for_code).pack(pady=5)
    Button(root, text='CHECK BALANCE', width=20, fg='white', bg='black', command=get_balance).pack(pady=5)
    
    result = Text(root, width=35, height=10, font=('', '10'), fg='white', bg='black')
    result.pack(pady=10)
    Button(root, text='CLEAR', fg='white', bg='black', command=clear_result).pack()
    
    clicked = StringVar()
    service_options = {"TELEGRAM": 'tg', "FACEBOOK": "fb", "YOUTUBE": "go", "MICROSOFT": "mm"}
    OptionMenu(root, clicked, *service_options.values()).pack(pady=10).config(bg="black", fg="WHITE")

    root.mainloop()

# Authenticate user and start the Tkinter app
def login():
    response = requests.get('https://anotepad.com/note/read/3shqntdy').text
    soup = BeautifulSoup(response, 'lxml')
    plaintext = soup.find('div', class_='plaintext').text

    uuid = subprocess.check_output('wmic csproduct get uuid').decode().split('\n')[1].strip()
    if uuid in plaintext.split('\n'):
        start_tk_app()
    else:
        with open('Key_Activation.txt', 'w') as file:
            file.write(uuid)

# Start the application
def main():
    login()

if __name__ == "__main__":
    main()
