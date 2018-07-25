import socket
import sys

port=27010

s = socket.socket()
if(len(sys.argv)>1):
    print("Connecting...")
    s.connect((sys.argv[1], port))
    c=s
    print("Connection successful: ")
else:
    print("Server mode.")
    s.bind(('', 27010))
    s.listen()
    c, addr = s.accept()
    print("Connected: ", addr)

maxrecv=50000

msg=bytearray(maxrecv)

nrcv=c.recv_into(msg,maxrecv)

# parse the message
print("Cmd =",msg[0])

lth_ctnt=int.from_bytes(msg[1:9],byteorder='big')
print("Size =",lth_ctnt)

port=10
while(msg[port]!=10):
    port+=1
fnm=bytes(msg[9:port])
print("File name =",fnm)

recvd=nrcv-port-1

fp=open(fnm,"wb")

fp.write(msg[port+1:recvd])

while(recvd<lth_ctnt):
    nrcv=c.recv_into(msg, maxrecv)
    recvd+=nrcv
    fp.write(msg[0:nrcv])

# send reply
c.send((recvd).to_bytes(8,byteorder='big'))

if(c!=s):
    s.shutdown(socket.SHUT_RDWR)
    s.close()

c.shutdown(socket.SHUT_RDWR)
c.close

print("Done!")
