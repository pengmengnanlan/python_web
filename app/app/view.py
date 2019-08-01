import pymysql
import json
import time
import re
import os
import ctypes
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from ctypes import *

# 连接数据库
db = pymysql.connect(host='localhost', user='root',
                     password='123456', db='north', charset='utf8')
cursor = db.cursor()

# html数值参数
context = {}
# 数据库表单映射
terminal_type_dir = {'pc': 1, 'mobile': 2}
media_type_dir = {'photo': 1, 'video': 2, 'audio': 3}
algorithm_dir = {'a1': 1, 'a2': 2, 'a3': 3, 'a4': 4}
permission_dir = {'yes': 1, 'no': 0}
media_type_display_dir = {1:'图片', 2:'视频', 3:'音频'}

# 登陆
def login(request):
    # 查看是否已登录
    is_login = request.session.get('is_login')
    if is_login == 'true':
        return HttpResponseRedirect('/administrator/')
    else:
        # 获取用户列表和用户信息:验证登陆
        cursor.execute("select distinct user_name from user_info")
        user_data = cursor.fetchall()
        user_list = []
        user_dir = {}
        sql_user = "select * from user_info where user_name = %s"
        for i in user_data:
            user_list.append(i[0])
        for user in user_list:
            cursor.execute(sql_user, user)
            data = cursor.fetchone()
            user_dir[user] = {'pwd': data[2],
                              'group_id': data[3], 'user_permission': data[4]}

        error_msg = ''
        # 获取表单信息
        if request.method == 'POST':
            name = request.POST.get('name')
            pwd = request.POST.get('pwd')

            if name and pwd:
                # 密码正确
                if name in user_list and pwd == user_dir[name]['pwd']:
                    checkbox = request.POST.get('checkbox')
                    # 设置有效期
                    if checkbox == '1':
                        request.session.set_expiry(7*24*3600)
                    else:
                        # 关闭页面失效
                        request.session.set_expiry(0)

                    # 查看是否有管理员权限，有则进入管理页面
                    if user_dir[name]['group_id'] == 0:
                        request.session['is_login'] = 'true'
                        request.session['username'] = name
                        context['user_name'] = request.session.get(
                            'username', '')
                        return HttpResponseRedirect('/administrator/')
                    else:
                        error_msg = '您没有进入管理页面的权限！'
                else:
                    error_msg = '账号或密码错误！'
            else:
                error_msg = '请输入用户名和密码！'
    context['error_msg'] = error_msg
    return render(request, 'login.html', context)

# 检查登录状态
def checkStatus(request, page):
    is_login = request.session.get('is_login', '')
    name = request.session.get('username', '')
    context['user_name'] = name

    # 没有登陆则返回login页面
    if not is_login:
        return HttpResponseRedirect('/login/')
    return render(request, page, context)

# 退出登陆
def logout(request):
    try:
        del request.session['is_login']
        del request.session['username']
    except KeyError:
        pass
    return HttpResponseRedirect('/login/')

