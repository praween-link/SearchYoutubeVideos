# My Project 68172
# api : AIzaSyB2_zfEj-nRmf5W7iKLSS4gCYcVE7SGIIQ

import requests
import datetime

from isodate import parse_duration # for video time duration

from django.conf import settings
from django.shortcuts import render
# ___________STACK START___________
class Stack:
    # --------PUSH----------
    def push(self, arr, n):
        arr.append(n)
        # print(f"{n} is inserted successfully !")
        return arr

    # --------POP-------
    def pop(self): 
        loc = len(arr)
        d = arr[loc-1]
        arr.pop(loc-1)
        # print(f"{d} is deleted successfully !")

# ___________STACK END___________

# ___________DateTime____________

# class Pday:
#     def get_user_birthday(self):
#         year = int(input('When is your birthday? [YY] '))
#         month = int(input('When is your birthday? [MM] '))
#         day = int(input('When is your birthday? [DD] '))
#         birthday = datetime.datetime(year,month,day)
#         return birthday


#     def calculate_dates(self, original_date, now):
#         date1 = now
#         date2 = datetime.datetime(original_date.year, original_date.month, original_date.day)
#         delta = date2 - date1
#         days = delta.total_seconds() / 60 /60 /24

#         return days

# Create your views here.
videos = []
def index(request):
    global videos
    videos = []
    
    date = datetime.datetime.now()
    currentYear = date.strftime("%Y")
    currentMonth = date.strftime("%m")
    currentDay = date.strftime("%d")

    if request.method == 'POST':
        if request.POST.get('search'):
            search_url = 'https://www.googleapis.com/youtube/v3/search'
            video_url = 'https://www.googleapis.com/youtube/v3/videos'
            
            search_params = {
                'part' : 'snippet',
                'q' : request.POST['search'],
                'key' : settings.YOUTUBE_DATA_API_KEY,
                'maxResults' : 20,
                'type' : 'video'
            }
            # print("-----------------------")
            # print(request.POST['search'])
            # print("-----------------------")

            video_ids = []
            r = requests.get(search_url, params=search_params)

            # print("---", r.text)
            results = r.json()['items']
            
            for result in results:
                video_ids.append(result['id']['videoId'])

            video_params = {
                'key' : settings.YOUTUBE_DATA_API_KEY,
                'part' : 'snippet, contentDetails',
                'id' : ','.join(video_ids),
                'maxResults' : 20
            }

            r = requests.get(video_url, params=video_params)
            
            results = r.json()['items']

            for result in results:
                
                

                # Age of video
                ageOfVideo = ""
                if(int(currentYear) == int(result['snippet']['publishedAt'][:4])):
                    if(int(currentMonth) == int(result['snippet']['publishedAt'][5:7])):
                        if(int(currentDay) == int(result['snippet']['publishedAt'][8:10])):
                            ageOfVideo = "today"
                        else:
                            x = int(currentDay) - int(result['snippet']['publishedAt'][8:10])
                            ageOfVideo = f"{x} days ago"
                    else:
                        x = int(currentMonth) - int(result['snippet']['publishedAt'][5:7])
                        ageOfVideo = f"{x} months ago"
                else:
                    x = int(currentYear) - int(result['snippet']['publishedAt'][:4])
                    ageOfVideo = f"{x} years ago"
                # print(ageOfVideo)

                print(parse_duration(result['contentDetails']['duration']))
                
                # print(result['snippet']['thumbnails']['high']['url'])
                video_data = {
                    'title' : result['snippet']['title'],
                    'id' : result['id'],
                    'videoduration' : parse_duration(result['contentDetails']['duration']),
                    'thumbnail' : result['snippet']['thumbnails']['high']['url'],
                    'publishedat' : result['snippet']['publishedAt'],
                    'ageofvideo' : ageOfVideo

                    #'url' : f"https://www.youtube.com/embed/{result['id']}?playlist={result['id']}&loop=1"
                }
                
                # ---------- SET DATE TIME CONDITIONS ----------------------

                if(request.POST['date1'][:] != '' and request.POST['date2'][:] != ''):
                    publiceY = int(result['snippet']['publishedAt'][:4])
                    publiceM = int(result['snippet']['publishedAt'][5:7])
                    publiceD = int(result['snippet']['publishedAt'][8:10])

                    currentY = int(currentYear)
                    currentM = int(currentMonth)
                    currentD = int(currentDay)

                    getY1 = int(request.POST['date1'][:4])
                    getM1 = int(request.POST['date1'][5:7])
                    getD1 = int(request.POST['date1'][8:10])

                    getY2 = int(request.POST['date2'][:4])
                    getM2 = int(request.POST['date2'][5:7])
                    getD2 = int(request.POST['date2'][8:10])

                    if getY1<=publiceY and getY2>=publiceY:
                        print(result['snippet']['publishedAt'][:4])
                        videos.append(video_data)

                elif(request.POST['date1'][:] != ''):
                    publiceY = int(result['snippet']['publishedAt'][:4])
                    publiceM = int(result['snippet']['publishedAt'][5:7])
                    publiceD = int(result['snippet']['publishedAt'][8:10])

                    currentY = int(currentYear)
                    currentM = int(currentMonth)
                    currentD = int(currentDay)

                    getY1 = int(request.POST['date1'][:4])
                    getM1 = int(request.POST['date1'][5:7])
                    getD1 = int(request.POST['date1'][8:10])

                    if getY1<= publiceY and currentY >= publiceY:
                        print(result['snippet']['publishedAt'][:4])
                        videos.append(video_data)
                else:
                    print(result['snippet']['publishedAt'][:4])
                    videos.append(video_data)
                #-----------------------------------------------------------

            if request.POST.get('textp'):
                test = request.POST.get('textp')
                

    context = {
        'videos' : videos
    }
    return render(request, 'tubefiles/index.html', context)

def watchingVideo(request):

    contextp = {
        'videos' : videos
    }
    return render(request, 'tubefiles/watching_video.html', contextp)