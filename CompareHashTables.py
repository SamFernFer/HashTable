import sys, os, json

if len(sys.argv < 3):
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
        
        for k,v in _firstTable.items():
            _other = _secondTable.get(k, None)
            # The second table does not contain the file.
            if _other is None:
                print("Missing: {0}".format(json.dumps(k)))
            # The second table's file has a different hash.
            elif v != _other:
                print("Different: {0}".format(json.dumps(k)))
            # Removes the entry from the second table for later checking for extra files.
            _secondTable.pop(k)

        # List the extra files from the second table.
        for k,v in _secondTable:
                print("Extra: {0}".format(json.dumps(k)))
