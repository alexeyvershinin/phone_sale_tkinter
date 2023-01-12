import re
import psycopg2  # требуется установить модуль для соединения с б/д
import tkinter as tk
import bcrypt  # требуется установить модуль для хеширования пароля
from tkinter import *
from tkinter import messagebox, ttk

'''Блок создания окна приложения'''


class App(tk.Tk):
    # в конструкторе определяем параметры нашего приложения
    def __init__(self):
        super().__init__()
        self.title("Attestation_Tkinter")
        self['background'] = '#fff'
        self.resizable(False, False)

        self.create_frame_autorization()  # вызываем методы создания фреймов
        self.connection = None
        self.connection_postgre()
        self.select = ''  # в этот список ложим селект из б/д
        self.curret_user = None
        self.login_user = None

        '''Шрифты'''
        self.hel_23 = 'Helvetica 23'
        self.hel_18 = 'Helvetica 18'
        self.hel_12 = 'Helvetica 12'
        self.hel_11 = 'Helvetica 11'

    # метод создания фрейма в окне авторизации
    def create_frame_autorization(self):
        self.autorization_frame = AutorizationFrame(self).grid(row=0, column=0, sticky='nswe')

    # метод создания фрейма в окне админа
    def create_frame_admin(self):
        self.admin_frame = AdminFrame(self).grid(row=0, column=0, columnspan=2, sticky='nswe')

    # метод создания фрейма в окне регистрации
    def create_frame_register(self):
        self.register_frame = RegisterFrame(self).grid(row=0, column=0, columnspan=2, sticky='nswe')

    # метод создания фрейма в окне магазина
    def create_frame_magazine(self):
        self.magazine_frame = MagazineFrame(self).grid(row=0, column=0, columnspan=2, sticky='nswe')

    # метод создания фрейма в окне редактирования товара
    def create_frame_edit_phone(self):
        self.edit_phone_frame = EditPhoneFrame(self).grid(row=0, column=0, columnspan=2, sticky='nswe')

    # метод создания фрейма в окне редактирования пользователей
    def create_frame_edit_user(self):
        self.edit_user_frame = EditUserFrame(self).grid(row=0, column=0, columnspan=2, sticky='nswe')

    # метод обновновления виджета
    def delete_all_frame(self):
        all_frames = [f for f in self.children]  # получаем все дочерние фреймы родительского окна
        for f_name in all_frames:
            self.nametowidget(f_name).destroy()  # уничтожаем его

    def connection_postgre(self):
        # подключаемся к базе данных
        global connection
        # данные для подключения
        try:
            connection = psycopg2.connect(
                database='attestation',
                user='postgres',
                password='password',
                host='127.0.0.1',
                port='5432'
            )
        except psycopg2.OperationalError as e:
            messagebox.showwarning("Error\n", e)  # в случае ошибок выводим сообщение

    def connection_close(self):
        connection.close()


class AutorizationFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self['background'] = self.master['background']  # наследуем фон
        # определяем необходимые переменные, куда бедем записывать введенные значения
        self.user_text = StringVar()
        self.pass_text = StringVar()
        self.create_widgets()  # вызываем метод создания виджетов

    # метод создания виджетов для окна авторизации
    def create_widgets(self):

        '''Блок создания полей для ввода данных и лейблов'''
        self.image = PhotoImage(file='img/login.png')
        self.image_label = tk.Label(self, image=self.image, bg='white')
        self.image_label.grid(row=0, column=0, sticky='w', padx=5, pady=5, rowspan=20)

        self.intro_lbl = tk.Label(self, text='Авторизация', fg='#57a1f8', bg='white', font='Helvetica 23')
        self.register_lbl = tk.Label(self, text='           Нет аккаунта?', fg='black', bg='white', font='Helvetica 9')

        self.intro_lbl.grid(row=2, column=1, sticky='n', padx=5, pady=5)
        self.register_lbl.grid(row=6, column=1, sticky='w', padx=5, pady=5)

        self.username_txt = tk.Entry(self, width=25, fg='black', border=0, bg='white', textvariable=self.user_text,
                                     font='Helvetica 11')
        self.username_txt.insert(0, 'Имя пользователя')
        self.username_txt.bind('<FocusIn>', self.enter_username)
        self.username_txt.bind('<FocusOut>', self.back_insert_username)

        self.password_txt = tk.Entry(self, width=25, fg='black', border=0, bg='white', textvariable=self.pass_text,
                                     font='Helvetica 11')
        self.password_txt.insert(0, 'Пароль')
        self.password_txt.bind('<FocusIn>', self.enter_password)
        self.password_txt.bind('<FocusOut>', self.back_insert_password)

        self.username_txt.grid(row=3, column=1, sticky='w', padx=5, pady=5)
        self.password_txt.grid(row=4, column=1, sticky='w', padx=5, pady=5)

        self.username_frame = tk.Frame(self, width=285, height=2, bg='black')
        self.password_frame = tk.Frame(self, width=285, height=2, bg='black')

        self.username_frame.grid(row=3, column=1, sticky='s', padx=5, pady=5)
        self.password_frame.grid(row=4, column=1, sticky='s', padx=5, pady=5)

        '''Блок создания кнопок'''

        self.btn_login = tk.Button(self, width=39, pady=7, text='Войти', bg='#57a1f8', activebackground='white',
                                   fg='white', border=0,
                                   command=self.login)
        self.btn_login.grid(row=5, column=1, padx=5, pady=5, sticky='n')

        self.btn_register = tk.Button(self, width=6, text='Создать', border=0, bg='white', activebackground='white',
                                      fg='#57a1f8', cursor='hand2',
                                      command=self.register)
        self.btn_register.grid(row=6, column=1, padx=5, pady=5, sticky='ns')

    def enter_username(self, e):
        self.username_txt.delete(0, 'end')

    def back_insert_username(self, e):
        name = self.username_txt.get()
        if name == '':
            self.username_txt.insert(0, 'Имя пользователя')

    def enter_password(self, e):
        self.password_txt.delete(0, 'end')
        self.password_txt.config(show='*')

    def back_insert_password(self, e):
        name = self.password_txt.get()
        if name == '':
            self.password_txt.config(show='')
            self.password_txt.insert(0, 'Пароль')

    def login(self):
        password = self.password_txt.get()
        login_user = self.username_txt.get()

        curs = connection.cursor()
        # получаем список всех логинов таблицы USERS
        Q_selectLoginUsers = '''
                            SELECT login FROM users '''
        lst_log = []
        curs.execute(Q_selectLoginUsers)
        for item in curs:
            lst_log.append(item[0])

        if login_user in lst_log:
            curs = connection.cursor()
            curs.execute("SELECT password FROM users WHERE login=%s", [login_user])
            pass_db = curs.fetchone()[0]  # получаем хешированный пароль из б/д

            pass_decode = pass_db[2:-1]

            pass_db_byte = pass_decode.encode('utf-8')
            input_pass = password.encode('utf-8')
            result = bcrypt.checkpw(input_pass, pass_db_byte)

        if login_user in lst_log and result is True:
            curs = connection.cursor()
            curs.execute("SELECT * FROM users WHERE login=%s", [login_user])
            user_data = curs.fetchone()
            role_user = user_data[6]
            exist = user_data[7]
            print(exist)
            self.master.curret_user = login_user
            if exist is True:
                if role_user == 1:
                    self.master.delete_all_frame()
                    self.master.create_frame_admin()
                else:
                    self.master.delete_all_frame()
                    self.master.create_frame_magazine()
            else:
                messagebox.showwarning("Ошибка\n", 'Ваш аккаунт заблокирован, обратитесь в службу поддержки')
        else:
            if login_user not in lst_log and login_user != 'Имя пользователя' and len(login_user) != 0:
                messagebox.showwarning("Ошибка валидации\n", 'Пользователь с таким логином не найден\n'
                                                             'проверте правильность введенных данных либо пройдите регистрацию')
            elif login_user in lst_log and result is False:
                messagebox.showwarning("Ошибка валидации\n", 'Проверьте правильность введенного пароля')
            elif login_user == 'Имя пользователя' or password == 'Пароль' or len(login_user) == 0 or len(password) == 0:
                messagebox.showwarning("Ошибка валидации\n", 'Необходимо ввести имя пользователя и пароль')

    def register(self):
        self.master.delete_all_frame()
        self.master.create_frame_register()


class AdminFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self['background'] = self.master['background']  # наследуем фон
        self.create_widgets()  # вызываем метод создания виджетов

    # метод создания виджетов для окна авторизации
    def create_widgets(self):
        '''Блок создания картинки'''
        self.image = PhotoImage(file='img/admin.png')
        self.image_label = tk.Label(self, image=self.image, bg='white')
        self.image_label.grid(row=0, column=0, columnspan=2, sticky='we', padx=5, pady=5)

        '''Блок создания лейблов'''
        self.info_lbl = tk.Label(self,
                                 text=f'Добро пожаловать, {self.master.curret_user}. Перейдя во вкладку "Товары магазина" ты можешь добавлять, удалять,\n'
                                      f'редактировать товары. Просто заполни правильно форму и нажми кнопку "Добавить товар". Чтобы\n'
                                      f'удалить товар, просто выбери его из таблицы и нажми "Удалить". Для редактирования, кликни по\n'
                                      f'нужной ячейке два раза и нажми "Enter", после того, как введешь новое значение. Во вкладке\n'
                                      f'"Пользователи" ты можешь изменить роль пользователя либо логически его удалить, после чего\n'
                                      f'пользователель не сможет войти на наш портал. Выбирай пользователя из таблицы и жми кнопку.\n',
                                 fg='black', bg='white', justify=LEFT, font=self.master.hel_11)
        self.info_lbl.grid(row=1, column=0, columnspan=2, sticky='we', padx=5, pady=5)  # размещаем лейбл

        '''Блок создания кнопок'''
        self.btn_users = tk.Button(self, width=39, pady=7, text='Пользователи', bg='#57a1f8',
                                   activebackground='white', fg='white', border=0, command=self.view_user)
        self.btn_phone = tk.Button(self, width=39, pady=7, text='Товары магазина', bg='#57a1f8',
                                   activebackground='white', fg='white', border=0, command=self.view_phone)

        # размещаем кнопки
        self.btn_users.grid(row=2, column=0, padx=5, pady=5, sticky='n')
        self.btn_phone.grid(row=2, column=1, padx=5, pady=5, sticky='n')

    # метод открытия окна редактирования товаров
    def view_phone(self):
        self.master.delete_all_frame()  # уничтожаем все фреймы
        self.master.create_frame_edit_phone()  # вызываем метод создания фреймы окна редактирования товара

    # метод открытия окна редактирования товаров
    def view_user(self):
        self.master.delete_all_frame()  # уничтожаем все фреймы
        self.master.create_frame_edit_user()  # вызываем метод создания фреймы окна редактирования пользователей


'''Блок редактирования пользователей'''


# определяем  дочерний класс EditUserFrame, который наследует базовый класс tk.Frame
class EditUserFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self['background'] = self.master['background']  # наследуем фон
        self.create_widgets()
        self.create_table_widget()

    # метод создания виджетов для окна редактирования ассортимента магазина
    def create_widgets(self):
        '''Блок создания картинки'''
        self.image = PhotoImage(file='img/users.png')
        self.image_label = tk.Label(self, image=self.image, bg='white')
        self.image_label.grid(row=0, column=0, columnspan=3, padx=5, pady=5)

        '''Блок создания кнопок'''
        self.btn_user_role = tk.Button(self, width=25, pady=7, text='Изменить роль пользователя', bg='#57a1f8',
                                       activebackground='white', fg='white', border=0, command=self.change_user_role)
        self.btn_delete_user = tk.Button(self, width=25, pady=7, text='Удалить/Вернуть', bg='#57a1f8',
                                         activebackground='white', fg='white', border=0, command=self.delete_user)
        self.btn_back = tk.Button(self, width=25, pady=7, text='Назад', bg='#57a1f8',
                                  activebackground='white', fg='white', border=0, command=self.back)

        # размещаем кнопки
        self.btn_user_role.grid(row=1, column=2, padx=5, pady=5, sticky='e')
        self.btn_delete_user.grid(row=1, column=1, padx=5, pady=5, sticky='n')
        self.btn_back.grid(row=1, column=0, padx=5, pady=5, sticky='w')

    # метод создания таблицы
    def create_table_widget(self):
        # получаем все записи из таблицы USER
        curs = connection.cursor()
        Q_selectUser = '''
        SELECT
        	users.user_id,
            users.lastname,
            users.firstname,
            users.patronymic,
        	users.login,
        	role_of_users.role,
        	users.exist
        FROM users JOIN role_of_users 
            ON users.role_user = role_of_users.id_role;
            '''

        curs.execute(Q_selectUser)
        lst_user = curs.fetchall()

        self.table = ttk.Treeview(self, show='headings')  # создаем таблицу, показывать будет только заголовки
        heads = ['id', 'Фамилия', 'Имя',
                 'Отчество', 'Логин', 'Роль пользователя', 'Логическое удаление']  # определяем имена заголовков
        self.table['columns'] = heads  # присваиваем именам колонок в таблице, наши заголовки

        # задаем цвета в зависимости от тегов
        self.table.tag_configure('oddrow', background='white')
        self.table.tag_configure('evenrow', background='#ABDEF4')

        # устанавливаем позиционирование заголовков и выводимых записей
        for header in heads:
            self.table.heading(header, text=header, anchor='center')
            self.table.column(header, anchor='center')

        # циклом ложим в таблицу данные из нашего селекта, при помощи счетчика определяем чередование цвета в записях
        count = 0
        for row in lst_user:
            if count % 2 == 0:
                self.table.insert('', tk.END, values=row, tags=('evenrow',))
            else:
                self.table.insert('', tk.END, values=row, tags=('oddrow',))
            count += 1

        # упаковываем таблицу и добавляем скроллинг
        self.scroll_pane = ttk.Scrollbar(self, command=self.table.yview)
        self.table.configure(yscrollcommand=self.scroll_pane.set)  # связываем скроллинг и таблицу
        # зададим размер для каждой колонки
        self.table.column('#1', width=30)
        self.table.column('#2', width=100)
        self.table.column('#3', width=100)
        self.table.column('#4', width=100)
        self.table.column('#5', width=100)
        self.table.column('#6', width=150)
        self.table.column('#7', width=150)
        self.scroll_pane.grid(row=2, column=2, sticky='nse', padx=5, pady=5)
        self.table.grid(row=2, column=0, sticky='we', padx=5, pady=5, columnspan=3)

    '''Блок метода возвращения назад'''

    # Определяем метод возвращения назад
    def back(self):
        self.master.delete_all_frame()  # уничтожаем все фреймы
        self.master.create_frame_admin()  # вызываем метод создания фрейма админки

    '''Блок метода логического удаления пользователя'''

    # Определяем метод логического удаления пользователя
    def delete_user(self):
        try:
            # получаем данные записи в таблице на которой установлен фокус
            item = self.table.focus()
            string = self.table.item(item, 'values')

            curs = connection.cursor()
            # получаем данные записи о пользователе по id
            curs.execute(
                'SELECT exist FROM users WHERE user_id=(%s)',
                [string[0]]
            )
            exist = curs.fetchone()[0]
            if exist is True:
                curs = connection.cursor()
                curs.execute(
                    'UPDATE users SET exist=FALSE WHERE user_id=(%s)',
                    [string[0]]
                )
                connection.commit()
                messagebox.showinfo('Success',
                                    f'Пользователь {string[4]} логически удален')  # выводим сообщение об успешном удалении
                self.update_table()
            else:
                curs = connection.cursor()
                curs.execute(
                    'UPDATE users SET exist=TRUE WHERE user_id=(%s)',
                    [string[0]]
                )
                connection.commit()
                messagebox.showinfo('Success',
                                    f'Вы отменили удаление пользователя {string[4]}')  # выводим сообщение об отмене удаления
                self.update_table()
        except:
            messagebox.showwarning("Ошибка\n",
                                   'Необходимо выбрать пользователя из списка')

    '''Блок метода смены роли пользователя'''

    # определяем метод смены роли пользователя
    def change_user_role(self):
        try:
            # получаем данные записи в таблице на которой установлен фокус
            item = self.table.focus()
            string = self.table.item(item, 'values')

            curs = connection.cursor()
            # получаем данные записи о пользователе по id
            curs.execute(
                'SELECT role_user FROM users WHERE user_id=(%s)',
                [string[0]]
            )
            role_user = curs.fetchone()[0]

            if role_user == 1:
                curs = connection.cursor()
                curs.execute(
                    'UPDATE users SET role_user=2 WHERE user_id=(%s)',
                    [string[0]]
                )
                connection.commit()
                messagebox.showinfo('Success',
                                    f'Роль пользователя {string[4]} изменена')  # выводим сообщение об изменении роли
                self.update_table()
            else:
                curs = connection.cursor()
                curs.execute(
                    'UPDATE users SET role_user=1 WHERE user_id=(%s)',
                    [string[0]]
                )
                connection.commit()
                messagebox.showinfo('Success',
                                    f'Пользователю {string[4]} предоставлены права администратора')  # выводим сообщение об изменении роли
                self.update_table()
        except:
            messagebox.showwarning("Ошибка\n",
                                   'Необходимо выбрать пользователя из списка')

    '''Блок обновления таблицы'''

    # определяем метод обновления таблицы
    def update_table(self):
        all_frames = [f for f in self.children]  # получаем все дочерние фреймы родительского окна
        for f_name in all_frames:
            if f_name == '!treeview':  # для фрейма с таблицей
                self.nametowidget(f_name).destroy()  # уничтожаем его
        self.create_table_widget()  # вызываем метод создания таблицы


