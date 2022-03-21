from tkGUI import Gui
from xmlData import get_from_xml
import tkinter
from InveoReader import do_xml_from_web
from sqlData import create_db_table, put_row_into_db, clear_db_table

WITH_SQL=True

#do_xml_from_web()

input_list=get_from_xml("Wejscia")
output_list=get_from_xml("Wyjscia")
all_users=input_list + output_list

if WITH_SQL:
    try:
        clear_db_table()
    except:
        create_db_table()
    for user in all_users:
        row=(user.no, user.nr_id, user.name, user.card_id, user.state, user.time, user.io)
        put_row_into_db(row)

master=tkinter.Tk()
gui_window=Gui(master, all_users, WITH_SQL)
master.mainloop()

