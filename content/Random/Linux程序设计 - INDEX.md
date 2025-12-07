---
date: 2025-12-01
tags:
  - index
---
# 第一章
##  1. Linux 背景与发展 (常考选择题)

- **起源**：Linux 雏形是 Minix，由 **Linus Torvalds** 于 1991 年编写 。
- **GNU与GPL**：
    - **GNU计划**：目标是发展完全免费自由的 Unix-like 操作系统 。
    - **GPL协议**：通用公共许可证，确保源码共享和自由修改 。Linux 内核基于 GPL 发布。
    - **开源 vs 免费**：开源不仅免费，还必须开放源代码允许修改 。
- **[[POSlX标准]]**：定义了操作系统为应用程序提供的接口标准，保证了程序在不同 Unix-like 系统间的可移植性 。

## 2. Linux 系统组成 (常考填空题)

Linux 系统主要由三部分组成 ：
1. **内核 (Kernel)**：核心，管理硬件、内存、进程等。
2. **Shell**：用户与内核交互的接口（命令解释器），常用的默认 Shell 是 **bash** 。
3. **应用程序**：编辑器、编译器、工具等。

## 3. 文件系统与目录 (基础概念)

- **树型结构**：Linux 没有盘符（C盘/D盘），只有一个根目录 `/` 。
- **路径**：
    - **绝对路径**：从 `/` 开始，如 `/home/sunny/a.c` 。
    - **相对路径**：相对于当前目录，如 `../bin` 。

- **重要符号**：
    - `.` 代表当前目录。
    - `..` 代表上一级目录 。
    - `~` 代表当前用户的主目录 (Home Directory) 。
## 4. 硬链接与软链接 (高频简答/选择题)

- **Inode ([[索引节点]])**：文件的唯一标识，存储文件的属性（权限、大小、位置等），但不包含文件名 。
- **[[硬链接]] (Hard Link)**：
    - **原理**：指向同一个 Inode 的不同文件名。
    - **特点**：删除原文件名，文件内容不丢失（除非链接数为0）。不能跨分区，不能链接目录 。
    - **命令**：`ln 源文件 目标文件` 。
        
- **[[软链接]]/符号链接 (Soft/Symbolic Link)**：
    - **原理**：类似 Windows 的快捷方式，是一个新文件，内容是指向源文件的路径。
    - **特点**：有新的 Inode。删除源文件，软链接失效。可以跨分区，可以链接目录 。
    - **命令**：`ln -s 源文件 目标文件` 。

## 5. 关键命令 (Shell脚本编程基础)


- **文件操作**：
    - `ls -l`：长格式显示文件详细信息 。
    - `cp -r`：递归复制目录 。
    - `rm -rf`：强制递归删除（慎用） 。
    - `cat`：显示文件内容 。

- **查找 (Find)** ：
    - 格式：`find [路径] [表达式]`
    - 常用：`find . -name "*.c"` (按名字找), `find . -type f` (找普通文件), `find . -size +10k` (按大小找)。
- **内容查找 (Grep)** ：
    - 格式：`grep [选项] "字符串" 文件`
    - 常用：`-n` (显示行号), `-v` (反选/不包含), `-r` (递归查找)。


## 6. 权限管理 (必考计算题)

Linux 文件权限由 9 位字符组成 (如 `rwxr-xr--`)，对应 User(属主), Group(属组), Other(其他人) 。

- **权限数值**：
    - `r` (Read, 读) = **4**
    - `w` (Write, 写) = **2**
    - `x` (Execute, 执行) = **1**
    - `-` (无权限) = **0**

- **chmod 命令**：
    - **数字法**：`chmod 755 file` (即 rwxr-xr-x: 4+2+1=7, 4+0+1=5, 4+0+1=5) 。
    - **符号法**：`chmod u+x file` (给属主增加执行权限) 。
- **chown 命令**：改变文件属主 `chown user:group file`

# 第二章 [[Shell]]程序设计

## 1. 脚本的基本格式与执行 (基础)

- **第一行 (Shebang)**：脚本必须以 `#!/bin/bash` (或 `#!/bin/sh`) 开头，告诉系统用哪个解释器 。
- **注释**：以 `#` 开头 。
- **退出码**：`exit 0` 表示成功，非0表示失败 。
- **执行方式**：
    1. 赋予权限：`chmod +x myscript.sh` 。
    2. 执行：`./myscript.sh` (如果不在PATH路径下，必须加 `./`) 。

## 2. 变量定义与引用 (易错点)

- **定义**：`变量名=值`。**注意：等号两边千万不能有空格！** 。
    - 错误：`myvar = hello`
    - 正确：`myvar=hello`
- **引用**：使用 `$` 符号，如 `$myvar` 或 `${myvar}` 。
- **引号的区别** (选择题常考) ：
    - **双引号 `""`**：允许变量替换 (如 `echo "x=$x"` 输出 `x=5`)。
    - **单引号 `''`**：所见即所得，不进行变量替换 (如 `echo 'x=$x'` 输出 `x=$x`)。
    - **反引号 `` ` ``**：执行命令并将结果赋值给变量 (如 `val=`expr 2 + 2``) 。

## 3. 位置参数 (必考：脚本如何接收参数)

这在编写通用脚本时非常关键，例如“写一个脚本，处理用户指定的文件”。
- `$0`：脚本程序本身的名称 。
- `$1`, `$2` ...：第一个参数，第二个参数 。
- `$#`：参数的总个数 。
- `$*` 或 `$@`：所有参数的列表 。
- `$?`：上一个命令的退出状态 (0表示成功) 。


