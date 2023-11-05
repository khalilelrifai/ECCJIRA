import ftplib


def upload_file_to_ftp(file_path, ftp_host, ftp_username, ftp_password, resume=False):
    try:
        with ftplib.FTP(ftp_host) as ftp:
            ftp.login(ftp_username, ftp_password)
            if resume:
                # Enable resumable upload
                ftp.sendcmd('TYPE I')
                file_size = os.path.getsize(file_path)
                ftp.sendcmd(f'REST {file_size}')
            with open(file_path, 'rb') as file:
                ftp.storbinary('STOR ' + file_path, file)
            ftp.quit()
        return True
    except Exception as e:
        print('Error uploading file to FTP:', str(e))
        return False
