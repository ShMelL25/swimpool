from sqlalchemy import create_engine, insert
import sqlalchemy
import config
import pandas as pd
from datetime import datetime


class SQL_request(object):
    
    def __init__(self):
        
        self.create_engine_postgr_sql
        self.register_user
        self.del_train
        self.answer_
        
        
    def create_engine_postgr_sql(self):
       
        engine = create_engine(config.sql_url)
        
        return engine
    
    def register_user(self, username:str, telgram_id:str):
        
        engine = self.create_engine_postgr_sql()
        data = f'select telegram_id from users where telegram_id={telgram_id}'
        
        if pd.read_sql(data, engine).shape[0] == 0:
           
            with engine.begin() as cnx:
                ret = 'Вы успешно зарегестрированы!'
                insert_sql = sqlalchemy.text(
                    f"INSERT INTO users (date_reg, user_name, telegram_id) values ('{datetime.now().date()}', '{username}', {telgram_id})"
                )
                cnx.execute(insert_sql)
                cnx.commit()
        else:
            ret = 'Вы уже зарегестрированы!'
        
        return ret
    
    def add_train(self, text, telegram_id):
        engine = self.create_engine_postgr_sql()
        text = text[5:].split('; ')
        z = []
        a=[]
        data = f'select id from users where telegram_id={telegram_id}'
        df = pd.read_sql(data, engine)
        
        
        for i in text:
            i = i.replace(';', '')
            z.append(i.split(','))
        for i in z[2]:
            a.append(int(i))
        z[2] = a
        

        if df.shape[0] != 0:
            
            
            with engine.begin() as cnx:
                
                for i in range(len(z[0])):
                    
                    ans = self.answer_(arr=[z[0][i], z[3][0]], id_=df.id.to_numpy()[0])
                    if ans == True:
                        insert_sql = sqlalchemy.text(
                            f'''INSERT INTO time_user (user_id, time_train, count_person, type_person, day_train) 
                            values ({df.id.to_numpy()[0]}, '{z[0][i]}', {z[2][i]}, '{z[1][i]}', '{z[3][0]}')'''
                        )
                        
                        cnx.execute(insert_sql)
                        ref = 'Успешно добавлено!'
                    else:
                        ref = 'Уже была добавлена!'
            
        else:
            ref = 'Вы не зарегестрированы'
            
        return ref
    
    def answer_(self, arr, id_):
        engine = self.create_engine_postgr_sql()
        
        with engine.begin() as cnx:
            insert_sql = f'''
                            select * from time_user
                            where user_id = {id_} and time_train = time'{arr[0]}' and day_train = '{arr[1]}'
                        '''
                      
            if pd.read_sql(insert_sql, engine).shape[0] == 0:
                return True
            else:
                return False
            
            
    
    def del_train(self, text, telegram_id):
        engine = self.create_engine_postgr_sql()
        text = text[5:].split('; ')
        z = []
        a=[]
        data = f'select id from users where telegram_id={telegram_id}'
        df = pd.read_sql(data, engine)
        
        
        for i in text:
            i = i.replace(';', '')
            z.append(i.split(','))
        for i in z[2]:
            a.append(int(i))
        z[2] = a
        

        if df.shape[0] != 0:
            
            
            with engine.begin() as cnx:
                 
                insert_sql = sqlalchemy.text(
                    f'''DELETE FROM time_user
                            WHERE user_id = {df.id.to_numpy()[0]} and  day_train = '{z[3][0]}' and time_train in {tuple(z[0])};
                                '''
                    )
                
                cnx.execute(insert_sql)
                cnx.commit()
            ref = 'Успешно удалено!'
        else:
            ref = 'Вы не зарегестрированы'
            
        return ref
    
    def request_train(self):
        
            
        
        
        
        



