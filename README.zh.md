这里是 decentral-http （去中心http应用 https://github.com/tomzcn/decentral-http ）的子项目 entrance （入口）。

deceltral-http 没有中心服务器，只要有至少一个服务器也能维持运行，所有服务器之间同步，类似于一个无中心的虚拟广播网络，只要能连上一个服务器就等于加入了服务器群。 decentral-http 可以布置到能够作为http客户端的http服务器上（亚马逊云的lambda不行，render.com可以）。entrance子项目的目的是多个服务器共同维护一个文档。

目前最好用的演示服务器： https://test-render-com.tomzcn.repl.co

演示：目前在 render.com 上可以试验一下这个项目。render.com可以免费运行python代码。

https://decentral-http-entrance.onrender.com/server/article 

https://tomzheng-test-python.onrender.com/server/article

https://decentral-http-entrance-1.onrender.com/server/article 

是目前部署的演示项目。经试验三个服务器之间互联没有问题。

【危险】要注意render.com不提供免费磁盘，在很短的时间内就会清空磁盘，因此试验操作最好在几十秒钟内完成，并且不能把render.com做为真实使用的服务器。 

【提醒】render.com 的免费服务很不稳定。如果提交后没有显示“ok”就要反复提交多次。同时部署速度也很慢。

下面是演示网站的操作步骤：
------------------------

在浏览器上将两个网址同时打开，直到网页显示完毕。

打开decentral服务器网址，点击“homepage”，点击“add server”，输入 https://tomzheng-test-python.onrender.com/server/post 和 https://decentral-http-entrance.onrender.com/server/post 并提交。这样decentral服务器的输入就可以同步到tomzheng服务器了。

点击”homepage“，点击“article”，输入“d”，点击“提交”。

打开tomzheng服务器网址，刷新网页。这时可以看到在另一个服务器上看到的“d”。

在tomzheng服务器上点击“homepage”，点击“article”，在“d”后面输入“t”，点击“提交”。

切换到decentral服务器刷新网页，可以看到“d”后面出现了“t”。

然后还可以重复上面的步骤试验添加第三个服务器。 

下面是在 render.com 上建立新服务器的操作步骤：
--------------------------------------------

注册登录render.com。

添加webservice。

在最后一行输入github项目地址： https://github.com/tomzcn/test-render-com 。点击下一步。

输入自己的新建的服务器地址。

在 start command 那里输入 "python3 app.py"，其它不需要输入。

点击发布，然后等待发布过程的完成，就可以了。



