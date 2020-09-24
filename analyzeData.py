import time, json, datetime
from datetime import date
from collections import Counter

counter, morning, noon, evening, night = 0,0,0,0,0
morningDur, noonDur, eveningDur, nightDur = 0,0,0,0
outData = {}

def getUserCreds(user,inFile):
    inData = json.load(open(inFile))
    for ind,d in enumerate(inData):
        if d['credsName'].lower() == user.lower():
            return inData[ind]

def outputToFile(fileName):
    with open(fileName,'w') as outfile:
        json.dump(outData,outfile,indent=4)

def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

def usageThroughDay(timeOfDay,duration):
    global morning, noon, evening, night
    global morningDur, noonDur, eveningDur, nightDur
    if timeOfDay == 'Morning': 
        morning += 1
        morningDur += duration
    elif timeOfDay == 'Afternoon': 
        noon += 1
        noonDur += duration
    elif timeOfDay == 'Evening': 
        evening += 1
        eveningDur += duration
    else: 
        night += 1
        nightDur += duration

def showUsageMetric():
    print("Songs Throughout the day")
    morningDurMin, noonDurMin, eveningDurMin, nightDurMin = int(morningDur/60), int(noonDur/60), int(eveningDur/60), int(nightDur/60)
    usage= {}
    numSong = {"Morning": morning, "Afternoon": noon, "Evening": evening, "Night": night}
    usage['numberOfSongs'] = numSong
    durOfSongs = {"Morning": morningDurMin, "Afternoon": noonDurMin, "Evening": eveningDurMin, "Night": nightDurMin}
    usage['durationOfSongs'] = durOfSongs
    usage['totalMins'] = morningDurMin + noonDurMin + eveningDurMin + nightDurMin
    return usage

# def getTopArtists():

def analyzeFile(inFile,currentDate):
    global counter
    global outData
    artistDict = {}
    trackDict = {}
    inData = json.load(open(inFile))
    for ind, d in enumerate(inData):
        counter += 1
        # if d['Date'] == currentDate: #In order to only process current date's
        #     counter += 1
        # else:
        #     break
        usageThroughDay(d['TimeOfDay'],d['durationSec'])
        artistDict[d['Artist']] = artistDict.get(d['Artist'],0) + 1
        trackDict[d['SongName']] = trackDict.get(d['SongName'],0) + 1

    usage = showUsageMetric()
    outData['usageStats'] = usage
    topArtists = Counter(artistDict).most_common(3)
    topTracks = Counter(trackDict).most_common(3)
    print(topArtists)
    print(topTracks)
    # Convert to min
    print("Songs played today: "+str(counter))

if __name__ == "__main__":
    # print("Running Data Analyzer")
    # print("Fetching User API Credentials")
    user = getUserCreds('TeJas','loginCreds.json')

    # print("Analyzing File..")
    curDate = date.today().strftime("%Y-%m-%d") #Passing in current date
    analyzeFile(user['outFile'],curDate)
    outputToFile('finalMetrics.json')

    
    