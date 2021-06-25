import pandas as pd
import datetime
import re
import sqlite3
import app

def delete(in_campid):
    # dbの初期化
    found_campid = app.db.session.query(app.CampReserve).filter_by(campid=in_campid).all()

    # 指定したデータを削除
    for _found_campid in found_campid:
        app.db.session.delete(_found_campid)
    app.db.session.commit()

def insert(in_campid,in_list,in_year,in_month):

    _campid = in_campid
    _Facilityname = in_list[1]
    _year = in_year
    _month = in_month
    _day1 = in_list[2]
    _day2 = in_list[3]
    _day3 = in_list[4]
    _day4 = in_list[5]
    _day5 = in_list[6]
    _day6 = in_list[7]
    _day7 = in_list[8]
    _day8 = in_list[9]
    _day9 = in_list[10]
    _day10 = in_list[11]
    _day11 = in_list[12]
    _day12 = in_list[13]
    _day13 = in_list[14]
    _day14 = in_list[15]
    _day15 = in_list[16]
    _day16 = in_list[17]
    _day17 = in_list[18]
    _day18 = in_list[19]
    _day19 = in_list[20]
    _day20 = in_list[21]
    _day21 = in_list[22]
    _day22 = in_list[23]
    _day23 = in_list[24]
    _day24 = in_list[25]
    _day25 = in_list[26]
    _day26 = in_list[27]
    _day27 = in_list[28]
    _day28 = in_list[29]
    _day29 = in_list[30]
    _day30 = in_list[31]
    _day31 = in_list[32]

    new_campres = app.CampReserve(campid=_campid,Facilityname = _Facilityname, year = _year, month =_month, \
        day1 = _day1,day2 = _day2,day3 = _day3,day4 = _day4,day5 = _day5,day6 = _day6,day7 = _day7, \
        day8 = _day8,day9 = _day9,day10 = _day10,day11 = _day11,day12 = _day12,day13 = _day13,day14 = _day14, \
        day15 = _day15,day16 = _day16,day17 = _day17,day18 = _day18,day19 = _day19,day20 = _day20,day21 = _day21, \
        day22 = _day22,day23 = _day23,day24 = _day24,day25 = _day25,day26 = _day26,day27 = _day27,day28 = _day28, \
        day29 = _day29,day30 = _day30,day31 = _day31)
    app.db.session.add(new_campres)


# てんこもりの予約状況を取得し、DBに書き込み
def reserve_tenkomori():
    _url = 'http://www.tenkomori.info/yoyakujyoukyoumeyasu.html'
    dfs = pd.read_html(_url)
    # 現在年取得
    dt_now = datetime.datetime.now()
    year_=str(dt_now.year) +"年"
    # すべての月分ループ処理
    i=0
    for dfs_ in dfs[0:7]:
        i = i+1
        
        #　何月分の予約かを取得
        str_ = dfs_.iat[0, 0]
        month = str(re.findall('況(.*) ',str_))
        month = month[2:-2] 
        y_m = str(year_)+month

        # 不要な行を削除
        dfs_=dfs_.drop(index=dfs_.index[[0]])
        dfs_=dfs_.drop(index=dfs_.index[[0]])
        dfs_=dfs_.drop(index=dfs_.index[[5]])
        
        # NaNをーに変換
        dfs_=dfs_.fillna("－")
        
        # 行Key2～6を別データフレームワークへ代入
        dfs_1 = dfs_.iloc[[0,1,2,3,4]]
        
        # 行Key8～12を別データフレームワークへ代入
        dfs_2 = dfs_.iloc[[5,6,7,8,9]]
        
        # dfs_1とdfs_2のインデックスを合わせる
        dfs_1.index=['1', '2', '3', '4', '5']
        dfs_2.index=['1', '2', '3', '4', '5']
        
        # dfs_2の施設名列を削除する
        dfs_2=dfs_2.drop(0, axis=1)
        
        # dfs_1とdfs_2を横結合
        dfs_k =pd.concat([dfs_1, dfs_2], axis=1)
        
        # columnsを整える
        dfs_k.columns = [ y_m , 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32]
                            
        # 32行目を削除
        dfs_k=dfs_k.drop(32, axis=1)

        # 年月を取得
        nengetu = dfs_k.columns[0]
        nen = nengetu[0:4]
        getu = re.findall('年(.*)月', nengetu)

        # campid set
        set_campid = 18
        # DBに書き込みする処理を追加
        for row in dfs_k.itertuples():
            insert(set_campid,row,nen,getu[0])
        

