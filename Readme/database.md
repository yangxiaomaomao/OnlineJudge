1. 直接使用docker，不需要另外安装。其中，
2. mysql版本为5.7，用来保存学生的数据
3. redis用来保存验证码（登录时候需要验证码）
4. 学生信息在ucas_mysql容器中保存
    1. `docker exec -it ucas_mysql /bin/bash`进入容器
    2. `mysql -u root -p`后根据提示输入密码`2020Cnic@!`后进入mysql
    3. `show databases;`展示数据库有哪些，使用`use oj;`选择`oj`数据库 
    4. `show tables;`显示`oj`数据库中有哪些表
    5. `select * from User;`，打印用户信息
    6. `delete from User where userId>=300`删除用户信息，lyg和yjb的编号远小于300
