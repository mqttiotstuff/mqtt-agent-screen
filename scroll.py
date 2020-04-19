
import font
import time

#
# construct a char representation
# 
def charSequence(char,color):
    e = font.printChar(char)
    return toLED(e,color)


def toLED(buffer, color):
    """ take a buffer, color it and return the led buffer """
    s = ""
    for i in range(7,-1,-1):
        for j in range(0,8):
            b = (buffer[j][i:i+1]) == "X"
            s = (s + color) if b else (s + chr(0)+chr(0) + chr(0))

    return s

def shiftBufferLeft(buffertoshift,enteringelements,outelements):
    assert type(buffertoshift) == list
    assert type(enteringelements) == list    
    assert len(buffertoshift) == 8
    assert len(enteringelements) == 8
    assert type(outelements) == list

    for i in range(0,8):
        s = buffertoshift[i]
        c = s[0:1]
	r = s[1:8]
        buffertoshift[i] = r + enteringelements[i] 
        outelements[i] = c


def newBuffer():
    """ allocate a new buffer for screen """
    buffer = []
    for i in range(0,8):
        buffer.append("        ")
    return buffer


def colorToPixel(r,g,b):
    return chr(r) + chr(g) + chr(b)

def interpolateColor(color,factor):
    rmax = ord(color[0])
    gmax = ord(color[1])
    bmax = ord(color[2])
    return chr(int(rmax * factor * factor)) + chr(int(gmax * factor * factor)) + chr(int(bmax * factor * factor )) 


def fading(client, topic,  char, color , r = 1):
    c = font.printChar(char) 
    fadingBuffer(client, topic, c, color, r)

def fadingBuffer(client, topic,buffer, color , r = 1):
    start = 0 if r == 1 else 9
    end = 9 if r == 1 else 0 
    for i in range (start,end,r):
        b = toLED(buffer, interpolateColor(color, i * 1.0  / 10.0))        
        client.publish(topic, b)
        time.sleep(0.05)


def fadinfadout(client, topic,  char, color ):
    fadinfadoutBuffer(client, topic, font.printChar(char), color);

def fadinfadoutBuffer(client, topic, buffer , color ):
    fadingBuffer(client, topic, buffer, color, 1)
    time.sleep(1)
    fadingBuffer(client, topic, buffer, color, -1)

def scroll(client, message, topic):
    """
	client : clientmqtt
        message : message to scroll
        topic: topic on which we send the elements for scroll
    """
    print("message to scroll :" + str(message))
    buffer = []
    for i in range(0,8):
        buffer.append("        ")

    displayed = [buffer]
    for m in message:
        displayed.append(font.printChar(ord(m)))    

    # print(displayed)


    for i in range(0,8*(len(message) + 1)):
        a=[" "," "," "," "," "," "," "," "]
        for j in range(len(message),-1,-1):
            b=[" "," "," "," "," "," "," "," "]
            shiftBufferLeft(displayed[j],a,b)
            a=b
        #print(" display " + str(i))
        #print(displayed)
        m = toLED(displayed[0], colorToPixel(10,0,0)) 
        client.publish(topic,m)
	
        time.sleep(0.05)


