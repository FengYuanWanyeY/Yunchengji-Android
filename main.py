import os
import sys
import uuid

import openpyxl
import api

# 提示文本
text1 = '{}  实际成绩：{:<7}/{:<7} 卷面成绩：{:<7}/{:<7} 班级排名：{:<3} 学校排名：{:<5} 全市排名：{:<6}'
text2 = '考生数  班级：{:<7} 学校：{:<7} 全市：{:<7}\n最高分  班级：{:<7} 学校：{:<7} 全市：{:<7}\n平均分  班级：{:<7} 学校：{:<7} 全市：{:<7}'
text3 = '题量  简单题：{:<7} 中等题：{:<7} 难题：{:<7}\n分值  简单题：{:<7} 中等题：{:<7} 难题：{:<7}\n丢分  简单题：{:<7} 中等题：{:<7} 难题：{:<7}\n得分  简单题：{:<7} 中等题：{:<7} 难题：{:<7}'
text4 = '{:<8} 得分：{:<5}/{:<5} 我的得分率：{:<7} 班得分率：{:<7} 校得分率：{:<7} 市得分率：{:<7}'

# 初始session_id生成或获取
session_id = ''
if not os.path.exists("session_id.txt"):
    session_id = uuid.uuid4()
else:
    with open("session_id.txt", "r", encoding='utf-8') as f:
        session_id = f.read()

# API对象
ycj = api.YunchengjiAPI(session_id)

def logout():
    """
    登出系统
    :return: None
    """
    print('登出中')
    content = ycj.logout()
    with open('session_id.txt', 'w+', encoding='utf-8') as f:
        f.write(content)

