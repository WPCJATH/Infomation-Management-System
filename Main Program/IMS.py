# -*- coding: utf-8 -*- 
import tkinter 
from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfilename
from PIL import Image
from PIL import ImageTk
import sqlite3
import matplotlib.pyplot as plt
import matplotlib.image as mping
import os
from tkinter.filedialog import askdirectory
import datetime

# store information of all staffs in lists
staff_info=[]
# store information of all departs in lists
depart_info=[]
# store the information of current staff or department
curr_info=[]

# connect to the database
content=sqlite3.connect('data.db')
# create the cursor
cur=content.cursor()

# main window
root = tkinter.Tk()
root.title('Information Management System')
root.minsize(910,615)
root.resizable(False, False)

# frame at top 
top=tkinter.Frame(root,height=30)
top['bg']='#F8F8FF'
top.pack(side='top',fill=X)
top=tkinter.Frame(root,height=30)

# frame at buttom
bottom=tkinter.Frame(root,height=30)
bottom['bg']='#F8F8FF'
bottom.pack(side='bottom',fill=X)

# frame of tree which is in the sidebar to show the relationships of departs and staffs
frameOfTree=tkinter.Frame(root,width=160)
frameOfTree.pack(side='left',fill=Y)

# scrollerbar for sidebar
scrollerbarY=Scrollbar(frameOfTree)
scrollerbarY.pack(fill=Y,side='right')
scrollerbarX=Scrollbar(frameOfTree,orient=HORIZONTAL)
scrollerbarX.pack(fill=X,side='bottom')

# the state to store a whether a temporary pic file is exist 
state=False

def main():
    # read and extract all infomation of database
    get_info()
    # open the welcome page
    welcome()
    # import the relationship into treeview
    tree.insert('',0,text='-------------Bottom------'+'-'*50)
    init_tree()

def get_info():
    # extract information of departs
    cur.execute("SELECT * FROM `Depart`")   ##`Depart`(`ID`,`CD`,`Name`,`SettingTime`,`Intro`)
    for i in cur.fetchall():
        depart_info.append(list(i))
    # extratct information of staffs
    cur.execute("SELECT * FROM `Staff`")    ##`Staff`(`StaffID`,`CD`,`Name`,`Gender`,`ID`,`Duty`,`Rank`,`Speciality`,`Pic`,`Date`)
    for i in cur.fetchall():
        staff_info.append(list(i)) 
    

# global varible for store the current 2nd tree temporarily
tree2=''
# init the treeveiw in a recursive way
def init_tree(code1=None,num2=0):
    global tree2
    for i in depart_info:
        if i[0]==code1:     
            tree1=tree.insert(tree2,num2,text='__'+i[2]+': ')
            num1=0
            for k in staff_info:
                if k[0]==i[1]:
                    tree.insert(tree1,num1,text=k[2])
                    num1+=1
            code2=i[1]

            for j in depart_info:
                if j[0]==code2:
                    tree2=tree.insert(tree1,num1,text='__'+j[2]+': ')
                    num1+=1
                    code3=j[1]
                    num2=0
                    for k in staff_info:
                        if k[0]==j[1]:
                            tree.insert(tree2,num2,text=k[2])
                            num2+=1
                    init_tree(code3,num2)


# when system inited, the welcome page will be shown to the user
def welcome():
    #show the welcome page
    conRepo=tkinter.Label(top2,text='Welcome',width=20,bg='white')
    conRepo.pack(fill=Y,side='left')

    empty1=tkinter.Label(top2,width=60)
    empty1.pack(fill=Y,side='left')
    #the 'help' buttom
    button1=tkinter.Button(top2,text='Help',width=20,bg='#7FFFD4',command = lambda :help())
    button1.pack(fill=Y,side='left')

    welcome=tkinter.Label(maincontent,text='Welcome to using the Information Management System',width=60,height=5,bg='#98F5FF',font=40)
    welcome.place(x=70,y=180)

# the help page after the user clicking the 'help' buttom            
def help():
    #User guide
    help=tkinter.Tk()
    help.title('User Guide')
    help.minsize(630,420)
    help.resizable(False, False)
    ins='''
    1. Click the name of the left department or the employee's name to see the relevant department and employee information.
    2. The information interface can be deleted, modified, or directly added to the department or staff at the display information interface.
    3. employees photos can be replaced with local files.
    4. the program will read the competent department code to attribute employees or departments to the corresponding competent authorities.
    5.The removal department will cause all employees under the department to be deleted.
    6. modifying or adding information needs to be confirmed, otherwise the input will not be saved.
    '''
    conten=tkinter.Label(help,text=ins,justify=LEFT)
    conten.pack(fill=BOTH)

