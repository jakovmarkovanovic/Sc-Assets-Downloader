# -*- coding: utf-8 -*-

from Packet.Writer import *
from Packet.Reader import * 
from Packet.PreAuth import *
from Downloader import *
import socket
import argparse
import json
import sys

def recvall(sock,size):
	data = []
	while size > 0:
		sock.settimeout(5.0)
		s = sock.recv(size)
		sock.settimeout(None)
		if not s: raise EOFError
		data.append(s)
		size -= len(s)
	return b''.join(data)

if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='Download assets from official servers')
	parser.add_argument('-s', help='Download only files with specified extension', type=str, nargs='+')
	args = parser.parse_args()

	s = socket.socket()
	s.connect(('game.clashroyaleapp.com',9339))
	s.send(Write(PreAuth))

	Header = s.recv(7)
	size = int.from_bytes(Header[2:5],'big')
	print('[*] Receiving {}'.format(int.from_bytes(Header[:2],'big')))
	data = recvall(s,size)
	Reader = CoCMessageReader(data)
	if Reader.read_rrsint32() == 7:
		print('[*] FingerPrint has been received')
	else:
		print('[*] PreAuth packet is outdated , please get the latest one on GaLaXy1036 Github !')
		sys.exit()

	FingerPrint = Reader.read_string()
	Reader.read_string()
	AssetsUrl = Reader.read_string()

	Json = json.loads(FingerPrint)
	print('[INFO] Version = {}, MasterHash = {}'.format(Json['version'],Json['sha']))
	if args.s:	
		StartDownload(AssetsUrl,Json,tuple(args.s))
	else:
		StartDownload(AssetsUrl,Json)
