import requests
import json, os, shutil
import re
import youtube_dl
import urllib
from pyquery import PyQuery as Pq
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser


# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "AIzaSyCbeoSVR4_T8axH9tQaNGq3VG8SQMUB2jU"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

 
def tracks(playlist):
		if "user/spotifycharts" in playlist:
			playlist = playlist.replace('user/spotifycharts/','')
			print(playlist)
		r = requests.get(playlist)
		r.encoding = 'utf-8'
		f = open("kk.txt","w")
		f.write(r.text)
		f.close()
		jeje = r.text.split('Spotify.Entity = ')[1].split(';')[0]
		
		cosas = json.loads(jeje)
		songs = []
		for cancion in cosas['tracks']['items']:
			s = cancion['track']['name']
			if(len(s)<10):
				autores = ''
				for autor in cancion['track']['artists']:
					autores = autores + ' {}'.format(autor['name'])
				songs.append('{} {}'.format(autores, s))
			else:
				songs.append('{}'.format(s))
		urls = []
		for s in songs:
			print(s)
			try:
				url = api_youtube_search(s)
				if url is not None:
					urls.append(url)
			except Exception as e:
				print(e)
	
		try:
			bajarCancion(urls)
			
		except:
			pass
		if not os.path.isdir('./mp3'):
			os.mkdir('./mp3')
		for fi in os.listdir(os.getcwd()):
			if fi.endswith('.mp3'):
				shutil.move(fi,'./mp3')
		path = os.path.abspath("mp3")
		tracks = []
		for fi in os.listdir("mp3"):
			tracks.append(path + "/" + os.path.basename(fi))
		return tracks

	
 
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
	
	indice = lista_views.index(max(lista_views))
	return lista_url[indice]


def api_youtube_search(options):
	youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
	  developerKey=DEVELOPER_KEY)
  
	# Call the search.list method to retrieve results matching the specified
	# query term.
	search_response = youtube.search().list(
	  q=options,
	  part="id,snippet",
	  #maxResults=options.max_results,
	  order="viewCount"
	).execute()
	#f = open("kk.txt","w")
	#f.write(str(search_response.get("items", [])))
	#f.close()
	var = search_response.get("items", [])
	final = var[0]["id"]
	res = final["videoId"]
	url_final = "https://www.youtube.com/watch?v={}".format(res)
	return url_final

#api_youtube_search()

#print(tracks("https://open.spotify.com/playlist/2eW4xFXLFzk2XnYkxFbAu4?si=coNmfv68Q3KsQoZnqzPXLw"))