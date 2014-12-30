#encoding=utf-8
import web
import sys
import MySQLdb
import MySQLdb.cursors
import time

reload(sys)
sys.setdefaultencoding('utf-8')
render = web.template.render('templates/')

urls = (
    '/', 'index' ,
	'/problem' , 'problem' ,
	'/register' , 'register' , 
	'/user' , 'user' ,
	'/manage' , 'manage',
	'/new' , 'new' ,
	'/edit' , 'edit' ,
	'/delete' , 'delete' ,
	'/group' , 'group',
	'/join' , 'join' ,
	'/favo' , 'favo' ,
	'/message' , 'message'
)

conn = MySQLdb.connect(
	host='localhost',
	user='root',
	passwd='zxa',
	db='Marshtomp',
	#port=3306,
	charset='utf8',
	cursorclass = MySQLdb.cursors.DictCursor
)

def run_sql(sql):
	print sql
	cur = conn.cursor()	
	cur.execute(sql)
	conn.commit()
	cur.close()

def get_one_sql(sql):
	print sql
	cur = conn.cursor()	
	cur.execute(sql)
	result =cur.fetchone()
	conn.commit()
	cur.close()
	return result

def get_all_sql(sql):	
	print sql
	cur = conn.cursor()	
	cur.execute(sql)
	result =cur.fetchall()
	conn.commit()
	cur.close()
	print '*****';
	print result
	return result

def drop(typ,id):
	sql = "delete from %s where id=%s;"%(typ,id)
	run_sql(sql)
	return

def new_user(user):
	sql = "insert into user value(null,'%s','%s','%s','%s','%s','%s');"%(user['name'],user['psword'],user['gender'],user['email'],user['school'],user['major'])
	run_sql(sql)
	return user['name']

def login(name):
	web.setcookie('name',name,3600)
	return 

def login_admin(name):
	login(name)
	web.setcookie('admin',"1",3600)
	return 

def logout():
	web.setcookie('name',"",-1)
	web.setcookie('admin',"",-1)	
	return

def find_user_by_id(id):
	sql = "select * from user where id=%s;" %(id)
	result = get_one_sql(sql)
	return result

def find_user_by_name(name):
	sql = "select * from user where name='%s';" %(name)
	result = get_one_sql(sql)
	return result

def find_admin_by_name(name):
	sql = "select * from admin where name='%s';" %(name)
	result = get_one_sql(sql)
	return result

def find_by_id(typ,id):
	sql = "select * from %s where id=%s;"%(typ,id)
	return get_one_sql(sql)

def find_by_name(typ,name):
	if name=="":
		sql = "select * from %s;"%(typ)
	else:
		sql = "select * from %s where name='%s';" %(typ,name)
	return get_all_sql(sql)

def my_page(body):
	user = web.cookies().get("name","")
	adm = (find_admin_by_name(user) != None)
	return render.layout(render.header(user , adm),body)

def	new_problem(i):		
	sql = "insert into problem value(null,'%s','%s','%s','%s','%s','%s',null);"%(i["title"],i["description"],i["input_formal"],i["output_formal"],i["sample_input"],i["sample_output"])
	run_sql(sql)
	return 

def	new_tag(i):		
	sql = "insert into tag value(null,'%s');"%(i["name"])
	run_sql(sql)
	return 

def new_pbm_tag(i):
	sql = "select * from pbm_tag where p_id ='%s' and t_id='%s';"%(i["problem"],i["tag"])
	if get_one_sql(sql)==None:
		sql = "insert into pbm_tag value('%s','%s');" % (i["problem"],i["tag"])
		run_sql(sql)
	return

def new_group(i):
	sql = "insert into groups values(null , '%s' , '%s' , '%s');" % (i["name"] , i["abstract"] , i["imgurl"])
	run_sql(sql)
	return

def is_u_g(user_id,group_id):
	sql = "select * from user_group where user_id='%s' and group_id='%s';" % (user_id,group_id)
	return get_one_sql(sql)!=None

def new_u_g(user_id , group_id):
	if is_u_g(user_id,group_id):
		return False
	else:	
		sql = "insert into user_group value('%s','%s');" % (user_id,group_id)
		run_sql(sql)

def del_u_g(user_id,group_id):
	if is_u_g(user_id,group_id):
		sql = "delete from user_group where user_id='%s' and group_id='%s';" %(user_id,group_id)
		run_sql(sql)	
	else:
		return False

