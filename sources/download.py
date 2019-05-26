import time, urllib.request, urllib.error, threading
import fn, config as c, write as w, ask as a
#--------------------------------------------------------------------------------
def download_http_data ( data_url, file_name ):
    '''Functie download een bestand van het internet'''
    oke, lock_http = False, threading.Lock()
    with lock_http:
        start_ns = time.time_ns()
        if c.log:
            print(f"Start downloading url: '{data_url}'")
            print(f"To file name: '{file_name}'")
        try:
            response = urllib.request.urlretrieve( data_url, file_name )
        except urllib.error.URLError as e:
            print(f"Error downloading url: '{data_url}'")
            if c.log:
                print(f'{e.reason}{c.ln}{e.strerror}')
        else:
            print(f"Dowloading url: '{data_url}' succesful !")
            w.write_process_time_s('File downloaded in ', start_ns)
            oke = True

    return oke

def download_and_unzip_etmgeg_station ( station ):
    '''Functie downloadt een bestand met etmaalgegevens en unzipt het'''
    lock_down_zip = threading.Lock()
    with lock_down_zip:
        if download_http_data( station.url_etmgeg, station.file_etmgeg_zip ):
            print(' ')
            fn.unzip( station.dir_data, station.file_etmgeg_zip, station.file_etmgeg_txt )
    print(' ')
