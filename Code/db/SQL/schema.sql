drop database if exists planning;
create database planning;
use planning;

drop table if exists answers;
create table answers
(
    idx int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_name VARCHAR(100),
    q1 VARCHAR(11),
    q2 VARCHAR(11),
    q3 VARCHAR(11),
    q4 VARCHAR(11),
    q5 VARCHAR(11),
    q6 VARCHAR(11),
    q7 VARCHAR(11),
    q8 VARCHAR(11),
    q9 VARCHAR(11),
    q10 VARCHAR(11),
    q11 VARCHAR(11),
    q12 VARCHAR(11),
    q13 VARCHAR(11),
    q14 VARCHAR(11),
    q15 VARCHAR(11),
    q16 VARCHAR(11),
    q17 VARCHAR(11),
    q18 VARCHAR(11),
    q19 VARCHAR(11),
    q20 VARCHAR(11)
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

drop table if exists evaluations;
create table evaluations
(
    idx int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_name VARCHAR(100),
    evaluation int
)