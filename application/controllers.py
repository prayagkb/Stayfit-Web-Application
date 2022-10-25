from flask import Flask, redirect, render_template, request, session,g
from flask import current_app as app
from application.models import User
from application.models import Tracker
from application.models import User_to_Tracker
from application.models import LogTable
from application.database import db
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

@app.route('/')
def home():
    return render_template("Home.html")

@app.route("/trackers", methods=["GET", "POST"])
def tracker_def():
    if request.method == "GET":
        return render_template("trackerdefault.html")

#session.clear()

@app.route("/user/signup", methods=["GET", "POST"])
def add_user():
    if request.method == "GET":
        return render_template("signup.html")
    if request.method == "POST":
        uname=request.form["Name"]
        uage=request.form["Age"]
        uemail=request.form["Email"]
        upassword=request.form["Password"]
        ucontact=request.form['contact']

        if User.query.filter(User.email == uemail).first():
            return render_template("userexist.html")
        else:
            query1=User(name=uname,email=uemail,password=upassword,age=uage,contact=ucontact,subscriber=[])
            db.session.add(query1)
            db.session.commit()
            return render_template("signupsuccess.html")

@app.route("/user/login", methods=["GET", "POST"])
def login_user():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        uemail=request.form["Email"]
        upassword=request.form["Password"]
        session['email']=uemail
        email=session['email']

        query2=User.query.filter_by(email=uemail).one_or_none()
        
        if query2==None:
            return render_template('wrongpassword.html')
        else:
            if query2.password==upassword:
                session['userid']=query2.userid
                userid=session['userid']
                session['name']=query2.name
                name=session['name']
                url="/"+str(userid)+"/dashboard"              
                return redirect(url)
            else:
                return render_template('wrongpassword.html')

@app.route("/<int:userid>/dashboard", methods=["GET","POST"])
def dashboard(userid):
    if 'userid' in session:
        data1={}
        data1['name']=session.get('name')
        data1['userid']=userid
        tid_to_tname={}
        query3=User_to_Tracker.query.filter_by(user_uid=session.get("userid")).all()
        tracker_to_user=[]
        for j in query3: 
            tracker_to_user.append(j.tracker_tid)
        
        for i in tracker_to_user:
            query8=Tracker.query.filter_by(t_id=i).one()
            tid_to_tname[i]=query8.t_name
        query16=LogTable.query.filter_by(userlog_id=userid).all()
        tracker_to_lastlog={}
        for i in query16:
            for j in tracker_to_user:
                if j==i.tlog_id:
                    tracker_to_lastlog[int(j)]=i.timestamp

        return render_template('dashboard.html',data1=data1,data2=query3,data3=tid_to_tname,data5=tracker_to_lastlog)
    else:
        return render_template('Home.html')


@app.route("/<int:userid>/addtracker/user-defined", methods=["GET","POST"])
def add_userdefined_tracker(userid):
    g.data1={}
    g.data1['name']=session.get('name')
    g.data1['userid']=userid
    if request.method == "GET":
        return render_template('addtracker-userdefined.html',data1=g.data1)
    if request.method == "POST":
        tracker_name=request.form["tracker_name"]
        tracker_dscp=request.form["tracker_dscp"]
        tracker_type=request.form["tracker_type"]
        if tracker_type == "mul":
            tracker_value_str = request.form["mulval"]
            query4=Tracker(t_name=tracker_name,t_dscp=tracker_dscp,t_type=tracker_type,t_owner=session.get("userid"),t_values=tracker_value_str)
        else:
            query4=Tracker(t_name=tracker_name,t_dscp=tracker_dscp,t_type=tracker_type,t_owner=session.get("userid"))
        db.session.add(query4)
        query5=Tracker.query.filter_by(t_owner=session.get("userid"),t_name=tracker_name).first()
        #session.get('userid').subscriber.append(query5.t_id)
        query6=User_to_Tracker(user_uid=session.get("userid"),tracker_tid=query5.t_id)
        db.session.add(query6)
        g.query7=User_to_Tracker.query.filter_by(user_uid=session.get("userid")).all()
        db.session.commit()
        tracker_to_user=[]
        for j in g.query7: 
            tracker_to_user.append(j.tracker_tid)
        tid_to_tname={}
        for i in tracker_to_user:
            query8=Tracker.query.filter_by(t_id=i).one()
            tid_to_tname[i]=query8.t_name
        url2="/"+str(userid)+"/dashboard"
        return redirect(url2)
            