## 4. 运算与测试 (逻辑核心)

Shell 的逻辑判断语法非常特殊，**`[` 和 `]` 内部必须有空格** 。

- **算术运算**：使用 `$((expression))`，如 `echo $((1+3))` 。
- **条件测试 `[ expr ]`** (重点记忆表格)：
    - **数字比较** ：
        - `-eq` (等于), `-ne` (不等于)
        - `-gt` (大于), `-lt` (小于)
        - `-ge` (大于等于), `-le` (小于等于)
    - **字符串比较** ：
        - `=` (相等), `!=` (不相等)
        - `-z` (空串), `-n` (非空)
    - **文件测试** (常考) ：
        - `-f` (普通文件)
        - `-d` (目录)
        - `-e` (文件存在)
        - `-r` (可读), `-w` (可写), `-x` (可执行)

## 5. 流程控制 (大题骨架)

**A. if 语句**

```Bash
if [ 条件判断 ]; then
    命令1
elif [ 条件判断 ]; then
    命令2
else
    命令3
fi
```

_注意：`if` 和 `[` 之间要有空格，`[` 和条件之间也要有空格。_

**B. for 循环** 常用于遍历文件列表。

```Bash
for var in item1 item2 ...
do
    命令
done
```

_实例_：遍历 /etc 目录下所有 r 开头的文件 ：

```Bash
for myfile in /etc/r*
do
    if [ -d "$myfile" ]; then
        echo "$myfile is a directory"
    fi
done
```

**C. while 循环**

```Bash
while [ 条件 ]
do
    命令
done
```

**D. case 语句** (多重分支，类似 switch) 常用于处理菜单选择。

```Bash
case "$变量" in
    模式1)
        命令 ;;
    模式2)
        命令 ;;
    *)
        默认命令 ;;
esac
```

---

### 讲师画重点：如何应对“编写Shell脚本”大题

考试通常会出这类题目：“编写一个脚本，判断用户输入的文件是否存在，如果是目录则进入，如果是普通文件则显示内容。”

**模板代码 (背诵并理解)：**

```Bash
#!/bin/bash

# 1. 检查是否输入了参数
if [ $# -eq 0 ]; then
    echo "Usage: $0 <filename>"
    exit 1
fi

filename=$1

# 2. 判断文件是否存在
if [ ! -e "$filename" ]; then
    echo "Error: File $filename does not exist."
    exit 1
fi

# 3. 判断是目录还是文件
if [ -d "$filename" ]; then
    echo "$filename is a directory."
    cd "$filename"
    ls -l
elif [ -f "$filename" ]; then
    echo "$filename is a regular file."
    cat "$filename"
else
    echo "Unknown file type."
fi

exit 0
```




# 第三章 文件操作与文件管理 (Exam Focus: C程序编写核心)

## 1. 核心概念：文件描述符 (File Descriptor)

- **定义**：在 Linux 内核中，打开的文件通过**非负整数**来标识，这个整数就是文件描述符 1。
- **默认描述符**：程序运行时自动打开三个描述符 2：
    - `0`：标准输入 (Standard Input)
    - `1`：标准输出 (Standard Output)
    - `2`：标准错误 (Standard Error)

## 2. 关键系统调用 API (必背代码)

考试写 C 程序时，你必须熟练使用以下四个函数：`open`, `read`, `write`, `close`。
**A. open - 打开或创建文件**

```c
#include <fcntl.h>
#include <sys/types.h>
#include <sys/stat.h>

int open(const char *path, int oflags, mode_t mode);
```

- **功能**：建立到文件或设备的访问路径 3。
- **返回值**：成功返回文件描述符（最小未用整数），失败返回 -1 4。
- **关键参数 `oflags`** (必考，需按位或 `|` 组合) 5：
    - `O_RDONLY`：只读
    - `O_WRONLY`：只写
    - `O_RDWR`：读写
    - `O_CREAT`：文件不存在则创建（**重点**：此时必须提供第三个参数 `mode`）
    - `O_APPEND`：追加写入
    - `O_TRUNC`：长度截断为0（清空文件）
- **关键参数 `mode`** (权限设置) 6：
    
    - `S_IRUSR` (读), `S_IWUSR` (写), `S_IXUSR` (执行) —— 针对用户 (User)
    - `S_IRGRP` ... —— 针对组 (Group)
    - `S_IROTH` ... —— 针对其他人 (Other)
    - _提示：如果不记得宏名，也可以用八进制数字，如 `0644` (rw-r--r--)_

**B. write - 写文件**

```c
size_t write(int fildes, const void *buf, size_t nbytes);
```
- **功能**：把 `buf` 中的前 `nbytes` 个字节写入文件 7。
- **返回值**：实际写入的字节数；返回 0 表示未写入；返回 -1 表示出错 8。

**C. read - 读文件**

```c
size_t read(int fildes, void *buf, size_t nbytes);
```

- **功能**：从文件中读出 `nbytes` 个字节放入 `buf` 9。
- **返回值**：实际读入的字节数；**返回 0 表示到达文件尾 (EOF)**；返回 -1 表示出错 10。

