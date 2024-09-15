import sys, os, hashlib, base64, json

if (len(sys.argv) < 3):
    print(
        "Writes to <outputFile> a JSON object representing a hash"
        "table of all the files inside <directory>."
    )
    print("Usage: {0} <directory> <outputFile>".format(os.path.basename(sys.argv[0])))
    exit(0)

_dirPath = sys.argv[1]
_outPath = sys.argv[2]
_table = {}

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
def addToTable(dirPath: str, table: dict, relPath: str = "")->None:
    for o in os.listdir(dirPath):
        _fullPath = os.path.join(dirPath, o)
        if (os.path.isfile(_fullPath)):
            _relName = relPath + o
            # Adds the path to the dict as the key and the hash as the value.
            table[_relName] = base64.b64encode(
                sha256FromFile(_fullPath)).decode('utf-8')
            print("File {0}.".format(json.dumps(_relName)))
        elif (os.path.isdir(_fullPath)):
            # Recursively add the files from the other directories.
            addToTable(_fullPath, table, relPath + o + "/")

addToTable(_dirPath, _table)

with open(_outPath, "w") as _outFile:
    json.dump(_table, _outFile, indent=4)

print("Hash table file created successfully.")