# 获取考试信息并打印出来
def getAndShowExamDetail(examId):
    """
    :param id 考试id
    :return: None
    """
    # 获取考试详情
    print('获取考试详情中')
    exam_detail_total = ycj.get_exam_detail_total(examId)

    # 创建excel工作表
    book = openpyxl.Workbook()
    total = book.active
    total.title = '全科'

    # 整理并保存考试详情
    examName = '{}-{}'.format(exam_detail_total['studentname'], exam_detail_total['examName'])
    output = [examName,'全科','成绩单']
    total['A1'] = '成绩单'
    total['A2'] = '科目'
    total['B2'] = '实际成绩'
    total['C2'] = '卷面成绩'
    total['D2'] = '班级排名'
    total['E2'] = '学校排名'
    total['F2'] = '全市排名'
    i = 3
    for subject in exam_detail_total['stuOrder']['subjects']:
        output.append(text1.format(subject['name'],subject['score'],subject['fullScore'],subject['paperScore'],subject['fullScore'],subject['classOrder'],subject['schoolOrder'],subject['unionOrder']))
        total['A{}'.format(i)] = subject['name']
        total['B{}'.format(i)] = '{}/{}'.format(subject['score'],subject['fullScore'])
        total['C{}'.format(i)] = '{}/{}'.format(subject['paperScore'],subject['fullScore'])
        total['D{}'.format(i)] = subject['classOrder']
        total['E{}'.format(i)] = subject['schoolOrder']
        total['F{}'.format(i)] = subject['unionOrder']
        i+=1
    i+=1
    scoreGap = exam_detail_total['stuOrder']['scoreGap']
    output.append('分数差距')
    total['A{}'.format(i)] = '分数差距'
    total['A{}'.format(i+1)] = '数据'
    total['B{}'.format(i+1)] = '班级'
    total['C{}'.format(i+1)] = '学校'
    total['D{}'.format(i+1)] = '全市'
    total['A{}'.format(i+2)] = '考生数'
    total['B{}'.format(i+2)] = scoreGap['classNum']
    total['C{}'.format(i+2)] = scoreGap['schoolNum']
    total['D{}'.format(i+2)] = scoreGap['unionNum']
    total['A{}'.format(i+3)] = '最高分'
    total['B{}'.format(i+3)] = scoreGap['classTop']
    total['C{}'.format(i+3)] = scoreGap['schoolTop']
    total['D{}'.format(i+3)] = scoreGap['unionTop']
    total['A{}'.format(i+4)] = '平均分'
    total['B{}'.format(i+4)] = scoreGap['classAvg']
    total['C{}'.format(i+4)] = scoreGap['schoolAvg']
    total['D{}'.format(i+4)] = scoreGap['unionAvg']
    output.append(text2.format(scoreGap['classNum'],scoreGap['schoolNum'],scoreGap['unionNum'],scoreGap['classTop'],scoreGap['schoolTop'],scoreGap['unionTop'],scoreGap['classAvg'],scoreGap['schoolAvg'],scoreGap['unionAvg']))
    output.append('')

    # 获取科目列表
    print('获取科目列表中')
    subject_list = ycj.get_subject_list(examId)
    for subject in subject_list:
        print('获取 {} 单科详情中'.format(subject['name']))
        output.append(subject['name'])
        sheet = book.create_sheet(subject['name'])
        # 获取数据
        subject_data = ycj.get_exam_detail_subject(examId,subject['id'])
        questions_data = ycj.get_exam_detail_subject_questions(examId,subject['id'])
        # 综合数据
        output.append('分数差距')
        scoreGap = subject_data['stuOrder']['scoreGap']
        output.append(text2.format(scoreGap['classNum'],scoreGap['schoolNum'],scoreGap['unionNum'],scoreGap['classTop'],scoreGap['schoolTop'],scoreGap['unionTop'],scoreGap['classAvg'],scoreGap['schoolAvg'],scoreGap['unionAvg']))
        sheet['A1'] = '分数差距'
        sheet['A2'] = '数据'
        sheet['B2'] = '班级'
        sheet['C2'] = '学校'
        sheet['D2'] = '全市'
        sheet['A3'] = '考生数'
        sheet['B3'] = scoreGap['classNum']
        sheet['C3'] = scoreGap['schoolNum']
        sheet['D3'] = scoreGap['unionNum']
        sheet['A4'] = '最高分'
        sheet['B4'] = scoreGap['classTop']
        sheet['C4'] = scoreGap['schoolTop']
        sheet['D4'] = scoreGap['unionTop']
        sheet['A5'] = '平均分'
        sheet['B5'] = scoreGap['classAvg']
        sheet['C5'] = scoreGap['schoolAvg']
        sheet['D5'] = scoreGap['unionAvg']
        output.append('难度失分分析')
        sheet['A7'] = '难度失分分析'
        output.append(text3.format(subject_data['loseScoreCount1'],subject_data['loseScoreCount2'],subject_data['loseScoreCount3'],subject_data['loseTotalScore1'],subject_data['loseTotalScore2'],subject_data['loseTotalScore3'],subject_data['loseScore1'],subject_data['loseScore2'],subject_data['loseScore3'],subject_data['loseTotalRateScore1'],subject_data['loseTotalRateScore2'],subject_data['loseTotalRateScore3']))
        sheet['A8'] = '数据'
        sheet['B8'] = '简单题'
        sheet['C8'] = '中等题'
        sheet['D8'] = '难题'
        sheet['A9'] = '题量'
        sheet['B9'] = subject_data['loseScoreCount1']
        sheet['C9'] = subject_data['loseScoreCount2']
        sheet['D9'] = subject_data['loseScoreCount3']
        sheet['A10'] = '分值'
        sheet['B10'] = subject_data['loseTotalScore1']
        sheet['C10'] = subject_data['loseTotalScore2']
        sheet['D10'] = subject_data['loseTotalScore3']
        sheet['A11'] = '丢分'
        sheet['B11'] = subject_data['loseScore1']
        sheet['C11'] = subject_data['loseScore2']
        sheet['D11'] = subject_data['loseScore3']
        sheet['A12'] = '得分率'
        sheet['B12'] = subject_data['loseTotalRateScore1']
        sheet['C12'] = subject_data['loseTotalRateScore2']
        sheet['D12'] = subject_data['loseTotalRateScore3']
        # 小分查询
        output.append('小分情况')
        sheet['A14'] = '小分情况'
        sheet['A15'] = '题目'
        sheet['B15'] = '得分'
        sheet['C15'] = '我的得分率'
        sheet['D15'] = '班得分率'
        sheet['E15'] = '校得分率'
        sheet['F15'] = '市得分率'
        i = 16
        for j in range(len(subject_data['questRates'])):
            output.append(text4.format(subject_data['questRates'][j]['title'],questions_data[j]['score'],questions_data[j]['totalScore'],subject_data['questRates'][j]['scoreRate'],subject_data['questRates'][j]['classScoreRate'],subject_data['questRates'][j]['schoolScoreRate'],subject_data['questRates'][j]['unionScoreRate']))
            sheet['A{}'.format(i)] = subject_data['questRates'][j]['title']
            sheet['B{}'.format(i)] = '{}/{}'.format(questions_data[j]['score'],questions_data[j]['totalScore'])
            sheet['C{}'.format(i)] = subject_data['questRates'][j]['scoreRate']
            sheet['D{}'.format(i)] = subject_data['questRates'][j]['classScoreRate']
            sheet['E{}'.format(i)] = subject_data['questRates'][j]['schoolScoreRate']
            sheet['F{}'.format(i)] = subject_data['questRates'][j]['unionScoreRate']
            i+=1
        output.append('')

    # 写入文件
    outputDir = os.path.join(os.getcwd(), "output")
    outputTxtPath = os.path.join(outputDir, "{}.txt".format(examName))
    outputXlsxPath = os.path.join(outputDir, "{}.xlsx".format(examName))
    if not os.path.exists(outputDir):
        os.mkdir(outputDir)
    with open(outputTxtPath, 'w+', encoding='utf-8') as f:
        f.write('\n'.join(output))
    book.save(outputXlsxPath)
    print('结果已保存到 {} 目录下'.format(outputDir))

# 获取用户名密码
user = input("输入手机号/用户名(按Enter键确认)：")
pw = input("输入密码(按Enter键确认)：")

# 登录
print('登录中')
login_result = ycj.login(user,pw)
if login_result == -1:
    print('用户名或密码错误')
    sys.exit(1)

# 获取考试列表
print('获取考试列表中')
exam_list = ycj.get_exam_list()
# 整理并显示考试列表
exams = []
for exam in exam_list:
    exams.append({'desc':'{} {} {} {} {}'.format(exam['studentname'], exam['date'], exam['examdesc'], exam['examtypestr'], exam['name']), 'id':exam['id']})
while True:
    print('操作列表：')
    print('[0] 退出系统')
    print('获取考试数据：')
    for i in range(len(exams)):
        print('[{}] {}'.format(i+1,exams[i]['desc']))
    print('[{}] 手动输入考试ID'.format(len(exams)+1))
    # 选择考试
    selectedExamId = 0
    try:
        selectedNumber = int(input('请输入要执行的操作的序号(按Enter键确认)：'))
        if selectedNumber == 0:
            break
        elif selectedNumber == len(exams)+1:
            selectedExamId = int(input('请输入要获取的考试的考试ID(按Enter键确认)：'))
        else:
            selectedExamId = exams[selectedNumber-1]['id']
    except ValueError:
        print('输入的不是整数')
        logout()
        sys.exit(1)
    except IndexError:
        print('不存在该选项')
        logout()
        sys.exit(1)
    getAndShowExamDetail(selectedExamId)

# 登出
logout()
