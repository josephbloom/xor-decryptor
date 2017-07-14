#!/usr/bin/env
# -*- coding: utf-8 -*-
import base64

def decrypt():
    print
    print "Encrypted message must be encoded with base64."
    while True:
        newfile = raw_input("\nName of .txt file (ex. encyrptedfile.txt):\nType 'exit' to quit.\n")
        if newfile.lower() == "exit":
            main()
        if not newfile[len(newfile) - 4:] == ".txt":
            print "\n*** .txt files only, please. ***"
            continue
        else:
            try:
                encryptedfile = open(newfile,"r")
            except IOError as err:
                print err
                continue
        encryptedmessage = encryptedfile.read()
        encryptedfile.close()
        try:
            encryptedmessage = base64.b64decode(encryptedmessage)
        except:
            print "\nThis message is not base64 encoded."
            continue
        break
    while True:
        try:
            bottomrange = int(raw_input("Smallest size key to test: "))
            if bottomrange < 1:
                print "\n*** MINIMUM IS 1 ***\n"
                continue
            break
        except:
            print "\n*** POSITIVE INTEGERS ONLY ***\n"

    while True:
        try:
            toprange = int(raw_input("Biggest size key to test: "))
            if toprange < bottomrange:
                print "\n*** MUST NOT BE LOWER THAN SMALLEST KEY "+bottomrange+" ***\n"
                continue
            break
        except:
            print "\n*** POSITIVE INTEGERS ONLY ***\n"
    print "\n****************************************************\n" 
    keysize = range(bottomrange,toprange+1)

    def finddistance(input1, input2): # Hemming Distance
        ## convert input string chars to binary string
        input1 = ''.join(['{:08b}'.format(ord(i),'b') for i in input1]) ## 'b' in (ord(i),'b') is redundant for {:08b} 
        input2 = ''.join(['{:08b}'.format(ord(i),'b') for i in input2]) ## {:08b} means to make a string that is 8 chars long, ascii to bytes 
        ## int converts binary string to base 10 number(long) for xor'ing, format converts result to binary, then lists bits.
        try:
            result = list(format(int(input1,base=2) ^ int(input2,base=2),'b'))
        except ValueError: ## If the encrypted message is too short for the current loop and input2 has nothing
            return
        ## adds up the list of bits
        distance = sum([int(i) for i in result])
        return distance

    keysizeresults = {}
    for size in keysize:
        ## take first 2 sets of bytes, equal in size to 'size', find hemming distance
        ## repeat many times, add the distances together, divide by number of distance, then divide by 'size'
        ## distance from finddistance() is 'normalized' by dividing it by size
        d = []
        for i in range (0,100):
            try:
                d.append(float(finddistance(encryptedmessage[size*i:size*(i+1)],encryptedmessage[size*(i+1):size*(i+2)])))
            except TypeError: ## If the encrypted message is too short for the current loop and input2 has nothing
                # print "2nd keysize block empty while trying keysize "+str(size)+"."
                break
        thedistance = sum(d)/float(size)/(len(d))
        ## keysize and distance are added to dict
        keysizeresults[thedistance] = size

    probablekeysizes = []
    ## sort least to greatest by key (distance) and display least 3
    for i in sorted(keysizeresults.keys())[0:4]:
        print "keysize "+str(keysizeresults[i])+" with distance "+str(i)
        probablekeysizes += [keysizeresults[i]]
    print
    keychars = dict()
    
    ## Using the likely sizes, found the likeliest chars for each size then score each potential key
    for size in probablekeysizes:
        keychars[size] = []
        print "\n--------------------\n"
        print "trying key size "+str(size)+"..."
        ## Break encrypted message into blocks of likely keysizes (size)
        blockedmessage = [encryptedmessage[i:i+size] for i in range(0,len(encryptedmessage),size)]
        ## create new blocks from first byte of each block, then 2nd byte of each block, etc.
        j, newblockedmessage = 0, []
        errorraised = 0
        while j < size:
            tempchars = []
            for block in blockedmessage:
                try:
                    tempchars.append(block[j])
                except IndexError:
                    if errorraised == 0:
                        print "index error at index "+str(blockedmessage.index(block))+" out of "+str(len(blockedmessage)-1)
                        errorraised = 1
            newblockedmessage.append(''.join(tempchars))
            j += 1

        allprintable = 0 ## keep track if all characters in newblockedmessage are printable
        ## scoring single-byte xor decrypting for each new block
        for block in newblockedmessage:

            score = 0.0
            temprecord = []
            for i in range(127):
                tempscore = 0.0
                newstring = ''.join([chr(ord(char) ^ i) for char in block])
                for c in newstring:
                    if 'a'<=c<='z' or 'A'<=c<='Z' or c == ' ':
                        tempscore += 1
                tempscore = float(tempscore) / float(len(newstring))
                if tempscore >= score:
                    score = tempscore
                    temprecord = [chr(i),newblockedmessage.index(block), tempscore]
                    for c in newstring:
                        if 32<=ord(c)<=126 or ord(c) == 10:
                            addprintable = 1
                        else:
                            addprintable = 0
                            break
            if addprintable == 1:
                allprintable += len(newstring)
            keychars[size].append(temprecord)
        print "\nFor keysize "+str(size)+":"
        averagescore = 0.0
        for letter in keychars[size]:
            print "Letter "+letter[0]+" at position "+str(letter[1])+" with score "+str(letter[2])
            averagescore += letter[2]
        averagescore = averagescore/size
        if allprintable >= len(encryptedmessage): ## Advantage to keys that only produce printable characters
            print "allprintable = "+str(allprintable)
            print "encrypted message length = "+str(len(encryptedmessage))
            averagescore += 10
        print "Average Score: "+str(averagescore)
        keychars[size].append(averagescore)

    ## remove duplicate keys that are doubled, tripled, etc. ('password' vs 'passwordpassword')
    ## and add their average score to the original
    # print "* * *"
    # for i in keychars.iterkeys():
    #     print i
    todelete = []
    for i in keychars.iterkeys():
        iword = ''.join([keychars[i][b][0] for b in range(0,i)])
        for j in keychars.iterkeys():
            jword = ''.join([keychars[j][b][0] for b in range(0,j)])
            multiplesfound = jword.count(iword)
            if multiplesfound > 1 and \
            multiplesfound == float(len(jword)) / len(iword):
                keychars[i][i] += keychars[j][j]
                todelete.append(j)
    # print todelete
    for i in todelete:
        try:
            del keychars[i]
        except KeyError:
            pass # if a key is added to list more than once, and is already gone the second time it's referenced



    themax = max([keychars[i][i] for i in keychars.iterkeys()]) ## get highest average score among keysizes 
    for i in keychars.iterkeys():
        if keychars[i][i] == themax:
            print "\n****************************************************"
            print "Best key guess is:"
            thekey = ''.join([keychars[i][j][0] for j in range(0,i)])
            ## if key repeats, only show one rep
            a = (thekey + thekey).find(thekey, 1, -1)
            if not a == -1:
                thekey = thekey[:a]
            print "---> "+thekey+" <---"
            print "With average score: "+str(keychars[i][i])
            print "****************************************************\n"

    ## Use key to decrypt and display message
    ordkey = [ord(i) for i in thekey]
    ordmessage = [ord(i) for i in encryptedmessage]
    keycount = 0
    decryptedmessage = ""
    for c in ordmessage:
        decryptedmessage += str(chr(c ^ ordkey[keycount]))
        keycount += 1
        if keycount == len(ordkey):
            keycount = 0

    print "--------------------"
    print "message length = "+str(len(decryptedmessage))
    printableletters = 0
    for c in decryptedmessage:
        if 32<=ord(c)<=126 or ord(c) == 10:
            printableletters += 1
    print "printable letters = "+str(printableletters)
    print "--------------------\n"
    if not printableletters == len(encryptedmessage):
        print "Decrypted message includes non-printable characters."
        print "Keysize range may be too large, or not include correct keysize."
        choice = ""
        while choice != 'y' and choice != 'n':
            choice = raw_input("Show decrypted message anyway? (y/n)").lower()
            if choice =='y':
                print decryptedmessage
    else:
        print decryptedmessage
    print "\n****************************************************\n"
    main()

