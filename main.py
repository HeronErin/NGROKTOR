import os, sys, json, threading, time
from pyngrok import ngrok

GIT = os.path.dirname(__file__)
URLS = os.path.join(GIT, "URLS.json")

NGROK = "~/python/ngrok"




if len(sys.argv) == 3:
	urls_json = json.load(open(URLS, "r"))
	tcp = ngrok.connect(sys.argv[2], "tcp")

	urls_json[sys.argv[1]] = tcp.public_url

	f = open(URLS, "w")
	f.write(json.dumps(urls_json))
	f.close()
	os.system(f"{GIT} ; ")



	print(f"Started server on port {sys.argv[2]}. Use CTRL-Z to kill")
	ngrok_process = ngrok.get_ngrok_process()
	try:
		ngrok_process.proc.wait()
	except KeyboardInterrupt:
		print("Killing")

		ngrok.kill()

else:
	print("ERROR: use 2 arguments, [app name] [tcp port]")