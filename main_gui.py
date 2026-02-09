import os
import uuid
import threading
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.properties import StringProperty, NumericProperty, ListProperty
import openpyxl
import api

Window.size = (360, 640)

class ColoredButton(Button):
    background_color = ListProperty([0.2, 0.6, 1, 1])
    
    def __init__(self, **kwargs):
        super(ColoredButton, self).__init__(**kwargs)
        self.color = (1, 1, 1, 1)
        self.font_size = '16sp'
        self.size_hint_y = None
        self.height = dp(50)
        self.bold = True

class ColoredLabel(Label):
    def __init__(self, **kwargs):
        super(ColoredLabel, self).__init__(**kwargs)
        self.color = (0.2, 0.2, 0.2, 1)
        self.font_size = '14sp'
        self.halign = 'left'
        self.valign = 'top'
        self.text_size = (None, None)
        self.markup = True

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.name = 'login'
        
        main_layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20))
        main_layout.bind(size=self._update_rect, pos=self._update_rect)
        
        with main_layout.canvas.before:
            self.bg_color = Color(0.95, 0.97, 1, 1)
            self.rect = Rectangle(size=main_layout.size, pos=main_layout.pos)
        
        title_label = Label(
            text='[color=#1a5fb4][b]云成绩查询[/b][/color]',
            font_size='32sp',
            markup=True,
            size_hint_y=None,
            height=dp(80)
        )
        
        input_layout = BoxLayout(orientation='vertical', spacing=dp(15), size_hint_y=None, height=dp(200))
        input_layout.bind(size=self._update_input_rect, pos=self._update_input_rect)
        
        with input_layout.canvas.before:
            Color(1, 1, 1, 1)
            self.input_rect = RoundedRectangle(size=input_layout.size, pos=input_layout.pos, radius=[dp(10)])
        
        username_label = ColoredLabel(text='手机号/用户名', size_hint_y=None, height=dp(30))
        self.username_input = TextInput(
            multiline=False,
            size_hint_y=None,
            height=dp(50),
            font_size='16sp',
            background_color=(0.95, 0.97, 1, 1)
        )
        
        password_label = ColoredLabel(text='密码', size_hint_y=None, height=dp(30))
        self.password_input = TextInput(
            multiline=False,
            password=True,
            size_hint_y=None,
            height=dp(50),
            font_size='16sp',
            background_color=(0.95, 0.97, 1, 1)
        )
        
        input_layout.add_widget(username_label)
        input_layout.add_widget(self.username_input)
        input_layout.add_widget(password_label)
        input_layout.add_widget(self.password_input)
        
        self.login_button = ColoredButton(
            text='登录',
            background_color=[0.1, 0.5, 0.9, 1],
            size_hint_y=None,
            height=dp(55)
        )
        self.login_button.bind(on_press=self.login)
        
        self.status_label = ColoredLabel(
            text='',
            size_hint_y=None,
            height=dp(30),
            halign='center'
        )
        
        main_layout.add_widget(title_label)
        main_layout.add_widget(input_layout)
        main_layout.add_widget(self.login_button)
        main_layout.add_widget(self.status_label)
        
        self.add_widget(main_layout)
        
        self.session_id = ''
        if not os.path.exists("session_id.txt"):
            self.session_id = str(uuid.uuid4())
        else:
            with open("session_id.txt", "r", encoding='utf-8') as f:
                self.session_id = f.read()
        
        self.ycj = api.YunchengjiAPI(self.session_id)
    
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    
    def _update_input_rect(self, instance, value):
        self.input_rect.pos = instance.pos
        self.input_rect.size = instance.size
    
    def login(self, instance):
        username = self.username_input.text.strip()
        password = self.password_input.text.strip()
        
        if not username or not password:
            self.status_label.text = '[color=#e74c3c]请输入用户名和密码[/color]'
            return
        
        self.status_label.text = '[color=#3498db]登录中...[/color]'
        self.login_button.disabled = True
        
        thread = threading.Thread(target=self._login_thread, args=(username, password))
        thread.daemon = True
        thread.start()
    
    def _login_thread(self, username, password):
        login_result = self.ycj.login(username, password)
        
        Clock.schedule_once(lambda dt: self._login_complete(login_result), 0)
    
    def _login_complete(self, result):
        if result == -1:
            self.status_label.text = '[color=#e74c3c]用户名或密码错误[/color]'
            self.login_button.disabled = False
        else:
            exam_list = self.ycj.get_exam_list()
            if exam_list == -1:
                self.status_label.text = '[color=#e74c3c]获取考试列表失败[/color]'
                self.login_button.disabled = False
            else:
                app = App.get_running_app()
                app.exam_list = exam_list
                app.ycj = self.ycj
                self.manager.current = 'exam_list'

