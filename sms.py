from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
from sqlite3 import *
import matplotlib.pyplot as plt
import requests
import bs4

def f1():
	add_window.deiconify()
	main_window.withdraw()

def f2():
	main_window.deiconify()
	add_window.withdraw()
def f3():
	update_window.deiconify()
	main_window.withdraw()
def f4():
	main_window.deiconify()
	update_window.withdraw()
def f5():
	main_window.deiconify()
	view_window.withdraw()
def f6():
	delete_window.deiconify()
	main_window.withdraw()
def f7():
	main_window.deiconify()
	delete_window.withdraw()

def save():
	con = None
	try:
		con = connect('sms.db')
		cursor = con.cursor()
		sql = "insert into student values('%d','%s','%d')"
		rno = int(add_window_ent_rno.get())
		if(rno<0):
			raise Exception("Enter positive integer only")	

		name = add_window_ent_name.get()
		if(len(name)<2):
			raise NameError

		marks = int(add_window_ent_marks.get())
		if(marks<0 or marks>100):
			raise Exception("Marks should be between 0-100")
		cursor.execute(sql % (rno,name,marks))
		con.commit()
		showinfo('Success',"Record Inserted")
		add_window_ent_rno.delete(0,END)                        
		add_window_ent_rno.focus()
		add_window_ent_name.delete(0,END)                        
		add_window_ent_name.focus()
		add_window_ent_marks.delete(0,END)                        
		add_window_ent_marks.focus()

	except ValueError:
		showerror('Failure',"Fill all the boxes")

	except NameError:
		showerror('Failure',"Enter Name correctly")
                       
	except Exception as e:
		showerror('Failure',e)
	finally:

		if con is not None:
			con.close()

def view():
	view_window.deiconify()
	main_window.withdraw()
	view_window_st_data.delete(1.0,END)
	info = ""
	con = None
	try:
		con = connect('sms.db')
		cursor=con.cursor()
		sql="select * from student"
		cursor.execute(sql)
		data = cursor.fetchall()
		for d in data:
			info = info + " rno: "+str(d[0])+" name: "+str(d[1])+" marks: "+str(d[2])+"\n"
		print(info)
		view_window_st_data.insert(INSERT,info)
	except Exception as e:
		showerror('Failure',e)
	finally:

		if con is not None:
			con.close()
		
	


def update():
	con = None
	try:
		con = connect('sms.db')
		cursor = con.cursor()

		rno = int(update_window_ent_rno.get())
		if(rno<0):
			raise Exception("Enter Positive Integer only")
		cursor.execute("SELECT * FROM student WHERE rno ='%d'"%(rno))
		if len(cursor.fetchall()) <= 0:
			raise Exception("Record does not exists")
		
		name = update_window_ent_name.get()
		if(len(name)<2):
			raise NameError

		marks = int(update_window_ent_marks.get())
		if(marks<0 or marks>100):
			raise Exception("Marks should be between 0-100")
		cursor.execute("SELECT * FROM student WHERE rno ='%d'"%(rno))
		if len(cursor.fetchall()) > 0:
			Update="Update student set name='%s',marks='%d' where rno='%d'" %(name,marks,rno)
			cursor.execute(Update)
			con.commit()
			showinfo("Success","Record Update")
		
			
		update_window_ent_rno.delete(0,END)
		update_window_ent_rno.focus()
		update_window_ent_name.delete(0,END)                        
		update_window_ent_name.focus()
		update_window_ent_marks.delete(0,END)                        
		update_window_ent_marks.focus()


	except ValueError:
		showerror('Failure',"Empty boxes not allowed")

	except NameError:
		showerror('Failure',"Enter Name correctly")
                       
	except Exception as e:
		showerror('Failure',e)
	finally:

		if con is not None:
			con.close()


