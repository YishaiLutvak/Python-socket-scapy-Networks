input_file = open(r'c:\networks\work\basicExamples\dear_prudence.txt', 'r')

print(type(input_file))
print(input_file)
print()

lyrics = input_file.read()
print(lyrics)
input_file.close()
print()

input_file = open(r'c:\networks\work\basicExamples\dear_prudence.txt', 'r')
lyrics = input_file.readline()
input_file.close()
print(lyrics)

input_file = open(r'c:\networks\work\basicExamples\dear_prudence.txt', 'r')
lyrics = None
while lyrics != '':
   lyrics = input_file.readline()
   print(lyrics, end="")
input_file.close()

print()
input_file = open(r'c:\networks\work\basicExamples\dear_prudence.txt', 'r')
for line in input_file:
    print(line, end="")
input_file.close()
