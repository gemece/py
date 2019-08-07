import requests
import json, os, shutil
import re
import youtube_dl
import urllib
from pyquery import PyQuery as Pq


 
def tracks(playlist):
		r = requests.get(
			"https://open.spotify.com/playlist/37i9dQZF1DXaxEKcoCdWHD?si=6JkbI8CBTTWPTwRPOxJQzw")
		r.encoding = 'utf-8'
		jeje = r.text.split('Spotify.Entity = ')[1].split(';')[0]
		cosas = json.loads(jeje)
		songs = []
		for cancion in cosas['tracks']['items']:
			autores = ''
			for autor in cancion['track']['artists']:
				autores = autores + ' {}'.format(autor['name'])
			#print(autores)
			#songs.append('{} {}'.format(cancion['track']['name'],autores))
			songs.append('{}'.format(cancion['track']['name']))
		urls = []
		for s in songs:
			try:
				url = search_youtube_video(s,1)
				if url is not None:
					urls.append(url)
			except Exception as e:
				print(e)
	
		try:
			bajarCancion(urls)
			if not os.path.isdir('./mp3'):
				os.mkdir('./mp3')
			for fi in os.listdir(os.getcwd()):
				if fi.endswith('.mp3'):
					shutil.move(fi,'./mp3')
		except:
			pass

	
 
def bajarCancion(url):
	print("Bajando cancion")
	ydl_opts = {'format': 'bestaudio / best', 'postprocessors': [
		{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '720', }], }
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		ydl.download(url)
 
def search_youtube_video(title, pages):
	print("Entramos en la busqueda")
	cont = 0
	lista_url = []
	lista_views = []
	for page in range(pages):
		params = urllib.parse.urlencode({'search_query': 'intitle:"%s", video' % title, 'page': page})
		jq = Pq(url="http://www.youtube.com/results?%s" % params,headers={"user-agent": "Mozilla/5.0 (Windows NT 6.1; rv:24.0) Gecko/20140129 Firefox/24.0"})
		print(params)
		jq.make_links_absolute("http://www.youtube.com")
		for video in jq("ol.item-section").children().items():
			url = video.find("a.yt-uix-tile-link").attr("href")
			lista_url.append(url)
			views = video.find("ul.yt-lockup-meta-info li").eq(1).html()
			if views is not None:
				res = int(views.split('visualizaciones')[0].strip().replace('.', ''))
			else:
				res = 0
			lista_views.append(res)
			
			cont = cont + 1
			if cont == 8 :
				indice = lista_views.index(max(lista_views))
				print("views: {} ".format(max(lista_views)))
				print("indice: {}".format(indice))
				print("url: " + lista_url[indice])
				return lista_url[indice]

	return None

