import requests
import json
import os
import re
import subprocess
import sys
import time


def get_latest_proxy():
	url = 'https://proxy.horocn.com/api/free-proxy?format=json&loc_name=%E4%B8%AD%E5%9B%BD'
	r = requests.get(url)
	ip_ports = json.loads(r.text)
	return ip_ports

def check_location_cn(ip_add):
	try:
		url = 'http://ip.taobao.com/service/getIpInfo.php?ip='+ip_add
		r = requests.get(url)
		r = r.content.decode()
		data = json.loads(r)
		now_location = data['data']['country_id']
		if(now_location == 'CN'):
			return True
		else:
			return False
	except:
		return False

def check_ip(ip,port):
	proxy_url = "http://"+ip+":"+str(port)
	proxies = {
	  "http": proxy_url
	}
	try:
		try:
			r = requests.get("http://ip.chinaz.com/getip.aspx", proxies=proxies,timeout=5)
			now_ip = re.search('\d+\.\d+\.\d+\.\d+',r.text).group(0)
		except:
			r = requests.get("http://checkip.dyndns.com/", proxies=proxies,timeout=5)
			now_ip = re.search('\d+\.\d+\.\d+\.\d+',r.text).group(0)

		if check_location_cn(now_ip):
			return True
		else:
			return False
	except:
		return False

def write_netease_config(ip,port):
	try:
		sample_dict = {'Proxy': {'ie': {'Port': '', 'UserName': '', 'Password': '', 'Host': ''}, 'socks': {'Port': '', 'UserName': '', 'Password': '', 'Host': ''}, 'Type': 'http', 'http': {'Port': '', 'UserName': '', 'Password': '', 'Host': ''}, 'https': {'Port': '', 'UserName': '', 'Password': '', 'Host': ''}, 'socks5': {'Port': '', 'UserName': '', 'Password': '', 'Host': ''}, 'none': {'Port': '', 'UserName': '', 'Password': '', 'Host': ''}, 'socks4': {'Port': '', 'UserName': '', 'Password': '', 'Host': ''}}}
		path = os.getenv('LOCALAPPDATA')+"\\Netease\\CloudMusic\\"
		with open(path+'Config') as data_file:
		    data = json.load(data_file)
		if 'Proxy' in data.keys():
			data['Proxy']['Type'] ='http'
			data['Proxy']['http']['Host'] = ip
			data['Proxy']['http']['Port'] = str(port)
		else:
			data=dict(data, **sample_dict)
			data['Proxy']['Type'] ='http'
			data['Proxy']['http']['Host'] = ip
			data['Proxy']['http']['Port'] = str(port)
		pretty_data = json.dumps(data, indent=3, sort_keys=True)
		with open(path+'Config', 'w') as f:
			f.write(pretty_data)
	except:
		print("****************************************")
		print("Error 0:")
		print("Can not write config.")
		print("****************************************")

def run_netease():
	run_path = os.getcwd()+"\cloudmusic.exe"
	try:
		subprocess.Popen([run_path])
	except:
		print("****************************************")
		print("Error 1:")
		print("Can not run NetEase Music.")
		print("Please check location of this program.")
		print("****************************************")


def get_avalibale_ip():
	ip_ports = get_latest_proxy()
	print("Get "+str(len(ip_ports))+" proxies successfully!")
	i = 0
	for each in ip_ports:
		i += 1
		ip = each["host"]
		port = each["port"]
		print("Checking "+str(i)+" of "+str(len(ip_ports))+" proxies.Please Wait...")
		if check_location_cn(ip) and check_ip(ip,port):
			print("Find available proxy!")
			break
	return ip,port

if __name__ == '__main__':
	print("___________                 .__              ")
	print("\_   _____/__________  ____ |__|__  __ ____  ")
	print(" |    __)/  _ \_  __ \/ ___\|  \  \/ // __ \ ")
	print(" |     \(  <_> )  | \/ /_/  >  |\   /\  ___/ ")
	print(" \___  / \____/|__|  \___  /|__| \_/  \___  >")
	print("     \/             /_____/               \/ ")
	print("    _________ .__                   .___")
	print("    \_   ___ \|  |   ____  __ __  __| _/")
	print("    /    \  \/|  |  /  _ \|  |  \/ __ | ")
	print("    \     \___|  |_(  <_> )  |  / /_/ | ")
	print("     \______  /____/\____/|____/\____ | ")
	print("            \/                       \/ ")
	print("========================================")
	print("          Forgive Cloud V2.2            ")
	print("          Powered by o8b.club           ")
	print("========================================")
	print("STEP 1/2 Getting newest IP proxy pool...")
	ip,port = get_avalibale_ip()
	print("----------------------------------------")
	print("STEP 2/2 Writing configuration files...")
	write_netease_config(ip,port)
	print("========================================")
	print("Success!Now running NetEase CloudMusic...")
	run_netease()
	print("----------------------------------------")
	print("The program will exit in 3 seconds...")
	print("========================================")
	time.sleep(3)
	sys.exit(0)
