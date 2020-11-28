import os
import webbrowser
from tkinter import Tk, Canvas, Entry, LabelFrame, Label, \
    Button, END, DISABLED, NORMAL, PhotoImage, LEFT, X, Toplevel
import tkinter.scrolledtext as scroll

if os.name == 'nt':
    download_folder = 'GitPath'
else:
    download_folder = 'Документы'
path = os.path.join(os.path.expanduser('~'), download_folder)
VSC = "AppData/Local/Programs/Microsoft VS Code/Code.exe"
path_vsc = os.path.join(os.path.expanduser("~"), VSC)
# token = ''


def out():
    top = Toplevel()
    top.overrideredirect(True)
    label_about = Label(
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
    repos = rep.get()
    if os.path.isdir(repos):
        os.chdir(os.path.join(path, repos))
    else:
        text_output('[ERROR] На компьютере нет такого репозитория')
        return
    os.system('git add .')
    os.system('git commit -m "changed"')
    # os.system(f'git remote add origin https://github.com/{log.get()}/{rep.get()}.git')
    # print(os.system('git status'))
    # os.system('git push -u origin master')
    os.system('git push')
    text_output('[INFO] Изменения внесены, проверьте в браузере')
    text_output('[INFO] Нажмите кнопку "Выход"')
    webbrowser.open(f'https://github.com/{log.get()}')


def disabled():
    # pas.configure(show='*')
    log.configure(state=DISABLED)
    dom.configure(state=DISABLED)
    pas.configure(state=DISABLED)
    rep.configure(state=DISABLED)
    btn.configure(state=DISABLED)
    root.update()


def text_output(text_data):
    text.insert(END, f'{text_data}\n')
    root.update()


def authorization():
    clone_repository(log.get(), dom.get(), pas.get(), rep.get())


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
        pas.configure(fg='black', show='*')
        block_dict['pas_block'] = 1
    elif root.focus_get() == rep and block_dict['rep_block'] == 0:
        rep.delete(0, END)
        rep.configure(fg='black')
        block_dict['rep_block'] = 1


def clone_repository(login, email, password, repository):
    if login == '' or email == '' or password == '' or repository == '' or '@' not in email:
        text_output('[INFO] Внимательно заполните все поля')
        return
    """
    elif login == log_start or email == dom_start or password == pas_start or repository == rep_start:
        text_output('[INFO] Внимательно заполните все поля')
        return
    """
    disabled()

    # Компьютер
    os.chdir(path)
    _, folder = os.path.split(os.getcwd())
    if folder != os.path.split(path)[1]:
        text_output('[ERROR] Вы не в папке "GitPath"')
        return
    elif os.path.isdir(repository):
        os.system(f'rmdir /s /q {repository}')
        text_output('[INFO] Одноименная папка удалена')

    try:
        os.system(f'git clone -q https://github.com/{login}/{repository}.git')
        os.chdir(os.path.join(path, repository))
    except BaseException:
        text_output(f'[ERROR] На Github нет такого репозитория')
        return
    else:
        text_output(f'[INFO] Скачивается {repository}')
        os.system(
            f'git config user.email "{email}" && git config user.name "{login}" && '
            f'git remote set-url origin https://{login}:{password}@github.com'
            f'/{login}/{repository}.git')

        if not os.path.isfile('main.py'):
            f = open('main.py', 'a')
            f.close()

        text_output('[INFO] Выполнено')
        text_output('[INFO] Не закрывайте программу')
        # btn2.configure(state=NORMAL)
        os.system(f'start "Code" "{path_vsc}"')


block_dict = {'log_block': 0, 'dom_block': 0, 'pas_block': 0, 'rep_block': 0}

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
dom = Entry(lf, width=38, font='Arial 14', fg='light gray')
pas = Entry(lf, width=38, font='Arial 14', fg='light gray')
rep = Entry(lf, width=38, font='Arial 14', fg='light gray')
log.insert(0, 'IT-KvantumVl')
dom.insert(0, 'IT-KvantumVl@yandex.ru')
pas.insert(0, 'password')
rep.insert(0, 'repository')
log.pack()
dom.pack()
pas.pack()
rep.pack()
# log_start, dom_start, pas_start, rep_start = log.get(), dom.get(), pas.get(), rep.get()

btn = Button(lf, text='С GitHub', fg='green', command=authorization)
btn.pack(side=LEFT, expand=1, fill=X)
btn2 = Button(lf, text='НА GitHub', fg='green', command=push_repository)
# btn2.configure(state=DISABLED)
btn2.pack(side=LEFT, expand=1, fill=X)

lf1 = LabelFrame(canvas, text=' Терминал ', height=250, bd=4, fg='blue')
lf1.pack_propagate(False)
lf1.pack(fill='both')
text = scroll.ScrolledText(lf1, font='Arial 12')
text.pack()
Button(canvas, text='ВЫХОД', fg='red', command=out).pack()

root.bind('<1>', enter)
root.mainloop()