# Bind the event for the frame of tree
def clickTree(event):
    curItem = tree.focus()
    #print(tree.item(curItem)['text'])
    show(tree.item(curItem)['text'])

# show the corresponding page after clicking on frame of tree
def show(text):
    global curr_info
    for i in depart_info:
        if text=='__'+i[2]+': ':
            curr_info=i
            show_depart()
    for i in staff_info:
        if text==i[2]:
            curr_info=i
            show_staff()

# show the depart infomation
def show_depart():
    global maincontent
    global top2
    global curr_info
    des()
    info=curr_info

    conRepo=tkinter.Label(top2,text='Depart Info.',width=20,bg='white')
    conRepo.pack(fill=Y,side='left')

    empty1=tkinter.Label(top2,width=60)
    empty1.pack(fill=Y,side='left')

    button1=tkinter.Button(top2,text='New Depart',width=20,bg='#7FFFD4',command = lambda :depart_modi('new'))
    button1.pack(fill=Y,side='left')

    staffcode1=tkinter.Label(maincontent,text='Name of Depart: ',height=2,width=20,bg='#FFFFF0')
    staffcode1.place(x=0,y=50)
    staffcode2=tkinter.Label(maincontent,text=info[2],height=2,width=30,bg='white')
    staffcode2.place(x=147,y=50)
    gender1=tkinter.Label(maincontent,text='Code of Depart: ',height=2,width=20,bg='#FFFFF0')
    gender1.place(x=368,y=50)
    gender2=tkinter.Label(maincontent,text=info[1],height=2,width=30,bg='white')
    gender2.place(x=515,y=50)
    name1=tkinter.Label(maincontent,text='Charge Depart: ',height=2,width=20,bg='#FFFFF0')
    name1.place(x=0,y=150)
    name2=tkinter.Label(maincontent,text=get_depart(info[0]),height=2,width=30,bg='white')
    name2.place(x=147,y=150)
    depart1=tkinter.Label(maincontent,text='Code of Charge Depart: ',height=2,width=20,bg='#FFFFF0')
    depart1.place(x=368,y=150)
    depart2=tkinter.Label(maincontent,text=info[0],height=2,width=30,bg='white')
    depart2.place(x=515,y=150)
    strong1=tkinter.Label(maincontent,text='Intro.:  ',height=2,width=20,bg='#FFFFF0')
    strong1.place(x=0,y=250)
    strong2=tkinter.Label(maincontent,text=info[4],height=5,width=50,bg='white')
    strong2.place(x=35,y=300)
    date1=tkinter.Label(maincontent,text='Built-up Time: ',height=2,width=20,bg='#FFFFF0')
    date1.place(x=368,y=250)
    date2=tkinter.Label(maincontent,text=info[3],height=2,width=30,bg='white')
    date2.place(x=515,y=250)
    modify=tkinter.Button(maincontent,text='Modify',height=1,width=10,bg='gray',command = lambda :depart_modi())
    modify.place(x=515,y=330)
    delete=tkinter.Button(maincontent,text='Delete',height=1,width=10,bg='gray',command = lambda: delete_(get_staff(info[1]),info[1]) )
    delete.place(x=515,y=400)

