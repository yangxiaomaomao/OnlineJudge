重要提示：为了判题的准确性，请在提交作业时保证代码中没有往标准输出打印各种自定义debug信息的操作，如不要含有

printf("PLEASE DELETE ME")或者fprintf(stdout, "PLEASE DELETE ME")等语句

如果有其它问题请联系管理员

请提交zip格式的文件(直接压缩为zip文件而不是改变rar或者tar.gz后缀名)，并且不要多层嵌套zip（如zip解压之后仍为zip文件），文件大小不要超过5MB

不需要提交python拓扑文件，只需要提交可编译的 C 程序 即可

目录中必须有Makefile文件，而不是makefile，请保证用sep原始的Makefile可以编译成功提交的作业

本实验和本学期开始第一个实验“socket应用编程实验”判题方法一致：

    在直连的网络链路中，h1运行编译编译好的文件，h2运行python3 test/test.py并可以正确地访问h1中的资源返回正确地结果，为了避免本地和OJ不一致，请大家在test.py的每个get请求中加上timeout = 2参数

网络拓扑①：两个节点直连的拓扑；

测试1：http_200_test:  资源正确传输(http)；

测试2：http_404_test:  资源不存在(http)；

测试3：http_in_dir_test:  资源在其他目录中(http)；

测试4：http_range1_test:  一定范围[a,b]传输资源(http)；

测试5：http_range2_test: 一定范围[a,end]传输资源(http);

预计用时：提交成功后5s