import fn, config as c

def unzip_test():
    arcen = c.lijst_stations[-1]
    txt_f = arcen.file_etmgeg_txt
    zip_f = arcen.file_etmgeg_zip
    zip_d = arcen.dir_data
    print(f"txt:{txt_f} {c.ln}zip:{zip_f} {c.ln}dir:{zip_d}")
    if fn.unzip( zip_d, zip_f, txt_f ):
        print("zip ok")
    else:
        print("zip niet ok")