def delete():
	con=None
	try:
		con = connect('sms.db')
		cursor = con.cursor()

		rno = int(delete_window_ent_rno.get())
		if(rno<0):
			raise Exception("Roll No. must be positive integer only")
		cursor.execute("SELECT * FROM student WHERE rno ='%d'"%(rno))
		if len(cursor.fetchall()) > 0:
			Delete="delete from student where rno='%d'" %(rno)
			cursor.execute(Delete)
			con.commit()
			showinfo("Success","Record Deleted")
		else:
			raise Exception("Record does not exists")
		delete_window_ent_rno.delete(0,END)
		delete_window_ent_rno.focus()

	except ValueError:
		showerror('Failure',"Empty boxes not allowed")		
	except Exception as e:
		showerror('Failure',e)
	finally:

		if con is not None:
			con.close()

def charts():
	con=None
	name=[]
	marks=[]
	try:
		con = connect('sms.db')
		cursor = con.cursor()
		cursor.execute("SELECT * FROM student")
		records=cursor.fetchall()
		for rows in records:
			na=rows[1]
			name.append(na)
			ma=rows[2]
			marks.append(ma)
		plt.bar(name,marks,color=['red','green','blue'])
		plt.title("Batch Information")
		plt.ylabel('Marks')
		plt.show()

		

	except Exception as e:
		showerror('Failure',e)
	finally:

		if con is not None:
			con.close()
	
	


	


#MAIN WINDOW
main_window = Tk()
main_window.configure(background='light green')
main_window.title("S.M.S.")
main_window.geometry("600x600+400+100")

main_window_btn_add = Button(main_window, text="Add", font=('Arial',20,'bold'),width=7,command=f1)
main_window_btn_view = Button(main_window, text="View", font=('Arial',20,'bold'),width=7,command=view)
main_window_btn_update = Button(main_window, text="Update", font=('Arial',20,'bold'),width=7,command=f3)
main_window_btn_delete = Button(main_window, text="Delete", font=('Arial',20,'bold'),width=7,command=f6)
main_window_btn_charts = Button(main_window, text="Charts", font=('Arial',20,'bold'),width=7,command=charts)


main_window_btn_add.pack(pady=5)
main_window_btn_view.pack(pady=5)
main_window_btn_update.pack(pady=5)
main_window_btn_delete.pack(pady=5)
main_window_btn_charts.pack(pady=5)

canvas_width = 600
canvas_height =600
canvas = Canvas(main_window, width=canvas_width, height=canvas_height)
canvas.configure(background='light green')



r1 = canvas.create_rectangle(20,30,550,80)
t1 = canvas.create_text(85,50, text="Location : ",font=('Arial',20))

try:
	wa = "https://ipinfo.io/"
	res = requests.get(wa)

	data = res.json()

	city_name = data['city']
	t4 = canvas.create_text(200,50, text=city_name,font=('Arial',20))
	t5 = canvas.create_text(350,50, text="Temp : ",font=('Arial',20))

	
	a1 = "http://api.openweathermap.org/data/2.5/weather?units=metric"
	a2 = "&q=" + city_name
	a3 = "&appid=" + "c6e315d09197cec231495138183954bd"

	x = a1+a2+a3
	request = requests.get(x)


	data = request.json()

	

	main = data['main']

	temp = main['temp']
	t6 = canvas.create_text(440,50, text=temp,font=('Arial',20))


except Exception as e:
	print("issue ",e)


r2 = canvas.create_rectangle(20,100,550,200)
t2 = canvas.create_text(150,120, text="Quote Of The Day : ",font=('Arial',20))
try:
	wa = "https://www.brainyquote.com/quote_of_the_day"
	res = requests.get(wa)
	

	data = bs4.BeautifulSoup(res.text, 'html.parser')
	

	info = data.find('img',{'class':'p-qotd'})
	

	msg = info['alt']




except Exception as e:
	print("issue",e)

t3 = canvas.create_text(285,150, text=msg)

canvas.pack()


#ADD WINDOW
add_window = Toplevel(main_window)
add_window.title("Add St.")
add_window.geometry("600x600+400+100")
add_window.configure(background='light blue')

