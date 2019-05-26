import datetime, config as c

def check_date(yyyymmdd):
    '''Functie checkt datum op validiteit'''
    oke = True
    if not yyyymmdd:
        return False
    elif  len(yyyymmdd) != 8:
        if c.log:
            print(f"Date: '{yyyymmdd}'. Wrong length of date given. Use format of <yyyymmdd>")
        oke = False
    elif not yyyymmdd.isdigit():
        if c.log:
            print(f"Date: '{yyyymmdd}' must only contain of digits")
        oke = False
    else:
        y, m, d = int(yyyymmdd[:4]),int(yyyymmdd[4:6]),int(yyyymmdd[6:8])
        if y < 1901: # Geen data voor 1900
            if c.log:
                print(f"Year: '{y}' out a reach of available data")
            oke = False
        try:
            check = datetime.datetime(y, m, d)
        except ValueError:
            if c.log:
                print(f"Date: '{yyyymmdd}' validation error")
            oke = False # bv 20180229
        else:
            # Geen datum in de toekomst
            if check > datetime.datetime.now():
                if c.log:
                    print(f"Date: '{yyyymmdd}' lies in the future. Maybe try again later ;-)")
                oke = False

    if not oke:
        print(f"Error in date: '{yyyymmdd}' !")

    return oke
