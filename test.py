
import speech_recognition as sr

def main():

    sound = "harvard.wav"

    r= sr.Recognizer()

    with sr.AudioFile(sound) as source:
        r.adjust_for_ambient_noise(source=source)

        print("Converting to Text .. .. . . . .")

        audio = r.listen(source)

        try:
            print("Converting  Audio IS : \n" + r.recognize_google(audio))
        
        except Exception as e:
            print(e)


if __name__ == "__main__":
    main()