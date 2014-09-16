etcut
=====

Etcut, Escape-sequence Thru-ing CUT command.

What?
=====

Conider you are using some CLI command with ANSI color,
and its output includes some long lines. Pretty hard to read....

```bash
$ git blame -n Database.java | grep Kamiya --color=ALWAYS | less -r
```

A `etcut` acts similar to a `cut` command, however, etcut does not remove escape sequences.

```
$ git blame -n Database.java | grep Kamiya --color=ALWAYS | python etcut.py 60:135 | less -r
```

License
=======

Public-Domain. As you like :)


