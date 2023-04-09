from tkinter import Tk, Canvas, Entry, LabelFrame, Label, \
    Button, END, DISABLED, NORMAL, LEFT, X, Toplevel
import tkinter.scrolledtext as scroll
import os
import requests
import json
import webbrowser


if os.name == 'nt':
    download_folder = 'PythonProjects'
else:
    download_folder = 'Документы'
# path = os.path.dirname(os.path.abspath(__file__))
path = os.path.join('E:/', download_folder)
VSC = "AppData/Local/Programs/Microsoft VS Code/Code.exe"
path_vsc = os.path.join(os.path.expanduser("~"), VSC)


def out():
    top = Toplevel()
    top.overrideredirect(True)
    Label(
        top, fg='green', font='Arial 12',
        text='Вы действительно хотите выйти?').pack(padx=5, pady=5)
    Button(top, text='ВЫХОД', fg='red', command=root.destroy).pack(
        expand=1, fill=X)
    Button(top, text='ОТМЕНА', fg='red', command=top.destroy).pack(
        expand=1, fill=X)
    root.update()
    x = (root.winfo_width() - top.winfo_width()) // 2
    y = root.winfo_height() // 2
    top.geometry(f'+{x}+{y}')


def push_repository():
    os.chdir(path)
    rep_folder = rep.get()
    if os.path.isdir(rep_folder):
        os.chdir(os.path.join(path, rep_folder))
    else:
        text_output('[ERROR] На компьютере нет такого репозитория')
        return
    os.system('git add .')
    os.system('git commit -m "-"')
    # os.system(f"git remote add origin https://github.com/{log.get()}/{rep.get()}.git")
    # print(os.system('git status'))
    # os.system('git push -u origin master')
    os.system('git push')
    text_output('[INFO] Изменения внесены, проверьте в браузере')
    text_output('[INFO] Для выхода нажмите кнопку "Выход"')
    webbrowser.open(f'https://github.com/{log.get()}')


def disabled():
    # pas.configure(show='*')
    log.configure(state=DISABLED)
    pas.configure(state=DISABLED)
    rep.configure(state=DISABLED)
    btn.configure(state=DISABLED)
    root.update()


def text_output(text_data):
    text.insert(END, f'{text_data}\n')
    root.update()


def enter(event):
    if root.focus_get() == log and block_dict['log_block'] == 0:
        log.delete(0, END)
        log.configure(fg='black')
        block_dict['log_block'] = 1
    elif root.focus_get() == pas and block_dict['pas_block'] == 0:
        pas.delete(0, END)
        pas.configure(fg='black', show='*')
        block_dict['pas_block'] = 1
    elif root.focus_get() == rep and block_dict['rep_block'] == 0:
        rep.delete(0, END)
        rep.configure(fg='black')
        block_dict['rep_block'] = 1


def authorization():
    # Проверка заполнения полей при авторизации
    login, password, repository = log.get(), pas.get(), rep.get()
    if login == '' or password == '' or repository == '':
        text_output('[ERROR] Внимательно заполните все поля')
        return

    if password == '1':
        password = token
    else:
        text_output('[ERROR] Пароль неверный')
        return

    # Авторизация на Github
    url = 'https://api.github.com/user'
    headers = {
        "Authorization": f"token {password}",
        "Accept": "application/vnd.github.v3+json"
    }
    repos = requests.get(url, headers=headers)
    if repos.status_code == 200 and repos.json()['login'] == login:
        text_output(f'[INFO] Вход на Github успешный. Код: {repos.status_code}')
        email = repos.json()['email']
        clone_repository(login, email, password, repository, headers)
    else:
        text_output(f'[ERROR] Ошибка входа на Github {repos.status_code}')
        return


def clone_repository(login, email, password, repository, headers):

    disabled()

    # Компьютер
    os.chdir(path)
    _, folder = os.path.split(os.getcwd())
    if folder != os.path.split(path)[1]:
        text_output('[ERROR] Вы не в папке "Downloads"')
        return
    elif os.path.isdir(repository):
        os.system(f'rmdir /s /q {repository}')
        text_output('[INFO] Одноименная папка удалена')

    # Github
    r = requests.get('https://api.github.com/user/repos', headers=headers)
    text_output('[INFO] Список репозиториев:')
    for repo in r.json():
        repos_list.append(repo['name'])
        text_output(repo['html_url'])
    if repository in repos_list:
        os.system(f'git clone -q https://github.com/{login}/{repository}.git')
        os.chdir(os.path.join(path, repository))
    else:
        text_output('[INFO] На Github нет такого репозитория. Создаем!')
        url = 'https://api.github.com/user/repos'
        data = {
            "name": f"{repository}",
            "description": "Python"
        }
        r = requests.post(url, headers=headers, data=json.dumps(data))  # new repository
        text_output(f'[INFO] Репозиторий добавлен на GitHub. Код: {r.status_code}')
        os.system(f'git clone -q https://github.com/{login}/{repository}.git')
        os.chdir(os.path.join(path, repository))
        f = open('main.py', 'a')
        f.close()
        os.system('touch .gitignore')

    text_output(f'[INFO] Скачивается {repository}')
    os.system(
        f'git config user.email "{email}" && git config user.name "{login}" && '
        f'git remote set-url origin https://{login}:{password}@github.com'
        f'/{login}/{repository}.git')

    text_output('[INFO] Выполнено')
    text_output('[INFO] Не закрывайте программу')
    btn2.configure(state=NORMAL)
    os.system(f'start "Code" "{path_vsc}"')


repos_list = []
block_dict = {'log_block': 0, 'pas_block': 0, 'rep_block': 0}

root = Tk()
root.protocol('WM_DELETE_WINDOW', out)
root.geometry('+10+10')
root.title('Работа с GitHub')
# root.attributes('-topmost', True)

canvas = Canvas(root, bg='white')
canvas.pack()

lf = LabelFrame(canvas, text=' Авторизация ', bd=4, fg='red')
lf.pack()
log = Entry(lf, width=38, font='Arial 14', fg='light gray')
pas = Entry(lf, width=38, font='Arial 14', fg='light gray')
rep = Entry(lf, width=38, font='Arial 14', fg='light gray')
token = ''
log.insert(0, 'ovvladimir')
pas.insert(0, 'password')
rep.insert(0, 'repository')
log.pack()
pas.pack()
rep.pack()

btn = Button(lf, text='c GitHub', fg='green', command=authorization)
btn.pack(side=LEFT, expand=1, fill=X)
btn2 = Button(lf, text='на GitHub', fg='green', command=push_repository)
btn2.configure(state=DISABLED)
btn2.pack(side=LEFT, expand=1, fill=X)

lf1 = LabelFrame(canvas, text=' Терминал ', height=250, bd=4, fg='blue')
lf1.pack_propagate(False)
lf1.pack(fill='both')
text = scroll.ScrolledText(lf1, font='Arial 12')
text.pack()
Button(canvas, text='ВЫХОД', fg='red', command=out).pack()

root.bind('<1>', enter)
root.mainloop()