'''Блок редактирования товара'''


# определяем  дочерний класс EditPhoneFrame, который наследует базовый класс tk.Frame
class EditPhoneFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self['background'] = self.master['background']  # наследуем фон

        # определяем переменные, куда будем записывать введенные значения при заполнении формы добавления товара
        self.model_text = StringVar()  # Модель телефона
        self.model_text.trace('w',
                              self.limit_size_model)  # Методом trace вызываем функцию self.limit_size_model каждый раз, когда запрашивается переменная
        self.processor_text = StringVar()  # Процессор
        self.processor_text.trace('w',
                                  self.limit_size_processor)  # Методом trace вызываем функцию self.limit_size_processor каждый раз, когда запрашивается переменная
        self.memory_text = StringVar()  # Встроенная память
        self.ram_text = StringVar()  # Оперативная память
        self.item_memory = [8, 16, 32, 64, 128, 256]  # значения для выбора встроенной памяти
        self.item_ram = [1, 2, 3, 4, 6, 8, 12, 16]  # значения для выбора оперативной памяти

        self.create_widgets()  # вызываем метод создания виджетов
        self.create_table_widget()  # вызываем метод создания таблицы

    # метод создания виджетов для окна редактирования ассортимента магазина
    def create_widgets(self):
        '''Блок создания картинки'''
        self.image = PhotoImage(file='img/administration_phone.png')
        self.image_label = tk.Label(self, image=self.image, bg='white')
        self.image_label.grid(row=0, column=0, sticky='we', padx=5, pady=5, rowspan=19)

        '''Блок создания лейблов'''
        self.intro_lbl = tk.Label(self, text='Добавление товара', fg='#57a1f8', bg='white', font=self.master.hel_23)
        self.intro_lbl.grid(row=0, column=1, sticky='swe', padx=5, pady=5)

        '''Блок создания полей ввода'''
        self.model_txt = tk.Entry(self, width=35, fg='black', border=0, bg='white', textvariable=self.model_text,
                                  font=self.master.hel_11)  # поле ввода "Модели телефона"
        self.model_txt.insert(0, 'Модель телефона')  # методом insert вставляем значение
        self.model_txt.bind('<FocusIn>', self.enter_model_txt)  # действие при установлении фокуса
        self.model_txt.bind('<FocusOut>', self.back_insert_model_txt)  # действие при изменении фокуса
        self.processor_txt = tk.Entry(self, width=35, fg='black', border=0, bg='white',
                                      textvariable=self.processor_text,
                                      font=self.master.hel_11)  # поле ввода "Процессора"
        self.processor_txt.insert(0, 'Процессор')  # методом insert вставляем значение
        self.processor_txt.bind('<FocusIn>', self.enter_processor_txt)  # действие при установлении фокуса
        self.processor_txt.bind('<FocusOut>', self.back_insert_processor_txt)  # действие при изменении фокуса
        self.memory_txt = tk.Entry(self, width=25, fg='black', border=0, bg='white',
                                   textvariable=self.memory_text,
                                   font=self.master.hel_11)  # поле ввода "Встроенной памяти"
        self.memory_txt.insert(0, 'Встроенная память, Гб')  # методом insert вставляем значение
        self.memory_txt.config(state="readonly", readonlybackground='white')  # запрещаем вводить данные в поле
        self.ram_txt = tk.Entry(self, width=25, fg='black', border=0, bg='white', textvariable=self.ram_text,
                                font=self.master.hel_11)  # поле ввода "Оперативной памяти"
        self.ram_txt.insert(0, 'Оперативная память, Гб')  # методом insert вставляем значение
        self.ram_txt.config(state="readonly", readonlybackground='white')  # запрещаем вводить данные в поле

        self.memory_combo = ttk.Combobox(self, width=11, justify=tk.RIGHT, values=self.item_memory,
                                         state="readonly")  # значения для поля "Встроенная память будем выбирать из списка при помощи поля ComboBox"
        self.memory_combo.current(0)  # устанавливаем значение по умолчанию
        self.ram_combo = ttk.Combobox(self, width=11, justify=tk.RIGHT, values=self.item_ram,
                                      state="readonly")  # значения для поля "Оперативная память будем выбирать из списка при помощи поля ComboBox"
        self.ram_combo.current(0)  # устанавливаем значение по умолчанию

        # размещаем поля ввода
        self.model_txt.grid(row=1, column=1, sticky='w', padx=5, pady=5)
        self.processor_txt.grid(row=2, column=1, sticky='w', padx=5, pady=5)
        self.memory_txt.grid(row=3, column=1, sticky='w', padx=5, pady=5)
        self.ram_txt.grid(row=4, column=1, sticky='w', padx=5, pady=5)
        self.memory_combo.grid(row=3, column=1, sticky='ne', padx=5, pady=5)
        self.ram_combo.grid(row=4, column=1, sticky='ne', padx=5, pady=5)

        '''Блок создания фреймов'''
        # фреймами нарисуем черные полоски под полями ввода
        self.model_txt_frame = tk.Frame(self, width=355, height=2, bg='black')
        self.processor_txt_frame = tk.Frame(self, width=355, height=2, bg='black')
        self.memory_txt_frame = tk.Frame(self, width=355, height=2, bg='black')
        self.ram_txt_frame = tk.Frame(self, width=355, height=2, bg='black')

        # размещаем фреймы
        self.model_txt_frame.grid(row=1, column=1, sticky='ws', padx=5, pady=5)
        self.processor_txt_frame.grid(row=2, column=1, sticky='ws', padx=5, pady=5)
        self.memory_txt_frame.grid(row=3, column=1, sticky='ws', padx=5, pady=5)
        self.ram_txt_frame.grid(row=4, column=1, sticky='ws', padx=5, pady=5)

        '''Блок создания кнопок'''
        self.btn_add_phone = tk.Button(self, width=22, pady=7, text='Добавить товар', bg='#57a1f8',
                                       activebackground='white', fg='white', border=0, command=self.add_phone)
        self.btn_delete_phone = tk.Button(self, width=22, pady=7, text='Удалить товар', bg='#57a1f8',
                                          activebackground='white', fg='white', border=0, command=self.delete_phone)
        self.btn_back = tk.Button(self, width=22, pady=7, text='Назад', bg='#57a1f8',
                                  activebackground='white', fg='white', border=0, command=self.back)

        # размещаем кнопки
        self.btn_add_phone.grid(row=20, column=1, padx=5, pady=5, sticky='e')
        self.btn_delete_phone.grid(row=20, column=1, padx=5, pady=5, sticky='w')
        self.btn_back.grid(row=20, column=0, padx=5, pady=5, sticky='w')

    # данный метод ограничит количество вводимых символов в поле "Модель телефона"
    def limit_size_model(self, *args):
        value = self.model_text.get()
        if len(value) > 35: self.model_text.set(value[:35])

    # данный метод ограничит количество вводимых символов в поле "Процессор"
    def limit_size_processor(self, *args):
        value = self.processor_text.get()
        if len(value) > 35: self.processor_text.set(value[:35])

    # при установлении фокуса очищаем поле
    def enter_model_txt(self, e):
        self.model_txt.delete(0, 'end')

    # производим запись в поле при изменеии фокуса, если в поле отсутствует запись
    def back_insert_model_txt(self, e):
        name = self.model_txt.get()
        if name == '':
            self.model_txt.insert(0, 'Модель телефона')

    # при установлении фокуса очищаем поле
    def enter_processor_txt(self, e):
        self.processor_txt.delete(0, 'end')

    # производим запись в поле при изменеии фокуса, если в поле отсутствует запись
    def back_insert_processor_txt(self, e):
        name = self.processor_txt.get()
        if name == '':
            self.processor_txt.insert(0, 'Процессор')

    '''Блок создания таблицы с выводом данных о товарах'''

    # метод создания таблицы
    def create_table_widget(self):
        # получаем все записи из таблицы PHONE
        curs = connection.cursor()
        Q_selectPhone = '''SELECT * FROM phone '''

        curs.execute(Q_selectPhone)
        lst_phone = curs.fetchall()

        self.table = ttk.Treeview(self, show='headings')  # создаем таблицу, показывать будет только заголовки
        heads = ['Id', 'Модель телефона', 'Процессор', 'Объем встроенной памяти, Гб',
                 'Объем оперативной памяти, Гб']  # определяем имена заголовков
        self.table['columns'] = heads  # присваиваем именам колонок в таблице, наши заголовки

        # задаем цвета в зависимости от тегов
        self.table.tag_configure('oddrow', background='white')
        self.table.tag_configure('evenrow', background='#ABDEF4')

        # устанавливаем позиционирование заголовков и выводимых записей
        for header in heads:
            self.table.heading(header, text=header, anchor='center')
            self.table.column(header, anchor='center')

        # циклом ложим в таблицу данные из нашего селекта, при помощи счетчика определяем чередование цвета в записях
        count = 0
        for row in lst_phone:
            if count % 2 == 0:
                self.table.insert('', tk.END, values=row, tags=('evenrow',))
            else:
                self.table.insert('', tk.END, values=row, tags=('oddrow',))
            count += 1

        self.table.bind('<Double-1>',
                        self.double_click)  # определяем метод который будет вызываться по двойному клику по записи

        # размещаем таблицу и добавляем скроллинг
        self.scroll_pane = tk.Scrollbar(self, command=self.table.yview, width=10)
        self.table.configure(yscrollcommand=self.scroll_pane.set)  # связываем скроллинг и таблицу
        # зададим размер для каждой колонки
        self.table.column('#1', width=30)
        self.table.column('#2', width=180)
        self.table.column('#3', width=125)
        self.table.column('#4', width=180)
        self.table.column('#5', width=180)

        self.scroll_pane.grid(row=21, column=1, sticky='nse', padx=5, pady=5)
        self.table.grid(row=21, column=0, sticky='n', padx=5, pady=5, columnspan=2)

    # метод редактирования записи в таблице по двойному клику
    def double_click(self, event):
        # получааем зону в таблице, по которой был произведен двойной клик
        zone_clicked = self.table.identify_region(event.x, event.y)
        # если зона не ячейка таблицы, ничего не делаем
        if zone_clicked != 'cell':
            return

        column = self.table.identify_column(event.x)  # определяем колонку по которой был произведен двойной клик
        column_index = int(column[1:]) - 1  # преобразовываем номер колонки, по которой произведен клик(отбрасываем #)
        selected_iid = self.table.focus()  # получаем IID записи на которой установлен фокус
        selected_values = self.table.item(selected_iid)  # получаем все параметры строки по IID
        selected_text = selected_values.get('values')[
            column_index]  # получаем запись столбца и строки по которому был сделан клик

        column_box = self.table.bbox(selected_iid, column)  # получаем координаты ячейки таблицы
        entry_edit = ttk.Entry(self.table, width=column_box[2])  # определяем виджет редактирования записи

        entry_edit.editing_column_index = column_index  # присваиваем переменной номер колонки, по которой произведен клик
        entry_edit.editing_item_iid = selected_iid  # присваиваем переменной IID записи на которой установлен фокус

        entry_edit.insert(0, selected_text)  # вставляем в поле ввода запись, полученную из ячейки
        entry_edit.select_range(0, tk.END)
        entry_edit.focus()  # определяем фокус поля ввода, редактируемой ячейки

        entry_edit.bind('<FocusOut>', self.focus_out)  # определяем вызываемый метод при потере фокуса
        entry_edit.bind('<Return>', self.enter_press)  # определяем вызываемый метод при нажатии Enter

        # запрещаем создавать виджет редактирования поля в колонке солержащей ID
        if column_index == 0:
            return
        # размещаем виджет редактирования записи в колонке используя координаты полученные в column_box
        entry_edit.place(x=column_box[0], y=column_box[1], w=column_box[2], h=column_box[3])

    # определяем метод, к которому обращаемся при нажатии ENTER
    def enter_press(self, event):
        new_text = event.widget.get()  # присваиваем переменной значение отредактированной записи в ячейке

        selected_iid = event.widget.editing_item_iid  # получаем IID отредактированной записи
        column_index = event.widget.editing_column_index  # получаем номер колонки где производилось редактирование

        curret_values = self.table.item(selected_iid).get('values')  # получаем значение записи до редактирования
        curret_values[column_index] = new_text  # присваиваем отредактированное значение ячейки

        # валидация полей "Внутренняя память" и "Оперативная память"
        if column_index in (3, 4):
            if not new_text.isdigit() or len(new_text) not in range(1, 4):
                messagebox.showwarning("Ошибка валидации\n",
                                       'Проверьте следующие условияЖ:\n'
                                       '-hедактируемое поле может содержать только цифры\n'
                                       '-поле не может быть пустым\n'
                                       '-поле не может содержать больше 3х цифр')
                return
        # валидация полей "Модель" и "Процессор"
        if column_index in (1, 2):
            if len(new_text) not in range(1, 35):
                messagebox.showwarning("Ошибка валидации\n",
                                       'Проверьте следующие условияЖ:\n'
                                       '-поле не может быть пустым\n'
                                       '-поле не может содержать больше 35 символов')
                return

        # опредеояем переменные в которых будут храниться отредактированные значения
        edit_id = curret_values[0]  # id записи
        edit_model = curret_values[1]  # модель телефона
        edit_processor = curret_values[2]  # процессор
        edit_memory = curret_values[3]  # встроенная память
        edit_ram = curret_values[4]  # оперативная память

        # обращаемся к базе данных, в запрос вставляем отредактированные значения и обновляем запись
        curs = connection.cursor()
        update_query = '''UPDATE phone SET model=(%s), processor=(%s), memory=(%s), ram=(%s) WHERE id_phone=(%s)'''
        values = (edit_model, edit_processor, edit_memory, edit_ram, edit_id)
        curs.execute(update_query, values)
        connection.commit()
        messagebox.showinfo('Success', 'Товар успешно изменен')  # выводим сообщение об успешной записи

        # self.table.item(selected_iid, values=curret_values)  # записываем в таблицу отредактированное значение

        event.widget.destroy()  # уничтожаем виджет ввода для редактирования

        # как второй вариант, вызываем метод обновления таблицы
        self.update_table()

    # после снятия фокуса с ячейки уничтожаем виджет ввода записи
    def focus_out(self, event):
        event.widget.destroy()

    '''Блок обновления таблицы'''

    def update_table(self):
        all_frames = [f for f in self.children]  # получаем все дочерние фреймы родительского окна
        for f_name in all_frames:
            if f_name == '!treeview':  # для фрейма с таблицей
                self.nametowidget(f_name).destroy()  # уничтожаем его
        self.create_table_widget()  # вызываем метод создания таблицы

    '''Блок добавления товара'''

    def add_phone(self):
        # получаем введенные значения
        model = self.model_text.get()
        processor = self.processor_text.get()
        memory = self.memory_combo.get()
        ram = self.ram_combo.get()

        # проводим валидацию введенных значений до записи в базу данных
        if len(model) < 50 and model != 'Модель телефона':
            if len(processor) < 50 and processor != 'Процессор':
                # производим запись товара в БД, родставляя полученные значения
                curs = connection.cursor()
                curs.execute(
                    'INSERT INTO phone (model, processor, memory, ram) VALUES(%s,%s,%s,%s)',
                    (model, processor, memory, ram)
                )
                connection.commit()  # подтверждаем запись в б/д
                messagebox.showinfo('Success', 'Товар успешно добавлен')  # выводим сообщение об успешной записи

                # после записи в базу данных уничтожаем все фреймы в окне и создаем заново, чтобы обновились значения
                self.master.delete_all_frame()
                self.master.create_frame_edit_phone()

            else:
                if processor == 'Процессор':
                    messagebox.showwarning("Ошибка валидации\n",
                                           'Для записи данных необходимо заполнить поле "Процессор"')
                if len(processor) >= 50:
                    messagebox.showwarning("Ошибка валидации\n",
                                           'Длина поля "Процессор" не должна превышать 50 символов')
        else:
            if model == 'Модель телефона':
                messagebox.showwarning("Ошибка валидации\n",
                                       'Для записи данных необходимо заполнить поле "Модель телефона"')
            if len(model) >= 50:
                messagebox.showwarning("Ошибка валидации\n",
                                       'Длина поля "Модель телефона" не должна превышать 50 символов')

    '''Определяем метод возвращения назад'''

    def back(self):
        self.master.delete_all_frame()  # уничтожаем все фреймы
        self.master.create_frame_admin()  # вызываем метод создания фрейма админки

    '''Определяем метод удаления выбранного товара'''

    def delete_phone(self):
        try:
            # получаем данные записи в таблице на которой установлен фокус
            item = self.table.focus()
            string = self.table.item(item, 'values')

            curs = connection.cursor()
            # удаляем запись с id выбранного товара
            curs.execute(
                'DELETE FROM phone WHERE id_phone=(%s)',
                [string[0]]
            )
            connection.commit()

            messagebox.showinfo('Success',
                                'Товар успешно удален из базы данных')  # выводим сообщение об успешном удалении

            #  после удаления из базы данных уничтожаем все фреймы в окне и создаем заново, чтобы обновились значения
            self.master.delete_all_frame()
            self.master.create_frame_edit_phone()
        # прописываем исключение, на случай если будет нажата кнопка, а товар для удаления не будет выбран
        except:
            messagebox.showwarning("Ошибка\n",
                                   'Для удаления необходимо выбрать товар из списка')