**D. close - 关闭文件**

```c
int close(int fildes);
```
- **功能**：终止文件描述符与文件的关联 11。
- **返回值**：成功返回 0，失败返回 -1 12。
## 3. 其他重要操作 (辅助考点)

- **lseek**：移动文件的读写指针。
    - `lseek(fd, 0, SEEK_END)`：将指针移到文件末尾（常用于计算文件长度） 13131313。
- **copy程序逻辑**：这是最经典的考试题型——“编写一个程序实现文件复制”。逻辑是 `open` 源文件 -> `open` 目标文件 -> `while(read > 0) { write }` -> `close` 14。

---
### 讲师画重点：如何应对“编写C程序”大题 (Part 1)

考试可能会出这样的题：“编写一个C程序，创建一个名为 `test.txt` 的文件，写入字符串 'Hello Linux'，然后读取并打印到屏幕。”

**模板代码 (背诵并理解)：**

```c
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
    int fd;
    char *msg = "Hello Linux\n";
    char buffer[128];
    int len;

    // 1. 创建并打开文件 (核心考点：O_CREAT 和 权限)
    // O_RDWR | O_CREAT | O_TRUNC: 读写模式，不存在则创建，存在则清空
    // 0644: 用户读写，其他人只读
    fd = open("test.txt", O_RDWR | O_CREAT | O_TRUNC, 0644);
    if (fd == -1) {
        perror("Open file failed"); // 错误处理也是得分点
        exit(1);
    }

    // 2. 写入数据
    write(fd, msg, strlen(msg));

    // 3. 重置文件指针到开头 (否则读取时指针在末尾，读不到数据)
    lseek(fd, 0, SEEK_SET);

    // 4. 读取数据
    // 返回值大于0表示读取到了数据
    while ((len = read(fd, buffer, sizeof(buffer) - 1)) > 0) {
        buffer[len] = '\0'; // 添加字符串结束符
        printf("Read content: %s", buffer);
    }

    // 5. 关闭文件
    close(fd);

    return 0;
}
```

# 第四章 标准函数库 (Exam Focus: 高级文件操作与常用工具)

## 1. 核心概念：流 (Stream) 与 缓冲 (Buffer)

- **流 (Stream)**：标准库将文件看作流，使用 `FILE *` 指针来标识，而不是文件描述符（整数） 。
- **缓冲**：标准库提供缓冲机制。数据先写入内存缓冲区，满了才调用内核写入磁盘。这减少了系统调用的次数，提高了效率 。
- **三个默认流**：`stdin` (标准输入), `stdout` (标准输出), `stderr` (标准错误) 。

## 2. 文件的打开与关闭 (必考基础)

**A. fopen - 打开文件**

```c
FILE *fopen(const char *filename, const char *mode);
```

- **关键点**：`mode` 字符串的含义（**常考选择/填空**） ：
    - `"r"`：**只读**。文件必须存在。
    - `"w"`：**只写**。文件存在则清空（截断为0），不存在则创建。
    - `"a"`：**追加**。写操作都在文件末尾，不存在则创建。
    - `"r+"`：**读写**。文件必须存在，从头开始写（不会清空）。
    - `"w+"`：**读写**。文件存在则清空，不存在则创建。
    - `"a+"`：**读写**。读从头开始，写永远在末尾。
    - 提示：带 `b` (如 `"rb"`) 代表二进制模式，在 Linux 下通常忽略，但在跨平台代码中很重要 。

**B. fclose - 关闭文件**

```c
int fclose(FILE *stream);
```
- **重要性**：除了释放资源，`fclose` 会**强制刷新缓冲区**，确保数据真正写入磁盘 。

## 3. 读写操作 (根据数据类型选择)

**A. 按字符读写**

- `fgetc(FILE *stream)` / `getc`：读取一个字符。
- `fputc(int c, FILE *stream)` / `putc`：写入一个字符 。

**B. 按行/字符串读写 (常用于处理文本)**

- **`fgets(char *s, int n, FILE *stream)`** (推荐)：
    - 从流中读取字符串直到换行符或读满 `n-1` 个字符。
    - **注意**：它会把换行符 `\n` 也读进去，并在末尾加 `\0` 。
- **`gets(char *s)`** (**千万别用** - 考试考点)：
    - 从标准输入读。**不安全**，因为它不检查缓冲区大小，容易造成**缓冲区溢出** 。考试问“为什么不用 gets”，这就满分回答。

**C. 二进制/数据块读写 (对应系统调用的 read/write)**

```c
size_t fread(void *ptr, size_t size, size_t nitems, FILE *stream);
size_t fwrite(const void *ptr, size_t size, size_t nitems, FILE *stream);
```
- **返回值**：返回实际读/写的**记录数 (items)**，而不是字节数 。
- _场景_：读写结构体、数组等二进制数据。

**D. 格式化读写 (标准库的杀手锏)**

- `fprintf(FILE *stream, ...)`：向文件输出格式化字符串。
- `fscanf(FILE *stream, ...)`：从文件解析格式化输入。
- **`sprintf(char *s, ...)`** (必考)：把格式化的数据写入**字符串** 。
    - _用途_：在 C 程序中构造 Shell 命令或文件路径时非常有用。例如：`sprintf(cmd, "ls -l %s", dirname);`。

