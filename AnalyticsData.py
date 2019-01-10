from sqlalchemy import create_engine
import json
from pprint import pprint
from sqlalchemy import func, insert
import csv
from datetime import datetime

# Import and establish Base for which classes will be constructed 
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

# Import modules to declare columns and column data types
from sqlalchemy import Column, Integer, String, Float, Date, DECIMAL


class School(Base):
    __tablename__ = 'school'
    id = Column(Integer, primary_key=True)
    districtid = Column(Integer)
    districtname = Column(String(1000))
    url = Column(String(1000))
    latitude = Column(Float)
    longitude = Column(Float)
    zipcode = Column(String(10))
    lowGrade = Column(String(10))
    highGrade = Column(String(10))
    rank = Column(Integer)
    rankOf = Column(Integer)
    rankStars = Column(Integer)
    year = Column(Integer)
    city = Column(String(100))
    state = Column(String(100))

class School_Agg(Base):
    __tablename__ = 'school_agg'
    id = Column(Integer, primary_key=True)
    zipcode = Column(String(10))
    rank = Column(Integer)
    rankStars = Column(Float)

class HouseRent_Agg(Base):
    __tablename__ = 'houserent_agg'
    id = Column(Integer, primary_key=True)
    zipcode = Column(String(10))
    state = Column(String(100))
    city = Column(String(100))
    rent = Column(Float)

class MarketHealth_Agg(Base):
    __tablename__ = 'markethealth_agg'
    id = Column(Integer, primary_key=True)
    zipcode = Column(String(10))
    state = Column(String(100))
    city = Column(String(100))
    marketindex = Column(Float)

class Income_Agg(Base):
    __tablename__ = 'income_agg'
    id = Column(Integer, primary_key=True)
    zipcode = Column(String(10))
    state = Column(String(100))
    totalincome = Column(Integer)

class CrimePrice_Agg(Base):
    __tablename__ = 'crimeprice_agg'
    id = Column(Integer, primary_key=True)
    zipcode = Column(String(10))
    latitude = Column(Float)
    longitude = Column(Float)
    saleprice = Column(Integer)
    totalcrime = Column(Integer)

class ZipAnalytics(Base):
    __tablename__ = 'zipanalytics'
    id = Column(Integer, primary_key=True)
    zipcode = Column(String(10))
    latitude = Column(Float)
    longitude = Column(Float)
    saleprice = Column(Integer)
    totalcrime = Column(Integer)
    rank = Column(Integer)
    rankStars = Column(Float)
    rent = Column(Float)
    marketindex = Column(Float)
    totalincome = Column(Integer)


engine = create_engine('sqlite:///school.sqlite')

Base.metadata.drop_all(bind=engine, tables=[School.__table__, School_Agg.__table__,HouseRent_Agg.__table__,MarketHealth_Agg.__table__,Income_Agg.__table__,CrimePrice_Agg.__table__, ZipAnalytics.__table__])

Base.metadata.create_all(engine)

from sqlalchemy.orm import Session
session = Session(bind=engine)

with open('school.json') as f:
    data = json.load(f)
    data = data["districtList"]

for row in data:
    districtid = 0
    districtname = ''
    url = ''
    latitude = 0.00
    longitude = 0.00
    zipcode = ''
    city = ''
    state = ''
    lowGrade = ''
    highGrade = ''
    year = 0
    rank = 0
    rankOf = 0
    rankStars = 0

    districtid = int(row["districtID"])
    districtname = row["districtName"]
    url = row["url"]
    if "address" in row:
        if "latLong" in row["address"]:
            if "latitude" in row["address"]["latLong"]:
                lat = row["address"]["latLong"]["latitude"]
                lon = row["address"]["latLong"]["longitude"]
                latitude = float(lat) if lat else 0
                longitude = float(lon) if lon else 0

    zipcode = row["address"]["zip"]
    city = row["address"]["city"]
    state = row["address"]["state"]
    lowGrade = row["lowGrade"]
    highGrade = row["highGrade"]
    if row["rankHistory"]:
        year = int(row["rankHistory"][0]["year"])
        rank = int(row["rankHistory"][0]["rank"])
        rankOf = int(row["rankHistory"][0]["rankOf"])
        rankStars = round(float(row["rankHistory"][0]["rankStars"]),2)

    school_row = School(
        districtid = districtid,
        districtname = districtname,
        url = url,
        latitude = latitude,
        longitude = longitude,
        zipcode = zipcode,
        city = city,
        state = state,
        lowGrade = lowGrade,
        highGrade = highGrade,
        year = year,
        rank = rank,
        rankOf = rankOf,
        rankStars = rankStars
    )
    session.add(school_row)
    session.commit()


queryresult = session.query(School)