# 管理终端及用户
def admin_user(request, page):
    context['warning'] = ''
    context['error'] = ''

    # 获取所有组信息
    group_dir = {}
    sql_find_all_group = "select * from group_info"
    cursor.execute(sql_find_all_group)
    data = cursor.fetchall()
    for d in data:
        group_dir[d[0]] = d[1]
    context['group_dir'] = group_dir.items()

    # 获取所有用户信息
    user_name_list = []
    sql_find_all_user = "select user_name from user_info"
    cursor.execute(sql_find_all_user)
    data = cursor.fetchall()
    for d in data:
        user_name_list.append(d[0])

    # 获取表单信息
    if request.method == 'POST':
        data = {}
        data['terminal_type'] = terminal_type_dir[request.POST.get(
            'terminal_type')]
        data['key'] = request.POST.get('val-key')
        data['model'] = request.POST.get('val-model')
        data['mac'] = request.POST.get('val-mac')
        data['media_type'] = media_type_dir[request.POST.get('media_type')]
        data['algorithm'] = algorithm_dir[request.POST.get('algorithm')]
        username = data['username'] = request.POST.get('val-username')
        data['password'] = request.POST.get('val-password')
        data['permission'] = permission_dir[request.POST.get('permission')]
        data['group_id'] = request.POST.get('group')

        if username in user_name_list:
            context['error'] = '该用户已存在！'
            return render(request, 'admin_user.html', context)
        else:
            # 写terminal_info表
            sql_terminal = "insert into terminal_info(terminal_type, terminal_key, terminal_model, terminal_mac, media_type, algorithm) values (%s, %s, %s, %s, %s, %s);"
            cursor.execute(sql_terminal, [data['terminal_type'], data['key'],
                                          data['model'], data['mac'], data['media_type'], data['algorithm']])
            db.commit()

            # 获取新添加的terminal_id
            sql_find_terminal_id = "select terminal_id from terminal_info order by terminal_id DESC LIMIT 1"
            cursor.execute(sql_find_terminal_id)
            terminal_id = cursor.fetchone()

            # 写user_info表
            sql_user = "insert into user_info(user_name, user_password, group_id, user_permission, terminal_id) values (%s, %s, %s, %s, %s)"
            cursor.execute(sql_user, [data['username'], data['password'],
                                      data['group_id'], data['permission'], terminal_id])
            db.commit()
            context['warning'] = '您已成功创建新用户！'
    return checkStatus(request, page)

# 管理组
def admin_group(request, page):
    group_name = ''
    context['warning'] = ''

    # 获取已存在的所有组
    group_list = []
    cursor.execute("select * from group_info")
    for d in cursor.fetchall():
        group_list.append(d[1])

    if request.method == 'POST':
        # 获取新添组的名称，判断是否已存在
        group_name = request.POST.get('val-group')
        if group_name in group_list:
            context['warning'] = '该组已经存在！'
            return render(request, 'admin_group.html', context)
        else:
            # 插入数据
            sql_admin_group = "insert into group_info (group_name) values (%s)"
            cursor.execute(sql_admin_group, group_name)
            db.commit()
            context['warning'] = '您已成功创建组： ' + group_name

    return checkStatus(request, page)

# 主页面管理
def administrator(request, page):
    # 判断文件是否已读取
    context['is_click'] = []
    cursor.execute("select extract_state, task_id from task_info")
    data = cursor.fetchall()
    for d in data:
        if int(d[0]) != 0:
            context['is_click'].append(d[1])
    # 各类文件数量
    context['entracted_file_len'] = len(context['is_click'])
    context['unextracted_file_len'] = len(data) - context['entracted_file_len']
    
    # 获取所有文件
    file_list = []
    context_list = {}
    sql_find_all_files = "select * from task_info"
    cursor.execute(sql_find_all_files)
    data = cursor.fetchall()
    count = 1
    for d in data:
        file_dir = {}
        file_dir['index'] = count
        file_dir['user_id'] = d[2]
        file_dir['task_id'] = d[0]
        file_dir['media_type'] = media_type_display_dir[d[1]]
        try:
            file_dir['date'] = d[10].strftime("%Y-%m-%d %H:%M:%S")
        except AttributeError:
            file_dir['date'] = ''
        file_list.append(file_dir)
        count += 1

    for i in range(1, len(file_list)+1):
        context_list[file_list[i-1]['task_id']] = file_list[i-1].values()
    context['list'] = context_list.items()
    
    return checkStatus(request, page)