def is_u_p(u_id,p_id):
	sql = "select * from user_pro where u_id='%s' and p_id='%s';" % (u_id,p_id)
	return get_one_sql(sql)!=None

def new_u_p(u_id , p_id):
	if is_u_p(u_id,p_id):
		return False
	else:	
		sql = "insert into user_pro value('%s','%s');" % (u_id,p_id)
		run_sql(sql)

def del_u_p(u_id,p_id):
	if is_u_p(u_id,p_id):
		sql = "delete from user_pro where u_id='%s' and p_id='%s';" %(u_id,p_id)
		run_sql(sql)	
	else:
		return False


def edit_problem(i):
	sql = "update problem set title='%s',description='%s',input_formal='%s',output_formal='%s',sample_input='%s',sample_output='%s' where id='%s';"%(i["title"],i["description"],i["input_formal"],i["output_formal"],i["sample_input"],i["sample_output"],i["id"])
	run_sql(sql)
	return

def edit_user(i):
	sql = "update user set psword='%s',gender='%s',email='%s',school='%s',major='%s' where id='%s';" % (i["psword"] , i["gender"] , i["email"] , i["school"] , i["major"] , i["id"])
	run_sql(sql)
	return	

def edit_group(i):
	sql = "update groups set name='%s', abstract='%s',imgurl='%s' where id='%s';" % (i["name"] , i["abstract"] , i["imgurl"] ,i["id"])
	run_sql(sql)
	return	


class register:
	def GET(self):
		return my_page(render.register())
	def POST(self):
		i = web.input()
		if find_user_by_name(i["name"]) != None:
			web.seeother("/register")
		else:
			if i['psword']==i['psword_confirm'] and i['name']!="":
				login(new_user(i))
			web.seeother("/")

def find_pbm_tag(id):
	sql = "select name from tag where id in (select t_id from pbm_tag where p_id = %s);" % (id)
	return get_all_sql(sql)

def find_group_user(id):
	sql = "select name from user where id in (select user_id from user_group where group_id = %s);" % (id)
	return get_all_sql(sql)

def find_user_group(id):
	sql = "select name from groups where id in (select group_id from user_group where user_id = %s);" % (id)
	return get_all_sql(sql)

def find_user_pbm(id):
	sql = "select title from problem where id in (select p_id from user_pro where u_id = %s);" % (id)
	return get_all_sql(sql)

class group:
	def GET(self):
		i = web.input()
		if "id" in i:
			g = find_by_id("groups" , i["id"])	
			if g == None:
				web.seeother("/group")
				return
			else:
				u = find_group_user(g["id"])
				tmp = web.cookies().get("name","")
				adm = (find_admin_by_name(tmp) != None)
				if not adm:					
					user = find_user_by_name(tmp)
					if user == None:
						flag = False	
						user = {}						
  					else:
						flag = is_u_g(user["id"] , i["id"])
				else:
					flag = False
					user = {}
				return my_page(render.group(g , u , user , adm , flag))
		return my_page(render.groups(find_by_name("groups" , "")))

class problem:
	def GET(self):
		i = web.input()
		if "id" in i:
			pro = find_by_id("problem" , i["id"]);
			if pro == None:
				web.seeother("/problem");
				return
			else:
				tags = find_pbm_tag(pro["id"])
				tmp = web.cookies().get("name","")
				adm = (find_admin_by_name(tmp) != None)
				if not adm:					
					user = find_user_by_name(tmp)
					if user == None:
						flag = False	
						user = {}						
  					else:
						flag = is_u_p(user["id"] , i["id"])
				else:
					flag = False
					user = {}
				return my_page(render.problem(pro , tags , user , adm , flag))
		return my_page(render.problemset(find_by_name("problem" , "") , find_by_name("tag" , "")))

class message:
	def GET(self):
		sql = "select * from comments order by time;"
		tmp = get_all_sql(sql)
		comment = []
				
		for com in tmp:
			d = {}
			u = find_user_by_id(com["u_id"])
			d["id"] = com["id"]			
			d["name"] = u["name"]
			d["string"] = com["string"]
			d["time"] = com["time"]
			comment.append(d)

		tmp = web.cookies().get("name","")
		adm = (find_admin_by_name(tmp) != None)
		if not adm:					
			user = find_user_by_name(tmp)
		else:
			user = {}		
		if user == None:
			user = {}
		return my_page(render.message(comment , user , adm))
	def POST(self):
		i = web.input()
		t = time.strftime("%Y-%m-%d %H:%M:%S")
		tmp = web.cookies().get("name","")
		user = find_user_by_name(tmp)
		sql = "insert into comments value(null , '%s' , '%s' , '%s');" % (user["id"], t ,i["string"])
		run_sql(sql)
		web.seeother("/message")
		return 

