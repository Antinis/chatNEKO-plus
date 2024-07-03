import requests;
from flask import Flask;
from flask import request as fr;

from add_user import add_user;
from add_new_image_urls import add_new_image_urls;
from select_one_image import select_one_image;



app = Flask(__name__)

# 构造代理服务器字典
proxies = {
    "http": "http://127.0.0.1:7890",
    "https": "http://127.0.0.1:7890",
}

service_group_list=[
    92133655,
    519251361,
    908810214,
];



def send_manual(group_id):
    requests.get("http://127.0.0.1:3000/send_group_msg?group_id={}&message={}".format(group_id, 
            "这里是chatNEKO，快来跟我玩喵~\n\n\n" +
            "使用方法：\n\n" + 
            "发图：\n\"@chatNEKO 人物姓名\"\n\n" +
            "添加用户：\n\"@chatNEKO adduser 姓名 X_ID\"\n\n"+
            "更新图库：\n\"@chatNEKO refresh 姓名\"\n\"@chatNEKO refresh 姓名 新加图片最大数量\"，\n缺省25张，可能无法满足此数量\n\n\n"+
            "请注意，\"@chatNEKO\"标识符只有在手动键盘输入并选择用户时才能生效。直接从剪贴板粘贴\"@chatNEKO\"无效。同时@自带空格，无需手动输入。\n\n\n" + 
            "Github项目地址为 https://github.com/Antinis/chatNEKO 希望更多功能或建议请联系作者Antinis zhangyunxuan@zju.edu.cn\n\n\n快来跟我玩喵~")
        );

    return;

def service_loop(group_id: int, message: str):
    if (message[0]["type"]!="at"):
        return;

    if (message[0]["data"]["qq"]!="3105925657"):
        return;

    if (len(message)==1):
        send_manual(group_id=group_id);
        return;

    if (message[1]["type"]!="text"):
        send_manual(group_id=group_id);
        return;



    cmd=message[1]["data"]["text"].split(" ")[1: ];

    if cmd[0]=="adduser":
        if len(cmd)!=3:
            requests.get("http://127.0.0.1:3000/send_group_msg?group_id={}&message={}".format(group_id, "添加用户命令格式错误\n\"adduser 姓名 X_ID\""));
            return;
        
        name=cmd[1];
        x_id=cmd[2];

        status, msg=add_user(proxies=proxies, name=name, x_id=x_id);

        if status is False:
            requests.get("http://127.0.0.1:3000/send_group_msg?group_id={}&message={}".format(group_id, "错误，"+msg));
        else:
            requests.get("http://127.0.0.1:3000/send_group_msg?group_id={}&message={}".format(group_id, "用户{}添加成功".format(name)));

        return;

    if cmd[0]=="refresh":
        if (len(cmd)!=3) and (len(cmd)!=2):
            requests.get("http://127.0.0.1:3000/send_group_msg?group_id={}&message={}".format(group_id, "更新图库命令格式错误\n\"refresh 姓名\"\n\"@chatNEKO refresh 姓名 新加图片最大数量\"，\n缺省25张，可能无法满足此数量"));
            return;
        
        requests.get("http://127.0.0.1:3000/send_group_msg?group_id={}&message={}".format(group_id, "更新图库耗时较长，请耐心等待"));

        if len(cmd)==3:
            name=cmd[1];
            try:
                num=int(cmd[2]);
            except:
                requests.get("http://127.0.0.1:3000/send_group_msg?group_id={}&message={}".format(group_id, "错误，请输入正确的数值"));
                return;
            if num<=0:
                requests.get("http://127.0.0.1:3000/send_group_msg?group_id={}&message={}".format(group_id, "错误，请输入正确的数值"));
                return;
            status, msg=add_new_image_urls(proxies=proxies, name=name, total=num);
        
        if len(cmd)==2:
            name=cmd[1];
            status, msg=add_new_image_urls(proxies=proxies, name=name);

        if status is False:
            requests.get("http://127.0.0.1:3000/send_group_msg?group_id={}&message={}".format(group_id, "错误，"+msg));
        else:
            requests.get("http://127.0.0.1:3000/send_group_msg?group_id={}&message={}".format(group_id, "刷新成功，"+msg));

        return;
    
    if len(cmd)==1:
        status, msg=select_one_image(proxies=proxies, name=cmd[0]);
        if status is False:
            requests.get("http://127.0.0.1:3000/send_group_msg?group_id={}&message={}".format(group_id, "错误，"+msg));
        else:
            filename=msg;
            requests.get("http://127.0.0.1:3000/send_group_msg?group_id={}&message=[CQ:image,file={},id=40000]".format(group_id, "file:///home/kuroneko/service/qq-bot/img/{}".format(filename)));

        return;



    send_manual(group_id=group_id);

    return;



# 监听端口，获取QQ信息
@app.route('/', methods=["POST"])
def handle():
    message_type=fr.get_json()["message_type"];
    if message_type!="group":
        return "Needless";

    group_id=fr.get_json()["group_id"];
    if group_id not in service_group_list:
        return "Needless";

    message=fr.get_json()["message"];
    service_loop(group_id=group_id, message=message);

    return "Processed";



if __name__=="__main__":
    app.run(debug=False, host='127.0.0.1', port=3001);
