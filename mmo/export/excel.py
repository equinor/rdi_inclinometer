import tempfile
import xlsxwriter

DATE_FORMAT = "yyyy-mm-dd hh:mm:ss"


def export(rows):
    """
    Exports a series of OrderedDicts to a table in a new Excel spreadsheet

    :param rows: List of OrderedDict
    :type rows: list
    :return: Temporary xlsx file name
    """

    filename = tempfile.mktemp(".xlsx")

    workbook = xlsxwriter.Workbook(filename)

    date_time_format = workbook.add_format()
    date_time_format.set_num_format(DATE_FORMAT)

    worksheet = workbook.add_worksheet()
    worksheet.freeze_panes(1, 0)

    keys = rows[0].keys()

    num_cols = len(keys)
    num_rows = 1 + len(rows)

    # Find formats for the headers. Names containing "Time" will get
    # time format + extra width
    columns = []
    for column_index, key in enumerate(keys):
        column = {'header': key}
        if key.find("time") != -1:
            column["format"] = date_time_format
            worksheet.set_column(column_index, column_index, width=20)
        columns.append(column)

    data = []
    for row in rows:
        data.append([row[key] for key in keys])

    worksheet.add_table(0, 0, num_rows - 1, num_cols - 1,
                        {'columns': columns, 'data': data})

    workbook.close()

    return filename