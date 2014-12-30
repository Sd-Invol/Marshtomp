create table user
(
	id int unsigned not null auto_increment primary key,
	name varchar(30) not null,
	psword varchar(100) not null,
	gender int(1) not null,
	email varchar(100) not null,
	school varchar(100) default "BUAA",
	major varchar(100)
);

create table admin 
(
	id int unsigned not null auto_increment primary key,
	name varchar(30) not null, 
	psword varchar(100) not null
);

create table problem 
(
	id int unsigned not null auto_increment primary key,
	title varchar(100) not null,
	description varchar(1024),
	input_formal varchar(1024),
	output_formal varchar(1024),
	sample_input varchar(1024),
	sample_output varchar(1024),
	add_date date
);

create table tag
(
	id int unsigned not null auto_increment primary key,
	name varchar(100) not null,
	unique(name)
);

create table pbm_tag
(
	p_id int unsigned ,
	t_id int unsigned ,
	foreign key (p_id) references problem(id),
	foreign key (t_id) references tag(id),
	primary key (p_id,t_id)
);

create table groups
(
	id int unsigned not null auto_increment primary key,
	name varchar(100) not null,
	abstract varchar(1024),
	imgurl varchar(256) null,
	unique(name)
);

create table user_group
(
	user_id int unsigned,
	group_id int unsigned,
	foreign key (user_id) references user(id),
	foreign key (group_id) references groups(id),
	primary key (user_id,group_id)
);

create table user_pro
(
	u_id int unsigned , 
	p_id int unsigned ,
	foreign key (u_id) references user(id),
	foreign key (p_id) references problem(id),
	primary key (u_id , p_id)
);

create table comments 
(
	id int unsigned not null auto_increment primary key,
	u_id int unsigned ,
	time datetime ,
	string varchar(1024) ,
	foreign key (u_id) references user(id)
);

##################################

insert into admin values(null , "admin" , "admin");

##################################
delimiter $
create trigger Delete_Problem before delete on problem for each row
begin
delete from pbm_tag where old.id = p_id;
delete from user_pro where old.id = p_id;
end$
delimiter ;

create trigger Delete_Group before delete on groups for each row
	delete from user_group where old.id = group_id;

##################################



