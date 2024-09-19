import sys, os, json

if len(sys.argv) < 3:
    print(
        "Compares two JSON hash tables. The first file is considered "
        + "the reference one when listing the differences."
    )
    print("Usage: {0} <firstFile> <secondFile>".format(os.path.basename(sys.argv[0])))
    exit(0)

_firstPath = sys.argv[1]
_secondPath = sys.argv[2]

with open(_firstPath) as _firstFile:
    with open(_secondPath) as _secondFile:
        _firstTable: dict = json.load(_firstFile)
        _secondTable: dict = json.load(_secondFile)
        _hasMissing: bool = False
        _hasDifferent: bool = False
        _hasExtra: bool = False
        
        for k,v in _firstTable.items():
            _other = _secondTable.get(k, None)
            # The second table does not contain the file.
            if _other is None:
                print("[Missing]: {0}".format(json.dumps(k)))
                _hasMissing = True
            # If the file is present.
            else:
                # The second table's file has a different hash.
                if v != _other:
                    print("[Different]: {0}".format(json.dumps(k)))
                    _hasDifferent = True
                # Removes the entry from the second table for later checking for extra files.
                # Only pops if when the key is present, of course.
                _secondTable.pop(k)

        # List the extra files from the second table.
        for k,v in _secondTable.items():
            print("[Extra]: {0}".format(json.dumps(k)))
            _hasExtra = True

        if not _hasMissing:
            print("No missing files.")
        if not _hasDifferent:
            print("No different files.")
        if not _hasExtra:
            print("No extra files.")
        if not _hasMissing and not _hasDifferent and not _hasExtra:
            print("Both trees are equal.")
        
