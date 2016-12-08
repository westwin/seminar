# Shell 编程风格点滴

## 推荐风格参考
1. [Google Shell Code Syle](https://google.github.io/styleguide/shell.xml)
2. [Advanced Bash-Scripting Guide](http://www.tldp.org/LDP/abs/html/)

## 风格摘选
1. shebang #!/bin/bash 
    ```
    #!/bin/bash
    ```
    **注**: 在CentOS里，貌似/bin/sh , /usr/bin/bash, 
    /bin/bash都是同一个东西，用md5sum来查看他们的checksum都一样

2. 推荐用snake case风格.不推荐camelCase.
   **函数名里不要包括-(有些系统会报错)**
    ```
    #推荐函数名
    function say_hello()

    #不推荐函数名
    function notRecommendedFunctionName()
    function not-recommend-func()
    ```
3. soft quote vs hard quote（“ vs ')

4. 变量引用推荐使用${var}, 不推荐$var

5. 变量引用推荐使用soft quote, 即"${var}"

6. test操作推荐使用[[ ... ]], 不推荐[ ... ]
    ```
    #推荐做法
    age=100
    if [[ "${age}" -ge 30 ]]; then
        echo "you are not young!"
    fi

    #不推荐
    if [ "${age}" -ge 30 ]; then
        echo "you are not young!"
    fi
    ```

7. 字符串比较
    1. "等于"比较推荐使用 == 或者 =
    ```
    name="John Doe"
    if [[ "${name}" == "John Doe" ]]; then
        echo "same string"
    fi
    ```
    不推荐使用所谓的filler character,即不推荐酱紫:
    ```
    name="John Doe"
    if [[ "${name}X" == "John DoeX" ]]; then
        echo "same string"
    fi

    ```

    2. "大于"推荐使用>, "小于"使用<

    3. 正则匹配(模糊匹配)
    
       参见[Comparison Operators](http://www.tldp.org/LDP/abs/html/comparison-ops.html)

8. 数字比较
    1. 大于推荐使用 -gt(greater than),不推荐> 
    2. 大于等于推荐使用 -ge(greater or equal), 不推荐使用>= 
    3. 小于推荐使用 -lt(less than), 不推荐使用< 
    4. 小于大于推荐使用 -le (less or equal), 不推荐使用<= 
    5. 等于推荐使用-eq (equal), 不推荐使用==或=

9. 算数运算 ((  ))
    ```
    a=1
    b=2
    c=$((a+b))
    echo "1+2=${c}" #输出是3

    echo "$a+$b" #输出为1+2,不会做加法运算
    ```

10. 数组()
    ```
    names=("Chen Xi" "Wayne")
    for name in "${names[@]}"; do
        echo $name
    done

    echo "first name: ${names[0]}"
    echo "second name: ${names[1]}"

    echo "All names: ${names[@]}"
    ```

11. 局部变量定义, local

12. 只读变量定义, readonly const_var 或 declare -r CONST=100

13. "函数返回输出" vs "exit code"
    ```
    #得到函数的exit code
    echo "hi you" 
    ret=$?
    if [[ "${ret}"  -eq 0 ]]; then
        echo "succeeds"
    fi

    #得到函数的返回输出
    output="$(echo hi you)"
    echo "output is: ${output}"

    #另得到函数的返回输出，建议使用$()的方式，不建议用上引号`的方式
    output=`echo this is not recommended`
    echo "output is: ${output}"

    #如果不需要得到函数的返回输出，直接调用即可，不需要用$()
    #另注意这里用的是单引号的hard quote
    echo '$() is not necessary'
    ```

14. 命令行option， long-option vs short-option
    ```
    #getpots只支持short-option,如果需要long-option,可以使用GNU c写的外部程序getopt , (没有s)
    while getopts 'hb:' OPT; do
       case $OPT in
           h)
             usage
             ;;
           b)
             bak=${OPTARG}
             ;;
           ?)
             usage
       esac
    done
    shift $(($OPTIND - 1))
    ```

15. shell vs python script 

    > 个人建议简单短小的脚本可以使用shell，因为shell的可读性可维护性都不如python. 
    > 如果脚本比较大，或者比如需要操作高级的数据类型比如xml/json/sql等，建议使用python
