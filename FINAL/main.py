import speech_recognition as sr
import calendar
import os
import playsound
from gtts import gTTS

# pip install SpeechRecognition
# pip install playsound

# pip install pyaudio
# if above is not installable do
# brew install portaudio and then do
# pip3 install pyaudio
# pip install gTTS

voice = sr.Recognizer()


def speaker(inputString):
    textVoice = gTTS(text=inputString, lang='en')
    voiceFile = 'audio'
    textVoice.save(voiceFile)
    playsound.playsound(voiceFile)
    os.remove(voiceFile)

def answer(filename,date, year):
  with open(filename,'a+') as outfile:
    # if file is new then there is nothing in the file
    if (os.stat(filename).st_size == 0):
      speaker("You don't have any schedule on {} {}".format(date,year))
      # ask to add schedule
      speaker('Would you like to add a schedule?')
      with sr.Microphone() as inputDevice:
        newSchedule = voice.listen(inputDevice)
        newScheduleStr = voice.recognize_google(newSchedule)
        if (newScheduleStr == 'yes'):
            addSchedule(filename)

        elif (newScheduleStr != 'yes'):
            speaker('Good bye')
        # we opened it and there will be no sch
            os.remove(filename)
    else:
        f = open(filename)
        lines = f.readlines()
        for line in lines:
            speaker('You have: ')
            speaker(line)
        with sr.Microphone() as inputDevice:
            speaker("Do you need to see schedules on another date?")
            anotherD = voice.listen(inputDevice)
            anotherDStr = voice.recognize_google(anotherD)
            if (anotherDStr == 'yes'):
                repeat()
            else:
                speaker("good bye")

def addSchedule(filename):
    with sr.Microphone() as inputDevice:
        speaker('What is your schedule?')
        content = voice.listen(inputDevice)
        contentStr = voice.recognize_google(content)

        with open(filename, 'a+') as outfile:
            outfile.write(contentStr)
            speaker("Your schedule now has been saved")

            speaker("Is there anything else I can do for you?")
            tryAgain = voice.listen(inputDevice)
            tryAgainStr = voice.recognize_google(tryAgain)
            if (tryAgainStr == 'yes'):
                repeat()
            elif (tryAgainStr != 'yes'):
                speaker('Good bye')


def repeat():
    with sr.Microphone() as inputDevice:
        speaker("Do you need to see different year's calendar")
        differentY = voice.listen(inputDevice)
        differentYStr = voice.recognize_google(differentY)
        if (differentYStr == 'yes'):
            speaker("what year do you want me to pull up?")
            year = voice.listen(inputDevice)
            yearStr = voice.recognize_google(year)
            yearInt = int(yearStr)

            print(calendar.calendar(yearInt))

        speaker('Which date are you looking for?')
        date = voice.listen(inputDevice)
        dateStr = voice.recognize_google(date)

        speaker('You said {} {}. Is that correct?'.format(dateStr, yearStr))
        schedule = voice.listen(inputDevice)
        scheduleStr = voice.recognize_google(schedule)

        if (scheduleStr == 'yes'):
            # file name will be in this form ex)Decemberfirst2021.txt
            newfilename = dateStr + yearStr + '.txt'
            # go to schedule function and if there is no schedule ask to add one
            answer(newfilename, dateStr, yearStr)
        else:
            speaker("Let's try again")
            speaker('Tell me the date again')
            date = voice.listen(inputDevice)
            dateStr = voice.recognize_google(date)

            filename = dateStr + yearStr + '.txt'
            answer(filename, dateStr, yearStr)




#program starts from here
with sr.Microphone() as inputDevice:
        speaker('What year would you like to see?')
        year = voice.listen(inputDevice)
        yearStr = voice.recognize_google(year)
        yearInt = int(yearStr)

        speaker("Let me pull up the calendar for year {}".format(yearStr))
        print(calendar.calendar(yearInt))

        speaker('Which date are you looking for?')
        date = voice.listen(inputDevice)
        dateStr = voice.recognize_google(date)

        speaker('You said {} {}. Is that correct?'.format(dateStr,yearInt))
        schedule = voice.listen(inputDevice)
        scheduleStr = voice.recognize_google(schedule)

        if (scheduleStr == 'yes'):
            # file name will be in this form ex)Decemberfirst2021.txt
            filename = dateStr + yearStr + '.txt'
            # go to schedule function and if there is no schedule ask to add one
            answer(filename, dateStr, yearStr)
        elif (scheduleStr != 'yes'):
            speaker("Let's try again")
            speaker('Tell me the date again')
            another = voice.listen(inputDevice)
            anotherStr = voice.recognize_google(another)

            if (another == 'yes'):
                speaker('Which date are you looking for?')
                date = voice.listen(inputDevice)
                dateStr = voice.recognize_google(date)

                filename = dateStr + yearStr + '.txt'
                answer(filename, dateStr, yearStr)

            else:
                speaker('Good bye')
