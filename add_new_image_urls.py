import requests;
import json;
import pymysql;



def add_new_image_urls(proxies, name, total=25):
    # 建立数据库连接
    connection = pymysql.connect(
        host='localhost',       # MySQL 服务器主机名
        user='python-conn',        # 数据库用户名
        password='123456',    # 数据库密码
        database='seiyuu' # 要操作的数据库名
    )

    if not connection:
        return False, "数据库连接失败";

    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM users WHERE name='{}';".format(name));
    rows = cursor.fetchall();
    if len(rows)==0:
        return False, "用户不存在，请先添加用户";

    user_id=rows[0]["user_id"];
    inner_id=rows[0]["inner_id"];

    # 构造请求头字典
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0",
        "Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
        "X-Csrf-Token": "e43fdab27694d15258786b24a4654812e88006e87a0f15cd4e3b43af1957cc233098600a9a3ba00c2900ca617aa90122e0782726a173348c57946dfefe2df62908bf78c4c692f97cb73fd99e93520ac8",
        "Cookie": """auth_token=ee739cd77e2b28b5f5a133de99413bced2d27486; ct0=e43fdab27694d15258786b24a4654812e88006e87a0f15cd4e3b43af1957cc233098600a9a3ba00c2900ca617aa90122e0782726a173348c57946dfefe2df62908bf78c4c692f97cb73fd99e93520ac8;""",
    }

    tweet_cursor="";
    image_url_list=[];
    for iter in range(5):
        url="""https://x.com/i/api/graphql/Tg82Ez_kxVaJf7OPbUdbCg/UserTweets?variables={"userId":\""""+inner_id+"""\","count":20,"cursor":\""""+tweet_cursor+"""\","includePromotedContent":true,"withQuickPromoteEligibilityTweetFields":true,"withVoice":true,"withV2Timeline":true}&features={"rweb_tipjar_consumption_enabled":true,"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":false,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_timeline_navigation_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"communities_web_enable_tweet_community_results_fetch":true,"c9s_tweet_anatomy_moderator_badge_enabled":true,"articles_preview_enabled":true,"tweetypie_unmention_optimization_enabled":true,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"view_counts_everywhere_api_enabled":true,"longform_notetweets_consumption_enabled":true,"responsive_web_twitter_article_tweet_consumption_enabled":true,"tweet_awards_web_tipping_enabled":false,"creator_subscriptions_quote_tweet_preview_enabled":false,"freedom_of_speech_not_reach_fetch_enabled":true,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":true,"rweb_video_timestamps_enabled":true,"longform_notetweets_rich_text_read_enabled":true,"longform_notetweets_inline_media_enabled":true,"responsive_web_enhance_cards_enabled":false}&fieldToggles={"withArticlePlainText":false}"""

        response = requests.get(
            url=url,
            headers=headers,
            proxies=proxies,
        );

        # 打印响应结果
        if response.status_code!=200:
            # print(response.status_code)
            return False, "推文列表获取失败，请检查到X服务器的网络连接";

        table=json.loads(response.text);

        for tweet in table["data"]["user"]["result"]["timeline_v2"]["timeline"]["instructions"][-1]["entries"]:
            try:
                media_list=tweet["content"]["itemContent"]["tweet_results"]["result"]["legacy"]["entities"]["media"];
            except:
                continue;
            
            for image in media_list:
                try:
                    image_url=image["media_url_https"];
                    image_url_list.append(image_url);
                except:
                    continue;

        if len(image_url_list)>=total:
            break;

        tweet_cursor=table["data"]["user"]["result"]["timeline_v2"]["timeline"]["instructions"][-1]["entries"][-1]["content"]["value"];

    cnt=0;
    for image_url in image_url_list:
        try:
            cursor.execute("INSERT INTO images (filename, user_id, last_query_timestamp) VALUES ('{}', {}".format(image_url.split("/")[-1], user_id)+r", STR_TO_DATE('1971-01-01 00:00:00', '%Y-%m-%d %H:%i:%s'));");
            cnt+=1;
        except:
            continue;
    connection.commit();
    return True, "添加了{}的{}张新图片".format(name, cnt);



# # 构造代理服务器字典
# proxies = {
#     "http": "http://127.0.0.1:7890",
#     "https": "http://127.0.0.1:7890",
# }
# print(add_new_image_urls(proxies=proxies, name="立石凛"));