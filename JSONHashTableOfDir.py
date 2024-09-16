import sys, os, hashlib, base64, json, traceback

if (len(sys.argv) < 3):
    print(
        "Writes to <outputFile> a JSON object representing a hash"
        "table of all the files inside <directory>."
    )
    print("Usage: {0} <directory> <outputFile>".format(os.path.basename(sys.argv[0])))
    exit(0)

_dirPath = sys.argv[1]
_outPath = sys.argv[2]

# Computes the SHA-256 hash from the stream using a buffer.
def sha256FromStream(fileStream):
    h  = hashlib.sha256()
    b  = bytearray(128*1024)
    _mv = memoryview(b)
    while a := fileStream.readinto(_mv):
        h.update(_mv[:a])
    return h.digest()
# Reads the file from the path and computes its SHA-256 hash using a buffer.
def sha256FromFile(filePath):
    with open(filePath, 'rb', buffering=0) as f:
        return sha256FromStream(f)

# relPath is the current relative path in Posix notation (with each recursion the directory 
# name is appended, followed by "/").
def addToTable(dirPath: str, table: dict, relPath: str = "")->int:
    _errors: int = 0
    for o in os.listdir(dirPath):
        _fullPath = os.path.join(dirPath, o)
        try:
            if (os.path.isfile(_fullPath)):
                _relName = relPath + o
                _hashStr = base64.b64encode(
                    sha256FromFile(_fullPath)).decode('utf-8')
                # The relative path is the key and the hash is the value.
                table[_relName] = _hashStr
                print("File {0}.".format(json.dumps(_relName)))
            elif (os.path.isdir(_fullPath)):
                # Recursively add the files from the other directories.
                _errors += addToTable(_fullPath, table, relPath + o + "/")
        except Exception as e:
            # Prints the exception manually.
            traceback.print_exception(e)
            # Increment the error counter.
            _errors += 1
    return _errors

_table = {}
# Returns the amount of errors found during the procedure.
_errors = addToTable(_dirPath, _table)

with open(_outPath, "w") as _outFile:
    json.dump(_table, _outFile, indent=4)

if _errors > 0:
    print("Hash table file created with {0} errors.".format(_errors))
else:
    print("Hash table file created successfully.")