'''Блок регистрации пользователя'''


# создаем дочерний класс RegisterFrame, который наследует базовый класс tk.Frame
class RegisterFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self['background'] = self.master['background']  # наследуем фон

        # определяем переменные, куда будем записывать введенные значения при заполнении формы регистрации
        self.lastname_text = StringVar()  # Фамилия
        self.firstname_text = StringVar()  # Имя
        self.patronymic_text = StringVar()  # Отчество
        self.login_text = StringVar()  # Логин
        self.password_text = StringVar()  # Пароль
        self.confirm_password_text = StringVar()  # Подтверждение пароля
        self.enabled = IntVar()  # пользовательское соглашение
        self.create_widgets()  # вызываем метод создания виджетов

        # определяем переменные, которыми будем обозначать этапы валидации полей формы регистрации
        self.validation_lastname = False
        self.validation_firstname = False
        self.validation_patronymic = False
        self.validation_login = False
        self.validation_password = False
        self.validation_confirm_password = False
        self.validation_checkbutton = False

    # метод создания виджетов для окна регистрации пользователей
    def create_widgets(self):
        '''Блок создания картинки'''
        self.image = PhotoImage(file='img/register.png')
        self.image_label = tk.Label(self, image=self.image, bg='white')
        self.image_label.grid(row=0, column=0, sticky='w', padx=5, pady=5, rowspan=20)

        '''Блок создания лейблов'''
        self.intro_lbl = tk.Label(self, text='Регистрация', fg='#57a1f8', bg='white', font=self.master.hel_23)
        # этими лейблами укажем пользователю на поля, не прошедшие валидацию
        self.lastname_reg_lbl = tk.Label(self, text='•', fg='white', bg='white', font=self.master.hel_18)
        self.firstname_reg_lbl = tk.Label(self, text='•', fg='white', bg='white', font=self.master.hel_18)
        self.patronymic_reg_lbl = tk.Label(self, text='•', fg='white', bg='white', font=self.master.hel_18)
        self.login_reg_lbl = tk.Label(self, text='•', fg='white', bg='white', font=self.master.hel_18)
        self.password_reg_lbl = tk.Label(self, text='•', fg='white', bg='white', font=self.master.hel_18)
        self.confirm_password_reg_lbl = tk.Label(self, text='•', fg='white', bg='white', font=self.master.hel_18)

        # размещаем лейблы
        self.intro_lbl.grid(row=0, column=1, sticky='n', padx=5, pady=5, columnspan=2)
        self.lastname_reg_lbl.grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.firstname_reg_lbl.grid(row=2, column=0, sticky='e', padx=5, pady=5)
        self.patronymic_reg_lbl.grid(row=3, column=0, sticky='e', padx=5, pady=5)
        self.login_reg_lbl.grid(row=4, column=0, sticky='e', padx=5, pady=5)
        self.password_reg_lbl.grid(row=5, column=0, sticky='e', padx=5, pady=5)
        self.confirm_password_reg_lbl.grid(row=6, column=0, sticky='e', padx=5, pady=5)

        '''Блок создания полей ввода'''
        self.lastname_txt = tk.Entry(self, width=24, fg='black', border=0, bg='white', textvariable=self.lastname_text,
                                     font=self.master.hel_11, validate='focusout',
                                     validatecommand=(
                                         self.register(self.validate_lastname), '%P'))  # поле ввода "Фамидия"
        self.lastname_txt.insert(0, 'Фамилия')  # методом insert вставляем значение
        self.lastname_txt.bind('<FocusIn>', self.enter_lastname_txt)  # действие при установлении фокуса
        self.lastname_txt.bind('<FocusOut>', self.back_insert_lastname_txt)  # действие при изменении фокуса
        self.firstname_txt = tk.Entry(self, width=24, fg='black', border=0, bg='white',
                                      textvariable=self.firstname_text, font=self.master.hel_11, validate='focusout',
                                      validatecommand=(
                                          self.register(self.validate_firstname), '%P'))  # поле ввода "Имя"
        self.firstname_txt.insert(0, 'Имя')  # методом insert вставляем значение
        self.firstname_txt.bind('<FocusIn>', self.enter_firstname_txt)  # действие при установлении фокуса
        self.firstname_txt.bind('<FocusOut>', self.back_insert_firstname_txt)  # действие при изменении фокуса
        self.patronymic_txt = tk.Entry(self, width=24, fg='black', border=0, bg='white',
                                       textvariable=self.patronymic_text, font=self.master.hel_11, validate='focusout',
                                       validatecommand=(
                                           self.register(self.validate_patronymic), '%P'))  # поле ввода "Отчество"
        self.patronymic_txt.insert(0, 'Отчество')  # методом insert вставляем значение
        self.patronymic_txt.bind('<FocusIn>', self.enter_patronymic_txt)  # действие при установлении фокуса
        self.patronymic_txt.bind('<FocusOut>', self.back_insert_patronymic_txt)  # действие при изменении фокуса
        self.login_txt = tk.Entry(self, width=24, fg='black', border=0, bg='white', textvariable=self.login_text,
                                  font=self.master.hel_11, validate='focusout',
                                  validatecommand=(self.register(self.validate_login), '%P'))  # поле ввода "Логин"
        self.login_txt.insert(0, 'Логин')  # методом insert вставляем значение
        self.login_txt.bind('<FocusIn>', self.enter_login_txt)  # действие при установлении фокуса
        self.login_txt.bind('<FocusOut>', self.back_insert_login_txt)  # действие при изменении фокуса
        self.password_txt = tk.Entry(self, width=24, fg='black', border=0, bg='white', textvariable=self.password_text,
                                     font=self.master.hel_11, validate='focusout',
                                     validatecommand=(
                                         self.register(self.validate_password), '%P'))  # поле ввода "Пароль"
        self.password_txt.insert(0, 'Пароль')  # методом insert вставляем значение
        self.password_txt.bind('<FocusIn>', self.enter_password_txt)  # действие при установлении фокуса
        self.password_txt.bind('<FocusOut>', self.back_insert_password_txt)  # действие при изменении фокуса
        self.confirm_password_txt = tk.Entry(self, width=24, fg='black', border=0, bg='white',
                                             textvariable=self.confirm_password_text, font=self.master.hel_11,
                                             validate='focusout',
                                             validatecommand=(self.register(self.validate_confirm_password),
                                                              '%P'))  # поле ввода "Подтвердите пароль"
        self.confirm_password_txt.insert(0, 'Подтвердите пароль')  # методом insert вставляем значение
        self.confirm_password_txt.bind('<FocusIn>', self.enter_confirm_password_txt)  # действие при установлении фокуса
        self.confirm_password_txt.bind('<FocusOut>',
                                       self.back_insert_confirm_password_txt)  # действие при изменении фокуса

        # размещаем поля ввода данных для регистрации
        self.lastname_txt.grid(row=1, column=1, sticky='w', padx=5, pady=5)
        self.firstname_txt.grid(row=2, column=1, sticky='w', padx=5, pady=5)
        self.patronymic_txt.grid(row=3, column=1, sticky='w', padx=5, pady=5)
        self.login_txt.grid(row=4, column=1, sticky='w', padx=5, pady=5)
        self.password_txt.grid(row=5, column=1, sticky='w', padx=5, pady=5)
        self.confirm_password_txt.grid(row=6, column=1, sticky='w', padx=5, pady=5)

        '''Блок создания фреймов'''
        # фреймами нарисуем черные полоски под полями ввода
        self.lastname_txt_frame = tk.Frame(self, width=285, height=2, bg='black')
        self.firstname_txt_frame = tk.Frame(self, width=285, height=2, bg='black')
        self.patronymic_txt_frame = tk.Frame(self, width=285, height=2, bg='black')
        self.login_txt_frame = tk.Frame(self, width=285, height=2, bg='black')
        self.password_txt_frame = tk.Frame(self, width=285, height=2, bg='black')
        self.confirm_password_txt_frame = tk.Frame(self, width=285, height=2, bg='black')

        # размещаем фреймы
        self.lastname_txt_frame.grid(row=1, column=1, sticky='s', padx=5, pady=5)
        self.firstname_txt_frame.grid(row=2, column=1, sticky='s', padx=5, pady=5)
        self.patronymic_txt_frame.grid(row=3, column=1, sticky='s', padx=5, pady=5)
        self.login_txt_frame.grid(row=4, column=1, sticky='s', padx=5, pady=5)
        self.password_txt_frame.grid(row=5, column=1, sticky='s', padx=5, pady=5)
        self.confirm_password_txt_frame.grid(row=6, column=1, sticky='s', padx=5, pady=5)

        '''Блок создания поля CheckButton'''
        self.checkbutton = ttk.Checkbutton(self, text='Я принимаю условия соглашения', variable=self.enabled,
                                           command=self.checkbutton_changed)
        self.checkbutton.grid(row=7, column=1, padx=5, pady=5, sticky='w')

        '''Блок создания кнопок'''
        self.btn_back = tk.Button(self, width=20, pady=7, text='Назад', bg='#57a1f8',
                                  activebackground='white', fg='white', border=0, command=self.back)
        self.btn_register_user = tk.Button(self, width=39, pady=7, text='Создать аккаунт', bg='#57a1f8',
                                           activebackground='white', fg='white', border=0, command=self.register_user)
        # размещаем кнопки
        self.btn_back.grid(row=8, column=0, padx=5, pady=5, sticky='n')
        self.btn_register_user.grid(row=8, column=1, padx=5, pady=5, sticky='n')

    # при установлении фокуса очищаем поле
    def enter_lastname_txt(self, e):
        self.lastname_txt.delete(0, 'end')

    # производим запись в поле при изменеии фокуса, если в поле отсутствует запись
    def back_insert_lastname_txt(self, e):
        name = self.lastname_txt.get()
        if name == '':
            self.lastname_txt.insert(0, 'Фамилия')

    # при установлении фокуса очищаем поле
    def enter_firstname_txt(self, e):
        self.firstname_txt.delete(0, 'end')

    # производим запись в поле при изменеии фокуса, если в поле отсутствует запись
    def back_insert_firstname_txt(self, e):
        name = self.firstname_txt.get()
        if name == '':
            self.firstname_txt.insert(0, 'Имя')

    # при установлении фокуса очищаем поле
    def enter_patronymic_txt(self, e):
        self.patronymic_txt.delete(0, 'end')

    # производим запись в поле при изменеии фокуса, если в поле отсутствует запись
    def back_insert_patronymic_txt(self, e):
        name = self.patronymic_txt.get()
        if name == '':
            self.patronymic_txt.insert(0, 'Отчество')

    # при установлении фокуса очищаем поле
    def enter_login_txt(self, e):
        self.login_txt.delete(0, 'end')

    # производим запись в поле при изменеии фокуса, если в поле отсутствует запись
    def back_insert_login_txt(self, e):
        name = self.login_txt.get()
        if name == '':
            self.login_txt.insert(0, 'Логин')

    # при установлении фокуса очищаем поле
    def enter_password_txt(self, e):
        self.password_txt.delete(0, 'end')
        self.password_txt.config(show='*')

    # производим запись в поле при изменеии фокуса, если в поле отсутствует запись
    def back_insert_password_txt(self, e):
        name = self.password_txt.get()
        if name == '':
            self.password_txt.config(show='')
            self.password_txt.insert(0, 'Пароль')

    # при установлении фокуса очищаем поле
    def enter_confirm_password_txt(self, e):
        self.confirm_password_txt.delete(0, 'end')
        self.confirm_password_txt.config(show='*')

    # производим запись в поле при изменеии фокуса, если в поле отсутствует запись
    def back_insert_confirm_password_txt(self, e):
        name = self.confirm_password_txt.get()
        if name == '':
            self.confirm_password_txt.config(show='')
            self.confirm_password_txt.insert(0, 'Подтвердите пароль')

    '''Блок методов сообщений об ошибках валидацмм'''

    # метод вызова сообщения об ошибке валидации для полей ФИО
    def validation_error(self):
        error = messagebox.showwarning("Ошибка валидации\n", 'Проверьте следующие условия:\n'
                                                             '- поле обязательно для заполнения\n'
                                                             '- поле может содержать только буквы, нельзя вводить цифры и спецсимволы\n'
                                                             '- поле не может содержать знаков табуляции и пробела')
        return error

    # иетод вызова сообщения об ошибке валидации логина
    def validation_error_login(self):
        error = messagebox.showwarning("Ошибка валидации\n", 'Проверьте следующие условия:\n'
                                                             '- поле обязательно для заполнения\n'
                                                             '- поле должно содержать от 4х до 25ти знаков\n'
                                                             '- поле не может содержать знаков табуляции и пробела')
        return error

    # иетод вызова сообщения об ошибке валидации логина(в том случае, если логин уже используется)
    def validation_error_login_busy(self):
        error = messagebox.showwarning("Ошибка валидации\n", 'Данный логин занят, попробуйте другой')
        return error

    # иетод вызова сообщения об ошибке валидации пароля
    def validation_error_password(self):
        error = messagebox.showwarning("Ошибка валидации\n", 'Проверьте следующие условия:\n'
                                                             '- поле обязательно для заполнения\n'
                                                             '- пароль должен состоять из латинских букв\n'
                                                             '- пароль должен содержать от 6ти до 20ти знаков\n'
                                                             '- пароль должен содержать как минимум одну цифру и спецсимвол\n'
                                                             '- пароль должен содержать как минимум одну букву верхнего регистра\n'
                                                             '- пароль может содержать знаков табуляции и пробела')
        return error

    # иетод вызова сообщения об ошибке валидации поля подтверждения пароля
    def validation_error_confirm_password(self):
        error = messagebox.showwarning("Ошибка валидации\n", 'Поля "Пароль" и "Подтвердите пароль" не совпадают')
        return error

    '''Блок определения методов проверки формы на валидность'''

    # валидация поля Фамилия
    def validate_lastname(self, input_lastname):
        if input_lastname.isalpha() == False or re.search('[\s]', input_lastname) or len(input_lastname) not in range(1,
                                                                                                                      25):
            self.lastname_reg_lbl.config(fg="red")  # делаем подсветку невалидного поля
            self.validation_error()  # вызываем метод с сообщением об ошибке валидации
            self.validation_lastname = False  # меняем статус прохождения этапа валидации
        else:
            self.lastname_reg_lbl.config(fg="green")  # при прохождении валидации возвращаем цвет поля на стандартный
            self.validation_lastname = True  # меняем статус прохождения этапа валидации
        return True

    # валидация поля Имя
    def validate_firstname(self, input_firstname):
        if self.validation_lastname is True:
            if input_firstname.isalpha() == False or re.search('[\s]', input_firstname) or len(
                    input_firstname) not in range(1, 25):
                self.firstname_reg_lbl.config(fg="red")  # делаем подсветку невалидного поля
                self.validation_error()  # вызываем метод с сообщением об ошибке валидации
                self.validation_firstname = False  # меняем статус прохождения этапа валидации
            else:
                self.firstname_reg_lbl.config(
                    fg="green")  # при прохождении валидации возвращаем цвет поля на стандартный
                self.validation_firstname = True  # меняем статус прохождения этапа валидации
        return True

    # валидация поля Отчество
    def validate_patronymic(self, input_patronymic):
        if self.validation_lastname is True and self.validation_firstname is True:
            if input_patronymic.isalpha() == False or re.search('[\s]', input_patronymic) or len(
                    input_patronymic) not in range(1, 25):
                self.patronymic_reg_lbl.config(fg="red")  # делаем подсветку невалидного поля
                self.validation_error()  # вызываем метод с сообщением об ошибке валидации
                self.validation_patronymic = False  # меняем статус прохождения этапа валидации
            else:
                self.patronymic_reg_lbl.config(
                    fg="green")  # при прохождении валидации возвращаем цвет поля на стандартный
                self.validation_patronymic = True  # меняем статус прохождения этапа валидации
        return True

    # валидация поля Логин
    def validate_login(self, input_login):
        if self.validation_lastname is True and self.validation_firstname is True and self.validation_patronymic is True:
            # получаем список всех хранящихся в б/д логинов пользователей
            curs = connection.cursor()
            Q_selectUsers = '''
                    SELECT login FROM users '''
            lst = []
            curs.execute(Q_selectUsers)
            for item in curs:
                lst.append(item[0])  # добавляем полученные логины в список

            if re.search('[\s]', input_login) or len(input_login) not in range(4, 25):
                self.login_reg_lbl.config(fg="red")  # делаем подсветку невалидного поля
                self.validation_error_login()  # вызываем метод с сообщением об ошибке валидации
                self.validation_login = False  # меняем статус прохождения этапа валидации

            # производим проверку, есть ли введенный логин в списке существующих
            if input_login in lst:
                self.login_reg_lbl.config(fg="red")  # делаем подсветку невалидного поля
                self.validation_error_login_busy()  # вызываем метод с сообщением об ошибке валидации
                self.validation_login = False  # меняем статус прохождения этапа валидации
            else:
                self.login_reg_lbl.config(fg="green")  # при прохождении валидации возвращаем цвет поля на стандартный
                self.validation_login = True  # меняем статус прохождения этапа валидации
        return True

    # валидация поля Пароль
    def validate_password(self, input_password):
        if self.validation_lastname is True and self.validation_firstname is True and self.validation_patronymic is True and self.validation_login is True:
            if re.match('^(?=\S{6,20}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])', input_password) is None:
                self.password_reg_lbl.config(fg="red")  # делаем подсветку невалидного поля
                self.validation_error_password()  # вызываем метод с сообщением об ошибке валидации
                self.validation_password = False  # меняем статус прохождения этапа валидации
            else:
                self.password_reg_lbl.config(
                    fg="green")  # при прохождении валидации возвращаем цвет поля на стандартный
                self.validation_password = True  # меняем статус прохождения этапа валидации
        return True

    # валидация поля Подтверждение пароля
    def validate_confirm_password(self, input_confirm_password):
        if self.validation_lastname is True and self.validation_firstname is True and self.validation_patronymic is True and self.validation_login is True and self.validation_password is True:
            if input_confirm_password == self.password_text.get():
                self.confirm_password_reg_lbl.config(
                    fg="green")  # при прохождении валидации возвращаем цвет поля на стандартный
                self.validation_confirm_password = True  # меняем статус прохождения этапа валидации
            else:
                self.confirm_password_reg_lbl.config(fg="red")  # делаем подсветку невалидного поля
                self.validation_error_confirm_password()  # вызываем метод с сообщением об ошибке валидации
                self.validation_confirm_password = False  # меняем статус прохождения этапа валидации
        return True

    # метод изменения значения при принятии Пользовательского соглашения
    def checkbutton_changed(self):
        if self.enabled.get() == 1:
            self.validation_checkbutton = True
        else:
            self.validation_checkbutton = False

    '''Блок метода возвращения назад'''

    def back(self):
        self.master.delete_all_frame()  # уничтожаем все фреймы
        self.master.create_frame_autorization()  # вызываем метод создания фреймы окна авторизации

    '''Блок метода регистрации пользователя'''

    def register_user(self):
        # получаем введенные значения
        lastname = self.lastname_text.get()
        firstname = self.firstname_text.get()
        patronymic = self.patronymic_text.get()
        login = self.login_text.get()
        password = self.password_text.get()
        self.master.login_user = self.login_text.get()

        '''Блок хеширования пароля'''
        hash_pass = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())  # хешируем пароль и соль

        # если пользователь не принял соглашение, выведем сообщение с предупреждением
        if self.validation_checkbutton is not True:
            messagebox.showwarning("Ошибка валидации\n",
                                   'Внимание! Вы должны принять условия соглашения и заполнить все поля')
        else:
            # если все этапы валидации пройдены, производим запись нового пользователя в б/д, по умолчанию присваиваем статус пользователя
            if self.validation_lastname is True and self.validation_firstname is True and self.validation_patronymic is True and self.validation_login is True and self.validation_password is True and self.validation_confirm_password is True:

                # производим запись пользователя, родставляя полученные значения
                curs = connection.cursor()
                curs.execute(
                    'INSERT INTO users (lastname, firstname, patronymic, login, password, role_user) VALUES(%s,%s,%s,%s,%s, 2)',
                    (lastname, firstname, patronymic, login, str(hash_pass))
                )
                connection.commit()  # подтверждаем запись в б/д
                messagebox.showinfo('Success', 'Вы успешно зарегистрировались!')  # выводим сообщение об успешной записи

                # после успешного создания пользователя уничтажаем фрейм регистрации и вызываем метод создания фрейма магазина
                self.master.delete_all_frame()
                self.master.create_frame_magazine()

            # если не выполнен хотя бы один из этапов валидации выводим сообщение об ошибке валидации
            else:
                messagebox.showwarning("Ошибка валидации\n",
                                       'Внимание! Ошибка валидации, регистрация невозможна. Проверте коррекность введенных данных')


