import datetime
from flask import  Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from dateutil.relativedelta import relativedelta


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///camp.db'
db = SQLAlchemy(app)

class Camplist(db.Model):
    campid = db.Column(db.Integer, primary_key=True)
    areaid = db.Column(db.Integer, primary_key=True)
    campname = db.Column(db.String(30), nullable=False)
    area = db.Column(db.String(10), nullable=False)
    postcd = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(300))
    phone = db.Column(db.String(15))
    reservmethod = db.Column(db.String(10), nullable=False)
    reservumu = db.Column(db.Integer, nullable=False)
    costumu = db.Column(db.Integer, nullable=False)
    petumu = db.Column(db.Integer, nullable=False)
    bbqumu = db.Column(db.Integer, nullable=False)
    daycapmumu = db.Column(db.Integer, nullable=False)
    direct_heat = db.Column(db.String(20))
    start_month = db.Column(db.String(10))
    end_month = db.Column(db.String(10))
    check_in = db.Column(db.String(20))
    check_out = db.Column(db.String(20))
    cancel_policy = db.Column(db.String(300))
    garbage_station_umu = db.Column(db.String(10))
    closest = db.Column(db.String(50))
    coment = db.Column(db.String(200))
    googlemap = db.Column(db.String(1000))

class Campfacility(db.Model):
    campid = db.Column(db.Integer, primary_key=True)
    facility_id = db.Column(db.Integer, primary_key=True)
    facility_name = db.Column(db.String(50), nullable=False)
    cost = db.Column(db.String(15))

class Camp_hot_spring(db.Model):
    campid = db.Column(db.Integer, primary_key=True)
    hot_spring_id = db.Column(db.Integer, primary_key=True)
    hot_spring_name = db.Column(db.String(50), nullable=False)
    distance = db.Column(db.String(15))
    hot_spring_cost = db.Column(db.String(15))

class Camp_supermarket(db.Model):
    campid = db.Column(db.Integer, primary_key=True)
    supermarket_id = db.Column(db.Integer, primary_key=True)
    supermarket_name = db.Column(db.String(50), nullable=False)
    distance = db.Column(db.String(15))

