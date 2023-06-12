from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.conf import settings

import sys
import os
import socketio
import pty
import select
import subprocess
import struct
import fcntl
import termios 
import signal
import eventlet
import time
import json
import hashlib

async_mode = "eventlet"
sio = socketio.Server(async_mode=async_mode,
                     cors_allowed_origins='*')

# will be used as global variables
fd = None
child_pid = None
dic = {}


def index(request):
    print(request.COOKIES.get("io"))
    content = {}
    if (request.COOKIES.get("io") == None):
        current_time = bytes(str(time.time()), 'utf-8')
        hash_value = hashlib.sha256(current_time).hexdigest()
        content["hash_value"] = str(hash_value)
        print(content)
    return render(request, 'catutor/index.html', content)

def code(request):
    return render(request, 'catutor/code.html')

def result(request):
    global dic
    
    if request.method == 'POST':        
        test = request.COOKIES.get("test")
        file_name = test+'.c'
        code_content = request.POST.get('codearea')
        fs = FileSystemStorage(location=settings.MEDIA_ROOT)
        # .c 파일로 저장하기 위해 임시 파일 객체를 생성하여 저장
        with fs.open(file_name, 'wb') as file:
            file.write(code_content.encode())
    return render(request, 'catutor/result.html')


#changes the size reported to TTY-aware applications like vim
def set_winsize(fd, row, col, xpix=0, ypix=0):
    winsize = struct.pack("HHHH", row, col, xpix, ypix)
    fcntl.ioctl(fd, termios.TIOCSWINSZ, winsize)


def read_and_forward_pty_output(sid):
    #global fd
    global dic
    fd = dic.get(sid)[1]
    max_read_bytes = 1024 * 20
    while True:
        sio.sleep(0.01)
        if fd:
            timeout_sec = 0
            (data_ready, _, _) = select.select([fd], [], [], timeout_sec)
            if data_ready:
                output = os.read(fd, max_read_bytes).decode()
                sio.emit("pty_output", {"output": output, "sid": sid})
        else:
            print("process killed")
            return
        
@sio.event
def resize(sid, message):   
    global dic
    fd = dic.get(sid)[1]
    if fd:
        set_winsize(fd, message["rows"], message["cols"])

@sio.event
def pty_input(sid, message):
    global dic
    fd = dic.get(sid)[1]
    
    if fd:
        os.write(fd, message["input"].encode())
        
@sio.event
def load_register(sid):
    global dic
    fd = dic.get(sid)[1]
    data={}

    file_name = str(dic.get(sid)[1])+".bin.json"
    
    
    with open(file_name, 'r') as file:
        data = json.load(file)
        data["sid"] = sid
    
    sio.emit("send_register", data)
    os.write(fd, "rm {}.bin.json\n".format(fd).encode())
       
@sio.event
def load_code(sid):
    global dic
    fd = dic.get(sid)[1]
    file_name = "./media/single_cycle/"+str(dic.get(sid)[1])+".txt"
    
    file = open(file_name, 'r')
    lines = file.readlines()
    lines = lines[6:]
    code = ""
    for line in lines:
        code += line
    file.close()
    sio.emit("send_code", {"code": lines, "sid": sid})
    os.write(fd, "rm ./media/single_cycle/{}.txt\n".format(fd).encode())

@sio.event
def disconnect_request(sid):
    sio.disconnect(sid)

@sio.event
def connect(sid, environ):
    #global fd
    #global child_pid
    global dic
    print("-------")
    print(sid) #test cookie
    
    http_cookie = environ.get('HTTP_COOKIE')
    test = http_cookie.split()[1].split("=")[1].replace(";","")
    
    
    if dic.get(sid): #child_pid:
        # already started child process, don't start another
        # write a new line so that when a client refresh the shell prompt is printed
        fd = dic.get(sid)[1]
        os.write(fd, "\n".encode())
        return
    # create child process attached to a pty we can read from and write to
    (child_pid, fd) = pty.fork()
    dic[sid] = [child_pid, fd]
    
    if dic.get(sid)[0] == 0:
        # this is the child process fork.
        # anything printed here will show up in the pty, including the output
        # of this subprocess
        subprocess.run('bash')
    else:
        fd = dic.get(sid)[1]
        # this is the parent process fork.
        sio.start_background_task(target=read_and_forward_pty_output, sid=sid)
        sio.sleep(0.5)
        time.sleep(0.5)
        os.write(fd, "export PS1=\"\\u > \"\n".encode())
        os.write(fd, "mips-linux-gnu-gcc -c media/{}.c -mips1 -mfp32\n".format(test).encode())
        os.write(fd, "mips-linux-gnu-objcopy -O binary -j .text {}.o {}.bin\n".format(test, fd).encode())
        os.write(fd, "readelf -r {}.o > {}_rel.txt\n".format(test, fd).encode())
        os.write(fd, "python test.py {}\n".format(fd).encode())
        os.write(fd, "cd media/single_cycle\n".encode())
        #os.write(fd, "make clean\n".encode())
        #os.write(fd, "make\n".encode())
        os.write(fd, "chmod +x single_cycle_unit\n".encode())
        os.write(fd, "./single_cycle_unit ../../{}.bin\n".format(fd).encode())
        os.write(fd, "mips-linux-gnu-objdump -dS ../../{}.o > {}.txt\n".format(test, fd).encode())
        os.write(fd, "rm ../../{}.o\n".format(test).encode())
        os.write(fd, "rm ../../{}.bin\n".format(fd).encode())
        os.write(fd, "rm ../../{}_rel.txt\n".format(fd).encode())
        os.write(fd, "cd ../../\n".encode())
        os.write(fd, "gcc media/{}.c -o {}.out\n".format(test, fd).encode())
        os.write(fd, "rm media/{}.c\n".format(test).encode())
        os.write(fd, "clear\n".encode())
        os.write(fd, "./{}.out\n".format(fd).encode())
        #sio.emit("dispose")

@sio.event
def disconnect(sid):

    #global fd
    #global child_pid
    global dic
    fd = dic.get(sid)[1]
    child_pid = dic.get(sid)[0]
    
    os.write(fd, "rm ./media/single_cycle/{}.txt\n".format(fd).encode())
    os.write(fd, "rm {}.bin.json\n".format(fd).encode())
    os.write(fd, "rm {}.out\n".format(fd).encode())
    
    # kill pty process
    os.kill(child_pid,signal.SIGKILL)
    os.wait()

    # reset the variables
    #fd = None
    #child_pid = None
    del dic[sid]
    print('Client disconnected')