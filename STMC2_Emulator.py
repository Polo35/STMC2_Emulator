# STMC2_Emu.py
# ST Micro Connect V2 Emulator
# Emule functionnality of STMC2 box used to JTAG ST40 processors.

# Copyright 2011, Polo35
# Licenced under Academic Free License version 3.0
# Review STMC2_Emu README & LICENSE files for further details.


import os
import sys
import time
import thread
import base64
import socket
import struct
import SimpleXMLRPCServer


# STMC2 Hardware Check Server
class Hardware_Check_Server(object):

	def Start_Server(self, server_port):
		global Hardware_Check_Server_Pid
		Hardware_Check_Server_Pid = os.getpid()
		print 'STMC2 HW Check Server started on port %d' % server_port
		while True:
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
			sock.bind(('', server_port))
			sock.listen(1)
			conn, addr = sock.accept()
			print '\nSTMC2 HW Check Server: Connected by', addr
			# Receive Packet
			Data = conn.recv(1024)
			if len(Data) == 128:
				RecvPacket =  struct.unpack('128B', Data)
				if RecvPacket[0] == 0xA:
					print 'STMC2 HW Check Server: Sending HW type STMC2\n'
					SendPacket  = struct.pack('5s', 'STMC2')
					for i in range(5, 532):
						SendPacket += struct.pack('B', 0)
					conn.send(SendPacket)
			conn.close()


