"""内置示例课程内容与成就定义。"""
import json

from . import database

ACHIEVEMENTS = [
    {"code": "first_step", "name": "初来乍到", "description": "完成第 1 节课", "icon": "🌱", "condition_type": "lessons_completed", "condition_value": 1},
    {"code": "persistent", "name": "持之以恒", "description": "累计完成 5 节课", "icon": "🔥", "condition_type": "lessons_completed", "condition_value": 5},
    {"code": "scholar", "name": "学霸之路", "description": "累计完成 15 节课", "icon": "🎓", "condition_type": "lessons_completed", "condition_value": 15},
    {"code": "streak_3", "name": "三日连击", "description": "连续学习 3 天", "icon": "⚡", "condition_type": "streak", "condition_value": 3},
    {"code": "streak_7", "name": "七日达人", "description": "连续学习 7 天", "icon": "🌟", "condition_type": "streak", "condition_value": 7},
    {"code": "polyglot", "name": "多语达人", "description": "学习 2 种以上语言", "icon": "🌍", "condition_type": "languages", "condition_value": 2},
    {"code": "social", "name": "社区活跃", "description": "发布第 1 个帖子", "icon": "💬", "condition_type": "posts", "condition_value": 1},
    {"code": "points_100", "name": "积分破百", "description": "累计获得 100 积分", "icon": "💎", "condition_type": "points", "condition_value": 100},
]

