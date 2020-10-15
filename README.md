# AESEncryptFolders
This library was created to encrypt some folders within a directory using AES256 encryption from [OpenSSL](https://www.openssl.org). 


# Table of Contents
- [How to Use](#how-to-use)
- [OS](#os)

# How to Use

There are two ways to use it:
1. To encrypt a folder: 
    - search for all folders with specif flag in their names
    - zip each one of them
    - encrypt it changing the flag to `(ENC)`
    - delete the created zip

2. To decrypt a folder: 
    - search for all files with `(ENC)` in their names and
    - decrypt it changing the flag to the old one (you need to specify it)
    - move the zip to the input folder

We will give tou an example showing both at the same time, and you can use the examples folder in this repository, just remmember to change its full path according to where you place it.

```python
from EncryptFolders import AESEncryptFolders

KEY_SIZE = 32
PATH_TO_FOLDERS = '/Users/username/Documents/testing/input/'
FOLDERS_WITH = '(D_ENC)' # will search for this in the folders name
ENC_PATH = '/Users/username/Documents/testing/output/' # you can change if you want

test = AESEncryptFolders(KEY_SIZE, PATH_TO_FOLDERS, ENC_PATH, FOLDERS_WITH)
password = test.encrypt()
test.decrypt(password)
```

**Output:**
```sh
Folders to be encrypted: ['(D_ENC) folder', '(D_ENC) folder2']
        Folder /Users/username/Documents/testing/input/\(D_ENC\)\ folder zipped
        Folder /Users/username/Documents/testing/input/(D_ENC) folder encrypted
        Folder /Users/username/Documents/testing/input/\(D_ENC\)\ folder2 zipped
        Folder /Users/username/Documents/testing/input/(D_ENC) folder2 encrypted
Folders to be decrypted: ['(ENC) folder2.enc', '(ENC) folder.enc']
        Folder /Users/username/Documents/testing/input/(ENC) folder2.enc decrypted
        Folder /Users/username/Documents/testing/input/(ENC) folder.enc decrypted
```

# OS
This library was tested in a OSX 10.15 and i strongly believe that it will work with linux. 
It will probably crash in Windows due to the ecape_characters function, thought is easy to fix this.