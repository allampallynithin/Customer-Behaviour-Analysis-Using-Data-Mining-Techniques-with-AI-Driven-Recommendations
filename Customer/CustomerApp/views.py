from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponse
from django.conf import settings
import os
import io
import base64
import matplotlib.pyplot as plt
import pymysql
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import seaborn as sns

global dataset

def SuggestionAction(request):
    if request.method == 'POST':
        global dataset
        pname = request.POST.get('t1', False)
        dataset['Product_Category_Preference'] = dataset['Product_Category_Preference'].str.lower()
        dataset = dataset.drop_duplicates(subset='Product_Category_Preference')
        vectorizer = CountVectorizer()
        vectorized = vectorizer.fit_transform(dataset['Product_Category_Preference'])
        similarities = cosine_similarity(vectorized)
        df = pd.DataFrame(similarities, columns=dataset['Product_Category_Preference'], index=dataset['Product_Category_Preference']).reset_index()
        input_book = pname.strip().lower()
        print(df.values.tolist())
        df[input_book] = pd.to_numeric(df[input_book])
        recommendations = pd.DataFrame(df.nlargest(11,input_book)['Product_Category_Preference'])
        recommendations = recommendations[recommendations['Product_Category_Preference']!=input_book]
        columns = ['Product Suggestion']
        output='<table border=1 align=center width=100%><tr>'
        for i in range(len(columns)):
            output += '<th><font size="3" color="black">'+columns[i]+'</th>'
        output += '</tr>'
        recommendations = recommendations.values
        for i in range(len(recommendations)):
            output += '<tr><td><font size="3" color="black">'+str(recommendations[i,0])+'</td>'
            output += '</tr>'
        output+= "</table></br></br></br></br>"
        context= {'data':output}
        return render(request, 'UserScreen.html', context)
        

def Suggestion(request):
    if request.method == 'GET':
       return render(request, 'Suggestion.html', {})

def Visualization(request):
    if request.method == 'GET':
       return render(request, 'Visualization.html', {})

def VisualizationAction(request):
    if request.method == 'POST':
        global dataset
        age = request.POST.get('t1', False)
        age = int(age)
        dataset1 = dataset.loc[dataset['Age'] >= age]
        figure, axis = plt.subplots(nrows=2, ncols=2,figsize=(15, 10))#display original and predicted segmented image
        axis[0,0].set_title("Top Purchase Items Customer Wise")
        axis[0,1].set_title("Gender Wise Product Purchase Graph")
        data = dataset1.groupby(["Product_Category_Preference"])['Purchase_Frequency' ].sum().sort_values(ascending=False).reset_index(name='Purchase Count').reset_index()
        sns.lineplot(data=data, x="Product_Category_Preference", y="Purchase Count", ax=axis[0,0])
        #distribution of gender wise product purchase
        data = dataset1.groupby(['Product_Category_Preference','Gender']).size().reset_index()
        data = data.rename(columns={0: 'Count'})
        sns.barplot(x='Product_Category_Preference',y='Count',hue='Gender',data=data, ax=axis[0,1])
        axis[1,0].set_title("Customers % from Different Locations")
        axis[1,1].set_title("Distribution of Total Spending Graph")
        dataset1.groupby("Location").size().plot.pie(autopct='%.0f%%', ax=axis[1,0])
        sns.distplot(dataset1['Total_Spending'], bins = 15, ax=axis[1,1])
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        #plt.close()
        img_b64 = base64.b64encode(buf.getvalue()).decode()
        plt.clf()
        plt.cla()
        context= {'data':"Customer Behaviour Visualization", 'img': img_b64}
        return render(request, 'UserScreen.html', context)

def LoadDataset(request):    
    if request.method == 'GET':
        global dataset
        dataset = pd.read_csv("Dataset/Dataset.csv")
        columns = dataset.columns
        data = dataset.values
        output='<table border=1 align=center width=100%><tr>'
        for i in range(len(columns)):
            output += '<th><font size="3" color="black">'+columns[i]+'</th>'
        output += '</tr>'
        for i in range(len(data)):
            output += '<tr>'
            for j in range(len(data[i])):
                output += '<td><font size="3" color="black">'+str(data[i,j])+'</td>'
            output += '</tr>'
        output+= "</table></br></br></br></br>"
        context= {'data':output}
        return render(request, 'UserScreen.html', context)

def UserLoginAction(request):
    global username
    if request.method == 'POST':
        global username
        status = "none"
        users = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = '', database = 'behaviour',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select username,password FROM register")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == users and row[1] == password:
                    username = users
                    status = "success"
                    break
        if status == 'success':
            context= {'data':'Welcome '+username}
            return render(request, "UserScreen.html", context)
        else:
            context= {'data':'Invalid username'}
            return render(request, 'UserLogin.html', context)

def SignupAction(request):
    if request.method == 'POST':
        global username
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        contact = request.POST.get('t3', False)
        email = request.POST.get('t4', False)
        address = request.POST.get('t5', False)
               
        output = "none"
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = '', database = 'behaviour',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select username FROM register")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == username:
                    output = username+" Username already exists"
                    break                
        if output == "none":
            db_connection = pymysql.connect(host='127.0.0.1:8000',port = 3306,user = 'root', password = '', database = 'behaviour',charset='utf8')
            db_cursor = db_connection.cursor()
            student_sql_query = "INSERT INTO register VALUES('"+username+"','"+password+"','"+contact+"','"+email+"','"+address+"')"
            db_cursor.execute(student_sql_query)
            db_connection.commit()
            print(db_cursor.rowcount, "Record Inserted")
            if db_cursor.rowcount == 1:
                output = "Signup process completed. Login to perform Customer Behaviour Analysis"
        context= {'data':output}
        return render(request, 'Signup.html', context)       

def UserLogin(request):
    if request.method == 'GET':
       return render(request, 'UserLogin.html', {})

def AdminLogin(request):
    if request.method == 'GET':
       return render(request, 'AdminLogin.html', {})    

def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})

def Signup(request):
    if request.method == 'GET':
       return render(request, 'Signup.html', {})

def AdminLoginAction(request):
    global username
    if request.method == 'POST':
        users = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        if users == 'admin' and password == "admin":
            context= {'data':'Welcome '+users}
            return render(request, "AdminScreen.html", context)
        else:
            context= {'data':'Invalid username'}
            return render(request, 'AdminLogin.html', context)
    
def ViewUsers(request):
    if request.method == 'GET':
        global username
        cols = ['Username', 'Password', 'Contact No', 'Email ID', 'Address']
        output = '<table border="1" align="center" width="100%"><tr>'
        font = '<font size="" color="black">'
        for i in range(len(cols)):
            output += "<td>"+font+cols[i]+"</font></td>"
        output += "</tr>"
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = '', database = 'behaviour',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM register")
            rows = cur.fetchall()
            for row in rows:
                output += "<tr><td>"+font+str(row[0])+"</font></td>"
                output += "<td>"+font+str(row[1])+"</font></td>"
                output += "<td>"+font+str(row[2])+"</font></td>"
                output += "<td>"+font+str(row[3])+"</font></td><td>"+font+str(row[4])+"</font></td></tr>"     
        output += "</table><br/><br/><br/><br/>"    
        context= {'data':output}
        return render(request, "AdminScreen.html", context)
