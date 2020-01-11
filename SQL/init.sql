create database if not exists FlaskDB;
use FlaskDB;
-- create table IF NOT EXISTS test_table(
-- 	id int AUTO_INCREMENT primary key ,
-- 	name varchar(32)
-- );

create table IF NOT EXISTS user(
	id int AUTO_INCREMENT primary key ,
	username varchar(32) NOT NULL,
	passwd  varchar(32) NOT NULL,
	email varchar(32) NOT NULL
);


show tables;
-- 插入
insert into user (name ) values('Jim');

-- -- 查看数据
-- select * from test_table;