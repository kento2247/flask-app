drop table USERS;
drop table VOTES;
drop table GAMELOGS;
create table USERS (username varchar, password varchar, id varchar);
create table VOTES (title varchar, num varchar, id varchar);
create table GAMELOGS (username varchar, time varchar);

-- insert into USERS values ("admin", "admin", "0");
insert into VOTES values ("Mac OS", "50", "0");
insert into VOTES values ("Windows", "50", "1");
insert into VOTES values ("Linux", "50", "2");