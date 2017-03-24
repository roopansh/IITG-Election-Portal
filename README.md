# IITG Gymkhana Election Portal

The portal used for the Gymkhana Elections 2017 of Indian Institute of Technology Guwahati,India.

___

## Requirements

**Django 1.10** and any suitable database(postgreSQL or SQLite). Currently **SQLite** is being used.

___

## Setting Up

1. Installing Django

		sudo apt-get update

		sudo apt-get install python3 python3-pip

		sudo pip3 install django=1.10

2. Migrating the Models

		./manage.py makemigrations

		./manage.py migrate		

3. Populating the Database

A file has been provided for populating the database properly. You just need to make two 'csv' files in the desired formats :-

  * contestant.csv

  * voter.csv

Both the files will be in the directory containing the file ``` data_upload.py ```.

The format of ``` contestant.csv```

Full Name | Post | Webmail | Agenda 1 | Agenda 2 | Agenda 3 | Agenda 4 | Pic Name
----------|------|---------|----------|----------|----------|----------|---------
John Doe | VP | john.doe@iitg.ernet.in | Agenda 1 | Agenda 2 | Agenda 3 | Agenda 4 | file name of the picture of the contestant without extension(**jpg only**)

**Post** :-

    VP      =   Vice President  
    HAB     =   General Secretary of Hostel Affairs Board  
    UGS     =   Under Graduate Senator  
    PGS     =   Post Graduate Senator  
    GS      =   Girl Senator  
    Tech    =   General Secretary of Technical Board  
    Cult    =   General Secretary of Cultural Board  
    Welfare =   General Secretary of Students Welfare Board  
    Sports  =   General Secretary of Sports Board  
    SAIL    =   General Seceratry of SAIL  
    CBS     =   General Seceratry of CBS  

The format of ``` voter.csv```

Webmail | Category | Hostel | Department
--------|----------|--------|-----------
john.doe | 0 | Dihing | CSE

**Category** :-

    0   =   UG-Boy
    1   =   UG-Girl
    2   =   PG-Boy
    3   =   PG-Girl

* Then run the data uploading script :- 
		
		python3 manage.py shell < 'data_upload.py'

**Note :** It will take some time in uploading the data.

___

## User Interface

### Admin login portal

**URL:** */vote/admin*

![Admin](https://github.com/roopansh/IITG-Election-Portal/blob/master/Screenshots/1.png?raw=true)

### Key generator

**URL:** */vote/key*

![key](https://github.com/roopansh/IITG-Election-Portal/blob/master/Screenshots/4.png?raw=true)


### Voter login portal

**URL:** */vote/voter*

![Voter](https://github.com/roopansh/IITG-Election-Portal/blob/master/Screenshots/3.png?raw=true)

### Voting pages

![Voting](https://github.com/roopansh/IITG-Election-Portal/blob/master/Screenshots/6.png?raw=true)
![Voting](https://github.com/roopansh/IITG-Election-Portal/blob/master/Screenshots/9.png?raw=true)

###Time up notification

**Automatic logout after timeout**

![Timeout](https://github.com/roopansh/IITG-Election-Portal/blob/master/Screenshots/15.png?raw=true)


____________________

### About the project author

#### Roopansh Bansal

B.Tech undergraduate  
Computer Science & Engineering  
Indian Institute of Technology  
Guwahati, India  

roopansh.bansal@gmail.com  
www.linkedin.com/in/roopansh-bansal
