import requests;
import json;
import pymysql;



def add_user(proxies, name, x_id):
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

    cursor.execute("SELECT * FROM users WHERE name='{}';".format(name));
    rows = cursor.fetchall();
    if len(rows)!=0:
        return False, "用户已存在";

    # 构造请求头字典
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0",
        "Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
        "X-Csrf-Token": "e43fdab27694d15258786b24a4654812e88006e87a0f15cd4e3b43af1957cc233098600a9a3ba00c2900ca617aa90122e0782726a173348c57946dfefe2df62908bf78c4c692f97cb73fd99e93520ac8",
        "Cookie": """auth_token=ee739cd77e2b28b5f5a133de99413bced2d27486; ct0=e43fdab27694d15258786b24a4654812e88006e87a0f15cd4e3b43af1957cc233098600a9a3ba00c2900ca617aa90122e0782726a173348c57946dfefe2df62908bf78c4c692f97cb73fd99e93520ac8;""",
    }

    url="""https://x.com/i/api/graphql/BQ6xjFU6Mgm-WhEP3OiT9w/UserByScreenName?variables={"screen_name":\""""+x_id+"""","withSafetyModeUserFields":true}&features={"hidden_profile_subscriptions_enabled":true,"rweb_tipjar_consumption_enabled":true,"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":false,"subscriptions_verification_info_is_identity_verified_enabled":true,"subscriptions_verification_info_verified_since_enabled":true,"highlights_tweets_tab_ui_enabled":true,"responsive_web_twitter_article_notes_tab_enabled":true,"subscriptions_feature_can_gift_premium":false,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"responsive_web_graphql_timeline_navigation_enabled":true}&fieldToggles={"withAuxiliaryUserLabels":false}""";

    response = requests.get(
        url=url,
        headers=headers,
        proxies=proxies,
    );

    # 打印响应结果
    if response.status_code!=200:
        return False, "用户信息获取失败，请检查到X服务器的网络连接";

    table=json.loads(response.text);
    try:
        inner_id=table["data"]["user"]["result"]["rest_id"];
    except:
        return False, "用户ID不存在";

    cursor.execute("INSERT INTO users (name, inner_id) VALUES ('{}', '{}');".format(name, inner_id));
    connection.commit();

    return True, "";

# # 构造代理服务器字典
# proxies = {
#     "http": "http://127.0.0.1:7890",
#     "https": "http://127.0.0.1:7890",
# }
# print(add_user(proxies=proxies, name="立石凛", id="ttisrn_0710"));