#Set the input box
a,b,c,d,e,f,g,h=StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar()
i=''
j=''
# show the info of depart in modifing model
def depart_modi(state='old'):
    global maincontent
    global top2
    global curr_info
    global a,b,c,d,e,f
    # destroy the previous page
    des()
    content=curr_info
    conRepo=tkinter.Label(top2,text='Info of Depart',width=20,bg='white')
    conRepo.pack(fill=Y,side='left')

    empty1=tkinter.Label(top2,width=60)
    empty1.pack(fill=Y,side='left')

    if state=='old':
        button1=tkinter.Button(top2,text='Cancel',width=20,bg='#7FFFD4',command = lambda :show_depart())
        button1.pack(fill=Y,side='left')
        a.set(content[2])
        b.set(content[1])
        c.set(get_depart(content[0]))
        d.set(content[0])
        e.set(content[4])
        f.set(content[3])
    else:
        button1=tkinter.Button(top2,text='Cancel',width=20,bg='#7FFFD4',command = lambda :show_depart())
        button1.pack(fill=Y,side='left')
        a.set('')
        b.set('')
        c.set('')
        d.set('')
        e.set('')
        f.set('')
        
 
    
    staffcode1=tkinter.Label(maincontent,text='Name of Depart: ',height=2,width=20,bg='#FFFFF0')
    staffcode1.place(x=0,y=50)
    staffcode2=tkinter.Entry(maincontent,width=30,bg='white',textvariable = a)
    staffcode2.place(x=147,y=62)
    gender1=tkinter.Label(maincontent,text='Code of Depart: ',height=2,width=20,bg='#FFFFF0')
    gender1.place(x=368,y=50)
    gender2=tkinter.Entry(maincontent,width=30,bg='white',textvariable = b)
    gender2.place(x=515,y=62)
    name1=tkinter.Label(maincontent,text='Charge Depart: ',height=2,width=20,bg='#FFFFF0')
    name1.place(x=0,y=150)
    name2=tkinter.Entry(maincontent,width=30,bg='white',textvariable = c)
    name2.place(x=147,y=162)
    depart1=tkinter.Label(maincontent,text='Code of Charge Depart: ',height=2,width=20,bg='#FFFFF0')
    depart1.place(x=368,y=150)
    depart2=tkinter.Entry(maincontent,width=30,bg='white',textvariable = d)
    depart2.place(x=515,y=162)
    strong1=tkinter.Label(maincontent,text='Intro:  ',height=2,width=20,bg='#FFFFF0')
    strong1.place(x=0,y=250)
    strong2=tkinter.Entry(maincontent,width=40,bg='white',textvariable = e)
    strong2.place(x=120,y=312)
    date1=tkinter.Label(maincontent,text='Built-up Time: ',height=2,width=20,bg='#FFFFF0')
    date1.place(x=368,y=250)
    date2=tkinter.Entry(maincontent,width=30,bg='white',textvariable = f)
    date2.place(x=515,y=250)
    if state=='old':
        modify=tkinter.Button(maincontent,text='Confirm',height=1,width=10,bg='gray',command = lambda :depart_update('old'))
        modify.place(x=515,y=330)
    else:
        modify=tkinter.Button(maincontent,text='Confirm',height=1,width=10,bg='gray',command = lambda :depart_update('new'))
        modify.place(x=515,y=330)
    delete=tkinter.Button(maincontent,text='Cancel',height=1,width=10,bg='gray',command = lambda :show_depart())
    delete.place(x=515,y=400)


