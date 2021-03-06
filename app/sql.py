#!/usr/bin/env python3
# -*- coding: utf-8 -*-"
import cgi
import create_db
from configparser import ConfigParser, ExtendedInterpolation

path_config = "haproxy-webintarface.config"
config = ConfigParser(interpolation=ExtendedInterpolation())
config.read(path_config)

mysql_enable = config.get('mysql', 'enable')

if mysql_enable == '1':
	from mysql.connector import errorcode
	import mysql.connector as sqltool
else:
	db = "haproxy-wi.db"
	import sqlite3 as sqltool
	
def add_user(user, email, password, role, group):
	con, cur = create_db.get_cur()
	sql = """INSERT INTO user (username, email, password, role, groups) VALUES ('%s', '%s', '%s', '%s', '%s')""" % (user, email, password, role, group)
	try:    
		cur.execute(sql)
		con.commit()
	except sqltool.Error as e:
		print('<span class="alert alert-danger" id="error">An error occurred: ' + e.args[0] + ' <a title="Close" id="errorMess"><b>X</b></a></span>')
		con.rollback()
		return False
	else:
		return True
	cur.close()    
	con.close()   
	
def update_user(user, email, password, role, group, id):
	con, cur = create_db.get_cur()
	sql = """update user set username = '%s', 
			email = '%s',
			password = '%s', 
			role = '%s', 
			groups = '%s' 
			where id = '%s'""" % (user, email, password, role, group, id)
	try:    
		cur.execute(sql)
		con.commit()
	except sqltool.Error as e:
		print('<span class="alert alert-danger" id="error">An error occurred: ' + e.args[0] + ' <a title="Close" id="errorMess"><b>X</b></a></span>')
		con.rollback()
		return False
	else:
		return True
	cur.close()    
	con.close()

def delete_user(id):
	con, cur = create_db.get_cur()
	sql = """delete from user where id = '%s'""" % (id)
	try:    
		cur.execute(sql)
		con.commit()
	except sqltool.Error as e:
		print("An error occurred:", e.args[0])
		con.rollback()
	else: 
		return True
	cur.close()
	
def add_group(name, description):
	con, cur = create_db.get_cur()
	sql = """INSERT INTO groups (name, description) VALUES ('%s', '%s')""" % (name, description)
	try:    
		cur.execute(sql)
		con.commit()
	except sqltool.Error as e:
		print('<span class="alert alert-danger" id="error">An error occurred: ' + e.args[0] + ' <a title="Close" id="errorMess"><b>X</b></a></span>')
		con.rollback()
		return False
	else:
		print(cur.lastrowid)
		return True
	cur.close()    
	con.close() 

def delete_group(id):
	con, cur = create_db.get_cur()
	sql = """delete from groups where id = '%s'""" % (id)
	try:    
		cur.execute(sql)
		con.commit()
	except sqltool.Error as e:
		print('<span class="alert alert-danger" id="error">An error occurred: ' + e.args[0] + ' <a title="Close" id="errorMess"><b>X</b></a></span>')
		con.rollback()
	else: 
		return True
	cur.close()
	
def update_group(name, descript, id):
	con, cur = create_db.get_cur()
	sql = """
		update groups set 
		name = '%s',
		description = '%s' 
		where id = '%s';
		""" % (name, descript, id)
	try:    
		cur.execute(sql)
		con.commit()
	except sqltool.Error as e:
		print('<span class="alert alert-danger" id="error">An error occurred: ' + e.args[0] + ' <a title="Close" id="errorMess"><b>X</b></a></span>')
		con.rollback()
		return False
	else:
		return True
	cur.close()    
	con.close()

def add_server(hostname, ip, group, typeip, enable, master):
	con, cur = create_db.get_cur()
	sql = """INSERT INTO servers (hostname, ip, groups, type_ip, enable, master) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')""" % (hostname, ip, group, typeip, enable, master)
	try:    
		cur.execute(sql)
		con.commit()
	except sqltool.Error as e:
		print('<span class="alert alert-danger" id="error">An error occurred: ' + e.args[0] + ' <a title="Close" id="errorMess"><b>X</b></a></span>')
		con.rollback()
		return False
	else:
		return True
	cur.close()    
	con.close() 	

