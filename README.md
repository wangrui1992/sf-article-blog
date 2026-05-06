# SegmentFault 鍗氬鍚庡彴绠＄悊绯荤粺

鍩轰簬 SegmentFault 鏂囩珷鏁版嵁鐨?Flask 鍚庡彴绠＄悊绯荤粺锛屾敮鎸佹枃绔犵鐞嗐€佺敤鎴风鐞嗐€佹爣绛剧鐞嗐€佹暟鎹彲瑙嗗寲绛夊畬鏁村姛鑳姐€?
## 鍔熻兘鐗规€?
### 鏍稿績鍔熻兘
- **鏂囩珷绠＄悊**锛氬垱寤恒€佺紪杈戙€佸彂甯冦€佸垹闄ゆ枃绔狅紝鏀寔 Markdown 缂栬緫鍣ㄥ拰鏍囩绠＄悊
- **鐢ㄦ埛绠＄悊**锛氱敤鎴锋敞鍐岀櫥褰曘€佽鑹叉潈闄愮鐞嗭紙浣滆€?绠＄悊鍛橈級銆佺姸鎬佸惎鐢?绂佺敤
- **鏍囩绯荤粺**锛氱伒娲荤殑鏍囩 CRUD 鎿嶄綔锛屾敮鎸佽嚜瀹氫箟棰滆壊鍜屽埆鍚?- **鑽夌绠?*锛氳嚜鍔ㄤ繚瀛樻枃绔犺崏绋匡紝闃叉鍐呭涓㈠け
- **杞垹闄ゆ満鍒?*锛氭暟鎹畨鍏ㄥ垹闄わ紝鏀寔鎭㈠

### 鏁版嵁鍙鍖?- **浠〃鐩樼粺璁?*锛氭€绘枃绔犳暟銆佹€荤敤鎴锋暟銆佹€绘爣绛炬暟銆佹湰鏈堟柊澧?- **瓒嬪娍鍥捐〃**锛欵Charts 鎶樼嚎鍥惧睍绀烘枃绔犲彂甯冭秼鍔?- **鐑棬鏍囩**锛氶ゼ鍥惧睍绀烘爣绛惧垎甯?- **鏈€鏂版枃绔?*锛氬疄鏃跺睍绀烘渶杩戝彂甯冪殑鏂囩珷鍒楄〃

### 绯荤粺绠＄悊
- **绯荤粺璁剧疆**锛氬熀鏈厤缃€佺敤鎴疯缃€佸畨鍏ㄨ缃?- **鏁版嵁澶囦唤**锛欽SON/CSV 鏍煎紡瀵煎嚭瀵煎叆
- **鎿嶄綔鏃ュ織**锛氬畬鏁磋褰曠敤鎴锋搷浣滆涓?- **鍋ュ悍妫€鏌?*锛氱郴缁熻繍琛岀姸鎬佺洃鎺?
## 鎶€鏈爤

