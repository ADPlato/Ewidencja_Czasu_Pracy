import tkinter
from tkcalendar import DateEntry
import datetime as dt
from sqlData import get_data_from_db

class Gui():
        def __init__(self, master, data, WITH_SQL):
                self.WITH_SQL=WITH_SQL
                self.window=master
                self.data=data
                self.window.title("Kontrola wyjść/wejść SKSM")
                self.window.resizable(False, False)
                self.sorted_by= {"name":False, "time":False, "io":False}
                self.set_list_widget()
                self.set_sort_buttons_widget()
                self.set_search_widget()
                self.set_time_widget()
                self.sort_data("io")

        def set_time_widget(self):
                HOURS = tuple([f'{dt.time(i).strftime("%H:%M:%S")}' for i in range(0,24)])

                self.hour_from = tkinter.ttk.Combobox(self.window, width=10)
                self.hour_from['values'] = HOURS
                self.hour_from.current(5)
                self.hour_to = tkinter.ttk.Combobox(self.window, width=10)
                self.hour_to['values'] = HOURS
                self.hour_to.current(15)
                self.cal_from = DateEntry(self.window, width=10, date_pattern="yyyy-mm-dd")
                self.cal_to = DateEntry(self.window, width=10, date_pattern="yyyy-mm-dd")
                sep = tkinter.Label(self.window, width=2, text="-")
                self.cal_from.grid(row=3, column=1, sticky="nsew")
                self.cal_to.grid(row=3, column=4, sticky="nsew")
                self.hour_from.grid(row=3, column=2, sticky="nsew")
                self.hour_to.grid(row=3, column=5, columnspan=6, sticky="nsew")
                sep.grid(row=3, column=3, sticky="nsew")

        def set_list_widget(self):
                scrollbar = tkinter.Scrollbar(self.window)
                self.lista = tkinter.Listbox(self.window, yscrollcommand=scrollbar.set, width=45, height=45)
                self.lista.grid(row=6, column=1, columnspan=9, sticky="nsew")
                scrollbar.grid(row=6, column=10, sticky="ns")
                scrollbar.config(command=self.lista.yview)

        def set_sort_buttons_widget(self):

                button_name = tkinter.Button(self.window, text="Imię i Nazwisko", width=10, pady=1, command=lambda: self.sort_data("name"))
                button_time = tkinter.Button(self.window, text="Data", width=15, pady=1, command=lambda: self.sort_data("time"))
                button_io = tkinter.Button(self.window, text="We/Wy", width=12, pady=1, command=lambda: self.sort_data("io"))

                button_time.grid(row=5, column=2, columnspan=2, sticky="nsew")
                button_name.grid(row=5, column=3, columnspan=7, sticky="nsew")
                button_io.grid(row=5, column=1, sticky="nsew")

        def set_search_widget(self):
                button_search = tkinter.Button(self.window, text="Wyszukaj", width=10, pady=10, command=lambda: self.sort_data("time"))
                button_search.grid(row=2, column=1, columnspan=10, sticky="nsew")
                self.entry = tkinter.Entry(self.window, width=10, justify='center')
                self.entry.grid(row=1, column=1, columnspan=10, sticky="nsew")

        def show_data(self, data):
            self.lista.delete(0, 'end')
            color_temp = 0
            for user in data:
                if self.WITH_SQL:
                        name=user[2] # Takie zastosowanie umożliwia odczyt zarówno z listy obiektów danej klasy jak i zwykłej listy
                        time=user[5]
                        io=user[6]
                else:
                        name=user.name
                        time=user.time
                        io=user.io

                formated_time = dt.datetime.utcfromtimestamp(int(time)).strftime('%Y-%m-%d %H:%M:%S')
                self.lista.insert(tkinter.END, "{:^20s}   {:^25s}  {:<30s}".format(str(io), str(formated_time), str(name)))
                if (io == "Wejscia"):
                    self.lista.itemconfig(color_temp, {'bg': '#B4DBBA'})
                else:
                    self.lista.itemconfig(color_temp, {'bg': '#D1737C'})
                color_temp = color_temp + 1

        def get_time_range(self):
                time_in = f'{self.cal_from.get()} {self.hour_from.get()}'
                timestamp_in = dt.datetime.timestamp(dt.datetime.strptime(time_in, "%Y-%m-%d %H:%M:%S"))
                timestamp_in = int(timestamp_in + 3600)  # --------------------- CZAS ZIMOWY

                time_out = f'{self.cal_to.get()} {self.hour_to.get()}'
                timestamp_out = dt.datetime.timestamp(dt.datetime.strptime(time_out, "%Y-%m-%d %H:%M:%S"))
                timestamp_out = int(timestamp_out + 3600)

                return (timestamp_in, timestamp_out)

        def is_in_time_range(self, timestamp):

                timestamp_in, timestamp_out = self.get_time_range()
                if timestamp_in <= int(timestamp) <= timestamp_out:
                        return True
                else:
                        return False

        def sort_data(self, sort_type=""):
                if self.WITH_SQL:
                        sorted_data=get_data_from_db(self.entry.get(), self.get_time_range(), sort_type+" DESC"*self.sorted_by[sort_type])
                        self.sorted_by[sort_type]= not self.sorted_by[sort_type]
                else:
                        sorted_data=[]
                        for user in self.data:
                                if self.entry.get().lower() in user.name.lower():
                                        if self.is_in_time_range(user.time):
                                                sorted_data.append(user)

                        if sort_type == "name":
                                sorted_data.sort(key=lambda user: user.name, reverse=self.sorted_by['name'])
                                self.sorted_by["name"]= not self.sorted_by['name']
                        if sort_type == "time":
                                sorted_data.sort(key=lambda user: user.time, reverse=self.sorted_by['time'])
                                self.sorted_by["time"]= not self.sorted_by['time']
                        if sort_type == "io":
                                sorted_data.sort(key=lambda user: user.io, reverse=self.sorted_by['io'])
                                self.sorted_by["io"]= not self.sorted_by['io']

                self.show_data(sorted_data)