# Built for storing the data of pics 
img=''
im=''
# The page to show the info of Staffs
def show_staff():
    global maincontent
    global top2
    global curr_info
    global im,img
    global state
    state=True
    # destroy the previous page
    des()
    info=curr_info

    conRepo=tkinter.Label(top2,text='Info of Staff',width=20,bg='white')
    conRepo.pack(fill=Y,side='left')

    empty1=tkinter.Label(top2,width=60)
    empty1.pack(fill=Y,side='left')

    button1=tkinter.Button(top2,text='New Staff',width=20,bg='#7FFFD4',command = lambda :staff_modi('new'))
    button1.pack(fill=Y,side='left')

    # `StaffID`,`CD`,`Name`,`Gender`,`ID`,`Duty`,`Rank`,`Speciality`,`Pic`,`Date`
    staffcode1=tkinter.Label(maincontent,text='Staff ID: ',height=2,width=20,bg='#FFFFF0')
    staffcode1.place(x=0,y=0)
    staffcode2=tkinter.Label(maincontent,text=info[0],height=2,width=30,bg='white')
    staffcode2.place(x=147,y=0)
    gender1=tkinter.Label(maincontent,text='Gender: ',height=2,width=20,bg='#FFFFF0')
    gender1.place(x=368,y=0)
    gender2=tkinter.Label(maincontent,text=info[3],height=2,width=30,bg='white')
    gender2.place(x=515,y=0)
    name1=tkinter.Label(maincontent,text='Name: ',height=2,width=20,bg='#FFFFF0')
    name1.place(x=0,y=50)
    name2=tkinter.Label(maincontent,text=info[2],height=2,width=30,bg='white')
    name2.place(x=147,y=50)
    depart1=tkinter.Label(maincontent,text='Depart: ',height=2,width=20,bg='#FFFFF0')
    depart1.place(x=368,y=50)
    depart2=tkinter.Label(maincontent,text=get_depart(info[1]),height=2,width=30,bg='white')
    depart2.place(x=515,y=50)
    id1=tkinter.Label(maincontent,text='HKID: ',height=2,width=20,bg='#FFFFF0')
    id1.place(x=0,y=100)
    id2=tkinter.Label(maincontent,text=info[4],height=2,width=30,bg='white')
    id2.place(x=147,y=100)
    work1=tkinter.Label(maincontent,text='Duty: ',height=2,width=20,bg='#FFFFF0')
    work1.place(x=0,y=150)
    work2=tkinter.Label(maincontent,text=info[5],height=2,width=30,bg='white')
    work2.place(x=147,y=150)
    rank1=tkinter.Label(maincontent,text='Rank: ',height=2,width=20,bg='#FFFFF0')
    rank1.place(x=0,y=200)
    rank2=tkinter.Label(maincontent,text=info[6],height=2,width=30,bg='white')
    rank2.place(x=147,y=200)
    strong1=tkinter.Label(maincontent,text='Specialities:  ',height=2,width=20,bg='#FFFFF0')
    strong1.place(x=0,y=250)
    strong2=tkinter.Label(maincontent,text=info[7],height=5,width=50,bg='white')
    strong2.place(x=35,y=300)
    modify=tkinter.Button(maincontent,text='Modify',height=1,width=10,bg='gray',command = lambda :staff_modi())
    modify.place(x=489,y=450)
    staff=[]
    staff.append(curr_info[1])
    delete1=tkinter.Button(maincontent,text='Delete',height=1,width=10,bg='gray',command = lambda :delete_(staff))
    delete1.place(x=600,y=450)

    file=open('pic.jpg','wb')
    file.write(info[8])
    file.close()
    im=Image.open('pic.jpg')
    img=ImageTk.PhotoImage(im)
    date1=tkinter.Label(maincontent,text='Update:',height=1,width=10,bg='#FFFFF0')
    date1.place(x=470,y=350)
    date2=tkinter.Label(maincontent,text=info[9],height=1,width=10,bg='#FFFFF0')
    date2.place(x=535,y=350)
    pic=tkinter.Label(maincontent,height=210,width=150,image=img)
    pic.place(x=470,y=125)
    pic.config(image=img)
    pic.image = img

    
    