##########################################################
############        ENCRYPT     ##########################
##########################################################

def encrypt():
    while True:
        choice = raw_input("\nInput message method:\n(m) Manually input\n(f) use .txt file\n'exit' to go back to menu\nSelect: ").lower()
        if choice == "m":
            message = raw_input("What's the message?\n")
            break
        if choice == "f":
            messagefile = raw_input("What's the file?\n")
            if not messagefile[len(messagefile) - 4:] == ".txt":
                print "\n*** .txt files only, please. ***"
                continue
            try:
                messagefile = open(messagefile,"r")
            except IOError as err:
                print err
                continue
            message = messagefile.read()
            messagefile.close()
            # print message
            break
        if choice == "exit":
            main()
    
    while True:
        choice = raw_input("\nInput key method:\n(m) Manually input\n(f) use .txt file\n'exit' to go back to menu\nSelect: ").lower()
        if choice == "m":
            key = raw_input("What's the key?\n")
            break
        if choice == "f":
            keyfile = raw_input("What's the file?\n")
            if not newfile[len(newfile) - 4:] == ".txt":
                print "\n*** .txt files only, please. ***"
                continue
            try:
                keyfile = open(messagefile,"r")
            except IOError as err:
                print err
                continue
            key = keyfile.read()
            keyfile.close()
            break
        if choice == "exit":
            main()

    encryptedmessage = []
    key = [ord(i) for i in key]
    keycount = 0

    for char in range(len(message)):
        encryptedmessage.append(chr(ord(message[char]) ^ key[keycount]))
        keycount += 1
        if keycount >= len(key):
            keycount = 0
    encryptedmessage = base64.b64encode(''.join(encryptedmessage))

    encryptedfile = open(raw_input("Name encrypted message file:\n"),'w')
    encryptedfile.write(encryptedmessage)
    encryptedfile.close()
    main()

