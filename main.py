import vosper
import os

def main():
    recognizer = vosper.VosperRecognizer()

    while True:
        text = recognizer.listen()
        if '-' in text:
            print(text)
        elif text:
            os.system('cls')
            print(f'- {text}')

if __name__ == "__main__":
    main()
