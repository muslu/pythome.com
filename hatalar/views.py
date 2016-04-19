# -*- coding: utf-8 -*-
import MySQLdb
import logging
import subprocess
import sys

import memcache
from django_jinja.builtins.filters import slugify

reload(sys)
sys.setdefaultencoding('utf-8')

from django.shortcuts import render

memc = memcache.Client(['127.0.0.1:11211'], debug=1)

conn = MySQLdb.connect(host="localhost", user="muslu", passwd="CeMMec+6", db="HataBull", charset="utf8", use_unicode=True)
cursor = conn.cursor()
dcursor = conn.cursor(MySQLdb.cursors.DictCursor)


# @cache_page(60 * 15)
def detaygoster(request, modul, tur, slug):
    CacheDetay = memc.get(slug.encode('utf8'))

    if not CacheDetay:
        dcursor.execute("select * from Hatalar where Slug = '" + slug + "'")
        CacheDetay = dcursor.fetchone()

        dcursor.execute("select * from Hatalar where HataTuru = '" + CacheDetay['HataTuru'] + "'")
        CacheHataTuruDetay = dcursor.fetchall()

        memc.set(slug.encode('utf8'), CacheDetay, 6000)
        # logging.info("Updated memcached with MySQL data")

    else:
        CacheHataTuruDetay = {}
    # logging.info("Loaded data from memcached")

    return render(request, 'detay.html', {'kayitlar': CacheDetay, 'hataturayni': CacheHataTuruDetay})


#
# def anasayfa(request):
#     return render(request, 'index.html')
#



def anasayfa(request):
    ArananHata = request.GET.get('h', '')
    ArananHataTuru = request.GET.get('ht', '')

    Aranan = ArananHata + ArananHataTuru

    if ArananHata != "":
        CacheEk = "h"

    if ArananHataTuru != "":
        CacheEk = "ht"

    if Aranan != "":

        slugi = slugify(Aranan + "__" + CacheEk)

        CacheKayitlar = memc.get(slugi.encode('utf8'))

        if not CacheKayitlar:

            if ArananHata:
                cursor.execute(
                    "select * from Hatalar where HataEng like '%" + ArananHata.encode(
                        'utf8') + "%' order by Modul, HataTuru, SatirSayisi")

            if ArananHataTuru:
                cursor.execute(
                    "select * from Hatalar where HataTuru = '" + ArananHataTuru.encode(
                        'utf8') + "' order by Modul, HataTuru, SatirSayisi")

            CacheKayitlar = cursor.fetchall()

            memc.set(slugi.encode('utf8'), CacheKayitlar, 60)
            # logging.info("Updated memcached with MySQL data")

        else:
            # logging.info("Loaded data from memcached")
            pass

        return render(request, 'sorgu.html', {'kayitlar': CacheKayitlar, 'title': Aranan})

    else:

        CacheKayitlar = memc.get("tumu".encode('utf8'))

        if not CacheKayitlar:
            cursor.execute("select * from Hatalar order by Modul, HataTuru, SatirSayisi")
            CacheKayitlar = cursor.fetchall()
            memc.set("tumu".encode('utf8'), CacheKayitlar, 6000)

            dcursor.execute("select * from Hatalar order by Modul, HataTuru, SatirSayisi", )
            HataArama = dcursor.fetchall()

        else:
            HataArama = {}

    return render(request, 'sorgu.html', {'kayitlar': CacheKayitlar, 'title': Aranan, 'hataarama':HataArama,})




def hatabul(request):
    HataBul = 'Error("'

    Hatalar = subprocess.check_output("grep --include=*.py -inR '" + HataBul + "' /usr/local/lib/python2.7/",
                                      shell=True).splitlines()

    for kk in Hatalar:

        if kk != "":

            DosyaAdi = str(kk).split(":")[0].strip()
            Satir = str(kk).split(":")[1].strip()
            Hata = str(kk).split(":")[2].strip()

            SonrakiSatir = ""
            TopluHata = ""

            if Hata.endswith('")') or Hata.endswith(")"):
                TopluHata = Hata.strip()
            else:
                SonrakiSatir = subprocess.check_output("sed -n " + "'" + str(int(Satir) + 1) + "'p " + DosyaAdi,
                                                       shell=True)
                if SonrakiSatir.strip().endswith(')'):
                    TopluHata += Hata.strip() + SonrakiSatir.strip()
                else:
                    SonrakiSatirr = subprocess.check_output("sed -n " + "'" + str(int(Satir) + 2) + "'p " + DosyaAdi,
                                                            shell=True)
                    if SonrakiSatirr.strip().endswith(')'):
                        TopluHata += Hata.strip() + SonrakiSatir.strip() + SonrakiSatirr.strip()

            HataTuru = Hata.split("(")[0].replace("raise ", "")

            # try:

            HataFull = TopluHata.replace("'", "")

            if HataFull != "":
                HataEng = HataFull.replace("raise ", "").replace(HataTuru, '')
                Slug = slugify(HataEng)

                # logging.info(DosyaAdi + " " + Satir + " " + HataFull)

                Modul = DosyaAdi.replace('/usr/local/lib/python2.7/dist-packages/', '').split('/')[0].title()

                cursor.execute(
                    "INSERT INTO Hatalar (Dosyayolu, SatirSayisi, Modul, HataTuru, HataFull, HataEng, Aciklama, Slug) VALUES ('" + DosyaAdi + "', '" + str(
                        Satir) + "', '" + Modul + "', '" + HataTuru + "', '" + HataFull + "', '" + HataEng + "', '', '" + Slug + "');")
                conn.commit()

                # except:
                #     HataFull = ""

    conn.close()

# # @cache_page (60 * 15)
# def anasayfa(request):
#     # cache.delete('/')
#     return render(request, 'sorgu.html', {'title': 'Ana Sayfa'})