# 提取文件
def extract_file(request):
    extract_time = time.strftime("%Y-%m-%d %H:%M:%S")
    extract_id = request.GET.get('nid')
    
    # 提取参数
    if extract_id is not None:
        media_store_path = ''
        private_info = ''

        sql_extract_info = "select media_store_path, private_info from extract_info where task_id = %s order by seq_id"
        cursor.execute(sql_extract_info, extract_id)
        data = cursor.fetchall()
        for d in data:
            media_store_path += d[0]+';'
            private_info += d[1]+';'
        media_length = len(data)
        # print(media_store_path)
        # print(private_info)
        # print(media_length)

        sql_msg_file_path = "select media_name, media_store_path from extract_info where task_id = %s limit 1"
        cursor.execute(sql_msg_file_path, extract_id)
        data = cursor.fetchone()
        msg_file_path = re.sub(data[0],'',data[1])

        sql_task_info = "select media_type, file_len, key1, key2, key3 from task_info where task_id = %s"
        cursor.execute(sql_task_info, extract_id)
        data = cursor.fetchone()
        media_type = data[0]
        file_len = data[1]
        key1 = data[2]
        key2 = data[3]
        key3 = data[4]

        # 提取音频
        if media_type == 3:
            audio_status_code = extract_audio(c_char_p(media_store_path.encode('utf-8')), c_int(media_length), c_char_p(key1.encode('utf-8')), 
                                              c_char_p(key2.encode('utf-8')), c_char_p(key3.encode('utf-8')), c_char_p(private_info.encode('utf-8')), 
                                              c_char_p(msg_file_path.encode('utf-8')), c_int(file_len))
            print(audio_status_code)
            if audio_status_code == 100:
                update(extract_id, extract_time, msg_file_path)

        # 提取视频
        if media_type == 2:
            video_status_code = extract_video(c_char_p(media_store_path.encode('utf-8')), c_int(media_length), c_char_p(key3.encode('utf-8')),
                                              c_char_p(private_info.encode('utf-8')), c_char_p(msg_file_path.encode('utf-8')), c_long(file_len))
            print(video_status_code)
            if video_status_code == 0:
                update(extract_id, extract_time, msg_file_path)

        
        return HttpResponseRedirect('/administrator/')

# 更新task_info表
def update(extract_id, extract_time, msg_file_path):
    # 更新状态
    sql_update_state = "update task_info set extract_state = 1 where task_id = %s"
    cursor.execute("set SQL_SAFE_UPDATES = 0")
    cursor.execute(sql_update_state, extract_id)
    db.commit()
    # 更新时间
    sql_update_time = "update task_info set extract_date = %s where task_id = %s"
    cursor.execute("set SQL_SAFE_UPDATES = 0")
    cursor.execute(sql_update_time, [extract_time, extract_id])
    db.commit()
    # 更新文件路径
    sql_update_path = "update task_info set message_store_path = %s where task_id = %s"
    cursor.execute("set SQL_SAFE_UPDATES = 0")
    cursor.execute(sql_update_path, [msg_file_path, extract_id])
    db.commit()

# 查看文件
def check_file(request):
    check_id = request.GET.get('wid')
    if check_id is not None:
        sql_check_files = "select message_store_path from task_info where task_id = %s"
        cursor.execute(sql_check_files, check_id)
        message_store_path = cursor.fetchone()
        all_files = os.listdir(message_store_path[0])

        # 删除.wav文件
        for f in all_files:
            if f.endswith('.wav'):
                os.chdir(message_store_path[0])
                os.remove(f)
        os.startfile(message_store_path[0])

    return HttpResponseRedirect('/administrator/')

# 调用音频接口文件
def extract_audio(media_store_path, media_length, key1, key2, key3, private_info, msg_file_path, file_len):
    CUR_PATH = 'C:/Users/alina/Desktop/python_web/app/'
    audio_dllPath=os.path.join(CUR_PATH, 'AudioEmbed.dll')
    audio_dll = ctypes.WinDLL(audio_dllPath)
    audio_status_code = ctypes.c_int
    audio_status_code = audio_dll.extractAudio(media_store_path, media_length, key1, key2, 
                                               key3, private_info, msg_file_path, file_len)
    return audio_status_code

# 调用视频接口文件
def extract_video(media_store_path, media_length, key3, private_info, msg_file_path, file_len):
    CUR_PATH = 'C:/Users/alina/Desktop/python_web/app/'
    videp_dllPath=os.path.join(CUR_PATH, 'videoEmbed.dll')
    video_dll = ctypes.WinDLL(videp_dllPath)
    video_status_code = ctypes.c_int
    video_status_code = video_dll.extractSequence(media_store_path, media_length, key3, private_info, msg_file_path, file_len)
    return video_status_code

# db.close()
