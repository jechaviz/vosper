import vosper
import os

def main():
    recognizer = vosper.VosperRecognizer()

    while True:
        text = recognizer.listen()
        if text is not None:
            if text:
                os.system('cls' if os.name == 'nt' else 'clear')
                print(f'- {text}')
            else:
                print("Silencio detectado...")

if __name__ == "__main__":
    main()
