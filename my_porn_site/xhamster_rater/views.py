# coding:utf-8
from django.http import HttpResponse
from django.shortcuts import render
from util import pgdb
import string


def index(request):
    return HttpResponse(u"It works.")


def get_randomly(request):
    conn = pgdb.genSQLConnection()
    try:
        pgdb.rateVideo(conn,
           string.atoi(request.GET['id']),
           string.atof(request.GET['rate']))
    except Exception, e:
        print "Error", e.message
    search_result = pgdb.queryRandomUnratedVideo(conn)
    return render(request, "rand_rate.html", search_result)
    
def get_recommend(request):
    conn = pgdb.genSQLConnection()
    try:
        pgdb.rateVideo(conn,
           string.atoi(request.GET['id']),
           string.atof(request.GET['rate']))
    except Exception, e:
        print "Error", e.message
    search_result = pgdb.queryRecommandUnratedVideo(conn)
    return render(request, "rand_rate.html", search_result)