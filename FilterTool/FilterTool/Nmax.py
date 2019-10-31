from scipy import signal

def NmaxForQmax(Qmax, filterType):
    if filterType == "Cauer":
        temp = NmaxCauer(Qmax)
    elif filterType == "Bessel":
        temp = NmaxBessel(Qmax)
    elif filterType == "Butter":
        temp = NmaxButter(Qmax)
    elif filterType == "Chevy1":
        temp = NmaxCheby1(Qmax)
    elif filterType == "Chevy2":
        temp = NmaxCheby2(Qmax)
    else :
        temp = None
    return temp


def NmaxCauer(Qmax):
    wp = 1
    ws = 
    gpass = 
    gstop = 
    N, Wn = signal.ellipord(wp,ws,gpass,gstop,analog = True)
    return N
