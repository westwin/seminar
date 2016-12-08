# Tmux in nested Tmux

## 应用场景
两台机器machine-a和machine-b，分别安装了tmux。
在machine-a中开了一个tmux的窗口window-a, 然后在window-a中ssh到机器machine-b中，而machine-b中也运行了tmux的窗口window-b.
那么window-b其实就是在window-a中的一个嵌套的tmux session.  
 
 问题就是如何在window-a中通过快捷键切换到window-b的tmux的session去。

## 快捷键切换
假设machine-a和machine-b中的.tmux.conf的配置一样，并假设prefix的配置为Ctrl+a(缺省的为Ctrl+b), 即

```
set-option -g prefix C-a

```

在tmux中可以配置个特殊的快捷键用来发送prefix这个键(即send-prefix)，我的配置如下(C-b在我的配置里没有被其他快捷键占用):

```
bind-key -n C-b send-prefix

```

那么可以通过在machine-a中用快捷键Ctrl+b来切换到window-b中去.. 然后用来触发window-b中的tmux窗口的切换。

## 偶的dotfiles配置（包括tmux以及bashrc,vimrc)

```
curl -sSL https://github.com/westwin/dotfiles/archive/master.zip > dotfiles.zip
  
unzip -o dotfiles.zip
    
sh dotfiles-master/install.sh
```
