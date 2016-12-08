# Sharp Your Saw

- [alias & dotfiles](#dotfiles)
- [bash-completion](#bash-completion)
- [ssh-no-pwd](#ssh-no-pwd)
- [vim](#vim)
- [tmux](#tmux)
- [automation using python fabric](#fabric)
- [zsh/oh-my-zsh/xx-completion](#zsh)
- [misc](#misc)

---

## <a name="dotfiles"></a> alias & dotfiles

1. alias/function

    - 把经常使用的很长的命令做成一个简短的alias/function

      ```bash
       # python fabric alias 
       alias fabb='fab --user=root --password='\''Nsky@0!6'\'' --parallel --pool-size=8 -H'
      ```

      ```bash
        # json pretty print
        alias pp_jon='python -mjson.tool'
      ```

      ```bash
       #alias to open OpenDJ control panel, auto filling username/pwd
       export OPENDJ_HOME="/usr/local/opendj/"
       #opendj control-panel connect 
      function ctl () {
          local host="${1:-localhost}"
          local port="${2:-4444}"
          ${OPENDJ_HOME}/bin/control-panel --remote --trustAll --hostname "${host}" --bindDN  'cn=Directory Manager' --bindPassword 'Nsky@0!6' --port "${port}" & 
      }
      ```

    - 把这些alias/function放到你的dotfiles, 比如 $HOME/.bashrc (每次启动bash时，会自动source $HOME/.bashrc)


2. dotfiles

    [我个人的.bashrc](https://github.com/westwin/dotfiles), 主要包括

    - PS1的设置(命令行提示符)
    - 常用的alias
    - bash auto completion(命令智能补齐)
    - cd/ls 时自动纠错
    - cd/ls 时自动纠正大小写
    - 常用的.vimrc
    - 其他

3. ctrl + r 搜索命令的历史记录

4. $! 代表上次执行命令的参数列表

5. !ps 上次执行的ps命令

6. \vi, 不用vi这个alias，用原生的vi命令

---


## <a name="bash-completion"></a> bash-completion

- bash下命令行智能补齐, 安装配置步骤如下:
    - yum install -y bash-completion
    - 在$HOME/.bashrc中source一下/usr/share/bash-completion/bash_completion

- 演示一下fabric/openshift的自动补齐

---

## <a name="ssh-no-pwd"></a> ssh-no-pwd
每次总是输入用户名和密码很繁琐，ssh可以通过验证证书的方式自动登录.

- 生成你自己的证书/私钥对
```
 def create_ssh_key():
     """
     create local ssh keys
     """
     local_key_dir = '/root/.ssh/id_rsa'
     run("echo -e 'y\n' | ssh-keygen -t rsa -N '' -f %s" % local_key_dir)
```

- 把你的证书导入至远程目标机器
```
ssh-copy-id -i $HOME/.ssh/id_rsa.pub root@remote_server
```

- git也可以通过这种方式免登录(bitbucket里设置access key)

- 甚至有些机器禁止"用户名+密码"这种登录方式，仅允许通过证书登录(比如emm proxy server禁止root用户用密码登录)

- N台server之间ssh互相免密码登录(比如Openshift通过ansible脚本安装之前就需要这个)

---

## <a name="vim"></a> vim
- 抛弃vi,拥抱vim/emacs吧. vim用户通常alias vi=vim
- vim分屏:vs 或:sp
- vim各种快捷键自行google
- vimrc常用设置
```
    set expandtab
    set tabstop=4
    set shiftwidth=4  " number of spaces to use for autoindenting
    set shiftround    " use multiple of shiftwidth when indenting with '<' and  '>'

    filetype plugin on

    set hidden
    syntax on
    set incsearch
    set hlsearch
    set autowrite
```
- vimr插件管理工具Vundle
- awesome vimrc (google 一下吧)
- vim常用插件
    - auto-pairs
    - supertab
    - instant-markdown
    - mru
    - 等等等等

---

## <a name="tmux"></a> tmux
 分屏神器，不用多说，最流行的tmux的配置照搬tmux的大神的配置即可(忘记大神的姓名了),或者照搬我的 [我个人的.bashrc](https://github.com/westwin/dotfiles)

- 演示
- [tmux in nested tmux](https://github.com/westwin/seminar/blob/master/linux/tips/tmux_in_nested_tmux.md)

---

## <a name="fabric"></a> automation using python fabric

- 已演示过，参见[我的fabfiles](https://github.com/westwin/fabfiles) 以及[fabric简介](https://github.com/westwin/seminar/blob/master/python-fabric/101.md)

- 或者参见我们的Jenkins各种自动装机脚本

---

## <a name="zsh"></a> zsh/oh-my-zsh/xx-completion
最大的必杀及来了，zsh， [oh-my-zsh社区](http://ohmyz.sh/)

- 和bash一比，bash简直弱暴了...
- oh-my-zsh社区中各种各样的插件
    - 演示一下命令行打开JIRA的某个链接(jira插件)
    - git的常用alias
    - 命令行打开google搜索(google插件)
- 各种各样的auto-completion
    - 演示一下高级的fabric自动补齐(可以提示fabric的task列表)
- cd到文件夹不用带cd命令
- ~设置切换到常用文件夹
- 等等等等，建议学一下(搞linux命令行不会zsh不好意思出门啊)

---

## <a name="misc"></a> misc
以下简单列举一下我日常工作中常用到的一些alias/function:

1. opendj相关的
2. 远程同步文件相关的rsync
3. team中大部分人的虚拟机列表

```
####################lab env################################
function lab_alias(){
    local SVC_USER=nqsky
    local SVC_HOME=/home/${SVC_USER}

    labs=(build wayne1:wayne1 cl1 cx1 xfd1 xfd2 xf1 xf2 xf3 xf4 xf5 xf6 xf7 xf8 xf9 wab1 hh1 int1 int2 ut1 qa1 qa4 qa5)
    for lab in "${labs[@]}"; do
        #echo $lab
        name=$(echo $lab | cut -d ':' -f1)
        ip=$(echo $lab | cut -d ':' -f2)

        #echo $name
        #echo $ip
        lower=$(echo $name | tr '[:upper:]' '[:lower:]')
        upper=$(echo $name | tr '[:lower:]' '[:upper:]')

        env_cmd="export $upper=$SVC_USER@$ip:$SVC_HOME/" 
        alias_svc_ssh="alias n$lower='ssh $SVC_USER@$ip'"
        alias_root_ssh="alias r$lower='ssh root@$ip'"
        eval "${env_cmd}"
        eval "${alias_svc_ssh}"
        eval "${alias_root_ssh}"
    done
}

#setup lab alias.
lab_alias

```


---