# создаем дочерний класс MagazineFrame, который наследует базовый класс tk.Frame
class MagazineFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self['background'] = self.master['background']
        self.create_widgets()  # вызываем метод создания виджетов
        self.create_table_widget()  # вызываем метод создания таблицы

    # метод создания виджетов
    def create_widgets(self):
        '''Блок создания картинки'''
        self.image = PhotoImage(file='img/phone.png')
        self.image_label = tk.Label(self, image=self.image, bg='white')
        self.image_label.grid(row=0, column=0, sticky='s', padx=5, pady=5, rowspan=4)

        '''Блок создания лейблов'''
        self.intro_lbl = tk.Label(self, text='Магазин телефонов', fg='#57a1f8', bg='white', font=self.master.hel_23)
        self.info_lbl = tk.Label(self,
                                 text=f'Добро пожаловать, {self.master.curret_user}\nдля покупки телефона выберите\nпонравившуюся модель из списка',
                                 fg='black', bg='white', justify=LEFT, font=self.master.hel_12)
        # если пользователь был переадресован на страницу магазиина из формы регистрации, получим логин из переменной self.master.login_user
        if self.master.curret_user is None:
            self.info_lbl.config(
                text=f'Добро пожаловать, {self.master.login_user}\nдля покупки телефона выберите\nпонравившуюся модель из списка')

        self.intro_lbl.grid(row=1, column=1, sticky='n', padx=5, pady=5)
        self.info_lbl.grid(row=2, column=1, sticky='n', padx=5, pady=5)

        '''Блок создания кнопки'''
        self.btn_buy = tk.Button(self, width=39, pady=7, text='Купить', bg='#57a1f8',
                                 activebackground='white', fg='white', border=0, command=self.select_item)
        self.btn_buy.grid(row=3, column=1, padx=5, pady=5, sticky='n')

    # метод создания таблицы
    def create_table_widget(self):
        # получаем все записи из таблицы PHONE
        curs = connection.cursor()
        Q_selectPhone = '''SELECT model, processor, memory, ram FROM phone '''

        curs.execute(Q_selectPhone)
        lst_phone = curs.fetchall()

        self.table = ttk.Treeview(self, show='headings')  # создаем таблицу, показывать будет только заголовки
        heads = ['Модель телефона', 'Процессор', 'Объем встроенной памяти в Гб',
                 'Объем оперативной памяти в Гб']  # определяем имена заголовков
        self.table['columns'] = heads  # присваиваем именам колонок в таблице, наши заголовки

        # задаем цвета в зависимости от тегов
        self.table.tag_configure('oddrow', background='white')
        self.table.tag_configure('evenrow', background='#ABDEF4')

        # устанавливаем позиционирование заголовков и выводимых записей
        for header in heads:
            self.table.heading(header, text=header, anchor='center')
            self.table.column(header, anchor='center')

        # циклом ложим в таблицу данные из нашего селекта, при помощи счетчика определяем чередование цвета в записях
        count = 0
        for row in lst_phone:
            if count % 2 == 0:
                self.table.insert('', tk.END, values=row, tags=('evenrow',))
            else:
                self.table.insert('', tk.END, values=row, tags=('oddrow',))
            count += 1

        # упаковываем таблицу и добавляем скроллинг
        self.scroll_pane = ttk.Scrollbar(self, command=self.table.yview)
        self.table.configure(yscrollcommand=self.scroll_pane.set)  # связываем скроллинг и таблицу
        self.scroll_pane.grid(row=21, column=1, sticky='nse', padx=5, pady=5)
        self.table.grid(row=21, column=0, sticky='n', padx=5, pady=5, columnspan=2)

    def select_item(self):
        # прописываем исключение, на случай если пользователь нажмет кнопку купить, не выбрав телефон
        try:
            # получаем данные записи в таблице на которой установлен фокус
            item = self.table.focus()
            string = self.table.item(item, 'values')
            # выводим сообщение о покупке телефона при помощи форматированной строки
            message = f'Поздравляю! Вы только что купили телефон {string[0]} с процессором {string[1]}, объемом встроенной памяти {string[2]}Гб и оперативной памятью в {string[3]}Гб!!!'
            messagebox.showinfo('Success', message)
        except:
            messagebox.showwarning("Ошибка\n", 'Внимание! Чтобы купить телефон, вы должны выбрать его из списка')


app = App()
app.mainloop()
app.connection_close()
