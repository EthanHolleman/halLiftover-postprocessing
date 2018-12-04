import orthologFindHelper


def columnChrNameStartEnd(f, f2):
    f.seek(0)
    f2.seek(0)
    index = 0
    peakName = "peak0"
    for line in f:
        peakName = "peak" + str(index)
        strList = line.split("\t")
        newStrList = strList[0:3]
        newStrList.append(peakName)
        newLine = fromStringListToStr(newStrList)
        f2.write(newLine)
        index = index + 1
    f2.close()
    f.close()

def summitPlusMinusLength(f, f2, slen, summit):
    f.seek(0)
    f2.seek(0)
    slen = int(slen)
    index = 0
    peakName = "peak0"
    summit_offset = 0
    if(summit):
        summit_offset = 1
    for line in f:
        peakName = "peak" + str(index)
        strList = line.split("\t")
        peakStart = int(strList[1])
        summitDisFromStart = int(strList[9])
        summitStart = peakStart + summitDisFromStart - slen + summit_offset
        summitEnd = peakStart + summitDisFromStart + slen

        newLineList = [strList[0], str(summitStart), str(summitEnd), peakName]
        newLine = fromStringListToStr(newLineList)
        f2.write(newLine)
        index = index + 1
    f2.close()
    f.close()

''' preposessing of revtFile if needed
peakName0
peakName0
peakName0
--> 
peakName0_1
peakName0_2
peakName0_3
'''
def assignPeakNameSuffix(fname, fname2):
    f = open(fname, "r+")
    f2 = open(fname2, "x+")
    curPeakName = ""
    acc = 0
    for line in f:
        strList = line.split("\t")  # CAUTION: assume always be delimited by tab
        peakNamePrefix = strList[-1]
        if(peakNamePrefix != curPeakName):
            curPeakName = peakNamePrefix
            acc = 0
        strList[-1] = peakNamePrefix[:-1] + "_" + str(acc)
        acc+=1
        newLine = fromStringListToStr(strList)
        f2.write(newLine)
    f2.close()
    f.close()

def preprocess_tFile(tFileH, outf):
    tFileH.seek(0)
    outH=open(outf,"w+")
    index = 0
    peakName = "peak0"
    for line in tFileH:
        peakName = "peak" + str(index)
        strList=line.split("\t")
        peak_s=int(strList[1])
        peak_e=int(strList[2])
        #
        newLineList = strList[0:3]
        newLineList.append(str(peak_e-peak_s+1))
        newLineList.append(peakName)
        newLine = fromStringListToStr(newLineList)
        outH.write(newLine)
        index = index + 1
    outH.close()