import sys, os, json

# NOTE: change this to False to disable the use of eval().
_allowEval: bool = True

# if len(sys.argv) < 4:
# No functionality implemented yet.
if True:
    _msg = (
        "Copies the files and directories from <sourceDir> to <destDir>, using the hash "
        "table <tableFile> to choose only the modified or missing files."
    )
    if _allowEval:
        _msg += (
            " Optionally, it is possible to specify the boolean Python expression "
            "<pythonCond> as a condition to specify which files to choose. The "
            "only module it has access to is re (for regular expressions) and the "
            "only value it has access to is 'fileName' (the Posix relative path of "
            "the current file being checked).\n"
        )
    print(_msg)
    print(
        "Usage: {0} <sourceDir> <destDir> <tableFile> [<pythonCond>]"
        .format(os.path.basename(sys.argv[0]))
    )
    exit(0)

