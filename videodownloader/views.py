import pyshorteners
import youtube_dl
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


def facebook_response(formats):
    download_url = {}
    download_url_audio = {}
    download_url_video = {}
    for format in formats:
        if 'height' and 'width' in format:
            if format['height'] is None and format['width'] is None:
                audio_quality = format['format'].split()
                type_tiny = pyshorteners.Shortener()
                short_url = type_tiny.tinyurl.short(format['url'])
                download_url_audio[audio_quality[2]] = short_url
        if 'quality' in format:
            type_tiny = pyshorteners.Shortener()
            short_url = type_tiny.tinyurl.short(format['url'])
            if format['format_id'] == 'sd':
                download_url_video['480'] = short_url
            elif format['format_id'] == 'hd':
                download_url_video['720'] = short_url
            else:
                download_url_video['high quality'] = short_url
    download_url['audio_urls'] = download_url_audio
    download_url['video_urls'] = download_url_video
    return download_url


def instagram_twitter_response(formats):
    download_url = {}
    download_url_audio = {}
    download_url_video = {}
    for format in formats:
        video_quality = format['format'].split()
        type_tiny = pyshorteners.Shortener()
        short_url = type_tiny.tinyurl.short(format['url'])
        download_url_video[video_quality[2]] = short_url
    download_url['audio_urls'] = download_url_audio
    download_url['video_urls'] = download_url_video
    return download_url


def youtube_response(formats):
    download_url = {}
    download_url_audio = {}
    download_url_video = {}
    for format in formats:
        if format['height'] is None and format['width'] is None:
            audio_quality = format['format'].split()
            type_tiny = pyshorteners.Shortener()
            short_url = type_tiny.tinyurl.short(format['url'])
            download_url_audio[audio_quality[0]] = short_url

        elif format['asr'] is not None and format['height'] is not None:
            video_quality = format['format'].split()
            type_tiny = pyshorteners.Shortener()
            short_url = type_tiny.tinyurl.short(format['url'])
            download_url_video[video_quality[2]] = short_url
    download_url['audio_urls'] = download_url_audio
    download_url['video_urls'] = download_url_video
    return download_url


def snack_video_response(formats):
    download_url = {}
    download_url_audio = {}
    download_url_video = {}
    for format in formats:
        type_tiny = pyshorteners.Shortener()
        short_url = type_tiny.tinyurl.short(format['url'])
        download_url_video['480'] = short_url
    download_url['audio_urls'] = download_url_audio
    download_url['video_urls'] = download_url_video
    return download_url


def url_data_fetcher(url):
    try:
        if url['extractor'] == 'facebook':
            formats = url['entries'][0]['formats']
            return facebook_response(formats)
        if url['extractor'] == 'instagram' or url['extractor'] == 'twitter':
            formats = url['formats']
            return instagram_twitter_response(formats)
        if url['extractor'] == 'youtube':
            formats = url['formats']
            return youtube_response(formats)
        if url['extractor'] == 'generic':
            formats = url['entries'][0]['formats']
            return snack_video_response(formats)
    except Exception as e:
        return Response({'Error': e}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def video_download(request):
    try:
        if request.method == 'GET':
            url = request.data.get('url')
            ydl_opts = {'nocheckcertificate': True}
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                url_response = ydl.extract_info(url, download=False)
                response = url_data_fetcher(url_response)
            return Response({'data': response}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'Error': e}, status=status.HTTP_400_BAD_REQUEST)