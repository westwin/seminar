# Controlling startup order in Compose

refer to [startup order](https://docs.docker.com/compose/startup-order/)

---

## started vs liveness vs readiness
启动状态/健康状态通常包括,  
  - started(but not ready for serivce yet)
  - liveness
  - readiness

started是指已经启动了，但是呢, app还不能正常对外提供服务.  
liveness往往是说app活着呢,(比如监听的端口是活着的), liveness并不意味着app可以正常工作   
readiness是指app真的已经对外提供服务了.   


---

## docker compose depends-on
compose中的depends-on只是决定了各个service的启动顺序，但是不是说必须得等到被依赖的service进入readiness状态，才开始启动依赖服务.

最常见的usercase比如，一个app需要依赖一个db的服务，app在启动时，往往会去尝试连接db服务，而db服务如果不是readiness状态，则app启动失败.(即所谓的一种resilience)

最简单的解决方案依赖wait-for-it wrapper script

---

## wait-for-it wrapper script
[wait-for-it](https://github.com/vishnubob/wait-for-it)


---

## secret behind /dev/tcp/$HOST/$PORT
wait-for-it这个脚本最核心的东西其实是一个/dev/tcp/$HOST/$PORT的东西，

在bash中，当你 echo > /dev/tcp/$HOST/$PORT的时候，会尝试去连接指定的$HOST:$PORT

参见  
  - [tldp](http://www.tldp.org/LDP/abs/html/devref1.html)
  - [linuxjournal](http://www.linuxjournal.com/content/more-using-bashs-built-devtcp-file-tcpip)


---