#### 4. 其他重要操作

- **`fflush(FILE *stream)`**：强制把缓冲区的数据写出，不必等到缓冲区满 。
- **`fseek` / `ftell`**：对应系统调用的 `lseek`，用于文件定位 。
- **`fileno(FILE *stream)`**：**桥梁函数**。返回流对应的底层**文件描述符** 。
    - _场景_：你用 `fopen` 打开了文件，但突然需要用 `fcntl` (系统调用) 来加锁，就需要 `fileno` 来转换。

---

## 讲师画重点：如何应对“编写C程序”大题 (Part 2 - 标准库版)

如果题目要求“编写程序，将一个结构体写入文件，然后再读取出来显示”，使用标准库比系统调用简单得多。

**模板代码 (标准库版)：**

```c
#include <stdio.h>
#include <stdlib.h>

struct Student {
    char name[20];
    int age;
};

int main() {
    FILE *fp;
    struct Student s1 = {"Li Chengyu", 20};
    struct Student s2;

    // 1. 打开文件用于写入二进制 (w)
    // 考点: fopen 的 mode 参数
    if ((fp = fopen("student.dat", "w")) == NULL) {
        perror("fopen write error");
        exit(1);
    }

    // 2. 写入结构体
    // 考点: fwrite 参数 (指针, 单个大小, 个数, 流)
    if (fwrite(&s1, sizeof(struct Student), 1, fp) != 1) {
        perror("fwrite error");
    }
    
    // 刷新缓冲区并关闭，确保写入磁盘
    fclose(fp);

    // 3. 重新打开用于读取 (r)
    if ((fp = fopen("student.dat", "r")) == NULL) {
        perror("fopen read error");
        exit(1);
    }

    // 4. 读取结构体
    // 考点: fread 参数
    if (fread(&s2, sizeof(struct Student), 1, fp) != 1) {
        perror("fread error");
    } else {
        printf("Read Name: %s, Age: %d\n", s2.name, s2.age);
    }

    // 5. 关闭
    fclose(fp);
    return 0;
}
```
# 第五章 文件和目录的维护 (Exam Focus: 目录操作与链接管理)

## 1. 权限与所有者 (系统调用版)

第一章我们讲了 `chmod` 命令，这里要掌握的是对应的 **C 系统调用**。

- **`chmod` 函数**：
    
    ```c
    int chmod(const char *path, mode_t mode);
    ```
    - **考点**：`mode` 参数通常使用八进制数字，如 `0644` 。
- **`chown` 函数**：

    ```c
    int chown(const char *path, uid_t owner, gid_t group);
    ```

    - **考点**：需要配合 `getuid()` (获取当前用户ID) 和 `getgid()` (获取当前组ID) 使用 。


## 2. 链接管理 (高频考点：硬链接 vs 软链接)

这是本章理论部分最容易出**简答题**或**选择题**的地方。

- **硬链接 (Hard Link)**：
    - **本质**：两个文件名指向同一个 **Inode** 。
    - **创建**：`link(const char *path1, const char *path2)` 。
    - **删除**：**`unlink(const char *path)`** 。
        - **注意**：`unlink` 只是将 Inode 的链接计数减 1。只有当计数为 0 且没有进程打开该文件时，文件内容才会被真正删除 。这也是为什么我们在代码中常用 `unlink` 来删除临时文件。
            
- **软链接 (Symbolic Link)**：
    
    - **本质**：一个独立的文件，内容是另一个文件的**路径** 。
    - **创建**：`symlink(const char *path1, const char *path2)` 。
        

## 3. 目录操作 (基础)

- **创建/删除**：
    - `mkdir(path, mode)`：创建目录 。
    - `rmdir(path)`：**只能删除空目录** 。
- **导航**：
    - `chdir(path)`：相当于 Shell 中的 `cd` 命令，改变当前工作目录 。
    - `getcwd(buf, size)`：相当于 Shell 中的 `pwd` 命令，获取当前绝对路径 。

## 4. 扫描目录 (C程序编写核心)

如果考试要求你“编写一个程序，列出当前目录下的所有文件”，这部分是必须掌握的。

Linux 使用**目录流 (Directory Stream)** 的概念，类似于文件流。

- **`DIR *opendir(const char *name)`**：打开目录，返回指向目录流的指针 。
- **`struct dirent *readdir(DIR *dirp)`**：读取下一个目录项 。
    - **`struct dirent` 结构体** (必背成员) ：
        - `d_ino`：Inode 编号。
        - **`d_name`**：文件名 (最常用)。
- **`int closedir(DIR *dirp)`**：关闭目录流 。

# 第六章 Linux环境 (Exam Focus: 参数解析、环境变量、时间处理)

## 1. 命令行参数 (必考：main函数的写法)

在 Linux C 编程中，`main` 函数的标准写法必须背下来：

```c
int main(int argc, char *argv[])
```

- **`argc` (Argument Count)**：参数的个数。注意：程序名本身算一个参数 。
- **`argv` (Argument Vector)**：字符串数组。`argv[0]` 是程序名，`argv[1]` 是第一个参数，以此类推 。


**进阶考点：`getopt` 函数** 如果题目让你写一个支持选项（如 `./test -a -b`）的程序，用 `getopt` 是最标准的做法。

