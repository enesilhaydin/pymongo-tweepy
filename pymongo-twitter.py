# -*- coding: utf-8 -*-
import pprint
import tweepy
from pymongo import MongoClient
import sys
from colorama import init
init(strip=not sys.stdout.isatty())
from termcolor import cprint
from pyfiglet import figlet_format
import itertools
import threading
import time

done=False;

class global_Yap:
    global animate
    global kullanici_kontrol
    def kullanici_kontrol():
        while True:
            try:
                kullanici_adi=input("\n\033[0;31;40m Arama yapılacak kullanıcı adını giriniz = ")
                user = api.get_user(kullanici_adi)
                return user,kullanici_adi
                break


            except tweepy.TweepError as e:
                print("Böyle bir kullanıcı bulunmamaktadır.")
                print("Lütfen tekrar giriniz...")

    def animate():
        for c in itertools.cycle(['|', '/', '-', '\\']):
            if done:
                break
            sys.stdout.write('\rDatabase üzerine yazılmaktadır. Lütfen bekleyiniz... ' + c)
            sys.stdout.flush()
            time.sleep(0.1)
        sys.stdout.write('\rBütün veriler database üzerine yazıldı!     ')

cprint(figlet_format('enesilhaydin', font='small'),
        attrs=['bold'])

print("twitter/enesilhaydin \n ======================")

client = MongoClient('localhost', 27017)

db_name=input("Bilgilerin yazılacağı DATABASE ismi yazınız = ")
database = client[db_name];
collist = database.list_collection_names()
collection2=database["takipciler"]
collection = database["takip_edilenler"]
if "takip_edilenler" in collist:
  drop_test=input("\"Takip Edilenler\" collection'ı zaten bulunmaktadir. Drop islemi yapmak istiyorsanız 1, istemiyorsanız 2 yazıp enterlamınız gerekmektedir...")
  if drop_test=='1':
      collection.drop()

if "takipciler" in collist:
    drop_test2=input("\"Takipciler\" collection'ı zaten bulunmaktadir. Drop islemi yapmak istiyorsanız 1, istemiyorsanız 2 yazıp enterlamınız gerekmektedir...")
    if drop_test2=='1':
      collection2.drop()


consumer_key=input("Consumer key'i giriniz = ")
consumer_secret=input("Consumer Secret'i giriniz = ")
access_token=input("Access Token'i giriniz = ")
access_token_secret=input("Access Token Secret'i giriniz = ")

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

user,kullanici_adi=kullanici_kontrol()

friend_ids = api.friends_ids(kullanici_adi);
followers_ids = api.followers_ids(kullanici_adi)
def takip_edilenler_gogb():
    t = threading.Thread(target=animate)
    t.start()

    try:
                for x in friend_ids:
                    user = api.get_user(id=x)                  
                    icerik = [{"kullanici_id":user.id,"kullanici_adi" : user.name ,"username":user.screen_name, "hakkinda" : user.description,"tweet_sayisi":user.statuses_count,"takipci_sayisi":user.followers_count,
                               "takip_edilen_sayisi":user.friends_count,"hesap_olusturma_tarihi":user.created_at,"favori_tweet_sayisi":user.favourites_count,
                               "konum_acikmi":user.geo_enabled,"onayli_hesapmi":user.verified,"armut_resimmi":user.default_profile_image,
                    "takip_ediyormusun":user.following,"istekmi_gönderildi":user.follow_request_sent,"bildirimler_acikmi":user.notifications}]
                    collection.insert_many(icerik)
                done = False


    except tweepy.TweepError:
                pass


def takipcileri_godb():
    t = threading.Thread(target=animate)
    t.start()
    try:
        for y in followers_ids:
            user = api.get_user(id=y)          
            sayac=0
            a=[]
                       
            try:
                tweetler = api.user_timeline(id=y, count=100, include_rts=True,tweet_mode="extended")

                tweetlerr= [tweet.full_text for tweet in tweetler]

                sayac=0

                for j in tweetlerr:

                    sayac=sayac+1
                    d=j.split()
                    a.append(d)

            except:
                pass

            icerik2 = [{"kullanici_id":user.id,"kullanici_adi" : user.name ,"username":user.screen_name, "hakkinda" : user.description,"tweet_sayisi":user.statuses_count,"takipci_sayisi":user.followers_count,
                       "takip_edilen_sayisi":user.friends_count,"hesap_olusturma_tarihi":user.created_at,"favori_tweet_sayisi":user.favourites_count,
                       "konum_acikmi":user.geo_enabled,"onayli_hesapmi":user.verified,"armut_resimmi":user.default_profile_image,
            "takip_ediyormusun":user.following,"istekmi_gönderildi":user.follow_request_sent,"bildirimler_acikmi":user.notifications,"anahtar_kelimeler":a}]

            collection2.insert_many(icerik2)
        done = False
    except tweepy.TweepError:
                pass

while True:
    kontrol = input("Takipcileri almak için 1'i  - Takip Edilenleri Almak için 2'yi - İkisinide birlikte almak için 3'ü tuşlayıp enterlayınız...")

    if kontrol=='1':
        takipcileri_godb()
        done = True
        break
    elif kontrol=='2':
        takip_edilenler_gogb()
        done = True
        break
    elif kontrol=='3':
        takipcileri_godb()
        print("\n Takipciler alındır sıra takip edilenlerde... \n")
        takip_edilenler_gogb()
        done = True
        break
    else:
        print("Yanlış tuşlama yaptınız... Tekrar tuşlayınız ")




