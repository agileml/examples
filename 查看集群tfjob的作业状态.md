## 查看tfjob的作业状态

使用 kubectl get tfjob能查看当前命名空间下所有 tfjob的状态

![image-20191117223146060](C:\Users\zoux\AppData\Roaming\Typora\typora-user-images\image-20191117223146060.png)





tfjob状态共五种：

​             ：       状态为空，对应的pod还没启动

Created:        已经成功创建，但是对应pod是 pending

Failed:            创建失败         

Running:        正在运行中

Completed:   作业已完成



可以通过kubectl describe tfjob tfjobName 查看具体情况

eg:

![image-20191117223657752](C:\Users\zoux\AppData\Roaming\Typora\typora-user-images\image-20191117223657752.png)



同时还可以对该tfjob下的pod使用 describe命令，查看pod的详细信息。