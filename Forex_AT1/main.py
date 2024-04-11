strOfInts = "0,0,0,0"

convertToList = [int(s) for s in strOfInts.split(',')]

convertToStr = (','.join(str(x) for x in convertToList))