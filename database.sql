CREATE DATABASE concisely;
USE concisely;
CREATE TABLE users(
user_id INT auto_increment PRIMARY KEY,
username VARCHAR(50) NOT NULL UNIQUE,
email VARCHAR(100) NOT NULL UNIQUE,
password_hash varchar(255) not null,
created_at timestamp default current_timestamp);

create table files(
file_id int auto_increment primary key,
user_id int not null,
foreign key(user_id) references users(user_id),
file_name varchar(255) not null,
file_type enum('text','video') not null,
file_path varchar(255) not null,
upload_timestamp timestamp default current_timestamp,
file_status enum('pending','processing','completed') not null default'pending'); 

create table summaries(
summary_id int auto_increment primary key,
file_id int not null,
foreign key(file_id) references files(file_id),
summary_text text,
summary_video_path varchar(255),
summary_type enum('text','video') not null,
created_at timestamp default current_timestamp);

create table login(
log_id int auto_increment primary key,
user_id int not null,
foreign key(user_id) references users(user_id),
file_id int not null,
foreign key(file_id) references files(file_id),
action varchar(100) not null,
log_timestamp timestamp default current_timestamp);