- **原型**：`int getopt(int argc, char *const argv[], const char *optstring);`
- **`optstring`**：例如 `"if:lr"` 表示支持 `-i`, `-l`, `-r` 选项，其中 `-f` 后面必须跟一个参数（冒号表示）。
- **外部变量**：`optarg` 指向选项后的参数值 。

## 2. 环境变量 (常考填空/简答)

环境变量（如 `PATH`, `HOME`）是 Shell 传递给程序的重要信息。

- **获取变量**：`char *getenv(const char *name)`。例如 `getenv("HOME")` 返回用户主目录路径 。
- **设置变量**：`int putenv(const char *string)`。格式为 `"NAME=value"` 。
- **全局变量**：`extern char **environ` 可以访问所有环境变量 。

## 3. 时间与日期 (高频编程题考点)

Linux 时间处理涉及几种格式的转换，这是考试中最容易晕的地方，请看清逻辑链条：

1. **原始时间 (`time_t`)**：从1970年1月1日0点到现在的**秒数**（长整型）。
    - 获取函数：`time_t time(time_t *tloc);` 。
2. **分解时间 (`struct tm`)**：将秒数分解为年、月、日、时、分、秒的结构体。
    - 转换函数：`struct tm *gmtime(const time_t *timeval)` (转为格林尼治时间) 或 **`localtime(...)`** (转为本地时间，考试通常用这个) 。
    - **`tm` 结构体陷阱** (必考选择题)：
        - `tm_year`：从1900年开始计算的年份（如2025年，值为125）。
        - `tm_mon`：月份范围是 **0-11** (0是1月) 。
3. **格式化时间 (字符串)**：
    
    - 简单版：`char *ctime(const time_t *timeval)` 直接返回类似 "Wed Jun 30 21:49:08 1993\n" 的字符串 。
    - **定制版**：**`strftime`** (最重要) 。
        - 用法：`strftime(buf, 256, "%Y-%m-%d %H:%M:%S", tm_ptr);`

---

## 讲师画重点：如何应对“编写C程序”大题 (Part 3 - 环境篇)

结合第三章的文件操作，考试可能会出一道综合题：“编写一个程序，支持通过命令行参数 `-f` 指定文件名，如果文件不存在则创建，并将当前的**系统时间**和**HOME环境变量**写入该文件。”

**模板代码 (背诵并理解)：**

```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <time.h>
#include <string.h>

// 覆盖知识点：命令行参数、文件操作、环境变量、时间处理
int main(int argc, char *argv[]) {
    int opt;
    char *filename = NULL;
    FILE *fp;
    time_t raw_time;
    struct tm *time_info;
    char time_str[80];
    char *home_dir;

    // 1. 解析命令行参数 (getopt)
    // 这里的 "f:" 表示 -f 后面必须跟一个文件名参数
    while ((opt = getopt(argc, argv, "f:")) != -1) {
        switch (opt) {
            case 'f':
                filename = optarg; // optarg 指向 -f 后的参数
                break;
            default:
                fprintf(stderr, "Usage: %s -f <filename>\n", argv[0]);
                exit(1);
        }
    }

    if (filename == NULL) {
        fprintf(stderr, "Error: Filename required. Use -f <filename>\n");
        exit(1);
    }

    // 2. 获取当前时间
    time(&raw_time); // 获取秒数
    time_info = localtime(&raw_time); // 转为本地时间结构
    // 格式化时间：年-月-日 时:分:秒
    strftime(time_str, sizeof(time_str), "%Y-%m-%d %H:%M:%S", time_info);

    // 3. 获取环境变量
    home_dir = getenv("HOME");
    if (home_dir == NULL) {
        home_dir = "Unknown";
    }

    // 4. 文件操作 (标准I/O)
    // "a" 模式：追加写入，如果文件不存在会自动创建
    if ((fp = fopen(filename, "a")) == NULL) {
        perror("File open error");
        exit(1);
    }

    // 格式化写入文件
    fprintf(fp, "[Log Entry]\n");
    fprintf(fp, "Time: %s\n", time_str);
    fprintf(fp, "User Home: %s\n", home_dir);
    fprintf(fp, "--------------------\n");

    printf("Data written to %s successfully.\n", filename);

    // 5. 关闭文件
    fclose(fp);

    return 0;
}
```


# 第七章 数据管理 (Exam Focus: 内存管理与锁机制)

## 1. 动态内存管理 (基础必考)

Linux 程序通常不允许直接访问物理内存，而是使用虚拟内存。
- **分配内存 `malloc`**：

    ```c
    void *malloc(size_t size);
    ```
    - **考点**：返回 `void *` 指针，失败返回 `NULL` 1。分配的内存未初始化，可能包含垃圾数据。
    - **`calloc`**：类似于 `malloc`，但会自动将内存初始化为 **0** 2。
    - **`realloc`**：改变已分配内存块的大小 3。
- **释放内存 `free`**：
    ```c
    void free(void *ptr_to_memory);
    ```
    - **考点**：必须配对使用。释放后不能再访问该块内存，否则会导致未定义行为。
- **常见错误**：
    - **段错误 (Segmentation Fault)**：访问了非法的内存地址（如空指针、越界）4。

## 2. 文件锁定 (高频难点)