# 课程结构：language 使用 ISO 代码，level 使用 CEFR 级别，type 为互动模块类型
COURSES = [
    # ======================= 英语 =======================
    {
        "language": "en", "level": "A1", "icon": "🔤", "color": "#6366f1",
        "title": "英语 · A1 入门",
        "description": "从问候与自我介绍开始，掌握英语最基础的词汇、语法与表达。",
        "lessons": [
            {
                "title": "词汇记忆 · 日常问候", "type": "vocabulary",
                "content": {"words": [
                    {"word": "hello", "phonetic": "/həˈloʊ/", "translation": "你好", "example": "Hello, nice to meet you.", "example_translation": "你好，很高兴认识你。"},
                    {"word": "goodbye", "phonetic": "/ˌɡʊdˈbaɪ/", "translation": "再见", "example": "Goodbye, see you tomorrow.", "example_translation": "再见，明天见。"},
                    {"word": "thank you", "phonetic": "/ˈθæŋk juː/", "translation": "谢谢", "example": "Thank you for your help.", "example_translation": "谢谢你的帮助。"},
                    {"word": "please", "phonetic": "/pliːz/", "translation": "请", "example": "Please sit down.", "example_translation": "请坐。"},
                    {"word": "sorry", "phonetic": "/ˈsɒri/", "translation": "对不起", "example": "I am sorry, I am late.", "example_translation": "对不起，我迟到了。"},
                    {"word": "friend", "phonetic": "/frend/", "translation": "朋友", "example": "She is my good friend.", "example_translation": "她是我的好朋友。"},
                    {"word": "family", "phonetic": "/ˈfæməli/", "translation": "家人", "example": "I love my family.", "example_translation": "我爱我的家人。"},
                    {"word": "water", "phonetic": "/ˈwɔːtər/", "translation": "水", "example": "Can I have some water?", "example_translation": "我能喝点水吗？"},
                ]},
            },
            {
                "title": "语法练习 · be 动词与一般现在时", "type": "grammar",
                "content": {
                    "intro": "英语基本句型：be 动词（am/is/are）表示“是”，一般现在时描述习惯与事实。",
                    "points": [
                        {"title": "be 动词的用法", "explanation": "I 用 am，he/she/it 用 is，you/we/they 用 are。", "example": "I am a student. / She is a teacher. / They are friends.", "example_translation": "我是学生。/ 她是老师。/ 他们是朋友。"},
                        {"title": "一般现在时", "explanation": "主语为第三人称单数时，动词词尾加 -s 或 -es。", "example": "He plays football. / She watches TV.", "example_translation": "他踢足球。/ 她看电视。"},
                        {"title": "否定与疑问", "explanation": "否定加 do not / does not，疑问把 do / does 提前。", "example": "I do not like coffee. / Do you like tea?", "example_translation": "我不喜欢咖啡。/ 你喜欢茶吗？"},
                    ],
                    "questions": [
                        {"question": "选择正确的 be 动词：She ___ a doctor.", "options": ["am", "is", "are", "be"], "answer": 1, "explanation": "主语 She 为第三人称单数，用 is。"},
                        {"question": "选择正确的形式：He ___ (go) to school every day.", "options": ["go", "going", "goes", "gone"], "answer": 2, "explanation": "第三人称单数一般现在时，动词加 -es。"},
                        {"question": "选择正确的否定句：I ___ like coffee.", "options": ["do not", "does not", "am not", "not"], "answer": 0, "explanation": "主语 I 用 do not。"},
                        {"question": "选择正确的疑问句：___ you like music?", "options": ["Does", "Do", "Is", "Are"], "answer": 1, "explanation": "主语 you 用 Do 提问。"},
                    ],
                },
            },
            {
                "title": "口语跟读 · 见面问候", "type": "speaking",
                "content": {"sentences": [
                    {"text": "Hello, nice to meet you.", "phonetic": "/həˈloʊ, naɪs tə miːt juː/", "translation": "你好，很高兴认识你。"},
                    {"text": "How are you today?", "phonetic": "/haʊ ɑːr juː təˈdeɪ/", "translation": "你今天好吗？"},
                    {"text": "I am fine, thank you.", "phonetic": "/aɪ æm faɪn, θæŋk juː/", "translation": "我很好，谢谢。"},
                    {"text": "What is your name?", "phonetic": "/wʌt ɪz jɔːr neɪm/", "translation": "你叫什么名字？"},
                    {"text": "Where are you from?", "phonetic": "/wer ɑːr juː frʌm/", "translation": "你来自哪里？"},
                ]},
            },
            {
                "title": "听力训练 · 自我介绍", "type": "listening",
                "content": {
                    "audio_text": "Hello, my name is Anna. I am from Japan. I am a student. Nice to meet you.",
                    "translation": "你好，我叫安娜。我来自日本。我是一名学生。很高兴认识你。",
                    "questions": [
                        {"question": "What is the speaker's name?", "options": ["Amy", "Anna", "Emma", "Alice"], "answer": 1},
                        {"question": "Where is she from?", "options": ["China", "Korea", "Japan", "America"], "answer": 2},
                        {"question": "What is her job?", "options": ["teacher", "doctor", "student", "driver"], "answer": 2},
                    ],
                },
            },
        ],
    },
    {
        "language": "en", "level": "A2", "icon": "🔤", "color": "#6366f1",
        "title": "英语 · A2 基础",
        "description": "扩展生活场景表达，学习进行时与过去时，练习点餐与问路。",
        "lessons": [
            {
                "title": "词汇记忆 · 出行与饮食", "type": "vocabulary",
                "content": {"words": [
                    {"word": "restaurant", "phonetic": "/ˈrestrɑːnt/", "translation": "餐厅", "example": "Let's go to the restaurant.", "example_translation": "我们去餐厅吧。"},
                    {"word": "menu", "phonetic": "/ˈmenjuː/", "translation": "菜单", "example": "Could I see the menu?", "example_translation": "能给我看看菜单吗？"},
                    {"word": "train", "phonetic": "/treɪn/", "translation": "火车", "example": "The train is coming.", "example_translation": "火车来了。"},
                    {"word": "ticket", "phonetic": "/ˈtɪkɪt/", "translation": "票", "example": "I bought two tickets.", "example_translation": "我买了两张票。"},
                    {"word": "hotel", "phonetic": "/hoʊˈtel/", "translation": "酒店", "example": "The hotel is near the station.", "example_translation": "酒店在车站附近。"},
                    {"word": "breakfast", "phonetic": "/ˈbrekfəst/", "translation": "早餐", "example": "Breakfast is at seven.", "example_translation": "早餐七点开始。"},
                    {"word": "delicious", "phonetic": "/dɪˈlɪʃəs/", "translation": "美味的", "example": "This soup is delicious.", "example_translation": "这汤很美味。"},
                    {"word": "travel", "phonetic": "/ˈtrævl/", "translation": "旅行", "example": "I want to travel to Paris.", "example_translation": "我想去巴黎旅行。"},
                ]},
            },
            {
                "title": "语法练习 · 现在进行时与一般过去时", "type": "grammar",
                "content": {
                    "intro": "现在进行时表示正在发生，一般过去时表示过去发生的事。",
                    "points": [
                        {"title": "现在进行时", "explanation": "结构：am/is/are + 动词-ing。", "example": "I am reading a book.", "example_translation": "我正在读书。"},
                        {"title": "一般过去时", "explanation": "规则动词词尾加 -ed，不规则动词需记忆。", "example": "I visited my friend yesterday.", "example_translation": "我昨天拜访了朋友。"},
                        {"title": "过去否定与疑问", "explanation": "用 did not / Did 构成。", "example": "I did not go out. / Did you see the movie?", "example_translation": "我没出去。/ 你看那部电影了吗？"},
                    ],
                    "questions": [
                        {"question": "选择正确形式：Right now, she ___ (cook) dinner.", "options": ["cook", "cooks", "is cooking", "cooked"], "answer": 2, "explanation": "right now 提示正在进行，用现在进行时。"},
                        {"question": "选择正确形式：We ___ (visit) the museum last week.", "options": ["visit", "visited", "visiting", "visits"], "answer": 1, "explanation": "last week 提示一般过去时，visited。"},
                        {"question": "选择正确形式：___ you watch TV last night?", "options": ["Do", "Does", "Did", "Are"], "answer": 2, "explanation": "过去疑问句用 Did。"},
                        {"question": "选择正确形式：They ___ (walk) in the park now.", "options": ["walk", "walked", "are walking", "walks"], "answer": 2, "explanation": "now 提示现在进行时。"},
                    ],
                },
            },
            {
                "title": "口语跟读 · 餐厅点餐", "type": "speaking",
                "content": {"sentences": [
                    {"text": "Could I see the menu, please?", "phonetic": "/kʊd aɪ siː ðə ˈmenjuː pliːz/", "translation": "请给我看看菜单好吗？"},
                    {"text": "I would like a cup of coffee.", "phonetic": "/aɪ wʊd laɪk ə kʌp əv ˈkɔːfi/", "translation": "我想要一杯咖啡。"},
                    {"text": "How much is this?", "phonetic": "/haʊ mʌtʃ ɪz ðɪs/", "translation": "这个多少钱？"},
                    {"text": "Could I have the bill, please?", "phonetic": "/kʊd aɪ hæv ðə bɪl pliːz/", "translation": "请给我账单好吗？"},
                ]},
            },
            {
                "title": "听力训练 · 问路对话", "type": "listening",
                "content": {
                    "audio_text": "Excuse me, where is the train station? Go straight and turn left at the bank. The station is next to the hotel.",
                    "translation": "打扰一下，火车站在哪里？直走，在银行处左转。车站在酒店旁边。",
                    "questions": [
                        {"question": "Where does the person want to go?", "options": ["the bank", "the hotel", "the train station", "the restaurant"], "answer": 2},
                        {"question": "What should the person do at the bank?", "options": ["turn left", "turn right", "go straight", "stop"], "answer": 0},
                        {"question": "The station is next to the ___?", "options": ["bank", "hotel", "restaurant", "park"], "answer": 1},
                    ],
                },
            },
        ],
    },
    # ======================= 日语 =======================
    {
        "language": "ja", "level": "A1", "icon": "⛩️", "color": "#ec4899",
        "title": "日语 · A1 入门",
        "description": "掌握五十音基础词汇、です 句型与自我介绍表达。",
        "lessons": [
            {
                "title": "词汇记忆 · 基本问候", "type": "vocabulary",
                "content": {"words": [
                    {"word": "こんにちは", "phonetic": "konnichiwa", "translation": "你好", "example": "こんにちは、元気ですか。", "example_translation": "你好，身体好吗？"},
                    {"word": "ありがとう", "phonetic": "arigatō", "translation": "谢谢", "example": "ありがとうございます。", "example_translation": "非常感谢。"},
                    {"word": "さようなら", "phonetic": "sayōnara", "translation": "再见", "example": "さようなら、また明日。", "example_translation": "再见，明天见。"},
                    {"word": "はい", "phonetic": "hai", "translation": "是", "example": "はい、そうです。", "example_translation": "是的，没错。"},
                    {"word": "いいえ", "phonetic": "iie", "translation": "不是", "example": "いいえ、違います。", "example_translation": "不，不是。"},
                    {"word": "水", "phonetic": "mizu", "translation": "水", "example": "水をください。", "example_translation": "请给我水。"},
                    {"word": "友達", "phonetic": "tomodachi", "translation": "朋友", "example": "彼は友達です。", "example_translation": "他是朋友。"},
                    {"word": "学校", "phonetic": "gakkō", "translation": "学校", "example": "学校へ行きます。", "example_translation": "去学校。"},
                ]},
            },
            {
                "title": "语法练习 · です 与基础助词", "type": "grammar",
                "content": {
                    "intro": "日语判断句以「です」结尾，助词「は／の／を」标记句子成分。",
                    "points": [
                        {"title": "判断句です", "explanation": "「A は B です」表示“A 是 B”。", "example": "私は学生です。", "example_translation": "我是学生。"},
                        {"title": "助词は", "explanation": "提示主题，可译为“是……”。", "example": "これは本です。", "example_translation": "这是书。"},
                        {"title": "助词の", "explanation": "表示所属或修饰关系“的”。", "example": "私の友達です。", "example_translation": "我的朋友。"},
                        {"title": "助词を", "explanation": "标记动作的对象。", "example": "水を飲みます。", "example_translation": "喝水。"},
                    ],
                    "questions": [
                        {"question": "选择正确说法：「我是田中。」", "options": ["私は田中です", "私を田中です", "私は田中をです", "私の田中です"], "answer": 0, "explanation": "「A は B です」判断句。"},
                        {"question": "选择正确助词：これ(  )本です。", "options": ["を", "は", "の", "に"], "answer": 1, "explanation": "「これは本です」提示主题用は。"},
                        {"question": "选择正确助词：私(  )友達。", "options": ["は", "を", "の", "へ"], "answer": 2, "explanation": "所属关系用の。"},
                        {"question": "选择正确助词：水(  )飲みます。", "options": ["は", "の", "を", "で"], "answer": 2, "explanation": "动作对象用を。"},
                    ],
                },
            },
            {
                "title": "口语跟读 · 自我介绍", "type": "speaking",
                "content": {"sentences": [
                    {"text": "はじめまして。", "phonetic": "hajimemashite", "translation": "初次见面。"},
                    {"text": "私は田中です。", "phonetic": "watashi wa Tanaka desu", "translation": "我是田中。"},
                    {"text": "お元気ですか。", "phonetic": "o-genki desu ka", "translation": "你好吗？"},
                    {"text": "はい、元気です。", "phonetic": "hai, genki desu", "translation": "是的，我很好。"},
                    {"text": "よろしくお願いします。", "phonetic": "yoroshiku onegaishimasu", "translation": "请多关照。"},
                ]},
            },
            {
                "title": "听力训练 · 自我介绍", "type": "listening",
                "content": {
                    "audio_text": "はじめまして。私は田中です。学生です。よろしくお願いします。",
                    "translation": "初次见面。我是田中。我是一名学生。请多关照。",
                    "questions": [
                        {"question": "说话人的名字是什么？", "options": ["鈴木", "佐藤", "田中", "高橋"], "answer": 2},
                        {"question": "他的身份是什么？", "options": ["老师", "学生", "医生", "警察"], "answer": 1},
                        {"question": "他最后说了什么？", "options": ["ありがとう", "よろしくお願いします", "さようなら", "お元気ですか"], "answer": 1},
                    ],
                },
            },
        ],
    },
    {
        "language": "ja", "level": "A2", "icon": "⛩️", "color": "#ec4899",
        "title": "日语 · A2 基础",
        "description": "学习过去时与て形，练习餐厅点餐等生活对话。",
        "lessons": [
            {
                "title": "词汇记忆 · 饮食与出行", "type": "vocabulary",
                "content": {"words": [
                    {"word": "レストラン", "phonetic": "resutoran", "translation": "餐厅", "example": "レストランへ行きます。", "example_translation": "去餐厅。"},
                    {"word": "メニュー", "phonetic": "menyū", "translation": "菜单", "example": "メニューを見せてください。", "example_translation": "请给我看菜单。"},
                    {"word": "電車", "phonetic": "densha", "translation": "电车", "example": "電車で行きます。", "example_translation": "乘电车去。"},
                    {"word": "切符", "phonetic": "kippu", "translation": "车票", "example": "切符を買います。", "example_translation": "买票。"},
                    {"word": "ホテル", "phonetic": "hoteru", "translation": "酒店", "example": "ホテルに泊まります。", "example_translation": "住酒店。"},
                    {"word": "朝ご飯", "phonetic": "asagohan", "translation": "早饭", "example": "朝ご飯を食べます。", "example_translation": "吃早饭。"},
                    {"word": "おいしい", "phonetic": "oishii", "translation": "好吃的", "example": "この料理はおいしいです。", "example_translation": "这道菜很好吃。"},
                    {"word": "旅行", "phonetic": "ryokō", "translation": "旅行", "example": "旅行が好きです。", "example_translation": "喜欢旅行。"},
                ]},
            },
            {
                "title": "语法练习 · 过去时与て形", "type": "grammar",
                "content": {
                    "intro": "过去时以「ました／でした」结尾，て形用于连接动作与请求。",
                    "points": [
                        {"title": "动词过去时", "explanation": "ます形变为ました。", "example": "昨日、本を読みました。", "example_translation": "昨天读书了。"},
                        {"title": "名词/形容词过去", "explanation": "です变为でした。", "example": "昨日は雨でした。", "example_translation": "昨天是雨天。"},
                        {"title": "て形请求", "explanation": "「てください」表示“请……”。", "example": "メニューを見せてください。", "example_translation": "请给我看菜单。"},
                    ],
                    "questions": [
                        {"question": "选择正确过去时：昨日、テレビを(  )。", "options": ["見ます", "見ました", "見て", "見ない"], "answer": 1, "explanation": "昨日提示过去，用見ました。"},
                        {"question": "选择正确过去时：昨日はいい天気(  )。", "options": ["です", "でした", "ます", "ません"], "answer": 1, "explanation": "名词过去用でした。"},
                        {"question": "选择正确说法：「请告诉我。」", "options": ["教えます", "教えてください", "教えました", "教えて"], "answer": 1, "explanation": "て形请求用てください。"},
                        {"question": "选择正确形式：「请等一下。」", "options": ["待ちます", "待ってください", "待ちました", "待たない"], "answer": 1, "explanation": "待つ的て形为待って。"},
                    ],
                },
            },
            {
                "title": "口语跟读 · 餐厅点餐", "type": "speaking",
                "content": {"sentences": [
                    {"text": "メニューを見せてください。", "phonetic": "menyū o misete kudasai", "translation": "请给我看菜单。"},
                    {"text": "コーヒーをください。", "phonetic": "kōhī o kudasai", "translation": "请给我咖啡。"},
                    {"text": "これはいくらですか。", "phonetic": "kore wa ikura desu ka", "translation": "这个多少钱？"},
                    {"text": "お会計をお願いします。", "phonetic": "okaikei o onegaishimasu", "translation": "请结账。"},
                ]},
            },
            {
                "title": "听力训练 · 问路对话", "type": "listening",
                "content": {
                    "audio_text": "すみません、駅はどこですか。まっすぐ行って、銀行で左へ曲がってください。駅はホテルの隣です。",
                    "translation": "打扰一下，车站在哪里？直走，在银行处左转。车站在酒店旁边。",
                    "questions": [
                        {"question": "想去哪里？", "options": ["銀行", "ホテル", "駅", "レストラン"], "answer": 2},
                        {"question": "在银行处应该怎么做？", "options": ["右转", "左转", "直走", "停下"], "answer": 1},
                        {"question": "车站在哪里的旁边？", "options": ["銀行", "ホテル", "レストラン", "公園"], "answer": 1},
                    ],
                },
            },
        ],
    },
    # ======================= 韩语 =======================
    {
        "language": "ko", "level": "A1", "icon": "🇰🇷", "color": "#14b8a6",
        "title": "韩语 · A1 入门",
        "description": "掌握韩语基本问候词汇与 입니다 句型，练习自我介绍。",
        "lessons": [
            {
                "title": "词汇记忆 · 基本问候", "type": "vocabulary",
                "content": {"words": [
                    {"word": "안녕하세요", "phonetic": "annyeonghaseyo", "translation": "你好", "example": "안녕하세요, 잘 지내세요?", "example_translation": "你好，过得好吗？"},
                    {"word": "감사합니다", "phonetic": "gamsahamnida", "translation": "谢谢", "example": "정말 감사합니다.", "example_translation": "非常感谢。"},
                    {"word": "네", "phonetic": "ne", "translation": "是", "example": "네, 맞아요.", "example_translation": "是的，没错。"},
                    {"word": "아니요", "phonetic": "aniyo", "translation": "不是", "example": "아니요, 아니에요.", "example_translation": "不，不是。"},
                    {"word": "물", "phonetic": "mul", "translation": "水", "example": "물 좀 주세요.", "example_translation": "请给我水。"},
                    {"word": "친구", "phonetic": "chingu", "translation": "朋友", "example": "그는 친구예요.", "example_translation": "他是朋友。"},
                    {"word": "학교", "phonetic": "hakgyo", "translation": "学校", "example": "학교에 가요.", "example_translation": "去学校。"},
                    {"word": "책", "phonetic": "chaek", "translation": "书", "example": "책을 읽어요.", "example_translation": "读书。"},
                ]},
            },
            {
                "title": "语法练习 · 입니다 与 은/는", "type": "grammar",
                "content": {
                    "intro": "韩语判断句以「입니다」结尾，助词「은/는/이/가」标记主题与主语。",
                    "points": [
                        {"title": "判断句입니다", "explanation": "「A는 B입니다」表示“A 是 B”。", "example": "저는 학생입니다.", "example_translation": "我是学生。"},
                        {"title": "主题助词은/는", "explanation": "有收音用은，无收音用는。", "example": "이것은 책입니다. / 저는 학생입니다.", "example_translation": "这是书。/ 我是学生。"},
                        {"title": "主格助词이/가", "explanation": "有收音用이，无收音用가。", "example": "물이 있어요.", "example_translation": "有水。"},
                    ],
                    "questions": [
                        {"question": "选择正确说法：「我是学生。」", "options": ["저는 학생입니다", "저를 학생입니다", "저는 학생을입니다", "저의 학생입니다"], "answer": 0, "explanation": "「A는 B입니다」判断句。"},
                        {"question": "选择正确助词：이것(  ) 책입니다。", "options": ["은", "를", "이", "의"], "answer": 0, "explanation": "이것有收音，用은。"},
                        {"question": "选择正确助词：저(  ) 학생입니다。", "options": ["은", "는", "을", "의"], "answer": 1, "explanation": "저无收音，用는。"},
                        {"question": "选择正确助词：물(  ) 있어요。", "options": ["는", "을", "이", "의"], "answer": 2, "explanation": "물有收音，主格用이。"},
                    ],
                },
            },
            {
                "title": "口语跟读 · 自我介绍", "type": "speaking",
                "content": {"sentences": [
                    {"text": "안녕하세요.", "phonetic": "annyeonghaseyo", "translation": "你好。"},
                    {"text": "저는 민수예요.", "phonetic": "jeoneun minsuyeyo", "translation": "我是民秀。"},
                    {"text": "잘 지내세요?", "phonetic": "jal jinaeseyo", "translation": "过得好吗？"},
                    {"text": "네, 잘 지내요.", "phonetic": "ne, jal jinaeyo", "translation": "是的，我很好。"},
                    {"text": "만나서 반갑습니다.", "phonetic": "mannaseo bangapseumnida", "translation": "很高兴认识你。"},
                ]},
            },
            {
                "title": "听力训练 · 自我介绍", "type": "listening",
                "content": {
                    "audio_text": "안녕하세요. 저는 민수입니다. 학생입니다. 만나서 반갑습니다.",
                    "translation": "你好。我是民秀。我是一名学生。很高兴认识你。",
                    "questions": [
                        {"question": "说话人的名字是什么？", "options": ["철수", "민수", "영희", "지훈"], "answer": 1},
                        {"question": "他的身份是什么？", "options": ["老师", "学生", "医生", "警察"], "answer": 1},
                        {"question": "他最后说了什么？", "options": ["감사합니다", "만나서 반갑습니다", "안녕히 가세요", "잘 지내세요"], "answer": 1},
                    ],
                },
            },
        ],
    },
    {
        "language": "ko", "level": "A2", "icon": "🇰🇷", "color": "#14b8a6",
        "title": "韩语 · A2 基础",
        "description": "学习过去时体았/었 与生活场景表达，练习餐厅点餐。",
        "lessons": [
            {
                "title": "词汇记忆 · 饮食与出行", "type": "vocabulary",
                "content": {"words": [
                    {"word": "식당", "phonetic": "sikdang", "translation": "餐厅", "example": "식당에 가요.", "example_translation": "去餐厅。"},
                    {"word": "메뉴", "phonetic": "menyu", "translation": "菜单", "example": "메뉴 좀 보여 주세요.", "example_translation": "请给我看菜单。"},
                    {"word": "기차", "phonetic": "gicha", "translation": "火车", "example": "기차로 가요.", "example_translation": "坐火车去。"},
                    {"word": "표", "phonetic": "pyo", "translation": "票", "example": "표를 사요.", "example_translation": "买票。"},
                    {"word": "호텔", "phonetic": "hotel", "translation": "酒店", "example": "호텔에 묵어요.", "example_translation": "住酒店。"},
                    {"word": "아침", "phonetic": "achim", "translation": "早饭", "example": "아침을 먹어요.", "example_translation": "吃早饭。"},
                    {"word": "맛있어요", "phonetic": "masisseoyo", "translation": "好吃", "example": "이 요리는 맛있어요.", "example_translation": "这道菜很好吃。"},
                    {"word": "여행", "phonetic": "yeohaeng", "translation": "旅行", "example": "여행을 좋아해요.", "example_translation": "喜欢旅行。"},
                ]},
            },
            {
                "title": "语法练习 · 过去时体", "type": "grammar",
                "content": {
                    "intro": "韩语过去时用「았/었어요」，连接请求用「주세요」。",
                    "points": [
                        {"title": "过去时았/었", "explanation": "词干末音节元音为ㅏㅗ用았，其他用었。", "example": "어제 책을 읽었어요.", "example_translation": "昨天读书了。"},
                        {"title": "请求주세요", "explanation": "「주세요」表示“请给我……”。", "example": "물 주세요.", "example_translation": "请给我水。"},
                        {"title": "否定안/못", "explanation": "안表示主观否定，못表示能力否定。", "example": "안 가요. / 못 가요.", "example_translation": "不去。/ 去不了。"},
                    ],
                    "questions": [
                        {"question": "选择正确过去时：어제 영화를(  ).", "options": ["봐요", "봤어요", "봐 주세요", "봐"], "answer": 1, "explanation": "어제提示过去，봤어요。"},
                        {"question": "选择正确过去时：어제 비가(  ).", "options": ["와요", "왔어요", "와 주세요", "와"], "answer": 1, "explanation": "오다过去为왔어요。"},
                        {"question": "选择正确说法：「请给我水。」", "options": ["물이에요", "물 주세요", "물 마셨어요", "물이 없어요"], "answer": 1, "explanation": "请求用주세요。"},
                        {"question": "选择正确过去时：밥을(  ).", "options": ["먹어요", "먹었어요", "먹어 주세요", "먹어"], "answer": 1, "explanation": "먹다过去为먹었어요。"},
                    ],
                },
            },
            {
                "title": "口语跟读 · 餐厅点餐", "type": "speaking",
                "content": {"sentences": [
                    {"text": "메뉴 좀 보여 주세요.", "phonetic": "menyu jom boyeo juseyo", "translation": "请给我看菜单。"},
                    {"text": "커피 한 잔 주세요.", "phonetic": "keopi han jan juseyo", "translation": "请给我一杯咖啡。"},
                    {"text": "이거 얼마예요?", "phonetic": "igeo eolmayeyo", "translation": "这个多少钱？"},
                    {"text": "계산해 주세요.", "phonetic": "gyesanhae juseyo", "translation": "请结账。"},
                ]},
            },
            {
                "title": "听力训练 · 问路对话", "type": "listening",
                "content": {
                    "audio_text": "실례합니다, 역이 어디예요? 직진해서 은행에서 왼쪽으로 도세요. 역은 호텔 옆에 있어요.",
                    "translation": "打扰一下，车站在哪里？直走，在银行处左转。车站在酒店旁边。",
                    "questions": [
                        {"question": "想去哪里？", "options": ["은행", "호텔", "역", "식당"], "answer": 2},
                        {"question": "在银行处应该怎么做？", "options": ["右转", "左转", "直走", "停下"], "answer": 1},
                        {"question": "车站在哪里的旁边？", "options": ["은행", "호텔", "식당", "공원"], "answer": 1},
                    ],
                },
            },
        ],
    },
]


