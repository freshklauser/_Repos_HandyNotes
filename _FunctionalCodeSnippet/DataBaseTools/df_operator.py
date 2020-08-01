# -*- coding: utf-8 -*-
# @Author   : Administrator
# @DateTime : 2020/6/5 21:13
# @FileName : df_operator.py
# @SoftWare : PyCharm


from _Modules import pandas as pd
from numpy import nan
from _FunctionalCodeSnippet.DataBaseTools import db_handler

NA_YES_COLUMNS = ['name', 'nicky', 'birthday', 'timer']
NA_NOO_COLUMNS = ['age', 'weight', 'dt', 'dttm']
# 每个时间戳都以自从1970年1月1日午夜（历元）经过了多长时间来表示
NA_NOO_COLUMNS_MAP = {'age': 0,
                      'weight': 0,
                      'dt': '1970-01-01',
                      'dttm': '1970-01-01 00:00:00'}


def generate_df():
    """
    mysql中 id 自增，primary key
    """
    alist = [['tom', nan, 12, nan, '1989.06', '12:15:20', '1989-06-01', '1989-06-01 15:15:15'],
             ['lucy', 'mm', 22, 53, nan, nan, nan, '1989-06-01 15:15:15'],
             ['messy', 'goal', nan, 90, '1980.08', '12:15:20', '1989-06-01', nan]]
    cols = ['name', 'nicky', 'age', 'weight', 'birthday', 'timer', 'dt', 'dttm']
    dfs = pd.DataFrame(alist, columns=cols)
    return dfs


def fillna_value(data_frame, cmap=NA_NOO_COLUMNS_MAP):
    """
    根据 DataFrame 字段属性，针对性第填充空值
    """
    cols = data_frame.columns
    data_frame[NA_YES_COLUMNS] = data_frame[NA_YES_COLUMNS].fillna('')
    for col in NA_NOO_COLUMNS:
        data_frame[col] = data_frame[col].fillna(cmap[col])
    return data_frame


def change_col_type(data_frame, column, new_type=None):
    """
    DataFrame转换类型注意事项：
        (1) 类型转换前，必须先对空值进行处理
    """
    # Method-1:  data_frame[column] = data_frame[column].astype(new_type)
    # Method-2:  data_frame[column] = pd.to_numeric(data_frame[column])
    data_frame[column] = data_frame[column].astype(new_type)
    return data_frame


def change_col_to_dt(data_frame, column, format_type='date'):
    """
    date: "%Y-%m-%d"
    datetime: "%Y-%m-%d %H:%M:%S"
    """
    # org_type = data_frame[column].dtypes
    # print("Column `{}`'s original type: {}".format(column, org_type))

    if format_type == 'date':
        data_frame[column] = pd.to_datetime(
            data_frame[column], format="%Y-%m-%d")
    elif format_type == 'datetime':
        data_frame[column] = pd.to_datetime(
            data_frame[column], format="%Y-%m-%d %H:%M:%S")
    else:
        raise AttributeError(
            "Incorrect attribute of {}: date or datetime.",
            format(format_type))
    # print("Column `{}`'s new type: {}".format(column, data_frame[column].dtypes))
    # print("Columns Type After Changed: ")
    # print(data_frame.dtypes)
    return data_frame


def main():
    df = generate_df()
    new_df = fillna_value(df)
    items = new_df.to_numpy().tolist()
    handler = db_handler.DatabaseHandler('mysql')
    sql = ("INSERT INTO person "
           "(`name`, `nicky`, `age`,`weight`,`birthday`,`timer`, `dt`, `dttm`) "
           "VALUES "
           "(%s,%s,%s,%s,%s,%s,%s,%s)")
    for i, args in enumerate(items):
        handler.insert(sql, args)
        print('--' * 10, "INDEX-{}".format(i), '--' * 10)


if __name__ == '__main__':
    main()
    # -------------------------------------- numeric and object --------------
    """
    df = generate_df()
    print(df.isnull().sum())
    print(df)
    print(df.dtypes)
    new_df = fillna_value(df)
    print('+++++'*5)
    print(new_df)
    print(new_df.dtypes)
    print(type(df.iloc[0, -1]), '>>>>>>>>>>>>>>>>>>>>>>>', df.iloc[0, -1])
    print('--'*10, 'MYSQL', '--'*10)
    df_2 = new_df
    # print(df_2)
    handler = db_handler.DatabaseHandler('mysql')
    df_list = df_2.to_numpy().tolist()
    sql = "INSERT INTO person (`name`, `nicky`, `age`,`weight`,`birthday`,`timer`, `dt`, `dttm`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
    # sql = "INSERT INTO person (`name`,`nicky`, `age`,`weight`) VALUES (%s, %s, %s, %s)"
    for i, item in enumerate(df_list):
        args = item
        print([k for k in args])
        handler.insert(sql, args)
        print('\n')
        print('--'*10, "INDEX-{}".format(i), '--'*10)
    """

    # -------------------------------------- numeric date datetime -----------
    """
    df = generate_df()
    print(df.isnull().sum())
    print(df)
    print(df.dtypes)
    new_df = fillna_value(df)
    print('+++++'*15)
    print(new_df)
    print(new_df.dtypes)

    # df_1 = change_col_type(df, column='', new_type=float)
    df_2 = change_col_to_dt(new_df, column='dt', format_type='date')
    df_2 = change_col_to_dt(new_df, column='dttm', format_type='datetime')
    df_2 = df_2.fillna('')
    print('-----' * 15)
    print(df_2.dtypes)

    handler = db_handler.DatabaseHandler('mysql')
    df_list = df_2.to_numpy().tolist()
    sql = "INSERT INTO person (`name`, `nicky`, `age`,`weight`,`birthday`,`timer`, `dt`, `dttm`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
    for i, item in enumerate(df_list):
        args = item
        print([k for k in args])
        handler.insert(sql, args)
        print('\n')
        print('--'*10, "INDEX-{}".format(i), '--'*10)
    """