为了防止多个进程同时修改同一个文件导致数据混乱，Linux 提供了锁定机制。

**A. 锁文件 (Lock Files) - 粗粒度**
- **原理**：创建一个临时文件作为“锁”。如果文件存在，表示资源被占用；如果不存在，则创建该文件并占用资源。
- 原子操作 (必考代码)：
    使用 open 系统调用，必须带有 O_CREAT 和 O_EXCL 标志 5。

    ```c
    // 如果文件已存在，open 将返回 -1，表示加锁失败
    int fd = open("/tmp/LCK.test", O_RDWR | O_CREAT | O_EXCL, 0444);
    ```
- **临界区 (Critical Section)**：需要独占访问资源的代码段 6。进入前加锁，退出后删除锁文件 (`unlink`)。

B. 区域锁定 (Region Locking) - 细粒度

使用 fcntl 系统调用对文件的某一部分进行锁定，效率更高。

- **函数原型**：`int fcntl(int fildes, int command, struct flock *flock_structure);` 7。
- **`command` 参数**：
    - `F_GETLK`：测试能不能加锁（不真加）8。
    - `F_SETLK`：尝试加锁，失败立刻返回 -1 9。
    - `F_SETLKW`：尝试加锁，被占用则**等待 (Wait)** 10。
- **锁的类型 (`l_type`)** (必考辨析)：
    - **`F_RDLCK` (共享锁/读锁)**：多个进程可以同时读。只要有一个读锁存在，就没人能加写锁 11。
    - **`F_WRLCK` (独占锁/写锁)**：一次只能有一个进程拥有。一旦加上写锁，其他进程既不能读也不能写 12。
        
- **`struct flock` 结构体**：
    - `l_type`：锁类型。
    - `l_whence`, `l_start`, `l_len`：定义锁定的区域范围 13。
    - `l_pid`：持有锁的进程ID。

# 第九章 开发工具 (Exam Focus: GCC与Makefile)

## 1. GCC 编译流程 (必考填空/选择)
GCC 编译一个 C 程序经历四个步骤，顺序不能乱 ：
1. **预处理 (Pre-Processing)**：处理 `#include`, `#define`。
    - 命令：`gcc -E`，生成 `.i` 文件。
2. **编译 (Compiling)**：检查语法，翻译成汇编语言。
    - 命令：`gcc -S`，生成 `.s` 文件。
3. **汇编 (Assembling)**：将汇编转成二进制目标代码。
    - 命令：`gcc -c`，生成 `.o` 文件。
4. **链接 (Linking)**：合并目标代码和库文件，生成可执行文件。
    - 命令：`gcc -o`。

## 2. 函数库 (静态 vs 动态)

- **静态库 (`.a`)**：代码被拷贝到可执行文件中，程序大，但独立运行。
- **动态库 (`.so`)**：代码不拷贝，程序运行时加载，节省空间 。

# 第十章 进程 (Exam Focus: 代码逻辑解释 & 僵尸进程)

## 1. 进程基础概念 (选择/填空)

- **定义**：进程是一个正在运行的程序实例 。
- **PID (Process ID)**：每个进程都有唯一的非负整数 ID 。
    - **PID 1**：**init 进程**（或 systemd），是系统所有其他用户进程的祖先 。
- **进程表**：Linux 内核维护的表，记录所有进程信息 。
- **进程状态** (重点记忆符号)：
    - **R** (Running)：正在运行或在队列中 。
    - **S** (Sleeping)：可中断睡眠 。
    - **Z** (Zombie)：**僵尸进程**。进程已结束，但父进程还没回收它的资源（还没调用 `wait`）。

#### 2. 启动新进程：`system` (简单但低效)

- **函数**：`int system(const char *string);`
- **原理**：它会启动一个 shell (`/bin/sh`) 来执行命令 。
- **缺点**：效率低（多启动了一个 shell），且无法控制细节 。

#### 3. 复制进程：`fork` (核心中的核心)

**这是代码解释题的必考点，请务必死磕以下逻辑：**

- **函数**：`pid_t fork(void);`
- **功能**：复制当前进程。在进程表中创建一个新的表项。新进程（子进程）几乎是父进程的完整副本（代码、数据、堆栈都复制）。
- **返回值** (判断父子的关键) ：
    - **返回 -1**：出错。
    - **返回 0**：**在子进程中**。
    - **返回 >0** (子进程的PID)：**在父进程中**。
- **执行顺序**：`fork` 之后，父子进程并发执行，谁先执行是不确定的（取决于调度器）。

## 4. 替换进程：`exec` 系列 (代码解释题常见)

- **原理**：`fork` 是复制，`exec` 是**替换**。它用一个新的程序替换当前进程的代码段、数据段。**PID 不变** 。
- **特点**：一旦 `exec` 成功，原进程后续的代码**不再执行**（因为它已经被新代码覆盖了）。
    
- **常见函数**：
    - `execl`, `execv` (基础版)
    - `execlp`, `execvp` (带 `p` 表示会在 `PATH` 环境变量中查找程序) 。

## 5. 等待进程与僵尸进程：`wait` (简答/代码题)