def staff_modi(state='old'):
    global maincontent
    global top2
    global curr_info
    global a,b,c,d,e,f,g,h,i
    global im,img
    des()
    content=curr_info

    conRepo=tkinter.Label(top2,text='Info of Staff',width=20,bg='white')
    conRepo.pack(fill=Y,side='left')

    empty1=tkinter.Label(top2,width=60)
    empty1.pack(fill=Y,side='left')

    if state=='old':
        button1=tkinter.Button(top2,text='Cancel',width=20,bg='#7FFFD4',command = lambda :show_staff())
        button1.pack(fill=Y,side='left')
        # `StaffID`,`CD`,`Name`,`Gender`,`ID`,`Duty`,`Rank`,`Speciality`,`Pic`,`Date`
        a.set(content[0])
        b.set(content[3])
        c.set(content[2])
        d.set(get_depart(content[1]))
        e.set(content[4])
        f.set(content[5])
        g.set(content[6])
        h.set(content[7])
        i=content[8]
        j=content[9]
    else:
        button1=tkinter.Button(top2,text='Cancel',width=20,bg='#7FFFD4',command = lambda :show_staff())
        button1.pack(fill=Y,side='left')
        a.set('')
        b.set('')
        c.set('')
        d.set('')
        e.set('')
        f.set('')
        g.set('')
        h.set('')
        i=''
        j=''

    staffcode1=tkinter.Label(maincontent,text='Staff ID: ',height=2,width=20,bg='#FFFFF0')#{a:staffid,b:gender,c:name,d:depart,e=id,work=f,rank=g,techang=h,i=pic}
    staffcode1.place(x=0,y=0)
    staffcode2=tkinter.Entry(maincontent,width=30,bg='white',textvariable=a)
    staffcode2.place(x=147,y=12)
    gender1=tkinter.Label(maincontent,text='Gender: ',height=2,width=20,bg='#FFFFF0')
    gender1.place(x=368,y=0)
    gender2=tkinter.Entry(maincontent,width=30,bg='white',textvariable=b)
    gender2.place(x=515,y=12)
    name1=tkinter.Label(maincontent,text='Name: ',height=2,width=20,bg='#FFFFF0')
    name1.place(x=0,y=50)
    name2=tkinter.Entry(maincontent,width=30,bg='white',textvariable=c)
    name2.place(x=147,y=62)
    depart1=tkinter.Label(maincontent,text='Depart: ',height=2,width=20,bg='#FFFFF0')
    depart1.place(x=368,y=50)
    depart2=tkinter.Entry(maincontent,width=30,bg='white',textvariable=d)
    depart2.place(x=515,y=62)
    id1=tkinter.Label(maincontent,text='HKID: ',height=2,width=20,bg='#FFFFF0')
    id1.place(x=0,y=100)
    id2=tkinter.Entry(maincontent,width=30,bg='white',textvariable=e)
    id2.place(x=147,y=112)
    work1=tkinter.Label(maincontent,text='Duty: ',height=2,width=20,bg='#FFFFF0')
    work1.place(x=0,y=150)
    work2=tkinter.Entry(maincontent,width=30,bg='white',textvariable=f)
    work2.place(x=147,y=162)
    rank1=tkinter.Label(maincontent,text='Rank: ',height=2,width=20,bg='#FFFFF0')
    rank1.place(x=0,y=200)
    rank2=tkinter.Entry(maincontent,width=30,bg='white',textvariable=g)
    rank2.place(x=147,y=212)
    strong1=tkinter.Label(maincontent,text='Specialities:  ',height=2,width=20,bg='#FFFFF0')
    strong1.place(x=0,y=250)
    strong2=tkinter.Entry(maincontent,width=40,bg='white',textvariable=h)
    strong2.place(x=120,y=300)
    if state=='new':
        modify=tkinter.Button(maincontent,text='Confirm',height=1,width=10,bg='gray',command = lambda :update_staff('new'))
        modify.place(x=489,y=450)
    else:
        modify=tkinter.Button(maincontent,text='Confirm',height=1,width=10,bg='gray',command = lambda :update_staff())
        modify.place(x=489,y=450)
    delete=tkinter.Button(maincontent,text='Cancel',height=1,width=10,bg='gray',command = lambda :show_staff())
    delete.place(x=600,y=450)

    if state=='old':
        changepic=tkinter.Button(maincontent,text='Change Pic',height=1,width=10,bg='gray',command = lambda: selpic())
        changepic.place(x=500,y=350)
        file=open('pic.jpg','wb')
        file.write(i)
        file.close()
        im=Image.open('pic.jpg')
        img=ImageTk.PhotoImage(im)
        pic=tkinter.Label(maincontent,height=210,width=150,image=img)
        pic.place(x=470,y=125)
        pic.config(image=img)
        pic.image = img
    else:
        changepic=tkinter.Button(maincontent,text='New Pic',height=1,width=10,bg='gray',command = lambda: selpic())
        changepic.place(x=500,y=350)
        pic=tkinter.Label(maincontent,height=10,width=18,text='Pic')
        pic.place(x=470,y=125)

# known the depart id then get the depart name
def get_depart(id):
    global depart_info
    if id==None:
        return id
    else:
        for i in depart_info:
            if i[1]==id:
                break
        return i[2]


# update the infomation of depart into the database
def depart_update(state='old'):
    global curr_info
    global a,b,d,e,f
    global cur
    global content
    new_info=[d.get(),b.get(),a.get(),f.get(),e.get()]
    if state=='old':
        for i in range(5):
            if new_info[i]=='None':
                new_info[i]=None
        title=['`ID`','`CD`','`Name`','`SettingTime`','`Intro`']
        for i in range(5):
            if new_info[i]!=curr_info[i]:
                print(title[i],new_info[i],curr_info[1])
                wa='update `Depart` set '
                wb=title[i]
                wc=' = ? where `ID` = ?'
                cur.execute(wa+wb+wc,(new_info[i],curr_info[1]))
    else:
        cur.execute("INSERT INTO `Depart` values(?,?,?,?,?)",(new_info[0],new_info[1],new_info[2],new_info[3],new_info[4]))
    content.commit()
    fresh()
    curr_info=new_info
    show_depart()


