import pymysql;
import requests;



def download_image(proxies, filename):
    headers={
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0",
    };

    url="https://pbs.twimg.com/media/"+filename;
    r=requests.get(url=url, headers=headers, proxies=proxies);

    if(r.status_code!=200):
        False, "图片{}下载失败，请检查文件名的正确性与X的网络连接".format(filename);
    
    with open("img/"+filename, mode="wb") as f:
        f.write(r.content);

    return True, "";

def select_one_image(proxies, name):
    # 建立数据库连接
    connection = pymysql.connect(
        host='localhost',       # MySQL 服务器主机名
        user='python-conn',        # 数据库用户名
        password='123456',    # 数据库密码
        database='seiyuu' # 要操作的数据库名
    )

    if not connection:
        return False, "数据库连接失败";

    cursor = connection.cursor()
    cursor.execute("SELECT user_id FROM users WHERE name='{}';".format(name));
    rows = cursor.fetchall();
    if len(rows)==0:
        return False, "用户不存在，请先添加用户";
    user_id=rows[0][0];

    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM images WHERE user_id='{}';".format(user_id));
    rows = cursor.fetchall();

    if len(rows)==0:
        return False, "用户{}的图库为空".format(name);

    timestamp_list=[];
    for row in rows:
        timestamp_list.append(row["last_query_timestamp"]);
    # min_timestamp=min(timestamp_list);
    idx=timestamp_list.index(min(timestamp_list));
    filename=rows[idx]["filename"];
    downloaded=rows[idx]["downloaded"];
    cursor.execute("UPDATE images SET last_query_timestamp=CURRENT_TIMESTAMP WHERE filename='{}'".format(filename));
    connection.commit();

    if not downloaded:
        status, message=download_image(proxies, filename);
        if status is False:
            return False, message;

    return True, filename;




# proxies = {
#     "http": "http://127.0.0.1:7890",
#     "https": "http://127.0.0.1:7890",
# }
# print(select_one_image(proxies, name="立石凛"));