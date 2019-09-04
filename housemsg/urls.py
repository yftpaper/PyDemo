from bs4 import BeautifulSoup as bs
import requests
import time

# 伪装Header
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
    'Connection': 'keep - alive'
}

# 贝壳找房
bk_url = 'https://{s}.zu.ke.com/zufang/{q}/pg{p}{r}brp{m1}erp{m2}/#contentList'  # https://sz.zu.ke.com/zufang/baoanqu/pg1brp1000erp2000/#contentList
bk_url_h = 'https://{s}.zu.ke.com'

# Q房网
q_url = 'https://{s}.qfang.com/rent/{q}/pfy{m1}-pty{m2}-f{p}'  # https://shenzhen.qfang.com/rent/baoan/pfy1000-pty3000-f1
q_url_h = 'https://{s}.qfang.com'


def _get_url(t):
    if t == 1:
        return bk_url
    elif t == 2:
        return q_url
    return bk_url


def _get_url_h(t):
    if t == 1:
        return bk_url_h
    elif t == 2:
        return q_url_h
    return bk_url_h


def get_msg_l(t, s, q, r, m1, m2):
    # 房子型
    house_list = []
    # 公寓型
    apartment_list = []
    p = 0
    url = _get_url(t)
    url_h = _get_url_h(t)
    while True:
        p += 1
        print("fetch: ", url.format(s=s, q=q, p=p, r=r, m1=m1, m2=m2))
        time.sleep(2)
        response = requests.get(url.format(s=s, q=q, p=p, r=r, m1=m1, m2=m2), header)
        html = bs(response.text, features="lxml")
        house_msg_l = html.select('.content__list--item')

        # 房源信息没有时退出
        if html.select('.content__empty1'):
            break

        for house in house_msg_l:
            # 处理完成临时存储
            _list = []
            # 链接
            _h_url = url_h.format(s=s) + house.select('.content__list--item--title > a')[0]['href']
            _list.append(_h_url)
            # 未处理信息集
            _h_msg = house.select('.content__list--item--des')[0].get_text()
            # 简单处理
            _h_msg = _h_msg.replace('\n', '').replace(' ', '')
            _h_msg_l = _h_msg.split('/')

            # 价格
            _h_price = house.select('.content__list--item-price')[0].get_text()
            _list.append(_h_price)

            if not house.select('.content__list--item--des > a'):  # 没有地址 情况标题中含有
                # 地址
                _h_address_l = house.select('.content__list--item--title > a')[0].string.split()
                # 地址
                _list.append(' '.join(_h_address_l[:2]))
                # 面积
                if _h_msg_l[0].find('㎡') > 0:
                    _list.append(_h_msg_l[0])
                else:
                    _list.append(_h_msg_l[1])
                # 房型
                _list.append(_h_msg_l[-1])
                # 整合
                apartment_list.append(_list)
            else:  # 存在地址直接获取
                # 地址
                _list.append(_h_msg_l[0].replace('-', ' '))
                # 面积
                _list.append(_h_msg_l[1])
                # 房型
                _list.append(_h_msg_l[-2])
                # 高度
                _list.append(_h_msg_l[-1])
                # 整合
                house_list.append(_list)

    house_list.append([0])
    return house_list + apartment_list
