from tkinter import *
from tkinter import messagebox
from forex_python.converter import CurrencyRates
import threading
import requests
from bs4 import BeautifulSoup
import subprocess

with open('API_Key.txt', 'r') as API_key:
    get_api = API_key.readline()


def get_balance():
    c = CurrencyRates()
    request_balance = requests.get(
        f'http://api.sms-man.com/stubs/handler_api.php?action=getBalance&api_key={get_api}')
    x = request_balance.text.split(':')[1]
    Currency = c.convert('RUB', 'USD', float(x))
    mybalance = {request_balance.text: Currency}
    result.insert(1.0, "$ " + str(mybalance.get(request_balance.text)) + '\n')


# noinspection PyGlobalUndefined
def get_number():
    global request_number
    try:
        with open('Numbers.txt', 'r') as warning:
            x = warning.readlines()
        if len(x) > 0:
            msbox = messagebox.askokcancel('WARNING', 'You will lose the previous number if you buy the new one !', )
            if msbox == 1:
                request_number = requests.get(
                    f'http://api.sms-man.com/stubs/handler_api.php?action=getNumber&api_key={get_api}&service={clicked.get()}&country=0&ref=$ref')
                get_id = request_number.text.split(':')
                result.insert(1.0, '+' + get_id[2] + '\n')
                with open('Numbers.txt', 'w') as save_id:
                    save_id.write(get_id[1] + '\n')
                    save_id.write(get_id[2])
                    save_id.close()
                with open('LOGS.txt', 'a') as LOG:
                    LOG.write(request_number.text + '\n')
                    LOG.close()
            else:
                pass
        else:
            request_number = requests.get(
                f'http://api.sms-man.com/stubs/handler_api.php?action=getNumber&api_key={get_api}&service={clicked.get()}&country=0&ref=$ref')
            get_id = request_number.text.split(':')
            result.insert(1.0, '+' + get_id[2] + '\n')
            with open('Numbers.txt', 'w') as save_id:
                save_id.write(get_id[1] + '\n')
                save_id.write(get_id[2])
                save_id.close()
            with open('LOGS.txt', 'a') as LOG:
                LOG.write(request_number.text + '\n')
                LOG.close()
    except IndexError:
        pass


def get_sms():
    try:
        with open('Numbers.txt', 'r') as get_code:
            x = get_code.readlines()
        request_sms = requests.get(
            f'http://api.sms-man.com/stubs/handler_api.php?action=getStatus&api_key={get_api}&id={x[0]}')
        if request_sms.text == 'STATUS_WAIT_CODE':
            result.insert(1.0, "WAIT FOR CODE " + '\n')

        elif request_sms.text == 'NO_ACTIVATION':
            result.insert(1.0, request_sms.text + '\n')

        elif request_sms.text == 'ACCESS_CANCEL':
            with open('Numbers.txt', 'w') as clear:
                result.insert(1.0, 'CODE SENT' + '\n')
                return clear.write('')
        else:
            x_code = request_sms.text.split(':')
            code = {request_sms.text: f'CODE:{x_code[1]}'}
            result.insert(1.0, code.get(request_sms.text) + '\n')
            with open('LOGS.txt', 'r') as read:
                if request_number.text in read.readlines():
                    with open('LOGS.txt', 'a') as write:
                        write.write(":"'OK' + '\n')
                        write.close()
            with open('Numbers.txt', 'w') as clear:
                return clear.write('')



    except IndexError:
        result.insert(1.0, 'NO NUMBER IN  LISTS' + '\n')
        with open('Numbers.txt', 'w') as clear:
            return clear.write('')


def delete_number():
    try:
        with open('Numbers.txt', 'r') as delete_number:
            x = delete_number.readlines()
        deleted_number = requests.get(
            f'http://api.sms-man.com/stubs/handler_api.php?action=setStatus&api_key={get_api}&id={x[0]}&status=-1')
        result.insert(1.0, 'NUMBER DELETED' + '\n')
        with open('Numbers.txt', 'w') as clear:
            return clear.write('')
    except IndexError:
        result.insert(1.0, 'NO NUMBER IN LISTS' + '\n')


def thread_for_code():
    thread = threading.Thread(target=get_sms)
    thread.start()


def clear():
    result.delete(1.0, END)


def tk():
    global result
    global Balane_result
    global clicked
    root = Tk()
    # root.iconbitmap('sms.ico')
    root.title('ICODE')
    root.resizable(False, False)
    root.config(bg='black')
    root.geometry('300x600')
    text = Label(root, text='ICODE', font=('', '50'), fg='white', bg='black')
    text.pack(pady=20)
    b_buy = Button(root, text='BUY NUMBER', width=20, fg='white', bg='black', command=get_number)
    b_buy.pack(pady=5)
    b_delete = Button(root, text='DELETE NUMBER', fg='white', bg='black', width=20, command=delete_number)
    b_delete.pack(pady=5)
    b_get_code = Button(root, text='GET CODE', fg='white', bg='black', width=20, command=thread_for_code)
    b_get_code.pack(pady=5)
    b_check_balance = Button(root, text='CHECK BALANCE', fg='white', bg='black', width=20, command=get_balance)
    b_check_balance.pack(pady=5)
    result = Text(root, width=35, height=10, font=('', '10'), fg='white', bg='black')
    result.pack(pady=10)
    Balane_result = Label(root, fg='white', bg='black')
    Balane_result.pack()
    clear_sc = Button(root, text='CLEAR', fg='white', bg='black', command=clear)
    clear_sc.pack()
    clicked = StringVar()
    service = {
        "TELEGRAM": 'tg',
        "FACEBOOK": "fb",
        "YOUTUBE": "go",
        "MICROSOFT": "mm",
    }
    dropmenu = OptionMenu(root, clicked, service.get('TELEGRAM'), service.get('FACEBOOK'), service.get('MICROSOFT'),
                          service.get('YOUTUBE'))
    dropmenu.pack(pady=10)
    dropmenu.config(bg="black", fg="WHITE")

    root.mainloop()


def login():
    get = requests.get('https://anotepad.com/note/read/3shqntdy').text
    soup = BeautifulSoup(get, 'lxml')
    x = soup.find('div', class_='plaintext').text
    user = []
    user.append(x)
    for i in user:
        try:
            ii = i.split('\n')
            xx = ii.index(subprocess.check_output('wmic csproduct get uuid').decode().split('\n')[1].strip())
            if xx >= 0:
                tk()

        except:
            with open('Key_Activation.txt', 'w') as key_activation:
                key_activation.write(subprocess.check_output('wmic csproduct get uuid').decode().split('\n')[1].strip())
                key_activation.close()


def myapp():
    login()
    
