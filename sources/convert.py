
def ms_to_bft ( ms ):
    bft = -1
    if   ms <  0.3: bft =  0
    elif ms <  1.5: bft =  1
    elif ms <  3.3: bft =  2
    elif ms <  5.4: bft =  3
    elif ms <  7.9: bft =  4
    elif ms < 10.7: bft =  5
    elif ms < 13.8: bft =  6
    elif ms < 17.1: bft =  7
    elif ms < 20.7: bft =  8
    elif ms < 24.4: bft =  9
    elif ms < 28.4: bft = 10
    elif ms < 32.6: bft = 11
    elif ms > 32.5: bft = 12

    return bft