def delete_server(id):
	con, cur = create_db.get_cur()
	sql = """delete from servers where id = '%s'""" % (id)
	try:    
		cur.execute(sql)
		con.commit()
	except sqltool.Error as e:
		print('<span class="alert alert-danger" id="error">An error occurred: ' + e.args[0] + ' <a title="Close" id="errorMess"><b>X</b></a></span>')
		con.rollback()
	else: 
		return True
	cur.close()    
	con.close() 		

def update_server(hostname, ip, group, typeip, enable, master, id):
	con, cur = create_db.get_cur()
	sql = """update servers set 
			hostname = '%s',
			ip = '%s',
			groups = '%s',
			type_ip = '%s',
			enable = '%s',
			master = '%s'
			where id = '%s'""" % (hostname, ip, group, typeip, enable, master, id)
	try:    
		cur.execute(sql)
		con.commit()
	except sqltool.Error as e:
		print('<span class="alert alert-danger" id="error">An error occurred: ' + e.args[0] + ' <a title="Close" id="errorMess"><b>X</b></a></span>')
		con.rollback()
	cur.close()    
	con.close()

def update_server_master(master, slave):
	con, cur = create_db.get_cur()
	sql = """ select id from servers where ip = '%s' """ % master
	try:    
		cur.execute(sql)
	except sqltool.Error as e:
		print('<span class="alert alert-danger" id="error">An error occurred: ' + e.args[0] + ' <a title="Close" id="errorMess"><b>X</b></a></span>')
	for id in cur.fetchall():
		sql = """ update servers set master = '%s' where ip = '%s' """ % (id[0], slave)
	try:    
		cur.execute(sql)
		con.commit()
	except sqltool.Error as e:
		print('<span class="alert alert-danger" id="error">An error occurred: ' + e.args[0] + ' <a title="Close" id="errorMess"><b>X</b></a></span>')
		con.rollback()
	cur.close()    
	con.close()
	
def select_users(**kwargs):
	con, cur = create_db.get_cur()
	sql = """select * from user ORDER BY id"""
	if kwargs.get("user") is not None:
		sql = """select * from user where username='%s' """ % kwargs.get("user")
	try:    
		cur.execute(sql)
	except sqltool.Error as e:
		print("An error occurred:", e.args[0])
	else:
		return cur.fetchall()
	cur.close()    
	con.close()    
	
def select_groups(**kwargs):
	con, cur = create_db.get_cur()
	sql = """select * from groups ORDER BY id"""
	if kwargs.get("group") is not None:
		sql = """select * from groups where name='%s' """ % kwargs.get("group")
	try:    
		cur.execute(sql)
	except sqltool.Error as e:
		print('<span class="alert alert-danger" id="error">An error occurred: ' + e.args[0] + ' <a title="Close" id="errorMess"><b>X</b></a></span>')
	else:
		return cur.fetchall()
	cur.close()    
	con.close()  
	
def select_user_name_group(id):
	con, cur = create_db.get_cur()
	sql = """select name from groups where id='%s' """ % id
	try:    
		cur.execute(sql)
	except sqltool.Error as e:
		print('<span class="alert alert-danger" id="error">An error occurred: ' + e.args[0] + ' <a title="Close" id="errorMess"><b>X</b></a></span>')
	else:
		return cur.fetchone()
	cur.close()    
	con.close()  

def get_groups_select(id, **kwargs):
	print('<select class="multiselect" id="%s" name="%s">' % (id, id))
	print('<option disabled selected>Choose group</option>')
	GROUPS = select_groups()
	selected = ""
	print(kwargs.get('selected'))
	for group in GROUPS:
		if kwargs.get('selected'):
			selected1 = kwargs.get('selected')
			selected1 = int(selected1)
			if selected1 == group[0]:
				selected = 'selected'
			else:
				selected = ""
		print('<option value="%s" %s>%s</option>' % (group[0], selected, group[1]))
	print('</select>')
	
