import vosper, os

vosper = vosper.new()

while 'listening':
  text = vosper.listen()
  if '-' in text:
    print(text)
  elif text != '':
    os.system('cls')
    print('- ' + text)
