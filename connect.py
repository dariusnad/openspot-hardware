import paramiko
import os

#Connect my PC to my RPi via SSH
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect("192.168.1.78", port = 22, username = "pi",password="hr634431")
print ("Connected to the Pi")
ssh_stdin, ssh_stdout, ssh_stderr = ssh_client.exec_command('python /home/pi/Desktop/Technician/test.py')
print("Sample Image Has Been Captured")
#Move file from RPi to my PC
ftp_client = ssh_client.open_sftp()
print("Transferring Image to Local Machine")
ftp_client.get("/home/pi/Desktop/Technician/check.jpg",os.path.join('/home/jnaorbe/Desktop', "worked.jpg"))
ftp_client.close()