#线上线下
#药品的线上销售的这样一个过程
#实现一个进》》存储到仓库
#销》》》销售
#存》》》商品的实时状态
#商品进销存系统
#1.写一个药品进货记录(字典)有药品编号.药品名称.药品的分类.药品单价.进货时间.进货人属性
#2.写一个药品的销售销售字典，有药品编号，药品名称.药品的分类.药品单价.药品总价.销售时间.销售人属性
#3.写一个药品库存放记录字典，有药品编号，药品名称.药品的分类.药品单价.入库时间.库存管理人属性
#4.写一个用户身份的字典，区分用户权限
#操作
#1.登录药品进销存模块
#2.药品购入(对进货记录，库存记录进行添加)
#3.销售药品(对销售记录，库存记录进行添加和自改)
#4.药品入库(对库存记录进行添加和修改)
#5.药品统计
# 通过输入药品名称，得到下列内容：
# 药品名称，药品购入数量，购入人，药品销售数量，销售人，药品的库存数量，保管人
# 统计所有库存药品的销售情况(按照销售数量，进行倒序)
#药品名称，药品销售数量，药品总价，药品的销售比例
#菜单管理界面：用于不同管理的程序入口
import os
user = {
    'admin':[
        {
            'uname':'admin',
            'upasswd':'123456'
        },
        {
            'uname':'solder',
            'upasswd':'123456'
        },
        {
            'uname':'buyer',
            'upasswd':'123456'
        }
    ]
}
def menu():
    print('****************************')
    print('*1.登录药品采购平台        *')
    print('*2.采购药品                *')
    print('*3.药品入库                *')
    print('*4.药品销售                *')
    print('*5.药品统计                *')
    print('*6.退出                    *')
    print('****************************')
#判断用户身份验证用户名密码
#返回状态True
def check_access(uname,upasswd):
    flag = False
    for item in user['admin']:
        if uname == item['uname']:
            flag = (upasswd == item['upasswd'])
            break
        else:
            flag = False
    return flag
#function:采购商品记录
#parameter：
#return：none
#description：将采购的商品进行序列化，并将结果保存到采购字典中
buy_dict = {}
def buy_record(buy_time,**kw):
    buy_dict[buy_time] = kw
#function:入库商品记录
#parameter：
#return：none
#description：将采购的商品进行入库，并将结果保存到库存字典中,如果当前库存里面有记录？
stock_dict = {}
def stock_record(buy_time,stocker,stock_time):
    if buy_time in buy_dict.keys():
        kw = buy_dict[buy_time].copy()
        #入库记录是以药品编号作为记录
        m_id = kw.pop('mid')
        kw['stocker'] = stocker
        kw['stockertime'] = stock_time
        stock_dict[m_id] = kw
    else:
        print('输入采购时间有误！！！')
def all_m_id():
    if len(stock_dict.keys()) > 0:
        for key in stock_dict.keys():
            item = stock_dict[key]
            print('%s:%s:%s'%(key,item['mname'],item['mnumber']))
    else:
        print('仓库的库存为0，请先录入商品')
sale_dict = {}
def sale_record(**kw):
    kw_dict = kw
    if kw_dict['m_id'] in stock_dict.keys():
        item_dict = {}
        item_dict['m_id'] = kw_dict['m_id']
        item_dict['mname'] = stock_dict[kw_dict['m_id']]['mname']
        item_dict['number'] = kw_dict['number']
        item_dict['buyer'] = kw_dict['buyer']
        if kw_dict['sale_time'] not in sale_dict.keys():
            sale_dict[kw_dict['sale_time']] = []
        sale_dict[kw_dict['sale_time']].append(item_dict)
    else:
        print('输入商品编号不存在，重新输入')
#统计商品的个数
def count_m(mid):
    res = {
        'buy':0,
        'stock':0,
        'sale':0
    }
    #首先统计采购的数量
    for key in buy_dict.keys():
        item = buy_dict[key]
        if item['mid'] == mid:
            res['buy'] += int(item['mnumber'])
        else:
            print('输入药品编号不存在！！！')
    if mid in stock_dict.keys():
        res['stock'] = stock_dict[mid]['mnumber']
    else:
        print('输入药品编号不存在！！！')
    for key in sale_dict.keys():
        item = sale_dict[key]
        for dic in item:
            if dic['m_id'] == mid:
                res['sale'] += int(dic['number'])
            else:
                print('输入药品编号不存在！！！')
    return res
def main():
    while True:
        menu()
        index = input('请输入选择的序号')
        if index == '1':
            user_name = input('请输入用户名')
            user_passwd = input('请输入密码')
            results = check_access(user_name,user_passwd)
            if results:
                print('登录成功，请继续选择其他操作')
            else:
                print('用户名或者密码不正确，请重新输入')
        elif index == '2':
            buy_time = input('请输入采购时间，按照YYYYMMDD格式输入：')
            m_name = input('请输入药品名：')
            m_id = input('请输入药品编号:')
            m_price = input('请输入药品单价:')
            m_buyer = input('请输入药品的采购者:')
            m_type = input('请输入药品的分类:')
            m_number = input('请输入药品采购的数量:')
            buy_record(buy_time,mname=m_name,mid=m_id,mprice=m_price,mbuyer=m_buyer,mtype=m_type,mnumber=m_number)
            print(buy_dict)
        elif index == '3':
            buy_time = input('请输入采购时间，按照YYYYMMDD格式输入：')
            stocker = input('请输入库管理员：')
            stocker_time = input('请输入入库时间，按照YYYYMMDD格式输入：')
            stock_record(buy_time,stocker,stocker_time)
            print(stock_dict)
        elif index == '4':
            #销售是按照某一天中销售商品的记录
            sale_time = input('请输入销售日期，按照YYYYMMDD格式输入：')
            all_m_id()
            #如何获取当前日期下的仓库目录下所有的药品编号
            m_id = input('请输入药品编号：')
            buyer = input('请输入购买者：')#谁买的
            number = input('请输入销售商品的数量：')
            sale_record(sale_time=sale_time,m_id=m_id,buyer=buyer,number=number)
            if m_id in stock_dict.keys():
                res = int(stock_dict[m_id]['mnumber'])-int(number)
                if res < 0:
                    print('当前库存不足，请重新购买')
                else:
                    stock_dict[m_id]['mnumber'] = str(res)
                    sale_record(sale_time=sale_time,m_id=m_id,buyer=buyer,number=number)
                    print(sale_dict)
            else:
                print('商品编号有误！！！')
        elif index == '5':
            print('当前库存药品：')
            for key in stock_dict.keys():
                print('%s:%s'%(key,stock_dict[key]['mname']))
            m_id = input('请输入药品编号')
            #采购数量 库存数量 销售数量
            print(count_m(m_id))
        elif index == '6':
            string = input('输入Q或q退出程序')
            if string == 'Q' or string =='q':
                os._exit(0)
            else:
                print('输入错误，请重新输入')
        else:
            print('输入序号错误，请重新输入')
if __name__ == '__main__':
    main()



























































































































