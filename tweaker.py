import customtkinter as ctk
from tkinter import messagebox, colorchooser, font
import winreg
import os
import webbrowser  # Импортируем библиотеку для открытия URL

def center_window(root, width=300, height=150):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    root.geometry(f'{width}x{height}+{x}+{y}')

def set_default_color():
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Control Panel\Colors",
            0, winreg.KEY_SET_VALUE
        )
        winreg.SetValueEx(key, "Hilight", 0, winreg.REG_SZ, '0 120 215')
        winreg.SetValueEx(key, "HotTrackingColor", 0 , winreg.REG_SZ, '0 102 204')
        winreg.CloseKey(key)
        answer = messagebox.askquestion('Успех', 'Изменения вступят в силу после перезагрузки. Выполнить перезагрузку сейчас?')
        if answer == 'yes':
            os.system('shutdown /r -t 0')
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось изменить настройки: {e}")

def choose_color():
    color_code = colorchooser.askcolor(title='Выберите цвет')
    if color_code[0]:
        rgb = ' '.join((str(color_code[0][0]), str(color_code[0][1]), str(color_code[0][2])))
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Control Panel\Colors",
                0, winreg.KEY_SET_VALUE
            )
            winreg.SetValueEx(key, "Hilight", 0, winreg.REG_SZ, rgb)
            winreg.SetValueEx(key, "HotTrackingColor", 0, winreg.REG_SZ, rgb)
            winreg.CloseKey(key)
            answer = messagebox.askquestion('Успех','Изменения вступят в силу после перезагрузки. Выполнить перезагрузку сейчас?')
            if answer == 'yes':
                os.system('shutdown /r -t 0')
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось изменить настройки: {e}")

def show_hide_seconds():
    status = tw1_switch_var.get()
    def f(msg, value):
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
                0, winreg.KEY_SET_VALUE
            )
            winreg.SetValueEx(key, "ShowSecondsInSystemClock", 0, winreg.REG_DWORD, value)
            winreg.CloseKey(key)
            messagebox.showinfo("Успех", f"Секунды будут {msg} после перезагрузки проводника.")
            os.system("taskkill /f /im explorer.exe && start explorer.exe")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось изменить настройки: {e}")
    if status == 'on':
        tw1_switch.configure(text='Включено')
        f('показаны', 1)
    elif status == 'off':
        tw1_switch.configure(text='Выключено')
        f('убраны', 0)

def show_old_uvc():
    status = tw2_var.get()
    def f(value, err_value, err_text):
        try:
            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\MTCUVC",
                0, winreg.KEY_SET_VALUE
            )
            winreg.SetValueEx(key, "EnableMtcUvc", 0, winreg.REG_DWORD, value)
            winreg.CloseKey(key)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось изменить настройки: {e}")
            tw2_switch.configure(text=err_text)
            tw2_var.set(err_value)
    if status == 'on':
        tw2_switch.configure(text='Включено')
        f(0, 'off', 'Выключено')
    elif status == 'off':
        tw2_switch.configure(text='Выключено')
        f(1, 'on', 'Включено')

root = ctk.CTk()
root.title('WinTweaks')
center_window(root, 500, 250)
root.resizable(width=False, height=False)

def read_tw1_value(hkey, sub_key, value_name):
    try:
        # Открыть ключ реестра
        with winreg.OpenKey(hkey, sub_key, 0, winreg.KEY_READ) as key:
            # Прочитать значение параметра
            value, regtype = winreg.QueryValueEx(key, value_name)
            return value
    except FileNotFoundError:
        return "off"
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка при чтении реестра: {e}")

# Путь и имя параметра
sub_key = r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced"
value_name = "ShowSecondsInSystemClock"

# Чтение значения параметра
value = read_tw1_value(winreg.HKEY_CURRENT_USER, sub_key, value_name)
if value is not None:
    tw1_switch_var = ctk.StringVar(value="on" if value == 1 else "off")
else:
    tw1_switch_var = ctk.StringVar(value="off")

def create_registry_key(hkey, sub_key):
    try:
        # Создание (или открытие, если уже существует) ключа реестра
        with winreg.CreateKey(hkey, sub_key) as key:
            print(f"Ключ '{sub_key}' успешно создан или открыт.")
    except Exception as e:
        print(f"Ошибка при создании ключа: {e}")