# update the info of an old staff in the database or create the info for a new staff
def update_staff(state='old'):
    #{a:workid,b:gender,c:name,d:depart,e=id,work=f,rank=g,techang=h,i=pic,date}
    global curr_info
    global a,b,c,d,e,f,g,h,i,j
    global cur
    global content
    new_info=[a.get(),get_deid(d.get()),c.get(),b.get(),e.get(),f.get(),g.get(),h.get(),i,j]
    # `StaffID`,`CD`,`Name`,`Gender`,`ID`,`Duty`,`Rank`,`Speciality`,`Pic`,`Date`
    for i in range(10):
        if new_info[i]=='None' or new_info[i]=='':
            new_info[i]=None
    title=['`StaffID`','`CD`','`Name`','`Gender`','`ID`','`Duty`','`Rank`','`Speciality`','`Pic`','`Date`']
    if state=='old':
        for index in range(len(curr_info)):
            if curr_info[index]!=new_info[index]:
                wa='update `Staff` set '
                wb=title[index]
                wc='= ? where `StaffID` = ?'
                cur.execute(wa+wb+wc,(new_info[index],curr_info[1]))
    else:
        cur.execute("INSERT INTO `Staff` values(?,?,?,?,?,?,?,?,?,?)",(new_info[0],new_info[1],new_info[2],new_info[3],new_info[4],new_info[5],new_info[6],new_info[7],new_info[8],new_info[9]))
    
    content.commit()
    fresh()
    curr_info=new_info
    show_staff()

# given the name of a staff, return the id of the staff
def get_deid(name):
    global depart_info
    for i in depart_info:
        if i[2]==name:
            break
    return i[1]
    
# delete staffs and departs
def delete_(staff,depart=None):
    global cur
    global content
    for i in staff:
        cur.execute('delete from `Staff` where `StaffID` = ?',(i,))
    if depart!=None:
        cur.execute('delete from `Depart` where `ID` = ?',(depart,))
    content.commit()
    fresh()

# select a pic locally
def selpic():
    global i,j
    path=askopenfilename()
    if path:
        date=datetime.datetime.now().strftime('%Y/%m/%d')
        j=date.encode('utf-8')
        #print(j)
        file=Image.open(path)
        new_file=file.resize((150,210),Image.ANTIALIAS)
        new_file=new_file.convert('RGB')
        new_file.save(path)
        file.close()
        im=Image.open(path)
        img=ImageTk.PhotoImage(im)
        pic=tkinter.Label(maincontent,height=210,width=150,image=img)
        pic.place(x=470,y=125)
        pic.config(image=img)
        pic.image = img

# know the departID, the all staff ids of staffs of it
def get_staff(depart):
    global staff_info
    staff=[]
    for i in staff_info:
        if depart==i[0]:
            staff.append(i[1])
    return staff

# refresh the page
def fresh():
    des()
    global tree
    global tree2
    global depart_info
    global staff_info
    global curr_info
    global counter
    global new2

    depart_info.clear()
    staff_info.clear()
    curr_info.clear()
    counter=dict()
    new2=''
    tree.destroy()
    tree2 = ''

    tree=Treeview(frameOfTree,selectmode = "extended")
    tree['yscrollcommand'] = scrollerbarY.set
    tree['xscrollcommand'] = scrollerbarX.set
    scrollerbarY.config(command=tree.yview)
    scrollerbarX.config(command=tree.xview)
    tree.bind("<<TreeviewSelect>>", clickTree)
    tree.pack(side='left',fill=Y)
    main()

# destroy the previous page
def des():
    global maincontent
    global top2
    maincontent.destroy()
    top2.destroy()

    maincontent=tkinter.Frame(root,height=500,bg='#FFFFF0')
    maincontent.pack(side='bottom',fill=X)

    top2=tkinter.Frame(root,bg='#F5F5F5')
    top2.pack(fill=BOTH,side='left')


#tree
tree=Treeview(frameOfTree,selectmode = "extended")
tree['yscrollcommand'] = scrollerbarY.set
tree['xscrollcommand'] = scrollerbarX.set
scrollerbarY.config(command=tree.yview)
scrollerbarX.config(command=tree.xview)
tree.bind("<<TreeviewSelect>>", clickTree)
tree.pack(side='left',fill=BOTH)
#main frame of the whole window
maincontent=tkinter.Frame(root,height=500,bg='#FFFFF0')
maincontent.pack(side='bottom',fill=X)
#top frame
top2=tkinter.Frame(root,bg='#F5F5F5')
top2.pack(fill=BOTH,side='left')



main()


root.mainloop()
#close sqlite
cur.close()
content.close()
if state==False:
    file=open('pic.jpg','wb')
    file.close()
os.remove('pic.jpg')
