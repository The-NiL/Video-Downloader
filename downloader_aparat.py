from bs4 import BeautifulSoup
import requests
import re


def getlinks():
    playlist_links = []
    links_with_dup = []
    links_without_dup = set()

    main_link = "https://www.aparat.com/playlist/203472"
    
    page = requests.get(main_link)
    soup = BeautifulSoup(page.text, "html.parser")

    for link in soup.find_all('a'):
        href = link.get("href")
        if ("/v/" in href):
            url = "https://aparat.com" + href
            playlist_links.append(url)

    for link in playlist_links:
        links_with_dup.append(re.findall("https://aparat.com/v/.+_[0-9]+", link))

    for item in links_with_dup[1:]:
        links_without_dup.add(item[0])
    

    return links_without_dup



def download_video_series(video_links, episode): 

	for link in video_links: 
		file_name = "bear"+ "{}".format(episode) + ".mp4"

		print ("Downloading file:%s" % file_name)
		
		r = requests.get(link, stream = True) 
	
		with open("/users/nil/Desktop/bear/{}".format(file_name), 'wb') as f: 
			for chunk in r.iter_content(chunk_size = 1024*1024): 
				if chunk: 
					f.write(chunk) 
		
		print ("%s downloaded!\n"%file_name )

	return



def get_down_link():

    links = getlinks()
    episode = 1

    for link in links:
        
            page = requests.get(link)
            matched = re.findall('"contentUrl":(.+)', page.text)
            matched[0] = matched[0].replace(",","")
            matched[0] = matched[0].replace('"', "")

            download_video_series(matched, episode)

            episode += 1
    

    print ("All videos downloaded!")

        
get_down_link()