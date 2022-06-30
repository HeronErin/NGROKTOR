import os, sys, json, threading, time
from pyngrok import ngrok

GIT = os.path.dirname(__file__)
URLS = os.path.join(GIT, "URLS.json")

NGROK = "~/python/ngrok"

def pushGit():
	os.system(f"cd {GIT} ; git commit . -m \"Updated Servers {time.ctime()}\" -q ; git push -q")



if len(sys.argv) == 3:
	urls_json = json.load(open(URLS, "r"))
	tcp = ngrok.connect(sys.argv[2], "tcp")
	pub = tcp.public_url.replace("tcp:/", "http:/")
	urls_json[sys.argv[1]] = pub

	f = open(URLS, "w")
	f.write(json.dumps(urls_json))
	f.close()


	pushGit()

	print(f"Started server on port {sys.argv[2]} on {pub}. Use CTRL-C to kill")
	ngrok_process = ngrok.get_ngrok_process()
	try:
		ngrok_process.proc.wait()
	except KeyboardInterrupt:
		print("Killing")

		ngrok.kill()

		del urls_json[sys.argv[1]]
		f = open(URLS, "w")
		f.write(json.dumps(urls_json))
		f.close()
		pushGit()
else:
	print("ERROR: use 2 arguments, [app name] [tcp port]")