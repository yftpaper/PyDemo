import xlwt
import housemsg.urls as urls


# import argparse
#
# # init
# parser = argparse.ArgumentParser()
#
# parser.add_argument('src', help='1:贝壳 2:Q房网', type=int)  # 输入参数
# parser.add_argument('-o', '--out', help='输出路径')  # 输出文件路径
#
# # 获取参数
# args = parser.parse_args()
#
# src = args.src
# out = args.out


def set_title(sh, st):
    sh.write(0, 0, '链接', st)
    sh.write(0, 1, '价格', st)
    sh.write(0, 2, '地址', st)
    sh.write(0, 3, '面积', st)
    sh.write(0, 4, '房型', st)


if __name__ == '__main__':
    house_list = urls.get_msg_l(1, 'sz', 'baoanqu', 'rco21', 800, 1000)

    # 创建工作簿
    book = xlwt.Workbook(encoding='utf-8')
    # 创建一个worksheet
    sheet_one = book.add_sheet('house')
    sheet_two = book.add_sheet('apartment')

    style = xlwt.XFStyle()  # 初始化样式
    font = xlwt.Font()  # 为样式创建字体
    font.name = 'Times New Roman'
    font.bold = True  # 黑体
    # font.underline = True  # 下划线
    # font.italic = True  # 斜体字
    style.font = font  # 设定样式
    set_title(sheet_one, style)
    sheet_one.write(0, 5, '高度', style)
    set_title(sheet_two, style)

    sheet = sheet_one
    i = 0
    for _item in house_list:
        i += 1
        j = -1
        if _item[0] == 0:
            sheet = sheet_two
            i = 0
            continue
        for _msg in _item:
            j += 1
            sheet.write(i, j, _msg)

    # 保存
    book.save('C:\\Users\\yftpa\\Desktop\\house msg.xls')