class ExamListScreen(Screen):
    def __init__(self, **kwargs):
        super(ExamListScreen, self).__init__(**kwargs)
        self.name = 'exam_list'
        
        main_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        main_layout.bind(size=self._update_rect, pos=self._update_rect)
        
        with main_layout.canvas.before:
            self.bg_color = Color(0.95, 0.97, 1, 1)
            self.rect = Rectangle(size=main_layout.size, pos=main_layout.pos)
        
        header_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(60), spacing=dp(10))
        
        title_label = Label(
            text='[color=#1a5fb4][b]考试列表[/b][/color]',
            font_size='24sp',
            markup=True,
            size_hint_x=0.7
        )
        
        self.back_button = ColoredButton(
            text='退出',
            background_color=[0.9, 0.3, 0.3, 1],
            size_hint_x=0.3,
            height=dp(50)
        )
        self.back_button.bind(on_press=self.logout)
        
        header_layout.add_widget(title_label)
        header_layout.add_widget(self.back_button)
        
        scroll = ScrollView(size_hint=(1, 1))
        self.exam_layout = BoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=None)
        self.exam_layout.bind(minimum_height=self.exam_layout.setter('height'))
        scroll.add_widget(self.exam_layout)
        
        main_layout.add_widget(header_layout)
        main_layout.add_widget(scroll)
        
        self.add_widget(main_layout)
    
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    
    def on_enter(self):
        self.exam_layout.clear_widgets()
        app = App.get_running_app()
        
        for exam in app.exam_list:
            exam_desc = '{} {} {} {}'.format(
                exam['studentname'], 
                exam['date'], 
                exam['examdesc'], 
                exam['examtypestr']
            )
            
            exam_card = BoxLayout(
                orientation='vertical',
                size_hint_y=None,
                height=dp(100),
                padding=dp(15),
                spacing=dp(5)
            )
            exam_card.bind(size=self._update_card_rect, pos=self._update_card_rect)
            
            with exam_card.canvas.before:
                Color(1, 1, 1, 1)
                card_rect = RoundedRectangle(size=exam_card.size, pos=exam_card.pos, radius=[dp(8)])
            
            name_label = ColoredLabel(
                text='[b]{}[/b]'.format(exam['name']),
                font_size='18sp',
                size_hint_y=None,
                height=dp(30)
            )
            
            desc_label = ColoredLabel(
                text=exam_desc,
                font_size='12sp',
                size_hint_y=None,
                height=dp(40),
                color=(0.5, 0.5, 0.5, 1)
            )
            
            view_button = ColoredButton(
                text='查看详情',
                background_color=[0.2, 0.7, 0.3, 1],
                size_hint_y=None,
                height=dp(40)
            )
            view_button.bind(on_press=lambda instance, eid=exam['id']: self.view_exam(eid))
            
            exam_card.add_widget(name_label)
            exam_card.add_widget(desc_label)
            exam_card.add_widget(view_button)
            
            self.exam_layout.add_widget(exam_card)
    
    def _update_card_rect(self, instance, value):
        instance.canvas.before.children[0].pos = instance.pos
        instance.canvas.before.children[0].size = instance.size
    
    def view_exam(self, exam_id):
        app = App.get_running_app()
        app.current_exam_id = exam_id
        self.manager.current = 'exam_detail'
    
    def logout(self, instance):
        app = App.get_running_app()
        session_id = app.ycj.logout()
        with open('session_id.txt', 'w+', encoding='utf-8') as f:
            f.write(session_id)
        self.manager.current = 'login'

