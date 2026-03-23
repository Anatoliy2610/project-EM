from texttable import Texttable
from datetime import date
import calendar


def get_data_hours(data):
    new_data = {}
    for data in data:
        if int(str(data.get('date'))[-8:-6]) in new_data:
            new_data[int(str(data.get('date'))[-8:-6])].append(data.get("name"))
        else:
            new_data[int(str(data.get('date'))[-8:-6])] = [data.get("name")]
    return new_data


def get_table_day(list_value):
    data = get_data_hours(list_value)
    table = Texttable()
    table.set_cols_align(["c", "c"])
    table.set_cols_valign(["m", "m"])
    res_rows = [["Hours", "Name event день"]]
    for hours in range(25):
        if data.get(hours):
            row = [f'{hours}:00', '\n'.join(data.get(hours))]
            res_rows.append(row)
        else:
            row = [f'{hours}:00', 'пусто']
            res_rows.append(row)


    table.add_rows(res_rows)
    return table.draw()

 
def get_data_month(data):
    new_data = {}
    for data in data:
        if int(str(data.get('date'))[8:10]) in new_data:
            new_data[int(str(data.get('date'))[8:10])].append(data.get("name"))
        else:
            new_data[int(str(data.get('date'))[8:10])] = [data.get("name")]
    return new_data

def get_table_month(list_value):
    data = get_data_month(list_value)
    table = Texttable()
    table.set_cols_align(["c", "c"])
    table.set_cols_valign(["m", "m"])
    res_rows = [["Date", "Name event день"]]
    now = date.today()
    num_days = calendar.monthrange(now.year, now.month)
    for day in range(1, num_days[1] + 1):
        if data.get(day):
            row = [f'{day}', '\n'.join(data.get(day))]
            res_rows.append(row)
        else:
            row = [str(day), 'пусто']
            res_rows.append(row)
    table.add_rows(res_rows)
    return table.draw()



