import sys
import xlrd

from MSSQL import MSSQL

msClient = MSSQL("", "", "", "")


# 连接数据库
# 读取数据库信息
def set_db_config():
    # print("请输入数据库地址：", end="")
    # db_host = input()
    # # print("请输入数据库端口：")
    # # db_port = input()
    # print("请输入数据库用户名：", end="")
    # db_user = input()
    # print("请输入数据库密码：", end="")
    # db_pwd = input()
    # print("请输入数据库名称：", end="")
    # db_name = input()
    db_host = "10.252.7.43"
    db_name = "IAMS"
    db_user = "sa"
    db_pwd = "Aa111111"
    print("正在初始化数据库连接：%s:%s:%s" % (db_host, 1433, db_name))
    global msClient
    msClient = MSSQL(db_host, db_user, db_pwd, db_name)
    try:
        msClient.GetConnect()
        print("数据库连接成功")
        # noinspection SqlResolve
        sql = "select count(name) as co from sysobjects where name = 'ds_dmall_store_data'"
        table_num = (msClient.ExecQuery(sql))[0][0]
        if table_num != 1:
            print("未检测到表，开始创建")
            # sql文件里写建表语句
            sql_file_content = readSqlFile("commodity_wholesale_price.sql")
            msClient.ExecSql(sql_file_content)
            table_num = (msClient.ExecQuery(sql))[0][0]
            if table_num == 1:
                print("创建数据表成功")
        else:
            print("检测到数据表")
    except:
        print("数据库创建表失败")
        sys.exit()


# 读取sql文件
def readSqlFile(file_name):
    sql_file = open(file_name, 'r', encoding='utf8')
    sql_file_content = sql_file.readlines()
    sql_file.close()
    return "".join(sql_file_content)


def open_excel():
    try:
        # 文件名，把文件与py文件放在同一目录下
        book = xlrd.open_workbook("ds_uf_price_gr_202101.xls")
        sheet_object = book.sheet_by_name("price")
        print("读取到数据%d行" % sheet_object.nrows)
        return sheet_object
    except:
        print("excel打开失败！")
        sys.exit()


# 构造插入语句
def build_batch_insert_sql(excel_data):
    sql = "insert into ds_uf_price_gr(store_id,demand_field_domain_id,pcg_main_cat_id,pcg_cat_id,mikg_art_no,art_name,suppl_no,suppl_type,suppl_address_name,suppl_street,GR_date,RECPT_QTY_COLLI,RECPT_VAL_NNBP,GR_price) values"
    return sql + ','.join(excel_data)


# 插入数据库
def insert_data(_sheet):
    row_num = _sheet.nrows
    if row_num == 0:
        print("工作簿中未读取到数据")
        sys.exit()
    excel_data = []
    # 第一行是标题名，对应表中的字段名所以应该从第二行开始，计算机以0开始计数，所以值是1
    for i in range(1, row_num):
        # 每个字段赋值，需要与插入字段类型一一对应
        excel_data.append("('%s','%s','%s','%s','%s',N'%s','%s','%s',N'%s',N'%s','%s','%s','%s','%s')" % (
            _sheet.cell(i, 0).value, _sheet.cell(i, 1).value, _sheet.cell(i, 2).value, _sheet.cell(i, 3).value,
            _sheet.cell(i, 4).value, _sheet.cell(i, 5).value, _sheet.cell(i, 6).value, _sheet.cell(i, 7).value,
            _sheet.cell(i, 8).value, _sheet.cell(i, 9).value, _sheet.cell(i, 10).value, _sheet.cell(i, 11).value,
            _sheet.cell(i, 12).value, _sheet.cell(i, 13).value))
        # 每1000条插入一次
        if i % 1000 == 0:
            # 构造sql语句
            sql = build_batch_insert_sql(excel_data)
            msClient.ExecSql(sql)
            print("第%d次插入,成功插入%d条" % (i / 1000, len(excel_data)))
            excel_data = []
    # 插入剩余的最后一次
    if len(excel_data) > 0:
        sql = build_batch_insert_sql(excel_data)
        msClient.ExecSql(sql)
        print("第%d次插入,成功插入%d条" % ((row_num / 1000) + 1, len(excel_data)))


if __name__ == "__main__":
    set_db_config()
    sheet = open_excel()
    insert_data(sheet)
