# coding:utf-8
import psycopg2


def genSQLConnection():
    return psycopg2.connect(
        database="pvideo",
        user="postgres",
        password="979323",
        host="localhost",
        port="5432")


def time2duration(time_secs):
    time_secs = int(time_secs)
    if time_secs<60:
        return "%d(s)" % time_secs
    elif time_secs<3600:
        return "%02d:%02d" % (time_secs/60,time_secs%60)
    else:
        h = time_secs / 3600
        m = (time_secs - 3600*h) /60
        return "%d:%02d:%02d" % (h, m, time_secs % 60)

        
def queryRandomUnratedVideo(sql_connection):
    cur = sql_connection.cursor()
    sql_cmd = "select id, title, img_urls, categories, video_time " \
              "from xhamster_spider where myrate is null order by random() limit 1 offset 0"
    cur.execute(sql_cmd)
    res = cur.fetchall()
    cur.close()
    if len(res) == 0:  # Can't find info
        raise Exception("Can't find log in database.")
    else:
        res = res[0]
        result = {
            "id": res[0],
            "title": res[1].replace("`", "'"),
            "img_urls": res[2],
            "categories": res[3],
            "video_time": time2duration(res[4])
        }
    return result

def queryRecommandUnratedVideo(sql_connection):
    cur = sql_connection.cursor()
    sql_cmd = "select id, title, img_urls, categories, video_time " \
              "from xhamster_spider where myrate is null order by recommand_info limit 1 offset 0"
    cur.execute(sql_cmd)
    res = cur.fetchall()
    cur.close()
    if len(res) == 0:  # Can't find info
        raise Exception("Can't find log in database.")
    else:
        res = res[0]
        result = {
            "id": res[0],
            "title": res[1].replace("`", "'"),
            "img_urls": res[2],
            "categories": res[3],
            "video_time": time2duration(res[4])
        }
    return result
    
def rateVideo(sql_connection, id, rate):
    sql_cmd = "UPDATE xhamster_spider SET myrate=%f WHERE id=%d" %  (rate, id)
    cur = sql_connection.cursor()
    cur.execute(sql_cmd)
    sql_connection.commit()
    cur.close()

    
def test():
    conn = genSQLConnection()
    print queryRandomUnratedVideo(conn)
    rateVideo(conn, 6329497, -2)
    conn.close()

if __name__ == "__main__":
    test()
