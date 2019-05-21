import datetime, config as c

def check_date(yyyymmdd):
    '''Functie checkt datum op validiteit'''
    if not yyyymmdd:
        return False
    elif  len(yyyymmdd) != 8:
        if c.log: print("Datum '%s' heeft niet de juiste lengte..." % yyyymmdd )
        return False
    elif not yyyymmdd.isdigit():
        if c.log: print("Datum '%s' moet enkel uit cijfers bestaan..." % yyyymmdd )
        return False
    else:
        y, m, d = int(yyyymmdd[:4]),int(yyyymmdd[4:6]),int(yyyymmdd[6:8])
        if y < 1901: # Geen data voor 1900
            if c.log: print("Jaartal '%i' buiten bereik gegevens..." % y )
            return False
        try:
            check = datetime.datetime(y, m, d)
        except ValueError:
            if c.log: print("Datum '%s' geeft fout..." % yyyymmdd )
            return False # bv 20180229
        else:
            # Geen datum in de toekomst
            if check > datetime.datetime.now():
                if c.log: print("Datum '%s' ligt in de toekomst..." % yyyymmdd )
                return False
    return True
