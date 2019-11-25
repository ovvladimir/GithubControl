import os
import shutil
import requests
import json
import webbrowser
import time
from tkinter import Tk, Canvas, Entry, LabelFrame, CENTER, Button, END, Text, DISABLED
import tkinter.scrolledtext as scroll


def clean():
    btn.configure(state=DISABLED)
    pas.delete(0, END)
    pas.insert(0, '************')
    root.update()


def text_output(text_data):
    text.insert(END, f'{text_data}\n')
    root.update()


def authorization():
    api(log.get(), dom.get(), pas.get(), rep.get())
    root.attributes('-topmost', True)


def enter(event):
    if root.focus_get() == log and block_dict['log_block'] == 0:
        log.delete(0, END)
        log.configure(fg='black')
        block_dict['log_block'] = 1
    elif root.focus_get() == dom and block_dict['dom_block'] == 0:
        dom.delete(0, END)
        dom.configure(fg='black')
        block_dict['dom_block'] = 1
    elif root.focus_get() == pas and block_dict['pas_block'] == 0:
        pas.delete(0, END)
        pas.configure(fg='black')  # , show='*')
        block_dict['pas_block'] = 1
    elif root.focus_get() == rep and block_dict['rep_block'] == 0:
        rep.delete(0, END)
        rep.configure(fg='black')
        block_dict['rep_block'] = 1


def api(login, email, password, repository):
    print('-'*70)
    clean()
    repos_list = []
    # Путь к папке, в которую клонируется репозиторий
    if os.name == 'nt':
        path = f'{os.getenv("USERPROFILE")}/Документы_'
    else:
        path = '/home/algoritmika/Документы'
    # api
    url = 'https://api.github.com/user/repos'
    auth = (login, password)
    repos = requests.get(url, auth=auth)
    if repos.status_code == 200:
        for repo in repos.json():
            repos_list.append(repo['name'])
        if repository not in repos_list:
            data = {
                "name": f"{repository}",
                "description": "Python"}
            new_repository = requests.post(url, auth=auth, data=json.dumps(data))
            repos = requests.get(url, auth=auth)
        else:
            text_output('[INFO] Такой репозиторий уже есть на github')
            print('[INFO] Такой репозиторий уже есть на github')
        text_output('[INFO] Список репозиториев на github:')
        print('[INFO] Список репозиториев на github:')
        for repo in repos.json():
            text_output(repo['html_url'])
            print(repo['html_url'])

        # Компьютер
        os.chdir(path)
        _, folder = os.path.split(os.getcwd())
        if folder != os.path.split(path)[1]:
            text_output('[ERROR] Вы не в папке "Документы"')
            print('[ERROR] Вы не в папке "Документы"')
        else:
            if os.path.isdir(repository):
                shutil.rmtree(repository)
                text_output(
                    '[INFO] Указанный Вами репозиторий '
                    'будет перезаписан в папке "Документы"')
                print(
                    '[INFO] Указанный Вами репозиторий '
                    'будет перезаписан в папке "Документы"')

            text_output(f'[INFO] Скачивается {repository}')
            print(f'[INFO] Скачивается {repository}')
            os.system(f'git clone https://github.com/{login}/{repository}.git')
            os.chdir(f'{path}/{repository}')
            os.system(
                f'git config user.email "{email}" && git config user.name "{login}" && '
                f'git remote set-url origin https://{login}:{password}@github.com'
                f'/{login}/{repository}.git')
            if repository not in repos_list:
                f = open('main.py', 'a')
                f.close()
            # Linux - в Chrome отключить аппаратное ускорение gpu
            webbrowser.open(f'https://github.com/{login}')
    else:
        text_output('[ERROR] Ошибка входа на github')
        print('[ERROR] Ошибка входа на github')

    text_output('[INFO] Выход')
    print(f'[INFO] Выход\n{"-"*70}')


block_dict = {'log_block': 0, 'dom_block': 0, 'pas_block': 0, 'rep_block': 0}

root = Tk()
root.geometry('+10+10')
root.title('Ввод параметров для входа на github')

canvas = Canvas(root, bg='white')
canvas.pack()

lf = LabelFrame(canvas, text=' Авторизация ', bd=4, fg='red')
lf.pack()
log = Entry(lf, width=38, font='Arial 14', fg='light gray')
dom = Entry(lf, width=38, font='Arial 14', fg='light gray')
pas = Entry(lf, width=38, font='Arial 14', fg='light gray')
rep = Entry(lf, width=38, font='Arial 14', fg='light gray')
log.insert(0, 'login, например ProV2019')
dom.insert(0, 'email, например ProV2019@yandex.ru')
pas.insert(0, 'password')
rep.insert(0, 'repository, например GitControl')
log.pack()
dom.pack()
pas.pack()
rep.pack()
btn = Button(lf, text='ВХОД', fg='green', command=authorization)
btn.pack()

lf1 = LabelFrame(canvas, text=' Терминал ', height=250, bd=4, fg='blue')
lf1.pack_propagate(False)
lf1.pack(fill='both')
text = scroll.ScrolledText(lf1, font='Arial 12')
text.pack()
Button(canvas, text=' QUIT ', fg='red', command=root.destroy).pack()

root.bind('<1>', enter)
root.mainloop()
