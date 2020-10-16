# get_random_password_string
import random
import string

# find the paths that needed to be encrypted
from os import listdir, remove, path
from os.path import isdir, join, isfile

# to run the commands
import subprocess

class AESEncryptFolders:
    """
    This object will get the folders with some signal in thier name, like (D_ENC), 
    zip them, and encrypt it using the generated password.
    After encrypting it, the zip will be deleted and the password returned so you 
    can write it down somewhere safe.
    """
    def __init__(self, KEY_SIZE ,PATH_TO_FOLDERS, PATH_TO_DEST, FOLDERS_WITH, PASSWORD = None, INTER = 20000):
        self.key_size = KEY_SIZE
        self.path_to_folders = PATH_TO_FOLDERS
        self.path_to_dest = PATH_TO_DEST
        self.folders_with = FOLDERS_WITH
        self.password = PASSWORD if PASSWORD else self.random_password_string().replace("'",'*')
        self.inter = INTER

    def random_password_string(self):
        """
        Generates a password with length of key_size 
        """
        password_characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(password_characters) for i in range(self.key_size))
        return password

    @staticmethod
    def ecape_characters(name):
        """
        Escape characters so we can use them as paths 
        """
        return name.replace('(','\(').replace(')','\)').replace(' ','\ ').replace('[','\[').replace(']','\]')

    @staticmethod
    def subprocess_shell_command(cmd, path=None):
        """
        Used to run shell comands 
        """
        
        try:
            sp = subprocess.Popen(cmd,
                cwd=path,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
            rc=sp.wait()
            out,err=sp.communicate()
        except FileNotFoundError as e:
            print('Comand: ',cmd)
            print('Path: ',path)
            raise FileNotFoundError(e)

        if err:
            print('ERROR: A problem ocurred when using subprocess')
            print('Return Code:',rc)
            print('output is: \n', out)
            print('error is: \n', err)

        return err

    def zip_folder(self, folder_path, folders_name, destination_path = None):
        """
        Zip folder and its subfolders 
        """
        if not(destination_path):
            destination_path = folder_path

        # folder path doesnt need to escape
        # folder_path = self.ecape_characters(folder_path)
        folder_name = self.ecape_characters(folders_name)
        destination_path = self.ecape_characters(destination_path)

        cmd = 'zip -9 -r -q {name}.zip {source}'.format(
                name=destination_path+folder_name, 
                source=folder_name)

        err = self.subprocess_shell_command(cmd, folder_path)
        
        if not(err):
            print("\tFolder {} zipped".format(folder_path+folder_name))

    def zip_folders(self, folder_path, folders_name, destination_path = None):
        """
        Zip multiple folders and its subfolders 
        """
        if isinstance(folders_name, list): 
            for folder_name in folders_name:
                self.zip_folder(folder_path, folder_name, destination_path)
        else: 
            folder_name=folders_name
            self.zip_folder(folder_path, folder_name, destination_path)

    def encrypt(self):
        """
        Encrypt zip folder using AES256 from openssl library 
        """
        folders = [f for f in listdir(self.path_to_folders) if isdir(join(self.path_to_folders, f)) and self.folders_with in f]
        print('Folders to be encrypted: {}'.format(folders))
        
        for folder in folders:
            self.zip_folders(self.path_to_folders, folder)

            folder_aux = folder
            folder_aux = folder_aux.replace(self.folders_with, '(ENC)')
            enc_full_path = self.ecape_characters(self.path_to_dest + folder_aux + '.enc')
            full_path_folder = self.ecape_characters(self.path_to_folders + folder + '.zip')

            cmd = "openssl enc -aes-256-cbc -pbkdf2 -md sha512 -iter {inter} -in {target} -out {destination} -k '{password}'".format(
                password=self.password, target=full_path_folder, destination=enc_full_path, inter=self.inter)

            err = self.subprocess_shell_command(cmd, self.path_to_folders)
        
            if not(err):
                print("\tFolder {} encrypted".format(self.path_to_folders + folder))
                remove(join(self.path_to_folders, folder+'.zip'))

        return self.password

    def decrypt(self, password):
        """
        Decript .enc folder with openssl library 
        """
        folders = [f for f in listdir(self.path_to_dest) if isfile(join(self.path_to_dest, f)) and '(ENC)' in f]
        print('Folders to be decrypted: {}'.format(folders))
        
        for folder in folders:
            enc_full_path = self.ecape_characters(self.path_to_dest + folder)
            full_path_folder = self.ecape_characters(self.path_to_folders + folder.replace('.enc','.zip').replace('(ENC)', self.folders_with))

            cmd = "openssl enc -d -aes-256-cbc -pbkdf2 -md sha512 -iter {inter} -in {target} -out {destination} -k '{password}'".format(
                password=password, target=enc_full_path, destination=full_path_folder, inter=self.inter)

            err = self.subprocess_shell_command(cmd, self.path_to_folders)
        
            if not(err):
                print("\tFolder {} decrypted".format(self.path_to_folders + folder))
                remove(join(self.path_to_dest, folder))