import sys

file_name = sys.argv[1]
txtfile = file_name + "_rel.txt"
binfile = file_name + ".bin"

f = open(txtfile,"r")
lines = f.readlines()
f.close()

isText = False
relText = []
for i in lines:
    if i == "\n":
        isText = False
    if isText:
        if i.find("Offset") != -1:
            continue
        relText.append(i)
    if i.find(".rel.text" ) != -1:
        isText = True        



arr = []
    
for i in relText:
    #print(i[:-1])
    tmp = i.split()
    arr.append( ((int(tmp[0],16)),(int(tmp[3],16))) )
    #print(hex(int(tmp[0],16)),hex(int(tmp[3],16)))
    
f = open(binfile, "rb")
a = bytearray(f.read())

f.close()

f = open(binfile, "wb")
for i in arr:
    
    index = i[0]
    adr = i[1] >>2
    ins = (a[index]<<24) + (a[index+1]<<16) + (a[index+2]<<8) + (a[index+3])
    opcode = ins & 0xfc000000
    tmp = opcode >> 26
    if (tmp == 0x2) or (tmp == 0x3):
        relins = opcode + adr
    else:
        relins = (ins & 0xffff0000) + i[1]
        
    #print("origin" , hex( (a[index]<<24) + (a[index+1]<<16) + (a[index+2]<<8) + (a[index+3]) ))
    
    a[index] = (relins >> 24) & 0xff
    a[index+1] = (relins >> 16) & 0xff
    a[index+2] = (relins >> 8) & 0xff
    a[index+3] = (relins) & 0xff
                                                           
    #print("rel",hex( (a[index]<<24) + (a[index+1]<<16) + (a[index+2]<<8) + (a[index+3]) ))
    #print(hex(a[index]),hex(a[index+1]),hex(a[index+2]),hex(a[index+3]))
f.write(a)
f.close()
