import pexpect
import gmpy2
from Crypto.Util.number import *

groupToken = ""
child = pexpect.spawn('python main.py')
# child = pexpect.spawn('nc 165.232.161.196 4020')
# send group token
child.sendline(groupToken)
# expect paket soal. read it and print it
def singleReading(child):

    child.expect('paket_soal = ')
    child.expect('n = ')

    # remove \r and \n
    questionType = child.before.decode().split('\r\n')
    questionType = questionType[0]

    print(questionType)
    # print("testing")

    child.expect('e = ')

    numberN = child.before.decode().split('\r\n')
    numberN = numberN[0]
    # print(numberN)


    child.expect('c = ')

    numberE = child.before.decode().split('\r\n')
    numberE = numberE[0]
    # print(numberE)

    child.expect('Jawaban = ')

    numberC = child.before.decode().split('\r\n')
    numberC = numberC[0]
    # print(numberC)


    return questionType, numberN, numberC, numberE


def breaker(questionType, numberN, numberC, numberE):
    if(questionType == "A" or questionType == "B"):
        # for case A and B
        n = int(numberN)
        # print n in decimal
        # floor it
        root_n = gmpy2.isqrt(n)
        
        root_n = (root_n)
        
        while True:
            # divide n by root_n
            if n % root_n == 0:
                p = root_n
                q = n // root_n
                break
            root_n += 1
        
        # print("p: ", p)
        # print("q: ", q)
        # find flag
        if(p == q):
            tot = (p-1) * (q)
        else:
            tot = (p-1) * (q-1)
        e = 65537
        d = pow(e, -1, tot)
        cipherText = int(numberC)
        m = pow(cipherText, d, n)
        plainText = long_to_bytes(m).decode()
        # print(plainText)

    elif(questionType == "C"):
        # for case C
        topE = 2 ** 16
        minE = 2 ** 15

        cipherText = int(numberC)   
        n = int(numberN)

        for e in range(minE, topE):
            plainTextLong = pow(cipherText, e, n)
            try:
                plainText = long_to_bytes(plainTextLong).decode()
            except:
                continue
            # if start with KRIPTOGRAFIITB then it's correct, stop the loop
            if plainText.startswith("KRIPTOGRAFIITB"):
                break
        
        # print(plainTextLong)
        # long to bytes to string
        # print(plainText)

    elif(questionType == "D"):
        # small e. 
        # we can brute force. probably no 'wrap around'
        # m^e = c mod n
        # m^e = c + k*n, probably k will be low.
  
        n = int(numberN)
        
        e = 3
        
        c = int(numberC)
        
        
        # m^e = c + k*n, probably k will be low.
        k = 0
        topK = 10
        for i in range(topK):
            m, isExact = gmpy2.iroot(c + i*n, e)
            if isExact:
                k = i
                break
        # print("k: ", k)
        # print("m: ", m)

        plainText = long_to_bytes(m).decode()
        # print(plainText)
    elif questionType == "E":
        # for case E
        n = int(numberN)
        tot = n - 1
        e = 65537
        cipherText = int(numberC)
        d = pow(e, -1, tot)
        m = pow(cipherText, d, n)
        plainText = long_to_bytes(m).decode()
        # print(plainText)
    else:
        print("Invalid question type")
    
    return(plainText)


# if found Uhuyyyy, then it's over
counter = 0
while(True):
    # isFound = child.expect('paket_soal =')
    # if(isFound == 0):
    #     print("not found")
    #     break
    # else:
    #     print("found")
    try:
        questionType, numberN, numberC, numberE = singleReading(child)
    except:
        break
    plainText = breaker(questionType, numberN, numberC, numberE)
    print(plainText)
    child.sendline(plainText)
    counter += 1
    print("solved: ", counter)

print(child.before.decode())

child.close()