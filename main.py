from flet import *
import sqlite3

# CONNECT TO DB
conn = sqlite3.connect("db/dbfood.db",check_same_thread=False)
cur = conn.cursor()

class Youclass(UserControl):
	def __init__(self):
		super().__init__()
		# LIST DATA
		self.alldata = Column()
		self.addData = TextField(label="add new data")
		self.editData = TextField(label="Edit data")

	# PROSES DELETE DATA
	def prosesDelete(self,x,b):
		# X AND B IS PARAM FOR FUNCTION
		cur.execute("delete from mainan where id = ? ",[x])
		conn.commit()
		# CLOSE YOU ALERT DIALOG
		b.open = False

		# CALL renderAll FUNCTION AGAIN FOR REFRESH THE DATA
		self.alldata.controls.clear()
		self.renderAll()
		self.page.update()



	# PROSES EDIT DATA

	def prosesEdit(self,a,x,b):
		print("a is" ,a)
		print("x is" ,x)
		print("b is" ,b)
		cur.execute("update mainan SET name = ? where id = ?",(x,a))
		conn.commit()
		# CLOSE YOU ALERT DIALOG
		b.open = False

		# CALL renderAll FUNCTION AGAIN FOR REFRESH THE DATA
		self.alldata.controls.clear()
		self.renderAll()
		self.page.update()



	def OpenYOuAction(self,e):
		# GET ID FROM DATA 
		id_edit = e.control.subtitle.value
		# EDIT TEXTEDIT TO VALUE NAME FROM LISTTILE
		self.editData.value = e.control.title.value
		self.update()

		# OPEN ALERT DIALOG
		alert_dialog = AlertDialog(
		title=Text(f"Edit id {id_edit}"),
		content=self.editData,
		# BUTTON ACTIONS
		actions = [
		# DELETE DATA
		ElevatedButton("Delete data",
		color="white",bgcolor="red",
		on_click=lambda e:self.prosesDelete(id_edit,alert_dialog)
		),
		# EDIT BUTTON
		TextButton("Save Edit",
		on_click=lambda e:self.prosesEdit(id_edit,self.editData.value,alert_dialog)	
		)
		],
		actions_alignment="spaceBetween",
		)
		self.page.dialog = alert_dialog
		alert_dialog.open = True
		# UPDATE DATA
		self.page.update()



	# RENDER TO PUSH TO WIDGET FETCH

	def renderAll(self):
		cur.execute("select * from mainan")
		# conn.commit()
		mydata = cur.fetchall()
		for x in mydata:
			self.alldata.controls.append(
				ListTile(
					# GET NAME
				title=Text(x[1]),
				# GET ID 
				subtitle=Text(x[0]),
				on_click=self.OpenYOuAction
				)

			)
		self.update()

	# LIFECYCLE FOR CALL RENDERALL 
	def did_mount(self):
		self.renderAll()


	def funaddNew(self,e):
		cur.execute("insert into mainan (name) values (?)",[self.addData.value])
		conn.commit()
		# CLEAR DATA AND CALL AGAIN
		self.alldata.controls.clear()
		self.renderAll()
		self.page.update()


	def build(self):
		return Column([
			Text("CRUD SQLITE",size=30),
			self.addData,
			ElevatedButton("Add new data",
			on_click=self.funaddNew

				),
			# SEE ALLDATA
			self.alldata 



			])

def main(page:Page):
	page.update()
	youclass = Youclass()
	page.add(youclass)

flet.app(target=main)
