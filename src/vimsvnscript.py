import vim
import subprocess


""" This function parses current line from vim. It takes file address and rev.
    Then it calls svn diff command.
"""


def showSVNDiff():
    line = vim.current.line
    if "@" not in line:
        return

    f = line.split("@")[0].strip()
    r = line.split("@")[1].strip()

    r = int(r)
    rprev = r - 1

    script = vim.eval('s:rootp') + '/vimdiffscript.py'
    rev = ("-r"
           + str(r)
           + ":"
           + str(rprev))
    subprocess.Popen(['svn',
                      'diff',
                      '--diff-cmd',
                      script,
                      f,
                      rev
                      ])
