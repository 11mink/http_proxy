import sys
import threading
from os import _exit
from socket import *

def usage():
	print("usage : python http_proxy.py <port>")

def quit(sock):
	print("Proxy Server is On")
	print("(press ENTER to quit)")
	if sys.stdin.readline():
		sock.close()
		os._exit(0)

def proxyFunc(browser):
	size = 8096
	data = browser.recv(size)
	if not data:
		return

	#get hostname from data
	h = data.split('\r\n')[1]
	host = h[h.index(" ")+1:]
	addr = (host,80)
	
	#unintended host handling
	try:
		webserver = socket(AF_INET, SOCK_STREAM)
		webserver.connect(addr)
		webserver.send(data)
	except:	
		return

	while True:
		data = webserver.recv(size)
		if not data:
			webserver.close()
			browser.close()
			return
		else:
			browser.send(data)

def main():
	if len(sys.argv) != 2:
		usage()
		sys.exit()

	ip = "127.0.0.1"
	port = sys.argv[1]
	addr = (ip, int(port))

	proxy = socket(AF_INET, SOCK_STREAM)
	proxy.bind(addr)
	proxy.listen(5)
	threading.Thread(target = quit, args = (proxy,)).start()

	while True:
		browser, addr = proxy.accept()
		threading.Thread(target = proxyFunc, args = (browser,)).start()

if __name__ == "__main__":
	main()