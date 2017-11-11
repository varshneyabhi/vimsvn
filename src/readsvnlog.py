from subprocess import check_output

svn_root = "InValid"
f = None


""" This function generates svn log output
"""


def get_logs():
    x = check_output(['svn', 'log', '-v', '-r', 'HEAD:0'])
    return x


""" svn log returns absolute path of files as per the repository, which
    which can be used directly in svn diff command. As a solution, if
    svn repo url is prepended to file path, it can be used in svn diff.
    This function parses svn repo address from svn info command.
"""


def get_svn_root():
    global svn_root
    if svn_root == "InValid":
        path = check_output(['svn', 'info'])
        path = list(
                filter(
                    lambda x: "Repository Root: " in x, path.split("\n")))
        svn_root = path[0].split("Repository Root: ")[-1]
    return svn_root


""" As mentioned above, this function creats path with URL.
"""


def get_path_with_url(path):
    c = get_svn_root()
    return c + path


""" In output of svn log, the last column contains number of lines used for
    comments. This function removes number of lines and replaces with first
    line of comment, improves readability.
"""


def create_header(x, p):
    a = x.split("|")
    a[-1] = p
    return "| ".join(a) + "\n"


""" Function to write to svnlogs file.
"""


def write_to_file(x):
    global f
    if f is None:
        f = open('svnlogs', 'w')
    f.write(x)
    pass


""" Main function to perform all propcessing.
"""


def main():
    # get all logs
    lines = get_logs().split("\n")

    start = False
    line = 0
    header = ""
    changed_path = False
    tstr = ""
    fcomm = False
    rev = 0

    for x in lines:
        if ("----------------------------------------------------------------------" in x and
           start is False):
            # Fount Start
            start = True
        elif start is True:
            if line == 0:                                # Just to avoid if any extra lines before first record.
                # Read header line
                header = x
                rev = "@"+x.split("|")[0][1:].rstrip()   # Adding rev with @ helps further to find all related info.
                line = 1                                 # After header, lets parse changed files.
                tstr = ""
            elif line == 1:                              # Not a good way to compare with 0,1 and 2. Will change later.
                if "Changed paths" in x:
                    # Changed files found
                    tstr = "    Changed paths\n"
                    changed_path = True
                elif changed_path is True:
                    if len(x) == 0:
                        changed_path = False
                        line = 2                         # From here Starts Comment
                        tstr += "    Comment"
                    else:
                        tstr += ("        "
                                 + get_path_with_url(x.split(" ")[-1])
                                 + rev
                                 + "\n")
            elif line == 2:
                if "----------------------------------------------------------------------" in x:
                    write_to_file(tstr + "\n")           # Current record parsing is over, lets write it.
                    line = 0                             # Next Record
                    fcomm = False
                else:
                    if fcomm is False:                   # First line of comment. Lets update header.
                        tstr = (create_header(header,
                                              x.lstrip())
                                + tstr)
                        fcomm = True

                    if len(x.strip()) > 0:
                        tstr += "\n        " + x.lstrip()  # Take only lines from comments which is not empty.

    write_to_file(tstr)                                   # Write last record.


main()