- **僵尸进程 (Zombie)**：子进程结束了，但父进程还在运行且没有调用 `wait` 来获取子进程的退出状态。子进程的尸体（进程表项）就会一直保留 。
- **处理方法**：父进程调用 `wait` 或 `waitpid`。
    - `pid_t wait(int *stat_val);`：挂起父进程，直到任意一个子进程结束 。
    - `pid_t waitpid(pid_t pid, int *stat_val, int options);`：可以等待指定 PID 的子进程，或者使用 `WNOHANG` 选项（非阻塞，即使子进程没结束也立刻返回）。

---

## 讲师画重点：如何应对“代码解释题” (fork篇)

考试常常会给出类似下面的代码，问你输出结果或进程关系。

**典型代码分析：**


```c
#include <sys/types.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>

int main() {
    pid_t pid;
    char *message;
    int n;

    printf("fork program starting\n"); // 只输出一次
    pid = fork(); // 分叉点！

    switch(pid) {
        case -1:
            perror("fork failed");
            exit(1);
        case 0:
            // 这里是子进程执行的代码
            message = "This is the child";
            n = 3;
            break;
        default:
            // 这里是父进程执行的代码 (pid 是子进程的 ID，肯定 > 0)
            message = "This is the parent";
            n = 3;
            break;
    }

    // 父子进程都会执行这段循环，因为它们是两个独立的进程
    for(; n > 0; n--) {
        puts(message);
        sleep(1);
    }
    exit(0);
}
```

**解题逻辑 (必背)：**

5. **分叉点**：看到 `fork()`，脑子里马上画出两条线，一条父进程，一条子进程。
6. **数据隔离**：虽然代码变量名一样，但父子进程的 `n` 和 `message` 是独立的内存空间，互不干扰。
7. **并发执行**：输出结果通常是交替的（Parent... Child... Parent...），但也可能乱序。
8. **Exec 陷阱**：如果代码在 `fork` 后调用了 `execlp("ps", ...)`，那么子进程那条线后面的 `printf` 只要写在 `exec` 后面，就**永远不会执行**（除非 exec 失败）。

# 第十一章 信号 (Exam Focus: 异步处理 & 代码解释)

## 1. 信号的基本概念 (选择/填空)

- **定义**：信号是 UNIX/LINUX 系统响应某些条件而产生的一个事件 。
- **本质**：**软中断**。在软件层次上对中断机制的一种模拟 。
- **来源**：
    - **终端用户**：输入 `Ctrl+C` (SIGINT) 。
    - **错误条件**：内存段冲突 (SIGSEGV)、非法指令 (SIGILL) 。
    - **程序发送**：`kill` 命令或函数 。
- **特点**：进程间通信中**唯一的异步通信机制** 。

## 2. 常见信号 (必背，用于分析代码行为)

考试中经常会看到 `kill(pid, SIGXXX)`，你需要知道这些信号是干嘛的：

- **`SIGINT`** (2)：**终端中断**。通常由用户按下 `Ctrl+C` 产生，默认动作是终止进程 。
- **`SIGQUIT`** (3)：**中断退出**。通常由用户按下 `Ctrl+\` 产生 。
- **`SIGKILL`** (9)：**强制终止**。**不能被捕获或忽略**。这是“必杀技” 。
- **`SIGALRM`** (14)：**超时警告**。由 `alarm()` 函数设定的定时器超时产生 。
- **`SIGCHLD`** (17)：**子进程状态改变**。当子进程停止或退出时产生，默认动作是**忽略** 。
- **`SIGSTOP`** (19)：**停止执行** (暂停)。**不能被捕获或忽略** 。
- **`SIGCONT`** (18)：**继续执行**。让暂停的进程恢复运行 。
## 3. 号处理 (代码解释题核心)

A. 处理方式 (三种)
9. **捕获 (Catch)**：指定处理函数。
10. **忽略 (Ignore)**：`SIG_IGN`。
11. **默认动作 (Default)**：`SIG_DFL` (通常是终止)。

**B. `signal` 函数 (注册信号处理)**

```c
#include <signal.h>
void (*signal(int sig, void (*func)(int)))(int);
```

- **功能**：给信号 `sig` 注册处理函数 `func` 。
- **参数 `func`**：
    - 自定义函数名：如 `ouch`。
    - **`SIG_IGN`**：忽略信号 。
    - **`SIG_DFL`**：恢复默认行为 。

**C. `sigaction` 函数 (健壮的接口)** 比 `signal` 更安全，支持信号屏蔽 。

- **结构体 `struct sigaction`**：
    - `sa_handler`：处理函数或 `SIG_DFL`/`SIG_IGN` 。
    - `sa_mask`：**信号屏蔽字**。在处理该信号时，临时屏蔽 `sa_mask` 中的其他信号 。

## 4. 发送信号的函数 (编程/解释)

- **`kill(pid_t pid, int sig)`**：发送信号 `sig` 给进程 `pid` 。
- **`alarm(unsigned int seconds)`**：设置闹钟。`seconds` 秒后发送 **`SIGALRM`** 信号 。
    - _注意_：每个进程只能有一个闹钟 。
- **`pause(void)`**：**挂起进程**，直到收到一个信号 。


## 5. 信号集与屏蔽 (进阶考点)

- **信号集操作**：`sigemptyset` (清空), `sigfillset` (全填), `sigaddset` (添加), `sigdelset` (删除), `sigismember` (判断) 。
- **屏蔽信号 (`sigprocmask`)**：
    - `SIG_BLOCK`：添加屏蔽。
    - `SIG_UNBLOCK`：解除屏蔽。
    - `SIG_SETMASK`：重置屏蔽 。
- **未处理信号 (`sigpending`)**：获取当前被阻塞（屏蔽）且已经产生的信号 。


---

## 讲师画重点：如何应对“代码解释题” (信号篇)

考试可能会给出一段包含 `signal`, `fork`, `alarm`, `pause` 的混合代码，问你程序的执行流程。

典型代码分析 (基于课件 )：


```c
#include <signal.h>
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