class CampReserve(db.Model):
    campid = db.Column(db.Integer, primary_key=True)
    Facilityname = db.Column(db.String(10), primary_key=True)
    year = db.Column(db.Integer, primary_key=True)
    month = db.Column(db.Integer, primary_key=True)
    day1 = db.Column(db.String(5), nullable=False)
    day2 = db.Column(db.String(5), nullable=False)
    day3 = db.Column(db.String(5), nullable=False)
    day4 = db.Column(db.String(5), nullable=False)
    day5 = db.Column(db.String(5), nullable=False)
    day6 = db.Column(db.String(5), nullable=False)
    day7 = db.Column(db.String(5), nullable=False)
    day8 = db.Column(db.String(5), nullable=False)
    day9 = db.Column(db.String(5), nullable=False)
    day10 = db.Column(db.String(5), nullable=False)
    day11 = db.Column(db.String(5), nullable=False)
    day12 = db.Column(db.String(5), nullable=False)
    day13 = db.Column(db.String(5), nullable=False)
    day14 = db.Column(db.String(5), nullable=False)
    day15 = db.Column(db.String(5), nullable=False)
    day16 = db.Column(db.String(5), nullable=False)
    day17 = db.Column(db.String(5), nullable=False)
    day18 = db.Column(db.String(5), nullable=False)
    day19 = db.Column(db.String(5), nullable=False)
    day20 = db.Column(db.String(5), nullable=False)
    day21 = db.Column(db.String(5), nullable=False)
    day22 = db.Column(db.String(5), nullable=False)
    day23 = db.Column(db.String(5), nullable=False)
    day24 = db.Column(db.String(5), nullable=False)
    day25 = db.Column(db.String(5), nullable=False)
    day26 = db.Column(db.String(5), nullable=False)
    day27 = db.Column(db.String(5), nullable=False)
    day28 = db.Column(db.String(5), nullable=False)
    day29 = db.Column(db.String(5), nullable=False)
    day30 = db.Column(db.String(5), nullable=False)
    day31 = db.Column(db.String(5), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reservinf')
def reservinf():

    dt_now = datetime.datetime.now()
    now_month = dt_now.month
    after_5_months = (dt_now + relativedelta(months=6)).month

    _Key = request.args.get('key')
    
    if _Key == now_month or _Key is None:
        _Campreserves = db.session.query(Camplist,CampReserve).\
            filter(CampReserve.month == now_month). \
            join(CampReserve, CampReserve.campid==Camplist.campid).\
                order_by(CampReserve.campid,CampReserve.year,CampReserve.month).all()
        _Campidsums = db.session.query(Camplist,CampReserve).\
            filter(CampReserve.month == now_month). \
            join(CampReserve, CampReserve.campid==Camplist.campid).\
                order_by(CampReserve.campid,CampReserve.year,CampReserve.month).\
                    group_by(Camplist.campid,CampReserve.year,CampReserve.month)
        _Campidgroup = db.session.query(Camplist,CampReserve).\
            filter(CampReserve.month == now_month). \
            join(CampReserve, CampReserve.campid==Camplist.campid).\
                order_by(CampReserve.campid,CampReserve.year,CampReserve.month).\
                    group_by(Camplist.campid)
        if _Key is None:
            _month = now_month
        else:
            _month = _Key
    else:
        _Campreserves = db.session.query(Camplist,CampReserve).\
            filter(CampReserve.month == _Key). \
            join(CampReserve, CampReserve.campid==Camplist.campid).\
                order_by(CampReserve.campid,CampReserve.year,CampReserve.month).all()
        _Campidsums = db.session.query(Camplist,CampReserve).\
            filter(CampReserve.month == _Key). \
            join(CampReserve, CampReserve.campid==Camplist.campid).\
                order_by(CampReserve.campid,CampReserve.year,CampReserve.month).\
                    group_by(Camplist.campid,CampReserve.year,CampReserve.month)
        _Campidgroup = db.session.query(Camplist,CampReserve).\
            filter(CampReserve.month == _Key). \
            join(CampReserve, CampReserve.campid==Camplist.campid).\
                order_by(CampReserve.campid,CampReserve.year,CampReserve.month).\
                    group_by(Camplist.campid)   
        _month = _Key      

    return render_template('reservinf.html',\
        _CampReserve=_Campreserves, \
            _Campidsum = _Campidsums, \
                _Campidgroup = _Campidgroup,\
                    _now_month = now_month,\
                        _after_5_months = after_5_months,\
                            _month = _month)


@app.route('/camplist')
def camplist():
    search = request.args.get('search')
    if search == 'yoyakunashi':
        _camplists = Camplist.query.filter(Camplist.reservumu=="0").order_by(Camplist.campid).all()
        _campareasgroups = Camplist.query.filter(Camplist.reservumu=="0").order_by(Camplist.campid).group_by(Camplist.area)
        _subtitle='予約不要なキャンプ場一覧'

    elif search == 'muryo':
        _camplists = Camplist.query.filter(Camplist.costumu=="0").order_by(Camplist.campid).all()
        _campareasgroups = Camplist.query.filter(Camplist.costumu=="0").order_by(Camplist.campid).group_by(Camplist.area)
        _subtitle='無料なキャンプ場一覧'

    elif search =='pets':
        _camplists = Camplist.query.filter(Camplist.petumu=="1").order_by(Camplist.campid).all()
        _campareasgroups = Camplist.query.filter(Camplist.petumu=="1").order_by(Camplist.campid).group_by(Camplist.area)
        _subtitle='ペット同伴OKなキャンプ場一覧'

    elif search =='bbq':
        _camplists = Camplist.query.filter(Camplist.bbqumu=="1").order_by(Camplist.campid).all()
        _campareasgroups = Camplist.query.filter(Camplist.bbqumu=="1").order_by(Camplist.campid).group_by(Camplist.area)
        _subtitle='BBQ施設があるキャンプ場一覧'
    
    elif search =='daycamp':
        _camplists = Camplist.query.filter(Camplist.daycapmumu=="1").order_by(Camplist.campid).all()
        _campareasgroups = Camplist.query.filter(Camplist.daycapmumu=="1").order_by(Camplist.campid).group_by(Camplist.area)
        _subtitle='日帰りOKなキャンプ場一覧'

    else:
        _camplists = Camplist.query.order_by(Camplist.campid).all()
        _campareasgroups = Camplist.query.order_by(Camplist.campid).group_by(Camplist.area)
        _subtitle='すべてのキャンプ場'

    return render_template('camplist.html' ,camplists=_camplists, _campareasgroups=_campareasgroups,_subtitle=_subtitle)

@app.route('/individual')
def individual(): 
    _campid = request.args.get('campid')
    _campinf = Camplist.query.filter(Camplist.campid ==_campid).all()
    _campfacility = Campfacility.query.filter(Campfacility.campid ==_campid).all()
    _camp_supermarket = Camp_supermarket.query.filter(Camp_supermarket.campid ==_campid).all()
    _camp_hot_spring = Camp_hot_spring.query.filter(Camp_hot_spring.campid ==_campid).all()
    return render_template('individual.html',_campinf=_campinf, \
        _campfacility=_campfacility,\
            _camp_supermarket=_camp_supermarket,\
                _camp_hot_spring=_camp_hot_spring)

@app.route('/privacy-policy')
def privacypolicy(): 
    return render_template('privacy-policy.html')

if __name__ == '__main__':
    app.run()
