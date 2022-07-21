CREATE DATABASE perfume default CHARACTER SET UTF8;
-- SET NAMES utf8;
-- SET CHARACTER SET utf8;
show databases;
SELECT VERSION();
-- drop database perfume;

use perfume;

create table perfume(
   id INT AUTO_INCREMENT,
    perfume_name varchar(100) NOT NULL,
    brand varchar(50) NOT NULL,
    brand_value varchar(20) NOT NULL,
    gender varchar(10) NOT NULL,
    launch_year INT,
    main_accord1 varchar(255) NOT NULL, 
    main_accord2 varchar(255) NOT NULL, 
    main_accord3 varchar(255) NOT NULL, 
    top_note varchar(300) NOT NULL, 
    middle_note varchar(300) NOT NULL, 
    base_note varchar(300) NOT NULL, 
    season varchar(10) NOT NULL, 
    day_or_night varchar(10) NOT NULL, 
    longevity varchar(15) NOT NULL, 
    sillage varchar(15) NOT NULL, 
    rating FLOAT(3) NOT NULL, 
    voters_num INT NOT NULL, 
    main_accord1_ratio FLOAT(3) NOT NULL, 
    main_accord2_ratio FLOAT(3) NOT NULL, 
    main_accord3_ratio FLOAT(3) NOT NULL,
    primary key(id)
);

-- insert into perfume values (NULL, "Oui à l'Amour Collector Edition 2018", "a", "a", NULL, "a", "a", "a", "a", "a", "a","a" ,"a" ,"a" ,"a", 1, 1, 1,1,1);
-- delete from perfume where id = 9449;
-- select count(b.perfume_name) from (select DISTINCT perfume_name from perfume) as b;

drop table perfume;
select * from perfume;
select count(*) from perfume;
select * from perfume where id = 534;
select * from perfume where perfume_name = "Azure – Лазурь";
select * from perfume where perfume_name = 'Rose';
select count(*) from (select distinct perfume_name from perfume) as t1;
-- 26 28 58 68 84 534 360 361 162 209
-- Rose Eclat No 5 

SELECT * FROM perfume
INTO OUTFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\sample_data2.csv'
CHARACTER SET euckr
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
ESCAPED BY '\\'
LINES TERMINATED BY '\n';

SELECT @@GLOBAL.secure_file_priv;

create table dup
select MAX(id) from perfume group by perfume_name having count(*) > 1;
select * from dup;
drop table dup;

delete from perfume where id IN (select * from dup);

create table preprocessed_perfume(
   id INT AUTO_INCREMENT,
    perfume_name varchar(100) NOT NULL,
    brand_value varchar(20) NOT NULL, 
    main_accord1 varchar(255) NOT NULL, 
    main_accord2 varchar(255) NOT NULL, 
    main_accord3 varchar(255) NOT NULL, 
    season varchar(10) NOT NULL, 
    longevity varchar(15) NOT NULL, 
    rating FLOAT(3) NOT NULL, 
    voters_num INT NOT NULL, 
    main_accord1_ratio FLOAT(3) NOT NULL, 
    main_accord2_ratio FLOAT(3) NOT NULL, 
    main_accord3_ratio FLOAT(3) NOT NULL,
    primary key(id)
);

-- RENAME TABLE perfume2 TO preprocessed_perfume;
drop table preprocessed_perfume;
select * from preprocessed_perfume;
select count(*) from preprocessed_perfume;

create table dup
select MAX(id) from preprocessed_perfume group by perfume_name having count(*) > 1;
select * from dup;
drop table dup;

delete from preprocessed_perfume where id IN (select * from dup);

create table perfume_mat(
   id INT AUTO_INCREMENT,
    beverages FLOAT(3) NOT NULL,
    brand_value FLOAT(3) NOT NULL, 
    citrussmells FLOAT(3) NOT NULL, 
    eternal FLOAT(3) NOT NULL, 
    fall FLOAT(3) NOT NULL, 
    flowers FLOAT(3) NOT NULL, 
    fruitsvegetablesandnuts FLOAT(3) NOT NULL, 
    greensherbsandfougeres FLOAT(3) NOT NULL, 
    long_lasting FLOAT(3) NOT NULL, 
    longevity FLOAT(3) NOT NULL,
    luxury FLOAT(3) NOT NULL,
    moderate FLOAT(3) NOT NULL,
    muskamberanimalicsmells FLOAT(3) NOT NULL,
    naturalandsyntheticpopularandweird FLOAT(3) NOT NULL,
    normal FLOAT(3) NOT NULL,
    popular FLOAT(3) NOT NULL,
    resinsandbalsams FLOAT(3) NOT NULL,
    season FLOAT(3) NOT NULL,
    spices FLOAT(3) NOT NULL,
    spring FLOAT(3) NOT NULL,
    summer FLOAT(3) NOT NULL,
    sweetsandgourmandsmells FLOAT(3) NOT NULL,
    very_weak FLOAT(3) NOT NULL,
    weak FLOAT(3) NOT NULL,
    whiteflowers FLOAT(3) NOT NULL,
    winter FLOAT(3) NOT NULL,
    woodsandmosses FLOAT(3) NOT NULL,
    primary key(id)
);

-- create table dup
-- select MAX(id) from perfume_mat group by perfume_name having count(*) > 1;
-- select * from dup;
-- drop table dup;

-- delete from perfume_mat where id IN (select * from dup);

drop table perfume_mat;
-- perfume_mat은 사용자의 input까지 포함되기 때문에 마지막 row 날려줘야 됨 
-- delete from perfume_mat where id = 마지막row;
delete from perfume_mat where id = 10305;
desc perfume_mat;
select count(*) from perfume_mat;
select * from perfume_mat;

-- perfume_mat 계절 별로 만들어야 됨