school_agg = session.query(School.zipcode, func.avg(School.rank), func.avg(School.rankStars)).\
group_by(School.zipcode).order_by(School.zipcode)

session.execute(insert(School_Agg).from_select((School_Agg.zipcode,School_Agg.rank, School_Agg.rankStars), school_agg))

with open("Data/Zip_MedianRentalPrice_AllHomes.csv", encoding="iso-8859-1") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    next(csv_reader)
    for row in csv_reader:
        zipcode = row[0]
        state = row[2]
        city = row[2]
        rent = row[110]
    
        rent_row = HouseRent_Agg(
            zipcode = zipcode,
            state = state,
            city = city,
            rent = rent
        )

        session.add(rent_row)
        session.commit()

        zipcode = None
        state = None
        city = None
        rent = None

with open("Data/MarketHealthIndex_Zip.csv", encoding="iso-8859-1") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    next(csv_reader)
    for row in csv_reader:
        zipcode = row[1]
        state = row[3]
        city = row[2]
        marketindex = round(float(row[7]),2)
    
        market_row = MarketHealth_Agg(
            zipcode = zipcode,
            state = state,
            city = city,
            marketindex = marketindex
        )

        session.add(market_row)
        session.commit()

        zipcode = None
        state = None
        city = None
        marketindex = None

with open("Data/IRSIncomeByZipCode.csv", encoding="iso-8859-1") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    next(csv_reader)
    for row in csv_reader:
        if row[0] == 'NY':
            zipcode = row[1]
            state = row[0]
            totalincome = row[6]
        
            income_row = Income_Agg(
                zipcode = zipcode,
                state = state,
                totalincome = totalincome
            )

            session.add(income_row)
            session.commit()

            zipcode = None
            state = None
            totalincome = None

with open("Data/Ny_Data.csv", encoding="iso-8859-1") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    next(csv_reader)
    for row in csv_reader:
        zipcode = row[1]
        latitude = row[2]
        longitude = row[3]
        saleprice = row[4]
        totalcrime = row[5]

        crimeprice_row = CrimePrice_Agg(
            zipcode = zipcode,
            latitude = latitude,
            longitude = longitude,
            saleprice = saleprice,
            totalcrime = totalcrime
        )

        session.add(crimeprice_row)
        session.commit()

        zipcode = None
        latitude = None
        longitude = None
        saleprice = None
        totalcrime = None

# zip_agg = session.query(School.zipcode, func.avg(School.rank), func.avg(School.rankStars)).\
# group_by(School.zipcode).order_by(School.zipcode)

zip_agg = (
    session.query(
        CrimePrice_Agg.zipcode,
        CrimePrice_Agg.latitude,
        CrimePrice_Agg.longitude,
        CrimePrice_Agg.saleprice,
        HouseRent_Agg.rent,
        func.round(MarketHealth_Agg.marketindex,2),
        Income_Agg.totalincome,
        CrimePrice_Agg.totalcrime,
        School_Agg.rank,
        func.round(School_Agg.rankStars,2)
        ).
        outerjoin(School_Agg, CrimePrice_Agg.zipcode==School_Agg.zipcode).
        outerjoin(HouseRent_Agg, CrimePrice_Agg.zipcode==HouseRent_Agg.zipcode).
        outerjoin(MarketHealth_Agg, CrimePrice_Agg.zipcode==MarketHealth_Agg.zipcode).
        outerjoin(Income_Agg, CrimePrice_Agg.zipcode==Income_Agg.zipcode)
)

session.execute(insert(ZipAnalytics).\
from_select((
    ZipAnalytics.zipcode,
    ZipAnalytics.latitude,
    ZipAnalytics.longitude,
    ZipAnalytics.saleprice,
    ZipAnalytics.rent,
    ZipAnalytics.marketindex,
    ZipAnalytics.totalincome,
    ZipAnalytics.totalcrime,
    ZipAnalytics.rank,
    ZipAnalytics.rankStars
    ), zip_agg))

session.commit()
# queryresult = session.query(ZipAnalytics)

# for row in queryresult:
#     print('--------')
#     print(row.zipcode)
#     print(row.latitude)
#     print(row.longitude)
#     print(row.saleprice)
#     print(row.rent)
#     print(row.marketindex)
#     print(row.totalincome)
#     print(row.totalcrime)
#     print(row.rank)
#     print(row.rankStars)
#     print('*********')

outfile = open('Data/zipanalytics_output.csv', 'w')
outcsv = csv.writer(outfile)
records = session.query(ZipAnalytics).all()
outcsv.writerow([column.name for column in ZipAnalytics.__mapper__.columns])
[outcsv.writerow([ getattr(curr, column.name) for column in ZipAnalytics.__mapper__.columns ]) for curr in records ]
outfile.close()
