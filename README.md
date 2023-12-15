# LLDB CLI custom function to print out school 42's t_list linked_list data

## prerequisite
* Only tested on MacOS.
* Python3 has to be installed.

## `.lldbinit`
* you have to create `.lldbinit` file at your home directory if you do not have the file by `cd && touch .lldbinit`.
* in the `.lldbinit`, add `command script import ~/PATH_Where_YOU_SAVE/t_list_utils.py`

## command line argments
this function accept 2 arguments as below.
1. `-l`or`--list-head` for the name of head of t_list as you assigned. Default is `head`.
2. `-n` or `--name` for a name of structure which your t_list's `(void *) content ` contains.

## Usage Example
compile your code with `-g` flag and launch the `LLDB` with your executable.
```SHELL
$ cc -g main.c libft.a
$ lldb a.out
(lldb) target create "a.out"
```

then, debug using `ptlist` custom command. 
For instance, below the `ptlist --list-head head_of_tlist --name t_data` command debug t_list with head name as `head_of_tlist` and data structure called `t_data` with 2 member vars `_int & _str``

```LLDB
(lldb) b main
Breakpoint 1: where = a.out`main + 24 at main.c:50:18, address = 0x0000000100003c28
(lldb) run
Process 31893 launched: '/Users/masaru/SynologyDrive/document/code/lldb/script_for_tlist/a.out' (arm64)
Process 31893 stopped
* thread #1, queue = 'com.apple.main-thread', stop reason = breakpoint 1.1
    frame #0: 0x0000000100003c28 a.out`main at main.c:50:18
   47   {
   48           t_list  *head_of_tlist;
   49  
-> 50           head_of_tlist = get_data();
   51           (void)head_of_tlist;// surpress a compiler's warning
   52           return (0);
   53   }
(lldb) next
Process 31893 stopped
* thread #1, queue = 'com.apple.main-thread', stop reason = step over
    frame #0: 0x0000000100003c38 a.out`main at main.c:52:2
   49  
   50           head_of_tlist = get_data();
   51           (void)head_of_tlist;// surpress a compiler's warning
-> 52           return (0);
   53   }
(lldb) ptlist --list-head head_of_tlist --name t_data
[_int:0][_str:None]
[_int:-100][_str:"Hello World"]
[_int:0][_str:"from 42 Tokyo!"]
[_int:42][_str:"This programe will create memory leak!"]
```