class join:
	def GET(self):
		i = web.input()
		if ("user_id" not in i) or ("group_id" not in i):
			web.seeother("/")
			return 	
		if is_u_g(i["user_id"],i["group_id"]):
			del_u_g(i["user_id"],i["group_id"])
		else:
			new_u_g(i["user_id"],i["group_id"])
		web.seeother("/group?id=%s" % (i["group_id"]))
		return 

class favo:
	def GET(self):
		i = web.input()
		if ("user_id" not in i) or ("pro_id" not in i):
			web.seeother("/")
			return 	
		if is_u_p(i["user_id"],i["pro_id"]):
			del_u_p(i["user_id"],i["pro_id"])
		else:
			new_u_p(i["user_id"],i["pro_id"])
		web.seeother("/problem?id=%s" % (i["pro_id"]))
		return 

class user:
	def GET(self):
		name = web.cookies().get("name","")
		if name == "":
			web.seeother("/")
		else:
			u = find_admin_by_name(name)
			if u != None:
				web.seeother("/manage")
			else:
				u = find_user_by_name(name)
				G = find_user_group(u["id"])
				P = find_user_pbm(u["id"])
				return my_page(render.user(u , G , P))
		return

class manage:
	def GET(self):
		adm = (find_admin_by_name(web.cookies().get("name","")) != None)
		if not adm:
			return my_page("404 not found")
		return my_page(render.manage())

class new:
	def GET(self):
		user = web.cookies().get("name","")
		adm = (find_admin_by_name(user) != None)
		if not adm:
			return my_page("404 not found")
		i = web.input()
		t = i.get("type","")
		if t == "problem":
			return my_page(render.newproblem())
		if t == "tag":
			return my_page(render.newtag())
		if t == "pbm_tag":
			return my_page(render.newpbm_tag(find_by_name("problem" , "") , find_by_name("tag" , "")))
		if t == "group":
			return my_page(render.newgroup())
	def POST(self):
		i = web.input()
		if i["type"] == "problem":
			new_problem(i)
		if i["type"] == "tag":
			new_tag(i)
		if i["type"] == "pbm_tag":
			new_pbm_tag(i)
		if i["type"] == "group":
			new_group(i)
		if i["type"] == "problem" or i["type"] == "group":
			web.seeother("/" + i["type"])
		else:
			web.seeother("/")

class edit:
	def GET(self):
		i = web.input()
		print i
		t = i.get("type","")
		if t == "group":
			t = "groups"		
		one = find_by_id(t,i['id'])
		print one
		if one==None:
			web.seeother("/")
			return 
		if t == "problem":
			return my_page(render.editproblem(one))
		if t == "user":
			return my_page(render.edituser(one))
		if t == "groups":
			return my_page(render.editgroup(one))
	def POST(self):
		i = web.input()
		if i["type"] == "problem":
			edit_problem(i)
		if i["type"] == "user":
			if i["psword"] == i["psword_confirm"]:
				edit_user(i)
		if i["type"] == "group":
			edit_group(i)
		web.seeother("/%s"% (i["type"]))

class delete:
	def GET(self):
		i = web.input()
		drop(i["type"],i["id"])
		if i["type"] == "problem":
			web.seeother("/problem")
		elif i["type"] == "groups":
			web.seeother("/group")
		elif i["type"] == "comments":
			web.seeother("/message")
		else:			
			web.seeother("/")
		return

class index:
	def GET(self):
		i = web.input()
		if "logout" in i:
			logout()
			web.seeother("/")		
		return my_page(render.index())
	def POST(self):
		i = web.input()
		if "admin" in i:
			tmp = find_admin_by_name(i["name"])
		else:
			tmp = find_user_by_name(i["name"])
		if (tmp != None and tmp["psword"] == i['psword']):
			if "admin" in i:
				login_admin(tmp["name"])
			else:	
				login(tmp["name"])
		else:
			pass
		web.seeother("/")
			

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