def select_servers(**kwargs):
	con, cur = create_db.get_cur()
	sql = """select * from servers where enable = '1' ORDER BY groups """
	if kwargs.get("server") is not None:
		sql = """select * from servers where hostname='%s' """ % kwargs.get("server")
	if kwargs.get("full") is not None:
		sql = """select * from servers ORDER BY groups """ 
	if kwargs.get("get_master_servers") is not None:
		sql = """select id,hostname from servers where master = 0 and type_ip = 0 and enable = 1 ORDER BY groups """ 
	try:    
		cur.execute(sql)
	except sqltool.Error as e:
		print("An error occurred:", e.args[0])
	else:
		return cur.fetchall()
	cur.close()    
	con.close()  
	
def get_type_ip_checkbox(id, **kwargs):
	con, cur = create_db.get_cur()
	sql = """select id, type_ip from servers where id='%s' """ % id
	try:    
		cur.execute(sql)
	except sqltool.Error as e:
		print("An error occurred:", e.args[0])
	else:
		for server in cur.fetchall():
			if server[1] == 1:
				checked = 'checked'
			else:
				checked = ""
			print('<label for="typeip-%s"></label><input type="checkbox" id="typeip-%s" %s>' % (server[0],server[0], checked))
	cur.close()    
	con.close() 
	
def get_enable_checkbox(id, **kwargs):
	con, cur = create_db.get_cur()
	sql = """select id, enable from servers where id='%s' """ % id
	try:    
		cur.execute(sql)
	except sqltool.Error as e:
		print("An error occurred:", e.args[0])
	else:
		for server in cur.fetchall():
			if server[1] == 1:
				checked = 'checked'
			else:
				checked = ""
			print('<label for="enable-%s"></label><input type="checkbox" id="enable-%s" %s>' % (server[0],server[0], checked))
	cur.close()    
	con.close() 
	
def get_dick_permit(**kwargs):
	import http.cookies
	import os
	cookie = http.cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
	login = cookie.get('login')
	con, cur = create_db.get_cur()
	sql = """ select * from user where username = '%s' """ % login.value
	if kwargs.get('virt'):
		type_ip = "" 
	else:
		type_ip = "and type_ip = 0" 
	try:    
		cur.execute(sql)
	except sqltool.Error as e:
		print("An error occurred:", e.args[0])
	else:
		for group in cur:
			if group[5] == '1':
				sql = """ select * from servers where enable = 1 %s """ % type_ip
			else:
				sql = """ select * from servers where groups like '%{group}%' and enable = 1 {type_ip} """.format(group=group[5], type_ip=type_ip)		
		try:   
			cur.execute(sql)
		except sqltool.Error as e:
			print("An error occurred:", e.args[0])
		else:
			return cur.fetchall()
	cur.close()    
	con.close() 
	
def is_master(ip, **kwargs):
	con, cur = create_db.get_cur()
	sql = """ select slave.ip from servers left join servers as slave on servers.id = slave.master where servers.ip = '%s' """ % ip
	if kwargs.get('master_slave'):
		sql = """ select master.hostname, master.ip, slave.hostname, slave.ip from servers as master left join servers as slave on master.id = slave.master where slave.master > 0 """
	try:
		cur.execute(sql)
	except sqltool.Error as e:
		return False
	else:
		return cur.fetchall()
	