@app.route("/<int:userid>/addtracker/inbuilt", methods=["GET","POST"])
def add_inbuilt_tracker(userid):
    data1={}
    data1['name']=session.get('name')
    data1['userid']=userid
    if request.method == "GET":
        return render_template('addtracker-inbuilt.html',data1=data1)
    else:
        tid_list=request.form.getlist('trackers')
        final_td_list=[]
        int_tid=[]
        for i in tid_list:
            int_tid.append(int(i))
        query7=User_to_Tracker.query.filter_by(user_uid=userid).all()
        if query7!=None:
            for i in query7:
                final_td_list.append(i.tracker_tid)
        else:
            pass

        for i in final_td_list:
            if i in int_tid:
                int_tid.remove(i)
        else:
            pass
        if len(int_tid)!=0:
            for j in int_tid:
                query6=User_to_Tracker(user_uid=session.get("userid"),tracker_tid=int(j))
                db.session.add(query6)
                db.session.commit()
        tracker_to_user=[]
        query3=User_to_Tracker.query.filter_by(user_uid=session.get("userid")).all()
        for j in query3: 
            tracker_to_user.append(j.tracker_tid)
        tid_to_tname={}
        for i in tracker_to_user:
            query9=Tracker.query.filter_by(t_id=i).one()
            tid_to_tname[i]=query9.t_name    
        query10=User_to_Tracker.query.filter_by(user_uid=session.get("userid")).all()
        url2="/"+str(userid)+"/dashboard"
        return redirect(url2)
        #return render_template('dashboard.html',data1=data1,data2=query10,data3=tid_to_tname)


@app.route("/<int:userid>/log/<int:tracker_id>",methods=["GET","POST"])
def log(userid,tracker_id):
    data1={}
    data1['name']=session.get('name')
    data1['userid']=userid
    tracker_to_user=[]
    query3=User_to_Tracker.query.filter_by(user_uid=session.get("userid")).all()
    for j in query3: 
        tracker_to_user.append(j.tracker_tid)
    tid_to_tname={}
    for i in tracker_to_user:
        query9=Tracker.query.filter_by(t_id=i).one()
        tid_to_tname[i]=query9.t_name 
    if request.method == "GET":   
        query17=Tracker.query.filter_by(t_id=tracker_id).one()
        if query17.t_type =="mul":
            value_list=query17.t_values.split(',')
            return render_template('enterlogmultivalue.html',data1=data1,tracker_id=tracker_id,data3=tid_to_tname,dataL=value_list)
        elif query17.t_type == "time":
            return render_template('enterlogtime.html',data1=data1,tracker_id=tracker_id,data3=tid_to_tname)
        elif query17.t_type == "bool":
            return render_template('enterlogbool.html',data1=data1,tracker_id=tracker_id,data3=tid_to_tname)
        else:
            return render_template('enterlog.html',data1=data1,tracker_id=tracker_id,data3=tid_to_tname)
    if request.method == "POST":
        log_value=request.form["value"]
        log_note=request.form["note"]
        userid=userid
        tracker_id=tracker_id
        time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query12=LogTable(userlog_id=userid,tlog_id=tracker_id,log_note=log_note,log_value=log_value,timestamp=time)
        db.session.add(query12)
        db.session.commit()
        url="/"+str(userid)+"/tracker/"+str(tracker_id)
        return redirect(url)
    
        

@app.route("/<int:userid>/log/<int:tracker_id>/mulval",methods=["POST"])
def mulvallog(userid,tracker_id):
    if request.method == "POST":
        mul_value=request.form["ansvalue"]
        mul_note=request.form["note"]
        time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query19=LogTable(userlog_id=userid,tlog_id=tracker_id,log_note=mul_note,log_value=mul_value,timestamp=time)
        db.session.add(query19)
        db.session.commit()
        url="/"+str(userid)+"/tracker/"+str(tracker_id)
        return redirect(url)