static int alarm_fired = 0;

// 信号处理函数
void ding(int sig) {
    alarm_fired = 1;
}

int main() {
    pid_t pid;
    printf("alarm application starting\n");
    
    pid = fork(); // 创建子进程
    switch(pid) {
        case -1: perror("fork failed"); exit(1);
        case 0: // 子进程
            sleep(5); // 睡5秒
            kill(getppid(), SIGALRM); // 给父进程发闹钟信号
            exit(0); // 子进程结束
    }

    // 父进程
    printf("waiting for alarm to go off\n");
    (void) signal(SIGALRM, ding); // 1. 注册信号处理函数
    pause(); // 2. 挂起，等待信号
    
    // 3. 收到信号后，pause返回，继续执行
    if (alarm_fired) printf("Ding!\n");
    printf("done\n");
    exit(0);
}
```

**解题逻辑 (必背)：**

12. **注册阶段**：`signal` 只是告诉内核“如果收到 SIGALRM，就去执行 `ding`”，此时 `ding` **不会** 执行。
    
13. **挂起阶段**：`pause()` 让父进程睡眠，节省 CPU。
    
14. **触发阶段**：子进程 5 秒后发信号。父进程收到信号，被唤醒。
    
15. **处理阶段**：父进程先去执行 `ding()` 函数 (`alarm_fired` 变 1)，函数返回后，`pause()` 返回，主程序继续往下执行 `if (alarm_fired)...`。


# 第十二章 套接字 (Exam Focus: TCP网络编程流程)

## 1. 核心概念 (选择/填空)

- **定义**：Socket 是一种通信机制，既用于同一台机器进程间通信，也用于网络间不同机器通信 1。
- **本质**：在 Linux 中，Socket 也是一种**文件描述符**，对其进行数据传输就像读写文件一样 2。
- **域 (Domain)** 3：
    - **`AF_INET`**：网络套接字 (IPv4)，最常用。
    - `AF_UNIX`：本地套接字 (文件系统路径)，用于本机通信。
- **类型 (Type)** 4：
    - **`SOCK_STREAM`**：**流式**套接字 (TCP)。有序、可靠、面向连接（像打电话）。
    - `SOCK_DGRAM`：**数据报**套接字 (UDP)。无序、不可靠、无连接（像发短信）。

## 2. TCP 通信流程 (必考流程图)

这是本章的灵魂，必须背下来服务器和客户端分别要做什么 5。

|**步骤**|**服务器端 (Server)**|**客户端 (Client)**|**备注**|
|---|---|---|---|
|1|**`socket()`** 创建|**`socket()`** 创建|买电话机|
|2|**`bind()`** 绑定地址|-|插上电话线，定号码|
|3|**`listen()`** 监听|-|打开铃声，准备接听|
|4|**`accept()`** 接受连接|**`connect()`** 连接|服务器接电话，客户拨号|
|5|`read()` / `write()`|`read()` / `write()`|通话 (收/发数据)|
|6|`close()`|`close()`|挂断|

## 3. 关键函数详解 (代码题核心)

**A. `socket` - 创建**

```c
int socket(int domain, int type, int protocol);
```
- **用法**：`fd = socket(AF_INET, SOCK_STREAM, 0);` 6。

B. 地址结构体 struct sockaddr_in (必背配置)

在使用 bind 或 connect 前，必须填充这个结构体 7。

```c
struct sockaddr_in addr;
addr.sin_family = AF_INET;
addr.sin_port = htons(9734); // 端口号 (主机字节序转网络字节序)
addr.sin_addr.s_addr = inet_addr("127.0.0.1"); // IP地址字符串转二进制
// 或者服务器监听所有IP: addr.sin_addr.s_addr = htonl(INADDR_ANY);
```
**C. `bind` - 绑定 (服务器)**

```c
int bind(int sockfd, const struct sockaddr *addr, socklen_t addrlen);
```
- **作用**：给 socket 起名字（绑定 IP 和 端口）8。

**D. `listen` - 监听 (服务器)**

```c
int listen(int sockfd, int backlog);
```

- **作用**：创建连接队列。`backlog` 指定队列最大长度 9。
**E. `accept` - 接受 (服务器 - 重点)**

```c
int client_fd = accept(int sockfd, struct sockaddr *addr, socklen_t *addrlen);
```

- **关键考点**：它会**阻塞**等待。**返回值是一个新的 socket 描述符** (`client_fd`)，专门用于和这个特定的客户端通信。原来的 `sockfd` 继续监听其他人的电话 10101010。

**F. `connect` - 连接 (客户端)**

```c
int connect(int sockfd, const struct sockaddr *addr, socklen_t addrlen);
```
- **作用**：拨号。成功返回 0 11