def show_update_servers():
	SERVERS = select_servers()
	print('<tr class="overviewHead">'
			'<td class="padding10">Hostname</td>'
			'<td>IP</td>'
			'<td>Group</td>'
			'<td></td>'
			'</tr>')
	for server in SERVERS:
		print('<tr id="server-%s">' % server[0])
		print('<td class="padding10 first-collumn"><input type="text" id="server-%s" value="%s" class="form-control"></td>' % (server[0], server[1]))
		print('<td><input type="text" id="descript-%s" value="%s" class="form-control"></td>' % (server[0], server[2]))
		print('<td>')
		get_groups_select("123", selected=server[3])
		print('</td>')
		print('<td>')
		get_enable_checkbox(server[0])
		print('</td>')
		print('<td>')
		get_type_ip_checkbox(server[0])
		print('</td>')
		print('<td><a class="delete" onclick="removeServer(%s)"  style="cursor: pointer;"></a></td>' % server[0])
		print('</tr>')

def show_update_user(user):
	USERS = select_users(user=user)
	for users in USERS:
		print('<tr id="user-%s">' % users[0])
		print('<td class="padding10 first-collumn"><input type="text" id="login-%s" value="%s" class="form-control"></td>' % (users[0], users[1]))
		print('<td><input type="password" id="password-%s" value="%s" class="form-control"></td>' % (users[0], users[3]))
		print('<td><input type="text" id="email-%s" value="%s" class="form-control"></td>' % (users[0], users[2]))
		print('<td>')
		need_id_role = "role-%s" % users[0]
		get_roles_select(need_id_role, selected=users[4])
		print('</td>')
		print('<td>')
		need_id_group = "usergroup-%s" % users[0]
		get_groups_select(need_id_group, selected=users[5])
		print('</td>')
		print('<td><a class="delete" onclick="removeUser(%s)"  style="cursor: pointer;"></a></td>' % users[0])
		print('</tr>')
		
def show_update_server(server):
	SERVERS = select_servers(server=server)
	for server in SERVERS:
		print('<tr id="server-%s">' % server[0])
		print('<td class="padding10 first-collumn"><input type="text" id="hostname-%s" value="%s" class="form-control"></td>' % (server[0], server[1]))
		print('<td><input type="text" id="ip-%s" value="%s" class="form-control"></td>' % (server[0], server[2]))
		print('<td>')
		need_id_group = "servergroup-%s" % server[0]
		get_groups_select(need_id_group, selected=server[3])
		print('</td>')
		print('<td>')
		get_enable_checkbox(server[0])
		print('</td>')
		print('<td>')
		get_type_ip_checkbox(server[0])
		print('</td>')
		print('<td><select id="slavefor-%s"><option value="0" selected>Not slave</option>' % server[0])
		MASTERS = select_servers(get_master_servers=1)
		for master in MASTERS:
			if master[0] == server[6]:
				selected = "selected"
			else:
				selected = ""
			print('<option value="%s" %s>%s</option>' % (master[0], selected, master[1]))
		print('</select></td>')
		print('<td><a class="delete" onclick="removeServer(%s)"  style="cursor: pointer;"></a></td>' % server[0])
		print('</tr>')

def show_update_group(group):
	GROUPS = select_groups(group=group)
	for group in GROUPS:
		print('<tr id="group-%s">' % group[0])
		print('<td class="padding10 first-collumn"><input type="text" name="name-%s" value="%s" class="form-control"></td>' % (group[0], group[1]))
		print('<td><input type="text" name="descript-%s" value="%s" class="form-control" size="100"></td>' % (group[0], group[2]))
		print('<td><a class="delete" onclick="removeGroup(%s)"  style="cursor: pointer;"></a></td>' % group[0])
		print('<td></td>')
		print('</tr>')

def select_roles(**kwargs):
	con, cur = create_db.get_cur()
	sql = """select * from role ORDER BY id"""
	if kwargs.get("role") is not None:
		sql = """select * from role where name='%s' """ % kwargs.get("group")
	try:    
		cur.execute(sql)
	except sqltool.Error as e:
		print("An error occurred:", e.args[0])
	else:
		return cur.fetchall()
	cur.close()    
	con.close()  
	