@app.route("/<int:userid>/log/<int:tracker_id>/timelog",methods=["POST"])
def timelog(userid,tracker_id):
    if request.method == "POST":
        hour=request.form["hr"]
        min=request.form["min"]
        note=request.form["note"]
        time_value=str(hour)+" Hr "+str(min)+" Min"
        time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query18=LogTable(userlog_id=userid,tlog_id=tracker_id,log_note=note,log_value=time_value,timestamp=time)
        db.session.add(query18)
        db.session.commit()
        url="/"+str(userid)+"/tracker/"+str(tracker_id)
        return redirect(url)

@app.route("/<int:userid>/tracker/<int:tracker_id>",methods=["GET","POST"])
def tracker_details(userid,tracker_id):
    data1={}
    data1['name']=session.get('name')
    data1['userid']=userid
    query15=Tracker.query.filter_by(t_id=tracker_id).one()
    tracker_dscp=query15.t_dscp
    query14=LogTable.query.filter_by(userlog_id=userid,tlog_id=tracker_id).all()
    if query15.t_type == "num":
        value_list=[]
        date_list=[]
        date_to_value={}
        sorted_value=[]
        sorted_date=[]
        for i in query14:
            date_list.append(i.timestamp)
        #value_list=sorted(value_list)
        for i in date_list:
            for j in query14:
                if i==j.timestamp:
                    value_list.append(int(j.log_value))
        for i in range(len(date_list)):
            date_to_value[date_list[i]]=value_list[i]
        sorted_value_dict_date={k: v for k, v in sorted(date_to_value.items(), key=lambda item: item[1])}
        #sorted_date_1=date_to_value.items()
        #for i in sorted_date_1:
            #sorted_date.append(date_to_value[i])
        #list1=sorted_value_dict_date.keys()
        #list2=sorted_value_dict_date.items()


        plt.clf()
        plt.plot_date(date_list,value_list, linestyle='solid')
        plt.gcf().autofmt_xdate()
        plt.xlabel("Timestamps")
        plt.ylabel("Values")
        plt.savefig("static/plot.png")

        return render_template('numtracker.html',data1=data1,tracker_id=tracker_id,data3=query15.t_name,data4=query14,value_list=value_list,date_list=date_list,tracker_dscp=tracker_dscp)
    elif query15.t_type == "mul":
        val_list=[]
        for i in query14:
            val_list.append(i.log_value)
        d={}
        for i in val_list:
            if i not in d:
                d[i]=1
            else:
                d[i]+=1

        l=[v for v in d]
        x=[]
        for i in l:
            x.append(d[i])
        plt.clf()
        plt.pie(x,labels=l,autopct=lambda p:f'{p:.2f}%')
        plt.savefig("static/plot.png")

        return render_template('numtracker.html',data1=data1,tracker_id=tracker_id,data3=query15.t_name,data4=query14,tracker_dscp=tracker_dscp)        


    else:
        return render_template('trackerpage.html',data1=data1,tracker_id=tracker_id,data3=query15.t_name,data4=query14,tracker_dscp=tracker_dscp)


@app.route("/<int:userid>/tracker/<int:tracker_id>/log/<int:log_id>/delete",methods=["GET"])
def log_delete(userid,tracker_id,log_id):
    if request.method == "GET":
        query20=LogTable.query.filter_by(log_id=log_id).one()
        db.session.delete(query20)
        db.session.commit()
        url="/"+str(userid)+"/tracker/"+str(tracker_id)
        return redirect(url)

@app.route("/<int:userid>/tracker/<int:tracker_id>/log/<int:log_id>/edit",methods=["GET","POST"])
def log_edit(userid,tracker_id,log_id):
    data1={}
    data1['name']=session.get('name')
    data1['userid']=userid
    tracker_to_user=[]
    query3=User_to_Tracker.query.filter_by(user_uid=session.get("userid")).all()
    for j in query3: 
        tracker_to_user.append(j.tracker_tid)
    tid_to_tname={}
    for i in tracker_to_user:
        query23=Tracker.query.filter_by(t_id=i).one()
        tid_to_tname[i]=query23.t_name
    if request.method == "GET":
        query21=LogTable.query.filter_by(log_id=log_id).one()
        temptracker_id=query21.tlog_id
        query22=Tracker.query.filter_by(t_id=temptracker_id).one()
        if query22.t_type == "mul":
            value_list=query22.t_values.split(',')
            return render_template('editlogmultivalue.html',data1=data1,tracker_id=tracker_id,data3=tid_to_tname,dataL=value_list,log_id=log_id) 
        elif query22.t_type == "time":
            return render_template('editlogtime.html',data1=data1,tracker_id=tracker_id,data3=tid_to_tname,log_id=log_id)
        elif query22.t_type == "bool":
            return render_template('editlogbool.html',data1=data1,tracker_id=tracker_id,data3=tid_to_tname,log_id=log_id)
        else:
            return render_template('editlog.html',data1=data1,tracker_id=tracker_id,data3=tid_to_tname,log_id=log_id)

    if request.method == "POST":
        log_value=request.form["value"]
        log_note=request.form["note"]
        userid=userid
        tracker_id=tracker_id
        query25=LogTable.query.filter_by(log_id=log_id).one()
        query25.log_note=log_note
        query25.log_value=log_value
        newtime=request.form["newtime"]
        if newtime!="":
            newtime=newtime.replace('T',' ')
            newtime=newtime+':00'
            query25.timestamp=newtime
        db.session.commit()
        url="/"+str(userid)+"/tracker/"+str(tracker_id)
        return redirect(url)
        