##########################################################
############        ABOUT       ##########################
##########################################################

def about():
    print """
****************************************************

Made by Joseph Bloom

This is a simple repeating-xor encryption and decryption tool. This tool is not
meant to securely encrypt any information, and in fact shows how insecure this
kind of encryption is. This is only a demonstration meant for my portfolio and
coding practice.

The two main options are Encrypt and Decrypt. You can encrypt a message by 
entering it manually or by using a simple text file (.txt), and then choosing
a key to encrypt themessage with, also either by manual input or by selecting a
text file with the key in it. A text file with the encrypted message is 
produced, and is base64 encoded so that the message can still be parsed, if not
read intelligibly. This is because an unencoded encrypted message may contain 
non-printable characters, and information could be lost in a simple text file,
or if the encrypted message is simply copy and pasted from the text file 
produced.

The decryption process does not use the selected key, but guesses it instead. 
Start by selecting a .txt file with the (base64 encoded) encrypted message. 
The text file doesn't necessarily need to be produced from this program. Any 
base64 encoded, repeating-xor encrypted message will do. Next, select the range
of possible keysizes, the number of characters, the key may have by choosing 
the lowest guess and then the highest guess. The program will make some 
calculations and will try to guess that was used to encrypt the message. If it
chooses a likely key, but that key still produces some non-printable characters,
then the correct key may not have been in that range of keysizes (or the message
was ecrypted by some other means). It will also show you the decrypted message
using that key. The next three key guesses are also listed above during 
the calculating.

This particular tool guesses based on how much the decrypted message looks like
normal English, or any language with the same set of letters. So any encrypted
message that uses non-standard English characters, like accented letters 
(é, ü, etc.), different alphabets like Korean or Urdu, or "alternative" 
alphabets like leet (1337), will not be decrypted. 

Again, this is for demonstration purposes only, and not serious use. 
I hope you enjoy it!

www.JosephBloomWorks.com
https://github.com/josephbloom

****************************************************
    """
    main()

##########################################################
############        MAIN        ##########################
##########################################################

def main():
    mainmenu = """
Menu:
(a) About / Help
(d) Decrypt
(e) Encrypt
(x) Exit
Select: """
    choice = raw_input(mainmenu).lower()

    if choice == "x":
        exit()
    elif choice == "d":
        decrypt()
    elif choice == "e":
        encrypt()
    elif choice == "a":
        about()
    else:
        main()

main()