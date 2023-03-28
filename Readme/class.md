## 新学期准备
系统暂时还未开发批量删除的功能，所以需要去数据库手动删除上一学期的学生数据信息
1. 进入mysql的docker，`docker ps`得到docker id，然后`docker exec -it id_num /bin/bash`
2. 进入之后`mysql -u oj -p`，密码为`NxeF8EWJ3Gak4eRi`
3. `show databases`展示数据库名字，有一个是oj
4. `use oj`选择oj数据库，进入之后`show tables`可以看到有名字叫做`User`的`table`
5. `select * from User`可以展示用户信息。如果显示不出中文可以`set character_set_results=utf8`后重试
6. `delete from User where userId >= low_bound and userId <= high_bound`删除一定范围内的学生信息
7. 结束