def select_roles(**kwargs):
	con, cur = create_db.get_cur()
	sql = """select * from role ORDER BY id"""
	if kwargs.get("roles") is not None:
		sql = """select * from role where name='%s' """ % kwargs.get("roles")
	try:    
		cur.execute(sql)
	except sqltool.Error as e:
		print("An error occurred:", e.args[0])
	else:
		return cur.fetchall()
	cur.close()    
	con.close()  
		
def get_roles_select(id, **kwargs):
	print('<select id="%s" name="%s">' % (id, id))
	print('<optin disabled selected>Choose role</option>')
	ROLES = select_roles()
	selected = ""
	for role in ROLES:
		if kwargs.get('selected'):
			if kwargs.get('selected') == role[1]:
				selected = "selected"
			else:
				selected = ""
		print('<option value="%s" %s>%s</option>' % (role[1], selected, role[1]))
	print('</select>')	
	
form = cgi.FieldStorage()
error_mess = '<span class="alert alert-danger" id="error">All fields must be completed <a title="Close" id="errorMess"><b>X</b></a></span>'

if form.getvalue('newusername') is not None:
	email = form.getvalue('newemail')
	password = form.getvalue('newpassword')
	role = form.getvalue('newrole')
	group = form.getvalue('newgroupuser')
	new_user = form.getvalue('newusername')	
	if password is None or role is None or group is None:
		print('Content-type: text/html\n')
		print(error_mess)
	else:		
		print('Content-type: text/html\n')
		if add_user(new_user, email, password, role, group):
			show_update_user(new_user)
		
if form.getvalue('updateuser') is not None:
	email = form.getvalue('email')
	password = form.getvalue('password')
	role = form.getvalue('role')
	group = form.getvalue('usergroup')
	new_user = form.getvalue('updateuser')	
	id = form.getvalue('id')	
	if password is None or role is None or group is None:
		print('Content-type: text/html\n')
		print(error_mess)
	else:		
		print('Content-type: text/html\n')
		update_user(new_user, email, password, role, group, id)
		
if form.getvalue('userdel') is not None:
	print('Content-type: text/html\n')
	if delete_user(form.getvalue('userdel')):
		print("Ok")
		
if form.getvalue('newserver') is not None:
	hostname = form.getvalue('newserver')	
	ip = form.getvalue('newip')
	group = form.getvalue('newservergroup')
	typeip = form.getvalue('typeip')
	enable = form.getvalue('enable')
	master = form.getvalue('slave')
	if ip is None or group is None:
		print('Content-type: text/html\n')
		print(error_mess)
	else:		
		print('Content-type: text/html\n')
		if add_server(hostname, ip, group, typeip, enable, master):
			show_update_server(hostname)

if form.getvalue('serverdel') is not None:
	print('Content-type: text/html\n')
	if delete_server(form.getvalue('serverdel')):
		print("Ok")
	
if form.getvalue('newgroup') is not None:
	newgroup = form.getvalue('newgroup')	
	desc = form.getvalue('newdesc')
	print('Content-type: text/html\n')
	if add_group(newgroup, desc):
		show_update_group(newgroup)

if form.getvalue('groupdel') is not None:
	print('Content-type: text/html\n')
	if delete_group(form.getvalue('groupdel')):
		print("Ok")
		
if form.getvalue('updategroup') is not None:
	name = form.getvalue('updategroup')
	descript = form.getvalue('descript')	
	id = form.getvalue('id')	
	if name is None:
		print('Content-type: text/html\n')
		print(error_mess)
	else:		
		print('Content-type: text/html\n')
		update_group(name, descript, id)
		
if form.getvalue('updateserver') is not None:
	name = form.getvalue('updateserver')
	ip = form.getvalue('ip')	
	group = form.getvalue('servergroup')	
	typeip = form.getvalue('typeip')		
	enable = form.getvalue('enable')		
	master = form.getvalue('slave')		
	id = form.getvalue('id')	
	if name is None or ip is None:
		print('Content-type: text/html\n')
		print(error_mess)
	else:		
		print('Content-type: text/html\n')
		update_server(name, ip, group, typeip, enable, master, id)
		