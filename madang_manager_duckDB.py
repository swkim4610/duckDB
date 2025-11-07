import streamlit as st 
import duckdb
import pandas as pd
import time

dbConn = duckdb.connect('madang.db')
cursor = dbConn.cursor()

def query(sql):
       return dbConn.execute(sql).fetchall()

st.title("마당 서점 관리 시스템")

books = [None]
result = query("select concat(bookid, '. ', bookname) from Book")
for res in result:
       books.append(res[0])

tab1, tab2 = st.tabs(["고객조회", "거래 입력"])
name = ""
custid = 999
result =pd.DataFrame()
name = tab1.text_input("고객명")
select_book = ""

if len(name) > 0:
       sql = "select c.custid, c.name, b.bookname, o.orderdate, o.saleprice from Customer c, Book b, Orders o \
              where c.custid = o.custid and o.bookid = b.bookid and name = '" + name + "';"
       result = pd.DataFrame(query(sql), columns=['custid', 'name', 'bookname', 'orderdate', 'saleprice'])
       tab1.write(result)
       custid = result['custid'][0]
       tab2.write("고객번호: " + str(custid))
       tab2.write("고객명: " + name)
       select_book = tab2.selectbox("구매 서적:",books)

       if select_book is not None:
              bookid = select_book.split(".")[0]
              dt = time.localtime()
              dt = time.strftime('%Y-%m-%d', dt)
              orderid = query("select max(orderid) from orders;")[0][0] + 1
              price = tab2.text_input("금액")
              sql = "insert into orders (orderid, custid, bookid, saleprice, orderdate) values (" \
                  + str(orderid) + ","  \
                  + str(custid) + ","  \
                  + str(bookid) + ","  \
                  + str(price) + ","   \
              "'" + str(dt) + "');"
              if tab2.button('거래 입력'):
                     cursor.execute(sql)
                     dbConn.commit()
                     tab2.write('거래가 입력되었습니다.')