def _insert_courses(conn) -> None:
    for order, course in enumerate(COURSES):
        cur = conn.execute(
            "INSERT INTO courses (language, level, title, description, order_index, icon, color) VALUES (?,?,?,?,?,?,?)",
            (course["language"], course["level"], course["title"], course["description"], order, course["icon"], course["color"]),
        )
        course_id = cur.lastrowid
        for lorder, lesson in enumerate(course["lessons"]):
            conn.execute(
                "INSERT INTO lessons (course_id, title, type, content, order_index) VALUES (?,?,?,?,?)",
                (course_id, lesson["title"], lesson["type"], json.dumps(lesson["content"], ensure_ascii=False), lorder),
            )


def seed_if_needed() -> None:
    conn = database.get_connection()
    try:
        count = conn.execute("SELECT COUNT(*) AS c FROM courses").fetchone()["c"]
        if count == 0:
            _insert_courses(conn)
        acount = conn.execute("SELECT COUNT(*) AS c FROM achievements").fetchone()["c"]
        if acount == 0:
            for a in ACHIEVEMENTS:
                conn.execute(
                    "INSERT INTO achievements (code, name, description, icon, condition_type, condition_value) VALUES (?,?,?,?,?,?)",
                    (a["code"], a["name"], a["description"], a["icon"], a["condition_type"], a["condition_value"]),
                )
        conn.commit()
    finally:
        conn.close()