add_window_lbl_rno = Label(add_window, text="Enter Roll No.", font=('Arial',20,'bold'))
add_window_ent_rno = Entry(add_window,bd=5, font=('Arial',20,'bold'))
add_window_lbl_name = Label(add_window, text="Enter Name", font=('Arial',20,'bold'))
add_window_ent_name = Entry(add_window,bd=5, font=('Arial',20,'bold'))
add_window_lbl_marks = Label(add_window, text="Enter Marks", font=('Arial',20,'bold'))
add_window_ent_marks = Entry(add_window,bd=5, font=('Arial',20,'bold'))
add_window_btn_save = Button(add_window, text="Save", font=('Arial',20,'bold'),command=save)
add_window_btn_back = Button(add_window, text="Back", font=('Arial',20,'bold'),command=f2)

add_window_lbl_rno.pack(pady=5)
add_window_ent_rno.pack(pady=5)
add_window_lbl_name.pack(pady=5)
add_window_ent_name.pack(pady=5)
add_window_lbl_marks.pack(pady=5)
add_window_ent_marks.pack(pady=5)
add_window_btn_save.pack(pady=5)
add_window_btn_back.pack(pady=5)
add_window.withdraw()

#UPDATE WINDOW
update_window = Toplevel(main_window)
update_window.title("Update St.")
update_window.geometry("600x600+400+100")
update_window.configure(background='light pink')

update_window_lbl_rno = Label(update_window, text="Enter Roll No.", font=('Arial',20,'bold'))
update_window_ent_rno = Entry(update_window,bd=5, font=('Arial',20,'bold'))
update_window_lbl_name = Label(update_window, text="Enter Name", font=('Arial',20,'bold'))
update_window_ent_name = Entry(update_window,bd=5, font=('Arial',20,'bold'))
update_window_lbl_marks = Label(update_window, text="Enter Marks", font=('Arial',20,'bold'))
update_window_ent_marks = Entry(update_window,bd=5, font=('Arial',20,'bold'))
update_window_btn_save = Button(update_window, text="Save", font=('Arial',20,'bold'),command=update)
update_window_btn_back = Button(update_window, text="Back", font=('Arial',20,'bold'),command=f4)

update_window_lbl_rno.pack(pady=5)
update_window_ent_rno.pack(pady=5)
update_window_lbl_name.pack(pady=5)
update_window_ent_name.pack(pady=5)
update_window_lbl_marks.pack(pady=5)
update_window_ent_marks.pack(pady=5)
update_window_btn_save.pack(pady=5)
update_window_btn_back.pack(pady=5)
update_window.withdraw()

#DELETE WINDOW
delete_window = Toplevel(main_window)
delete_window.title("Delete St.")
delete_window.geometry("600x600+400+100")
delete_window.configure(background='light blue')

delete_window_lbl_rno = Label(delete_window, text="Enter Roll No.", font=('Arial',20,'bold'))
delete_window_ent_rno = Entry(delete_window,bd=5, font=('Arial',20,'bold'))

delete_window_btn_delete = Button(delete_window, text="Delete", font=('Arial',20,'bold'),command=delete)
delete_window_btn_back = Button(delete_window, text="Back", font=('Arial',20,'bold'),command=f7)

delete_window_lbl_rno.pack(pady=5)
delete_window_ent_rno.pack(pady=5)
delete_window_btn_delete.pack(pady=5)
delete_window_btn_back.pack(pady=5)
delete_window.withdraw()

#VIEW WINDOW
view_window = Toplevel(main_window)
view_window.title("View St.")
view_window.geometry("600x600+400+100")
view_window.configure(background='light yellow')

view_window_st_data = ScrolledText(view_window,width=30,height=10,font=('Arial',20,'bold'))
view_window_btn_back = Button(view_window, text="Back", font=('Arial',20,'bold'),command=f5)

view_window_st_data.pack(pady=10)
view_window_btn_back.pack(pady=10)
view_window.withdraw()






main_window.mainloop()