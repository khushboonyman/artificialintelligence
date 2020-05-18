import glob, os

if os.name == "posix":
    print(os.system("uname -a"))

basepath = os.path.dirname(os.path.realpath(__file__))
os.chdir(basepath + "/levels/AlexTested")
#os.chdir(basepath + "/levels/competition_levelsSP17")
#os.chdir(basepath + "/levels/competition_levelsSP18")

tests = []
for file in glob.glob("*.lvl"):
    tests.append(file)

os.chdir(basepath)

total = succeeded = 0
not_solved = []
for test in tests:
    total += 1
    stream = os.popen('java -jar server.jar -l levels/AlexTested/' + test + ' -c "python planningClient.py --server=True" -t 300')
    #stream = os.popen('java -jar server.jar -l levels/competition_levelsSP17/' + test + ' -c "python planningClient.py --server=True" -t 300')
    #stream = os.popen('java -jar server.jar -l levels/competition_levelsSP18/' + test + ' -c "python planningClient.py --server=True" -t 300')
    output = stream.read()
    if output.find('Level solved: Yes.') != -1:
        succeeded += 1
    else:
        not_solved.append(test)
    print(output)

print('Succeeded: ' + str(succeeded) + '/' + str(total))

print("Did not solve: " + ', '.join(not_solved))


