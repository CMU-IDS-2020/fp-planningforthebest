drop database if exists planning;
create database planning;
use planning;

drop table if exists answers;
create table answers
(
    idx int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_name VARCHAR(100),
    q1 long,
    q2 long,
    q3 long,
    q4 long,
    q5 long,
    q6 long,
    q7 long,
    q8 long,
    q9 long,
    q10 long,
    q11 long,
    q12 long,
    q13 long,
    q14 long,
    q15 long,
    q16 long,
    q17 long,
    q18 long,
    q19 long,
    q20 long
);

drop table if exists feature_importances;
create table feature_importances
(
    idx int NOT NULL AUTO_INCREMENT PRIMARY KEY,
	user_name VARCHAR(100),
	paralysis double,
    voice double,
    feeding_tube double,
    vision double,
    cognitive double,
    perception double,
    self_care double,
    incontinence double,
    emotion double,
    sex double
);

drop table if exists feedbacks;
create table feedbacks
(
    idx int NOT NULL AUTO_INCREMENT PRIMARY KEY,
	user_name VARCHAR(100),
	feedback TEXT
);