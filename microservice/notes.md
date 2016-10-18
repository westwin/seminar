- [微服务: 为可部署和可扩展分解应用](http://www.jdon.com/46396)
    > 通过引入微服务，能让应用变得更小更简单，易于理解和开发，减少启动时间，这对于在云平台上
    > 运行很重要，远离Jar和ClassPath地狱，再也不需要OSGI了(banq注：这点我早在微服务刚出来就预感到了)
    > 这样让开发变得可扩展，开发 部署和扩展服务都变得独立，相互没有依赖。
    > **这样从一个单一技术堆栈演变成模块多框架的开发堆栈，每个服务都可以使用不同的技术堆栈来实现开发**。
    > 这样可以引入尝试更多的新技术如Scala Akka Play Node.js, Vertx等等。

    > 如果前端直接连接后端RESTful服务会显得琐碎，也会增加网络的通讯次数，提高延时，降低性能，推荐在两者之间引入API网关代理。
    > ![API Gateway](http://img.jdon.com/27031/23144928)
    >
    > 这个API Gateway可以使用Node.JS来实现，能够实现REST Proxy和Event Publishing事件发布。
    >
    > 成熟应用可见: [Netflix](http://techblog.netflix.com/2013/01/optimizing-netflix-api.html) 优化的API，
    > 总之这个API网关需要满足**性能和可扩展伸缩性**：**非堵塞和异步并发编程**.
    >
    > 最后整个架构如下，可兼容传统的服务器端MVC(也称为Web端)和现代移动设备。
    > ![micro-service archi](http://img.jdon.com/27032/23144928)

- [微服务框架](http://www.lightbend.com/lagom)
- [如何让Java以光的速度跨线程通信？](http://www.jdon.com/46039)
    > Akka的伟大之处是跨进程通信，特别是Actor是能够跨越不同JVM节点实现分布式通信。

    > [Lock-Free-Algorithms](http://www.infoq.com/presentations/Lock-Free-Algorithms)
    
    > 无锁队列提供比锁队列更好的性能。锁队列中在当一个线程获得锁，其他线程将被阻塞，直到该锁被释放的。
    > 在无锁算法的情况下，生产者线程可以产生消息，但不阻止其他生产者线程，以及其他消费者，而从队列中读取的消费者不会被阻塞

    > **这个无锁队列据测试结果是超过每秒100M ops，是JDK的并发队列实现的10倍**

    > LMAX Disruptor RingBuffer , 高性能线程间通信库包. SPSC/MPSC/MPMC

- [基于Spring Boot, Axon CQRS/ES,和Docker构建微服务](http://www.jdon.com/48138)