# STMC2 System Manager RPC Server
class System_Manager_Server(object):

	def Start_Server(self, server_port):
		# Memo PID Of This Thread
		global System_Manager_Server_Pid
		System_Manager_Server_Pid = os.getpid()
		# Create The System Manager RPC Server
		server_ip = socket.gethostbyname(socket.gethostname())
		server = SimpleXMLRPCServer.SimpleXMLRPCServer((server_ip, server_port))
		# Register The System Manager RPC Server Functions
		server.register_function(self.GetMC2Type, 'GetMC2Type')
		server.register_function(self.GetTargetManager, 'GetTargetManager')
		server.register_function(self.RunTargetManager, 'RunTargetManager')
		server.register_function(self.RunApp, 'RunApp')
		server.register_function(self.STMCReset, 'STMCReset')
		server.register_function(self.GetSysLog, 'GetSysLog')
		server.register_function(self.Dhcp, 'Dhcp')
		server.register_function(self.IFConfig, 'IFConfig')
		server.register_function(self.Route, 'Route')
		server.register_function(self.Restore, 'Restore')
		server.register_function(self.FirmwareReturnShiny, 'FirmwareReturnShiny')
		server.register_function(self.FirmwareUpgrade_ClearShiny, 'FirmwareUpgrade_ClearShiny')
		server.register_function(self.FirmwareUpgrade_CopySTMC, 'FirmwareUpgrade_CopySTMC')
		server.register_function(self.FirmwareUpgrade_StartServer, 'FirmwareUpgrade_StartServer')
		server.register_function(self.FirmwareDowngrade, 'FirmwareDowngrade')
		server.register_function(self.FirmwareVersion, 'FirmwareVersion')
		server.register_function(self.FirmwareVersionParsed, 'FirmwareVersionParsed')
		server.register_function(self.SerialConfig, 'SerialConfig')
		server.register_function(self.LCDMessage, 'LCDMessage')
		server.register_function(self.FlashLEDs, 'FlashLEDs')
		server.register_function(self.Status, 'Status')
		server.register_function(self.Debug, 'Debug')
		# Start the System Manager RPC Server
		print 'STMC2 System Manager Server started on port %d' % server_port
		try:
			server.serve_forever()
		finally:
			server.server_close()

	def GetMC2Type(self):
		print 'STMC2 System Manager Server: GetMC2Type Called'
		server_ip = socket.gethostbyname(socket.gethostname())
		return (('mb435', server_ip, [server_ip]), 0, 'Success', '')
	
	def GetTargetManager(self):
		print 'STMC2 System Manager Server: GetTargetManager Called'
		return (('14.0', 1337), 0, 'Success', '')
	
	def RunTargetManager(self, killCurrent, appId, path, data, commandList):
		print 'STMC2 System Manager Server: RunTargetManager Called'
		# Kill old TargetManager
		if killCurrent == True:
			psInfo = str(os.system("ps | grep '/tmp/stmc_coreagent_'"))
			psInfoLines = psInfo.split('\n')
			for p in psInfoLines:
				info = p.split()
				if (len(info) < 5):
					continue
				if ((0 == info[4].find('/tmp/stmc_coreagent_')) and _DebugSTMC('Killing zombie TargetManager.')):
					os.system('kill -9 %s' % (info[0]))
		# Copy data to path
                try:
                        os.makedirs('/tmp/STMC2_TargetManager')
                except:
                        pass
		if os.path.exists('/tmp/STMC2_TargetManager/%s' % path):
                        os.remove('/tmp/STMC2_TargetManager/%s' % path)
		fd = open('/tmp/STMC2_TargetManager/%s' % path, 'wb')
		fd.write(base64.decodestring(data))
		fd.close()
		# Execute commandList (untar, rm, python)
		for command in commandList:
                        print command
		return 'OK', 0, 'Success', ''
	
	def RunApp(self, appId, path, data, commandList):
		print 'STMC2 System Manager Server: RunApp Called'
		print 'appId: ',
		print appId
		print 'path: ',
		print path
		print 'data: ',
		print data
		print 'commandList: ',
		print commandList
		return 'OK', 0, 'Success', ''
	
	def STMCReset(self, t):
		print 'STMC2 System Manager Server: STMCReset Called'
		print 'Arg: ',
		print t
		return 'OK', 0, 'Success', ''
	
	def GetSysLog(self, p):
		print 'STMC2 System Manager Server: GetSysLog Called'
		print 'Arg: ',
		print p
		return 'OK', 0, 'Success', ''
	
	def Dhcp(self, p):
		print 'STMC2 System Manager Server: Dhcp Called'
		print 'Arg: ',
		print p
		return 'OK', 0, 'Success', ''
	
	def IFConfig(self, p):
		print 'STMC2 System Manager Server: IFConfig Called'
		print 'Arg: ',
		print p
		return 'OK', 0, 'Success', ''
	
	def Route(self, p):
		print 'STMC2 System Manager Server: Route Called'
		print 'Arg: ',
		print p
		return 'OK', 0, 'Success', ''
	
	def Restore(self, t):
		print 'STMC2 System Manager Server: Restore Called'
		print 'Arg: ',
		print t
		return 'OK', 0, 'Success', ''
	
	def FirmwareReturnShiny(self):
		print 'STMC2 System Manager Server: FirmwareReturnShiny Called'
		return 'OK', 0, 'Success', ''
	
	def FirmwareUpgrade_ClearShiny(self):
		print 'STMC2 System Manager Server: FirmwareUpgrade_ClearShiny Called'
		return 'OK', 0, 'Success', ''
	
	def FirmwareUpgrade_CopySTMC(self):
		print 'STMC2 System Manager Server: FirmwareUpgrade_CopySTMC Called'
		return 'OK', 0, 'Success', ''
	
	def FirmwareUpgrade_StartServer(self):
		print 'STMC2 System Manager Server: FirmwareUpgrade_StartServer Called'
		return 'OK', 0, 'Success', ''
	
	def FirmwareDowngrade(self, t):
		print 'STMC2 System Manager Server: FirmwareDowngrade Called'
		print 'Arg: ',
		print t
		return 'OK', 0, 'Success', ''
	
	def FirmwareVersion(self):
		print 'STMC2 System Manager Server: FirmwareVersion Called'
		return ('STMC2 firmware version 14.0 00 Feb 2011', 0, 'Success', '')
	
	def FirmwareVersionParsed(self):
		print 'STMC2 System Manager Server: FirmwareVersionParsed Called'
		return ('OK', 0, 'Success', '')
	
	def SerialConfig(self, p):
		print 'STMC2 System Manager Server: SerialConfig Called'
		print 'Arg: ',
		print p
		return ('OK', 0, 'Success', '')
	
	def LCDMessage(self, p):
		print 'STMC2 System Manager Server: LCDMessage Called'
		print 'Message: ',
		print p
		return ('OK', 0, 'Success', '')
	
	def FlashLEDs(self, f):
		print 'STMC2 System Manager Server: FlashLEDs Called'
		print 'Arg: ',
		print f
		return ('OK', 0, 'Success', '')
	
	def Status(self, p):
		print 'STMC2 System Manager Server: Status Called'
		print 'Arg: ',
		print p
		return ('OK', 0, 'Success', '')
	
	def Debug(self, p):
		print 'STMC2 System Manager Server: Debug Called'
		print 'Command: ',
		print p
		ret = os.system(p)
		return (str(ret), 0, 'Success', '')


# Threads PID
Hardware_Check_Server_Pid, System_Manager_Server_Pid = 0, 0

# Program Main
if (__name__ == '__main__'):
	print 'ST Micro Connect V2 Emulator by Polo35\n'
	# Start The Hardware Check Server Thread
	thread.start_new_thread(Hardware_Check_Server().Start_Server, (9735,))
	# Start The System Manager Server Thread
	thread.start_new_thread(System_Manager_Server().Start_Server, (7999,))
	time.sleep(1)
	# Wait Control-C To Stop Threads
	try:
		raw_input('\nType Control-C to exit\n')
	except KeyboardInterrupt:
		pass
	os.popen("kill -9 "+str(Hardware_Check_Server_Pid))
	os.popen("kill -9 "+str(System_Manager_Server_Pid))