# Основной путь и имя искомого ключа
base_key = winreg.HKEY_LOCAL_MACHINE
base_sub_key = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion"
target_key = "MTCUVC"
value_name1 = "EnableMtcUvc"

# Полный путь к искомому ключу
full_key_path = f"{base_sub_key}\\{target_key}"

# Попытка открыть ключ, если не существует - создаем его
try:
    with winreg.OpenKey(base_key, full_key_path, 0, winreg.KEY_READ):
        print(f"Ключ '{full_key_path}' уже существует.")
except FileNotFoundError:
    print(f"Ключ '{full_key_path}' не найден. Создание ключа.")
    create_registry_key(base_key, full_key_path)

def read_tw2_value(hkey, sub_key, value_name):
    try:
        # Открыть ключ реестра
        with winreg.OpenKey(hkey, sub_key, 0, winreg.KEY_READ) as key:
            # Прочитать значение параметра
            value, regtype = winreg.QueryValueEx(key, value_name)
            return value
    except FileNotFoundError:
        return "off"
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка при чтении реестра: {e}")

# Чтение значения параметра
base_sub_key = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\MTCUVC"
value1 = read_tw2_value(winreg.HKEY_LOCAL_MACHINE, base_sub_key, value_name1)
if value1 is not None:
    tw2_var = ctk.StringVar(value="on" if value1 == 0 else "off")
else:
    tw2_var = ctk.StringVar(value="off")

for c in range(3): root.columnconfigure(index=c, weight=1)
for r in range(6): root.rowconfigure(index=r, weight=1)

tweak1 = ctk.CTkLabel(
    root,
    text='Отобразить секунды на панели задач?'
)
tweak1.grid(row=0, column=0)

tweak2 = ctk.CTkLabel(
    root,
    text='Отобразить старый микшер Windows 7/8.1?'
)
tweak2.grid(row=1, column=0)

tweak3 = ctk.CTkLabel(
    root,
    text='Изменить цвет выделения Windows'
)
tweak3.grid(row=2, column=0, columnspan=3)

tw1_switch = ctk.CTkSwitch(
    root,
    text='Выключено',
    command=show_hide_seconds,
    onvalue='on',
    offvalue='off',
    variable=tw1_switch_var
)
if value is not None:
    tw1_switch.configure(text='Включено' if value == 1 else 'Выключено')
else:
    tw1_switch.configure(text='Выключено')
tw1_switch.grid(row=0, column=1)

tw2_switch = ctk.CTkSwitch(
    root,
    text='undefined',
    onvalue='on',
    offvalue='off',
    variable=tw2_var,
    command=show_old_uvc
)
if value1 is not None:
    tw2_switch.configure(text='Включено' if value1 == 0 else 'Выключено')
else:
    tw2_switch.configure(text='Выключено')
tw2_switch.grid(row=1, column=1)

# Создание Frame для кнопок изменения цвета выделения
btns_frame = ctk.CTkFrame(root)
btns_frame.grid(row=3, column=0, columnspan=3)

tw3_default = ctk.CTkButton(
    btns_frame,
    text='По умолчанию',
    command=set_default_color  # Замените на нужную функцию
)
tw3_default.grid(row=0, column=0, padx=10, pady=10)

tw3_choose = ctk.CTkButton(
    btns_frame,
    text='Выбрать цвет',
    command=choose_color
)
tw3_choose.grid(row=0, column=1, padx=10, pady=10)

def open_url(event):
    webbrowser.open_new("https://github.com/stageer1/WinTweaks")  # Замените на нужный URL

author = ctk.CTkLabel(
    root,
    text='stageer1',
    text_color='grey'
)
author.place(x=2, y=227)

github_label = ctk.CTkLabel(
    root,
    text='Исходный код (GitHub)',
    text_color='lightblue',
    cursor="hand2"  # Указатель мыши в виде руки при наведении
)
github_label.place(x=360, y=227)  # Расположим метку в правом нижнем углу
github_label.bind("<Button-1>", open_url)  # Привязка события клика к функции открытия URL

root.mainloop()
