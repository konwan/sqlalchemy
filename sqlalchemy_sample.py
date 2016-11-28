#!/usr/bin/env python
# -*- coding:utf-8 -*-

from sqlalchemy import Column, Integer, String, ForeignKey, create_engine 
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Person(Base):
    __tablename__ = 'person'

    person_id = Column(Integer, primary_key=True)
    nickname = Column(String(64), nullable=False)
    gender = Column(Integer)
    idcard = Column(String(20))


class Telephone(Base):
    __tablename__ = 'telephone'

    tel_id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey('person.person_id'))
    telphone_no = Column(String(64))
    memo = Column(String(20))

if __name__ == "__main__":
    DB_CONNECT_STRING = "sqlite:////Users/data/Desktop/cindy/gomi/npp/sqlalchemy/test.db"
    engine = create_engine(DB_CONNECT_STRING, echo=False)
    DB_Session = sessionmaker(bind=engine)
    session = DB_Session()

    # 1. 创建表(如果表已经存在，则不会创建)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    print("step1: create_all db") 

    # 2. 插入数据
    p1 = Person( person_id = 1, nickname = "wan", gender = "F", idcard = "31234")
    p2 = Person( person_id = 2, nickname = "jlin", gender = "M", idcard = "67890")
    p3 = Person( person_id = 3, nickname = "szj", gender = "M", idcard = "awsqde23")
    p4 = Person( person_id = 4, nickname = "jlin", gender = "M", idcard = "321awsd")
    tel1 = Telephone(tel_id = 1, person_id = 1, telphone_no = "0800123455", memo = "not real num")

    # 2.1 使用add，如果已经存在，会报错
    session.add_all([p1, p3, p4, tel1])
    session.add(p2)
    print("step2: insert {} person".format(len(session.query(Person).all())))
    session.commit()

    # 3 修改数据
    # 3.1 使用merge方法，如果存在则修改，如果不存在则插入（只判断主键，不判断unique列）
    p1.nickname = 'kw'
    session.merge(p1)
    print("step3.1: update data {}".format(session.query(Person).get(1).nickname))

    # 3.2 也可以通过这种方式修改
    session.query(Person).filter(Person.person_id == 1).update({'nickname': 'konwan'})
    print("step3.2: update data {}".format(session.query(Person).get(1).nickname))

    # 4. 删除数据
    session.query(Person).filter(Person.person_id == 1).delete()
    print("step4: delete data {}".format( [ i for i in session.query(Person).all()] ))

    # 5. 查询数据
    # 5.1 返回结果集的第二项
    user = session.query(Person).get(2)
    print("step5.1: get data {}".format(user.nickname))

    # 5.2 返回结果集中的第2-3项
    user2 = session.query(Person)[1:3]
    print("step5.2: get data {}".format( [x.nickname for x in user2]))

    # 5.3 查询条件
    user3 = session.query(Person).filter(Person.person_id < 6).first()
    print("step5.3: get data {}".format(user3.nickname))

    # 5.4 排序
    user4 = session.query(Person).order_by(Person.nickname)
    print("step5.4: get data {}".format([x.nickname for x in user4]))

    # 5.5 降序（需要导入desc方法）
    from sqlalchemy import desc
    user5 = session.query(Person).order_by(desc(Person.nickname))
    print("step5.5: get data {}".format([x.nickname for x in user5]))

    # 5.7 给结果集的列取别名
    user7 = session.query(Person.nickname.label('user_name')).all()
    print("step5.7: change column name to user_name {}".format([x.user_name for x in user7]))

    # 5.8 去重查询（需要导入distinct方法）
    from sqlalchemy import distinct
    user8 = session.query(distinct(Person.nickname).label('name')).all()
    print("step5.8: distinct nickname to name {}".format([x.name for x in user8]))
    
    # 5.9 统计查询
    from sqlalchemy.sql import func
    user_count = session.query(Person.nickname).order_by(Person.nickname).count()
    id_avg = session.query(func.avg(Person.person_id)).first()
    id_sum = session.query(func.sum(Person.person_id)).first()
    print("step5.9:person_cnt {} id_avg {} id_sum {}".format(user_count, id_avg, id_sum))
    
    # 5.10 分组查询
    users = session.query(func.count(Person.nickname).label('count'), Person.person_id).group_by(Person.person_id)
    print("step5.10: group by id {} ".format( (",".join(str([user.person_id, user.count]) for user in users)) ))
   
    session.close()