### 鍚庣
- **妗嗘灦**锛欶lask 2.3+ (搴旂敤宸ュ巶妯″紡)
- **ORM**锛歋QLAlchemy 2.0 (杞垹闄ゃ€佸鍚堢储寮?
- **璁よ瘉**锛欶lask-Login + Flask-WTF (CSRF 淇濇姢)
- **缂撳瓨**锛氬唴瀛樼紦瀛樼郴缁?(SimpleCache + @cached 瑁呴グ鍣?

### 鍓嶇
- **妯℃澘寮曟搸**锛欽inja2
- **鍥捐〃搴?*锛欵Charts 5.x
- **鏍峰紡**锛氬師鐢?CSS (GitHub Dark 椋庢牸)

### 鏁版嵁搴?- **绫诲瀷**锛歋QLite (寮€鍙戠幆澧? / PostgreSQL (鐢熶骇鐜)
- **鎬ц兘浼樺寲**锛氬鍚堢储寮曘€乯oinedload 棰勫姞杞姐€佸唴瀛樼紦瀛?
## 鐩綍缁撴瀯

```
sf-article-blog/
鈹溾攢鈹€ README.md                 # 椤圭洰璇存槑鏂囨。
鈹溾攢鈹€ LICENSE                   # MIT 寮€婧愬崗璁?鈹溾攢鈹€ CHANGELOG.md              # 鏇存柊鏃ュ織
鈹溾攢鈹€ requirements.txt          # Python 渚濊禆
鈹溾攢鈹€ index.html                # 闈欐€侀椤?鈹溾攢鈹€ fetch_articles.py         # 鏂囩珷鎶撳彇鑴氭湰
鈹溾攢鈹€ sample_data.json          # 绀轰緥鏁版嵁
鈹?鈹斺攢鈹€ backend/
    鈹溾攢鈹€ app.py                # Flask 搴旂敤鍏ュ彛 (create_app)
    鈹溾攢鈹€ config.py              # 閰嶇疆鏂囦欢
    鈹溾攢鈹€ run.py                 # 鍚姩鑴氭湰
    鈹溾攢鈹€ requirements.txt       # Python 渚濊禆
    鈹?    鈹溾攢鈹€ models/                # 鏁版嵁妯″瀷灞?    鈹?  鈹溾攢鈹€ database.py        # 鏁版嵁搴撳垵濮嬪寲 & 鍒嗛〉宸ュ叿
    鈹?  鈹溾攢鈹€ user.py            # 鐢ㄦ埛妯″瀷
    鈹?  鈹溾攢鈹€ article.py          # 鏂囩珷妯″瀷
    鈹?  鈹溾攢鈹€ tag.py              # 鏍囩妯″瀷
    鈹?  鈹溾攢鈹€ log.py              # 鎿嶄綔鏃ュ織妯″瀷
    鈹?  鈹斺攢鈹€ __init__.py
    鈹?    鈹溾攢鈹€ routes/                # 璺敱鎺у埗鍣ㄥ眰
    鈹?  鈹溾攢鈹€ auth.py            # 璁よ瘉璺敱 (鐧诲綍/娉ㄥ唽/鐧诲嚭)
    鈹?  鈹溾攢鈹€ article.py          # 鏂囩珷璺敱 (CRUD/API)
    鈹?  鈹溾攢鈹€ admin.py            # 绠＄悊鍚庡彴璺敱
    鈹?  鈹溾攢鈹€ api.py              # API 鎺ュ彛璺敱
    鈹?  鈹斺攢鈹€ __init__.py
    鈹?    鈹溾攢鈹€ utils/                 # 宸ュ叿鍑芥暟灞?    鈹?  鈹溾攢鈹€ helpers.py          # 閫氱敤杈呭姪鍑芥暟
    鈹?  鈹溾攢鈹€ validators.py       # 琛ㄥ崟楠岃瘉鍣?    鈹?  鈹溾攢鈹€ cache.py             # 缂撳瓨瑁呴グ鍣?    鈹?  鈹溾攢鈹€ security.py          # 瀹夊叏宸ュ叿
    鈹?  鈹斺攢鈹€ __init__.py
    鈹?    鈹斺攢鈹€ templates/             # Jinja2 妯℃澘
        鈹溾攢鈹€ dashboard.html      # 浠〃鐩?        鈹溾攢鈹€ 404.html            # 閿欒椤甸潰
        鈹溾攢鈹€ auth/
        鈹?  鈹溾攢鈹€ login.html      # 鐧诲綍椤?        鈹?  鈹斺攢鈹€ register.html   # 娉ㄥ唽椤?        鈹溾攢鈹€ article/
        鈹?  鈹溾攢鈹€ list.html       # 鏂囩珷鍒楄〃
        鈹?  鈹斺攢鈹€ edit.html        # 鏂囩珷缂栬緫鍣?        鈹斺攢鈹€ admin/
            鈹溾攢鈹€ users.html      # 鐢ㄦ埛绠＄悊
            鈹溾攢鈹€ tags.html       # 鏍囩绠＄悊
            鈹溾攢鈹€ settings.html    # 绯荤粺璁剧疆
            鈹斺攢鈹€ backup.html      # 鏁版嵁澶囦唤
```

## 蹇€熷紑濮?
### 鐜瑕佹眰
- Python 3.8+
- pip 鍖呯鐞嗗櫒

### 瀹夎姝ラ

1. **鍏嬮殕椤圭洰**
```bash
git clone <repository-url>
cd sf-article-blog
```

2. **鍒涘缓铏氭嫙鐜**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. **瀹夎渚濊禆**
```bash
pip install -r requirements.txt
```

4. **鍒濆鍖栨暟鎹簱**
```bash
cd backend
python run.py
```

5. **璁块棶绯荤粺**
鎵撳紑娴忚鍣ㄨ闂細`http://localhost:5000`

榛樿绠＄悊鍛樿处鍙凤細
- 鐢ㄦ埛鍚嶏細`admin`
- 瀵嗙爜锛歚admin123`

## API 鎺ュ彛

### 璁よ瘉鎺ュ彛
| 鏂规硶 | 璺緞 | 璇存槑 |
|------|------|------|
| POST | `/auth/login` | 鐢ㄦ埛鐧诲綍 |
| POST | `/auth/register` | 鐢ㄦ埛娉ㄥ唽 |
| GET | `/auth/logout` | 鐢ㄦ埛鐧诲嚭 |
| GET | `/api/profile` | 鑾峰彇褰撳墠鐢ㄦ埛淇℃伅 |
| POST | `/api/profile` | 鏇存柊鐢ㄦ埛璧勬枡 |
| POST | `/api/change-password` | 淇敼瀵嗙爜 |

### 鏂囩珷鎺ュ彛
| 鏂规硶 | 璺緞 | 璇存槑 |
|------|------|------|
| GET | `/article/list` | 鏂囩珷鍒楄〃 (鍒嗛〉/绛涢€? |
| POST | `/article/create` | 鍒涘缓鏂囩珷 |
| POST | `/article/update/<id>` | 鏇存柊鏂囩珷 |
| POST | `/article/delete/<id>` | 鍒犻櫎鏂囩珷 |
| POST | `/article/publish/<id>` | 鍙戝竷鏂囩珷 |
| GET | `/article/drafts` | 鑽夌绠?|

### 绠＄悊鎺ュ彛
| 鏂规硶 | 璺緞 | 璇存槑 |
|------|------|------|
| GET | `/admin/users` | 鐢ㄦ埛鍒楄〃 |
| POST | `/admin/users/role` | 淇敼鐢ㄦ埛瑙掕壊 |
| POST | `/admin/users/status` | 鍚敤/绂佺敤鐢ㄦ埛 |
| GET | `/admin/tags` | 鏍囩鍒楄〃 |
| POST | `/admin/tags/create` | 鍒涘缓鏍囩 |
| PUT | `/admin/tags/<id>` | 鏇存柊鏍囩 |
| DELETE | `/admin/tags/<id>` | 鍒犻櫎鏍囩 |
| GET | `/admin/backup` | 澶囦唤绠＄悊椤甸潰 |
| POST | `/admin/backup/export` | 瀵煎嚭鏁版嵁 |
| POST | `/admin/backup/import` | 瀵煎叆鏁版嵁 |

### 鏁版嵁鎺ュ彛
| 鏂规硶 | 璺緞 | 璇存槑 |
|------|------|------|
| GET | `/api/stats` | 浠〃鐩樼粺璁℃暟鎹?|
| GET | `/api/trend` | 瓒嬪娍鏁版嵁 |
| GET | `/api/search` | 鎼滅储鎺ュ彛 |
| GET | `/api/export/csv` | 瀵煎嚭 CSV |
| GET | `/api/health` | 鍋ュ悍妫€鏌?|
| POST | `/api/batch` | 鎵归噺鎿嶄綔 |

## SQL 鎬ц兘浼樺寲

| 浼樺寲椤?| 瀹炵幇鏂瑰紡 |
|--------|----------|
| 澶嶅悎绱㈠紩 | `idx_user_login(username, is_active)` 鍔犻€熺櫥褰曟煡璇?|
| 鍒嗛〉闄愬埗 | `LIMIT` + `OFFSET`锛宍per_page` 鏈€澶?100 鏉?|
| N+1 棰勯槻 | `db.joinedload(Article.author)` 棰勫姞杞戒綔鑰呬俊鎭?|
| 杞垹闄?| `status` 瀛楁鏍囪锛宍deleted_at` 鏃堕棿鎴充繚鐣欐暟鎹?|
| 鑱氬悎浼樺寲 | `db.func.count()` / `db.func.sum()` 鑱氬悎鏌ヨ |
| 缂撳瓨绛栫暐 | 鐑棬鏍囩 5 鍒嗛挓鍐呭瓨缂撳瓨 |
| 绱㈠紩瑕嗙洊 | 鍙煡璇㈢储寮曞瓧娈碉紝閬垮厤鍥炶〃鏌ヨ |

## 15 澶╄凯浠ｅ紑鍙戞棩蹇?
璇﹁ [CHANGELOG.md](./CHANGELOG.md)

### Day 1-3锛氶」鐩垵濮嬪寲
- Flask 搴旂敤宸ュ巶妯″紡鎼缓
- 鏁版嵁搴撴ā鍨嬭璁′笌瀹炵幇
- 鐢ㄦ埛璁よ瘉绯荤粺鍩虹

### Day 4-6锛氭牳蹇冨姛鑳?- 鏂囩珷 CRUD 瀹屾暣瀹炵幇
- Markdown 缂栬緫鍣ㄩ泦鎴?- 鏍囩绠＄悊绯荤粺

### Day 7-9锛氭潈闄愪笌瀹夊叏
- RBAC 鏉冮檺鎺у埗
- CSRF 闃叉姢鏈哄埗
- 琛ㄥ崟楠岃瘉寮哄寲

### Day 10-12锛氭€ц兘浼樺寲
- SQL 鏌ヨ浼樺寲
- 鍐呭瓨缂撳瓨绯荤粺
- 鍒嗛〉缁勪欢浼樺寲

### Day 13-15锛氬彲瑙嗗寲涓庤繍缁?- ECharts 鍥捐〃闆嗘垚
- 鏁版嵁澶囦唤瀵煎嚭
- 鎿嶄綔鏃ュ織绯荤粺

## 寮€鍙戞寚鍗?
### 娣诲姞鏂拌矾鐢?```python
# backend/routes/new_module.py
from flask import Blueprint

new_bp = Blueprint('new', __name__)

@new_bp.route('/page')
def page():
    return render_template('new/page.html')
```

```python
# backend/app.py
from routes.new_module import new_bp
app.register_blueprint(new_bp, url_prefix='/new')
```

### 娣诲姞鏂版ā鍨?```python
# backend/models/new_model.py
from database import db

class NewModel(db.Model):
    __tablename__ = 'new_models'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
```

### 浣跨敤缂撳瓨
```python
from utils.cache import cached, invalidate_cache

@cached(timeout=300, key_prefix='data')
def get_data():
    # 鑰楁椂鎿嶄綔
    return result

# 娓呴櫎缂撳瓨
invalidate_cache('data:get_data')
```

## 璁稿彲璇?
鏈」鐩熀浜?[MIT License](./LICENSE) 寮€婧愩€?
## 鑷磋阿

- [SegmentFault](https://segmentfault.com/) - 鎻愪緵鏂囩珷鏁版嵁婧?- [Flask](https://flask.palletsprojects.com/) - Web 妗嗘灦
- [ECharts](https://echarts.apache.org/) - 鏁版嵁鍙鍖栧簱