# 吉峰の予約状況を取得し、DBに書き込み
def reserve_yoshimine():
    _url = 'https://www.yoshimine.or.jp/usr-cgi/yoyaku/user.cgi'
    dfs = pd.read_html(_url,header=0)
    # すべての月分ループ処理
    for dfs_ in dfs[2:8]:
        # 1行目のずれを修正
        _dfs1=dfs_[0:1].shift(-1, axis=1)
        #print(_dfs1)
        #元の1行目を削除
        dfs_=dfs_.drop(index=dfs_.index[[0]])
        #print(dfs_)
        # ずれを修正したデータを再挿入
        dfs_=dfs_.append(_dfs1)
        # 挿入後のデータを並び替え
        dfs_=dfs_.sort_index()
        # NaNの値を-に変換
        dfs_=dfs_.fillna('－')
        # DBに書き込みする処理を追加
        # 年月を取得
        nengetu = dfs_.columns[0]
        nen = nengetu[-4:]
        getu = re.findall('(.*)月', nengetu)
        # campid set
        set_campid = 13
        # DBに書き込みする処理を追加
        for row in dfs_.itertuples():
            insert(set_campid,row,nen,getu[0])

# 牛だけの予約状況を取得し、DBに書き込み
def reserve_ushidake():
    _url = 'https://ushidake.com/cgi-bin/yoyaku005/user.cgi'
    dfs = pd.read_html(_url,header=0)
    # すべての月分ループ処理
 # すべての月分ループ処理
    i = 0
    for i in range(2,7,2):
        dfs_=dfs[i]
        #1行目の情報は不要なため削除
        dfs_=dfs_.drop(index=dfs_.index[[0]])
        # NaNの値を-に変換
        dfs_=dfs_.fillna('－')
        # DBに書き込みする処理を追加
        # DBに書き込みする処理を追加
        # 年月を取得
        nengetu = dfs_.columns[0]
        nen = nengetu[0:4]
        getu = re.findall('年(.*)月', nengetu)
        # campid set
        set_campid = 20
        # DBに書き込みする処理を追加
        for row in dfs_.itertuples():
            insert(set_campid,row,nen,getu[0])


# 立山家族旅行村の予約状況を取得し、DBに書き込み
def reserve_tateyama():
    # 現在年月取得
    dt_now = datetime.datetime.now()
    _year=str(dt_now.year)
    # 月はループしたときに考えてにとって来る必要あり！
    for k in range(0,6):

        _month =str(dt_now.month + k)

        ym = _year+'/'+_month
        ym_col = _year+'年'+_month +'月'
        
        # すべての月分ループ処理
        # 月数分(2か月分)ループ

        # 施設名分ループ
        for i in range(1,5):
            _url = 'https://kazokumura.easy489.com/front/calendars/'+ym+'/'+str(i)
            dfs = pd.read_html(_url)
            # dfs[1]
            # 行をすべて結合し、1行ですべての日程を表示
            dfs_1 = dfs[1].iloc[[0]]
            dfs_1.index=['1']
            dfs_2 = dfs[1].iloc[[1]]
            dfs_2.index=['1']
            dfs_3 = dfs[1].iloc[[2]]
            dfs_3.index=['1']
            dfs_4 = dfs[1].iloc[[3]]
            dfs_4.index=['1']
            dfs_5 = dfs[1].iloc[[4]]
            dfs_5.index=['1']
            dfs_k =pd.concat([dfs_1,dfs_2,dfs_3,dfs_4,dfs_5], axis=1)

            # NaNの値を-に変換
            dfs_k=dfs_k.fillna('－')
            _len = len(dfs_k.columns)
            _len = _len + 1

            # 列名を日付に変更
            dfs_k.columns=list(range(1,_len))
            # 値の中の数字項目を削除
            dfs_k = dfs_k.replace(['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'], '',regex=True)

            # 列の一番左に施設名をセット
            if i == 1:
                dfs_k.insert(0, ym_col , 'エコノミーキャンプ')
            elif i == 2:
                dfs_k.insert(0, ym_col , 'オートキャンプ')
            elif i == 3:
                dfs_k.insert(0, ym_col , '8人用ケビン')
            elif i == 4:
                dfs_k.insert(0, ym_col , '4人用ケビン')



            # DBにインサート
            # 年月を取得
            nengetu = dfs_k.columns[0]
            nen = nengetu[0:4]
            getu = re.findall('年(.*)月', nengetu)
            # campid set
            set_campid = 14
            # DBに書き込みする処理を追加
            for row in dfs_k.itertuples():
                insert(set_campid,row,nen,getu[0])

if __name__ == '__main__':
    try:
        delete(18)
        reserve_tenkomori()
        delete(13)
        reserve_yoshimine()
        delete(20)
        reserve_ushidake()
        delete(14)
        # reserve_tateyama()
        app.db.session.commit()
    except:
        app.db.session.rollback()
        print('err')
        raise
    finally:
        app.db.session.close()