@app.route("/<int:userid>/tracker/<int:tracker_id>/log/<int:log_id>/editmul",methods=["POST"])
def log_edit_mulval(userid,tracker_id,log_id):
    if request.method == "POST":
        mul_value=request.form["ansvalue"]
        mul_note=request.form["note"]
        query24=LogTable.query.filter_by(log_id=log_id).one()
        query24.log_note=mul_note
        query24.log_value=mul_value
        newtime=request.form["newtime"]
        if newtime!="":
            newtime=newtime.replace('T',' ')
            newtime=newtime+':00'
            query24.timestamp=newtime
        db.session.commit()
        url="/"+str(userid)+"/tracker/"+str(tracker_id)
        return redirect(url)


@app.route("/<int:userid>/tracker/<int:tracker_id>/log/<int:log_id>/edittime",methods=["POST"])
def log_edit_time(userid,tracker_id,log_id):
    if request.method == "POST":
        hour=request.form["hr"]
        min=request.form["min"]
        note=request.form["note"]
        time_value=str(hour)+" Hr "+str(min)+" Min"
        query26=LogTable.query.filter_by(log_id=log_id).one()
        query26.log_note=note
        query26.log_value=time_value
        newtime=request.form["newtime"]
        if newtime!="":
            newtime=newtime.replace('T',' ')
            newtime=newtime+':00'
            query26.timestamp=newtime
        db.session.commit()
        url="/"+str(userid)+"/tracker/"+str(tracker_id)
        return redirect(url)

@app.route("/<int:userid>/tracker/<int:tracker_id>/delete",methods=["GET","POST"])
def tracker_delete(userid,tracker_id):
    if request.method == "GET":
        query27=LogTable.query.filter_by(userlog_id=userid,tlog_id=tracker_id).all()
        for i in query27:
            db.session.delete(i)
        query28=User_to_Tracker.query.filter_by(user_uid=userid,tracker_tid=tracker_id).one()
        query29=Tracker.query.filter_by(t_owner=userid,t_id=tracker_id).first()
        db.session.delete(query28)
        if query29 == None:
            pass
        else:
            db.session.delete(query29)
        db.session.commit()
        url2="/"+str(userid)+"/dashboard"
        return redirect(url2)
        
@app.route("/<int:userid>/tracker/<int:tracker_id>/edit",methods=["GET","POST"])
def tracker_edit(userid,tracker_id):
    data1={}
    data1['name']=session.get('name')
    data1['userid']=userid
    if request.method == "GET":
        query30=Tracker.query.filter_by(t_id=tracker_id).one()
        if query30.t_owner==userid:
            return render_template('edittracker.html',data1=data1,tracker_id=tracker_id)
        else:
            return render_template('denyedittracker.html',data1=data1)
    if request.method == "POST":
        query31=Tracker.query.filter_by(t_id=tracker_id).one()
        if request.form["tracker_name"] != "":
            query31.t_name=request.form["tracker_name"]
        if request.form["tracker_dscp"] != "":
            query31.t_dscp=request.form["tracker_dscp"]

        db.session.commit()
        url2="/"+str(userid)+"/dashboard"
        return redirect(url2)
        



@app.route("/<int:userid>/logout", methods=["GET","POST"])
def logout(userid):
    session.pop('userid', None)
    session.pop('name', None)
    session.pop('email', None)
    return redirect('/')
