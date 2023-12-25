#基于mysql的去重判断依据的存储
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from . import BaseFilter

Base = declarative_base()

#
# class Filter(Base):
#     __tablename__ ='filter'
#     id = Column(Integer, primary_key=True)
#     hash_value = Column(String(40),index=True,unique=True)

class MySQLFilter(BaseFilter):

    def __init__(self,*args,**kwargs):
        self.table = type(kwargs["mysql_table_name"],(Base,),dict(__tablename__ = kwargs["mysql_table_name"],
                id = Column(Integer, primary_key=True),
                hash_value = Column(String(40), index=True, unique=True))
                 )
        BaseFilter.__init__(self,*args,**kwargs)
    def _get_storage(self):
        '''
        返回一个mysql的链接对象(sqlalchemy的数据库链接对象)
        :return:
        '''
        engine = create_engine(self.mysql_url)
        Base.metadata.create_all(engine)
        Session = sessionmaker(engine)
        return Session


    def _save(self, hash_value):
        """
        利用redis的无序编合进行存储
        :param hash_value:
        :return:
        """
        session = self.storage()
        filter = self.table(hash_value=hash_value)
        session.add(filter)
        session.commit()
        session.close()
    def _is_exists(self, hash_value):
        '''
        判断redis对应的无序集合中是否有对应的判断依据
        :param hash_value:
        :return:
        '''
        session = self.storage()
        ret = session.query(self.table).filter(self.table.hash_value == hash_value).first()
        if ret is None:
            return False
        else:
            return True