class ExamDetailScreen(Screen):
    def __init__(self, **kwargs):
        super(ExamDetailScreen, self).__init__(**kwargs)
        self.name = 'exam_detail'
        
        main_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        main_layout.bind(size=self._update_rect, pos=self._update_rect)
        
        with main_layout.canvas.before:
            self.bg_color = Color(0.95, 0.97, 1, 1)
            self.rect = Rectangle(size=main_layout.size, pos=main_layout.pos)
        
        header_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(60), spacing=dp(10))
        
        self.back_button = ColoredButton(
            text='返回',
            background_color=[0.6, 0.6, 0.6, 1],
            size_hint_x=0.3,
            height=dp(50)
        )
        self.back_button.bind(on_press=self.go_back)
        
        self.export_button = ColoredButton(
            text='导出Excel',
            background_color=[0.2, 0.6, 1, 1],
            size_hint_x=0.7,
            height=dp(50)
        )
        self.export_button.bind(on_press=self.export_data)
        
        header_layout.add_widget(self.back_button)
        header_layout.add_widget(self.export_button)
        
        scroll = ScrollView(size_hint=(1, 1))
        self.content_layout = BoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=None, padding=dp(10))
        self.content_layout.bind(minimum_height=self.content_layout.setter('height'))
        scroll.add_widget(self.content_layout)
        
        main_layout.add_widget(header_layout)
        main_layout.add_widget(scroll)
        
        self.add_widget(main_layout)
    
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    
    def on_enter(self):
        self.content_layout.clear_widgets()
        app = App.get_running_app()
        
        thread = threading.Thread(target=self._load_data)
        thread.daemon = True
        thread.start()
    
    def _load_data(self):
        app = App.get_running_app()
        exam_id = app.current_exam_id
        
        Clock.schedule_once(lambda dt: self._show_loading(), 0)
        
        exam_detail_total = app.ycj.get_exam_detail_total(exam_id)
        subject_list = app.ycj.get_subject_list(exam_id)
        
        Clock.schedule_once(lambda dt: self._display_data(exam_detail_total, subject_list), 0)
    
    def _show_loading(self):
        self.content_layout.clear_widgets()
        loading_label = Label(
            text='加载中...',
            font_size='18sp',
            size_hint_y=None,
            height=dp(50)
        )
        self.content_layout.add_widget(loading_label)
    
    def _display_data(self, exam_detail_total, subject_list):
        self.content_layout.clear_widgets()
        
        exam_name = '{}-{}'.format(exam_detail_total['studentname'], exam_detail_total['examName'])
        
        name_card = self._create_card(exam_name, '#1a5fb4', dp(60))
        self.content_layout.add_widget(name_card)
        
        subjects_card = self._create_card('各科成绩', '#2ecc71', dp(30))
        subjects_content = self._create_subjects_table(exam_detail_total['stuOrder']['subjects'])
        subjects_card.add_widget(subjects_content)
        self.content_layout.add_widget(subjects_card)
        
        score_gap = exam_detail_total['stuOrder']['scoreGap']
        gap_text = '考生数: 班级{} 学校{} 全市{}\n最高分: 班级{} 学校{} 全市{}\n平均分: 班级{} 学校{} 全市{}'.format(
            score_gap['classNum'], score_gap['schoolNum'], score_gap['unionNum'],
            score_gap['classTop'], score_gap['schoolTop'], score_gap['unionTop'],
            score_gap['classAvg'], score_gap['schoolAvg'], score_gap['unionAvg']
        )
        gap_card = self._create_card('分数差距', '#e67e22', dp(30))
        gap_label = ColoredLabel(text=gap_text, size_hint_y=None, height=dp(100))
        gap_card.add_widget(gap_label)
        self.content_layout.add_widget(gap_card)
        
        app = App.get_running_app()
        app.exam_detail_total = exam_detail_total
        app.subject_list = subject_list
    
    def _create_card(self, title, color, title_height):
        card = BoxLayout(orientation='vertical', size_hint_y=None, padding=dp(10), spacing=dp(10))
        
        title_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=title_height)
        title_label = Label(
            text='[color={}][b]{}[/b][/color]'.format(color, title),
            font_size='18sp',
            markup=True,
            halign='left'
        )
        title_layout.add_widget(title_label)
        
        card.add_widget(title_layout)
        
        with card.canvas.before:
            Color(1, 1, 1, 1)
            card_rect = RoundedRectangle(size=card.size, pos=card.pos, radius=[dp(8)])
        
        card.bind(size=self._update_card_rect, pos=self._update_card_rect)
        card.card_rect = card_rect
        
        return card
    
    def _update_card_rect(self, instance, value):
        instance.card_rect.pos = instance.pos
        instance.card_rect.size = instance.size
    
    def _create_subjects_table(self, subjects):
        table_layout = BoxLayout(orientation='vertical', spacing=dp(5))
        
        for subject in subjects:
            row = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(70), spacing=dp(5))
            
            name_label = ColoredLabel(
                text='[b]{}[/b]'.format(subject['name']),
                size_hint_x=0.3,
                font_size='16sp'
            )
            
            info_text = '实际: {}/{}\n卷面: {}/{}\n班级: {} 学校: {} 全市: {}'.format(
                subject['score'], subject['fullScore'],
                subject['paperScore'], subject['fullScore'],
                subject['classOrder'], subject['schoolOrder'], subject['unionOrder']
            )
            
            info_label = ColoredLabel(
                text=info_text,
                size_hint_x=0.7,
                font_size='12sp'
            )
            
            row.add_widget(name_label)
            row.add_widget(info_label)
            
            table_layout.add_widget(row)
        
        return table_layout
    
    def export_data(self, instance):
        popup = Popup(
            title='导出中',
            content=Label(text='正在导出数据到Excel...'),
            size_hint=(0.8, 0.3)
        )
        popup.open()
        
        thread = threading.Thread(target=self._export_thread, args=(popup,))
        thread.daemon = True
        thread.start()
    
    def _export_thread(self, popup):
        app = App.get_running_app()
        exam_id = app.current_exam_id
        exam_detail_total = app.exam_detail_total
        subject_list = app.subject_list
        
        book = openpyxl.Workbook()
        total = book.active
        total.title = '全科'
        
        examName = '{}-{}'.format(exam_detail_total['studentname'], exam_detail_total['examName'])
        
        total['A1'] = '成绩单'
        total['A2'] = '科目'
        total['B2'] = '实际成绩'
        total['C2'] = '卷面成绩'
        total['D2'] = '班级排名'
        total['E2'] = '学校排名'
        total['F2'] = '全市排名'
        
        i = 3
        for subject in exam_detail_total['stuOrder']['subjects']:
            total['A{}'.format(i)] = subject['name']
            total['B{}'.format(i)] = '{}/{}'.format(subject['score'], subject['fullScore'])
            total['C{}'.format(i)] = '{}/{}'.format(subject['paperScore'], subject['fullScore'])
            total['D{}'.format(i)] = subject['classOrder']
            total['E{}'.format(i)] = subject['schoolOrder']
            total['F{}'.format(i)] = subject['unionOrder']
            i += 1
        
        i += 1
        scoreGap = exam_detail_total['stuOrder']['scoreGap']
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
        
        for subject in subject_list:
            sheet = book.create_sheet(subject['name'])
            
            subject_data = app.ycj.get_exam_detail_subject(exam_id, subject['id'])
            questions_data = app.ycj.get_exam_detail_subject_questions(exam_id, subject['id'])
            
            scoreGap = subject_data['stuOrder']['scoreGap']
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
            
            sheet['A7'] = '难度失分分析'
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
            
            sheet['A14'] = '小分情况'
            sheet['A15'] = '题目'
            sheet['B15'] = '得分'
            sheet['C15'] = '我的得分率'
            sheet['D15'] = '班得分率'
            sheet['E15'] = '校得分率'
            sheet['F15'] = '市得分率'
            
            j = 16
            for k in range(len(subject_data['questRates'])):
                sheet['A{}'.format(j)] = subject_data['questRates'][k]['title']
                sheet['B{}'.format(j)] = '{}/{}'.format(questions_data[k]['score'], questions_data[k]['totalScore'])
                sheet['C{}'.format(j)] = subject_data['questRates'][k]['scoreRate']
                sheet['D{}'.format(j)] = subject_data['questRates'][k]['classScoreRate']
                sheet['E{}'.format(j)] = subject_data['questRates'][k]['schoolScoreRate']
                sheet['F{}'.format(j)] = subject_data['questRates'][k]['unionScoreRate']
                j += 1
        
        outputDir = os.path.join(os.getcwd(), "output")
        outputXlsxPath = os.path.join(outputDir, "{}.xlsx".format(examName))
        if not os.path.exists(outputDir):
            os.mkdir(outputDir)
        book.save(outputXlsxPath)
        
        Clock.schedule_once(lambda dt: self._export_complete(popup, outputXlsxPath), 0)
    
    def _export_complete(self, popup, path):
        popup.dismiss()
        
        success_popup = Popup(
            title='导出成功',
            content=Label(text='文件已保存到:\n{}'.format(path)),
            size_hint=(0.9, 0.4)
        )
        success_popup.open()
    
    def go_back(self, instance):
        self.manager.current = 'exam_list'

class YunchengjiApp(App):
    def build(self):
        self.title = '云成绩查询'
        sm = ScreenManager()
        sm.add_widget(LoginScreen())
        sm.add_widget(ExamListScreen())
        sm.add_widget(ExamDetailScreen())
        return sm
    
    def on_stop(self):
        pass

if __name__ == '__main__':
    YunchengjiApp().run()
