from flask import Flask, render_template, request, flash, redirect, url_for , session
import sqlite3
import os
import json
from form import RegistrationAdmin , LoginAdmin
from werkzeug.security import generate_password_hash, check_password_hash
import joblib
import numpy as np
from dotenv import load_dotenv
load_dotenv()  # تحميل متغيرات البيئة من ملف .env

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "database2.db")
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")

COLLEGES_SEED = [
("medical-sciences","كلية العلوم الطبية","مسارات الرعاية الصحية والعلوم الطبية وخدمة المجتمع.","تجمع المجالات الصحية المعرفة العلمية والتطبيق العملي للمساهمة في الوقاية والتشخيص والعلاج وتحسين جودة الحياة.",["الطب","طب الأسنان","الصيدلة","التمريض","العلوم الصحية","علوم المختبرات الطبية","المعلوماتية الصحية","التغذية السريرية","العلاج الطبيعي","الصحة العامة"],["الأحياء","الكيمياء","التشريح ووظائف الأعضاء","مبادئ الصحة العامة"],"images/medical.jpg"),
("computer-science-engineering","كلية علوم وهندسة الحاسب","التقنية والبرمجة والبيانات والأمن السيبراني.","تركز مجالات الحوسبة على تصميم البرمجيات والأنظمة وتحليل البيانات وحماية المعلومات وبناء الحلول التقنية.",["علوم الحاسب","هندسة البرمجيات","الأمن السيبراني","الذكاء الاصطناعي","علم البيانات","تقنية المعلومات","هندسة الحاسب","الشبكات"],["البرمجة","الرياضيات","قواعد البيانات","الشبكات","أمن المعلومات"],"images/O.webp"),
("business-administration","كلية إدارة الأعمال","الإدارة والتسويق والمحاسبة والتمويل وريادة الأعمال.","تساعد مجالات الأعمال على فهم المؤسسات والأسواق واتخاذ القرارات وتنظيم الموارد وإدارة المشاريع.",["إدارة الأعمال","التسويق","المحاسبة","المالية","الموارد البشرية","التجارة الإلكترونية","التأمين وإدارة المخاطر","المالية والاستثمار","نظم المعلومات الإدارية","إدارة سلسلة الإمداد"],["مبادئ الإدارة","المحاسبة","الاقتصاد","التسويق","الإحصاء"],"images/educacion.jpg"),
("sciences","كلية العلوم","العلوم الأساسية والبحث والتحليل والتجارب.","تقدم العلوم الأساسية طرقًا لفهم الظواهر الطبيعية وتحليلها من خلال التجارب والنماذج والبحث العلمي.",["الكيمياء","الفيزياء","الأحياء","الرياضيات"],["الرياضيات","الإحصاء","المختبرات العلمية","منهجية البحث"],"images/high-school-math-comp.webp"),
("humanities-arts","كلية الآداب والعلوم الإنسانية","اللغة والثقافة والمجتمع والتواصل والإبداع.","تدرس هذه المجالات الإنسان واللغة والثقافة والمجتمع، وتفتح مسارات في التعليم والبحث والإعلام والترجمة.",["التاريخ","الأدب","علم النفس","علم الاجتماع","الخدمة الاجتماعية","اللغة العربية","اللغة الإنجليزية","الترجمة","الإعلام الرقمي","الفنون الجميلة","التربية البدنية"],["الكتابة والتحرير","اللغة","مناهج البحث","دراسة المجتمع والثقافة"],"images/teatchar2.jpg"),
("law","كلية القانون","الأنظمة والحقوق والتحليل القانوني والعدالة.","تهتم مجالات القانون بفهم الأنظمة والحقوق والإجراءات القانونية، وقد تختلف البرامج بين الجامعات.",["القانون","الشريعة","الدراسات الإسلامية"],["مبادئ القانون","الأنظمة","مهارات البحث القانوني","الكتابة القانونية"],"images/Online.png"),
("engineering","كلية الهندسة","تصميم الحلول الهندسية وتحليل الأنظمة والبنية التحتية.","تجمع الهندسة بين الرياضيات والعلوم والتصميم لحل المشكلات العملية وتطوير المنتجات والأنظمة والبنية التحتية.",["الهندسة المدنية","الهندسة الميكانيكية","الهندسة الكهربائية","الهندسة الصناعية","العمارة","التصميم الداخلي","هندسة الطاقة المتجددة","هندسة الأنظمة الميكانيكية"],["الرياضيات","الفيزياء","الرسم الهندسي","التصميم","حل المشكلات"],"images/03.png")
]

def init_database():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.execute("CREATE TABLE IF NOT EXISTS student_feedback (id INTEGER PRIMARY KEY AUTOINCREMENT, feedback_text TEXT NOT NULL, date TEXT NOT NULL DEFAULT (DATE('now')))")
    conn.execute("CREATE TABLE IF NOT EXISTS counter (id INTEGER PRIMARY KEY, visits INTEGER NOT NULL DEFAULT 0)")
    conn.execute("INSERT OR IGNORE INTO counter (id, visits) VALUES (1, 0)")
    conn.execute("CREATE TABLE IF NOT EXISTS resulte (id INTEGER PRIMARY KEY AUTOINCREMENT, resulte_text TEXT, date TEXT)")
    conn.execute("""CREATE TABLE IF NOT EXISTS colleges (
        id INTEGER PRIMARY KEY AUTOINCREMENT, slug TEXT NOT NULL UNIQUE, name TEXT NOT NULL UNIQUE,
        short_description TEXT NOT NULL DEFAULT '', description TEXT NOT NULL DEFAULT '',
        majors_json TEXT NOT NULL DEFAULT '[]', subjects_json TEXT NOT NULL DEFAULT '[]',
        image_path TEXT NOT NULL DEFAULT 'images/graduation-cap-sits.webp',
        official_url TEXT, source_url TEXT, is_active INTEGER NOT NULL DEFAULT 1,
        created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)""")
    cols={row[1] for row in conn.execute("PRAGMA table_info(colleges)")}
    if "subjects_json" not in cols:
        conn.execute("ALTER TABLE colleges ADD COLUMN subjects_json TEXT NOT NULL DEFAULT '[]'")
    for slug,name,short,desc,majors,subjects,image in COLLEGES_SEED:
        conn.execute("""INSERT OR IGNORE INTO colleges
        (slug,name,short_description,description,majors_json,subjects_json,image_path,official_url,source_url,is_active)
        VALUES (?,?,?,?,?,?,?,?,?,1)""",(slug,name,short,desc,json.dumps(majors,ensure_ascii=False),json.dumps(subjects,ensure_ascii=False),image,"https://www.moe.gov.sa/","https://www.moe.gov.sa/"))
    conn.commit(); conn.close()

init_database()

# تحميل الموديلل واـ LabelEncoder 
model = joblib.load(os.path.join(BASE_DIR, "Model", "college1_model.pkl"))
le = joblib.load(os.path.join(BASE_DIR, "Model", "label1_encoder.pkl"))

#   عباره عن قاموس ولسته خريطة التخصصات
college_majors = {
    "كلية العلوم الطبية": [
        "الطب", "طب الأسنان", "الصيدلة", "التمريض",
        "العلوم الصحية", "علوم المختبرات الطبية",
        "المعلوماتية الصحية", "التغذية السريرية",
        "العلاج الطبيعي", "الصحة العامة"
    ],

    "كلية علوم وهندسة الحاسب": [
        "علوم الحاسب", "هندسة البرمجيات", "الأمن السيبراني",
        "الذكاء الاصطناعي", "علم البيانات", "تقنية المعلومات",
        "هندسة الحاسب", "الشبكات"
    ],

    "كلية إدارة الأعمال": [
        "إدارة الأعمال", "التسويق", "المحاسبة", "المالية",
        "الموارد البشرية", "التجارة الإلكترونية", "التأمين وإدارة المخاطر",
        "المالية والاستثمار", "نظم المعلومات الإدارية",
        "إدارة سلسلة الإمداد"
    ],

    "كلية العلوم": [
        "الكيمياء", "الفيزياء", "الأحياء", "الرياضيات"
    ],

    "كلية الآداب والعلوم الإنسانية": [
        "التاريخ", "الأدب", "علم النفس", "علم الاجتماع",
        "الخدمة الاجتماعية", "اللغة العربية", "اللغة الإنجليزية",
        "الترجمة", "الإعلام الرقمي", "الفنون الجميلة", "التربية البدنية"
    ],

    "كلية القانون": [
        "القانون", "الشريعة", "الدراسات الإسلامية"
    ],

    "كلية الهندسة": [
        "الهندسة المدنية", "الهندسة الميكانيكية",
        "الهندسة الكهربائية", "الهندسة الصناعية",
        "العمارة", "التصميم الداخلي",
        "هندسة الطاقة المتجددة", "هندسة الأنظمة الميكانيكية"
    ]
}

# 🔹 الصفحة الرئيسية
@app.route("/")
def home():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor() 
    cursor.execute("SELECT visits FROM counter WHERE id = 1")
    row = cursor.fetchone()
    visits = row[0] if row else 0
    conn.row_factory = sqlite3.Row
    colleges = conn.execute("SELECT slug, name, short_description, image_path FROM colleges WHERE is_active = 1 ORDER BY name").fetchall()
    conn.close()
    return render_template("Home.html", visits=visits, colleges=colleges)


@app.route("/colleges")
def colleges_page():
    conn=sqlite3.connect(DATABASE_PATH); conn.row_factory=sqlite3.Row
    colleges=conn.execute("SELECT slug,name,short_description,image_path FROM colleges WHERE is_active=1 ORDER BY name").fetchall()
    conn.close()
    return render_template("colleges.html", colleges=colleges)

@app.route("/colleges/<slug>")
def college_details(slug):
    conn=sqlite3.connect(DATABASE_PATH); conn.row_factory=sqlite3.Row
    row=conn.execute("SELECT * FROM colleges WHERE slug=? AND is_active=1",(slug,)).fetchone()
    conn.close()
    if row is None:
        from flask import abort
        abort(404)
    college=dict(row)
    college["majors"]=json.loads(college.get("majors_json") or "[]")
    college["subjects"]=json.loads(college.get("subjects_json") or "[]")
    return render_template("college_details.html", college=college)


@app.route('/start_test')
def start_test():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE counter SET visits = visits + 1 WHERE id=1")
    conn.commit()
    conn.close()

    return "OK"
# تسجيل جديد (مشرفين)
@app.route("/radmin", methods=['GET', 'POST'])
def radmin():
    form = RegistrationAdmin()
    if form.validate_on_submit():
        return redirect(url_for('dashboard'))
    
    return render_template("radmin.html", form=form)


#  تسجيل الدخول (مشرفين)
@app.route("/ladmin", methods=['GET', 'POST'])
def ladmin():
    form = LoginAdmin()

    if form.validate_on_submit():
        return redirect(url_for('dashboard'))
    
    return render_template("ladmin.html", form=form)

@app.route("/dashboard")
def dashboard():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # عدد النتائج
    cursor.execute("SELECT COUNT(*) FROM resulte")
    total_results = cursor.fetchone()[0]

    # عدد الآراء
    cursor.execute("SELECT COUNT(*) FROM student_feedback")
    total_feedbacks = cursor.fetchone()[0]

    # جميع الكليات مع عدد الترشيحات (للجدول)
    cursor.execute("""
        SELECT resulte_text, COUNT(*) as count 
        FROM resulte 
        GROUP BY resulte_text 
        ORDER BY count DESC
    """)
    result_stats = cursor.fetchall()

    # أكثر كلية ترشيحًا
    top_college = result_stats[0][0] if result_stats else "—"

    # أقل كلية ترشيحًا
    cursor.execute("""
        SELECT resulte_text, COUNT(*) as count
        FROM resulte
        GROUP BY resulte_text
        ORDER BY count ASC
        LIMIT 1
    """)
    lowest_college = cursor.fetchone()
    lowest_college = lowest_college[0] if lowest_college else "—"

    # آخر 5 آراء
    cursor.execute("""
        SELECT feedback_text, date 
        FROM student_feedback 
        ORDER BY date DESC 
        LIMIT 5
    """)
    feedbacks = cursor.fetchall()

    conn.close()

    return render_template(
        "dashboard.html",
        total_results=total_results,
        total_feedbacks=total_feedbacks,
        result_stats=result_stats,
        top_college=top_college,
        lowest_college=lowest_college,
        feedbacks=feedbacks
    )
    
@app.route("/informtion")
def informtion():
    return render_template("informtion.html")


@app.route("/feedback", methods=["POST"])
def feedback():
    feedback_text=(request.form.get("message") or "").strip()
    if not feedback_text:
        flash("اكتبي ملاحظتك قبل الإرسال.", "error")
        return redirect(url_for("home"))
    conn=sqlite3.connect(DATABASE_PATH)
    try:
        conn.execute("INSERT INTO student_feedback (feedback_text, date) VALUES (?, DATE('now'))",(feedback_text,))
        conn.commit()
    except sqlite3.Error:
        conn.rollback()
        app.logger.exception("تعذر حفظ ملاحظة الطالب")
        flash("تعذر حفظ الملاحظة الآن. حاولي مرة أخرى.", "error")
        return redirect(url_for("home"))
    finally:
        conn.close()
    flash("شكرًا لك! تم إرسال ملاحظتك بنجاح.", "success")
    return redirect(url_for("home"))



#  صفحة الفورم 
@app.route("/Forms", methods=['GET'])
def form():
    return render_template("form.html")

college_mapping = {
    "College of Medical Sciences": "كلية العلوم الطبية",
    "College of Computer Science and Engineering": "كلية علوم وهندسة الحاسب",
    "College of Business Administration": "كلية إدارة الأعمال",
    "College of Sciences": "كلية العلوم",
    "College of Humanities and Arts": "كلية الآداب والعلوم الإنسانية",
    "College of Law": "كلية القانون",
    "College of Engineering": "كلية الهندسة"
}

@app.route("/predict", methods=["POST"])
def predict(): #  تحويل الاجابات الا ارقام بالقاموس 
    text_to_int = {
        "Never": 1, #key , values
        "Rarely": 2,
        "Sometimes": 3,
        "Often": 4,
        "Always": 5
    }
    # استلام الإجابات من الفورم 
    answers = []
    for i in range(20):
        value = request.form.get(f"q{i}") # q  من 0 حتئ 19
        if value is None:
            value = "Sometimes"   # الافتراضي لو ما جاوب
        answers.append(text_to_int[value])

    # عشان احولها مصفوفه 
    X = np.array([answers]) 

    # توقع أفضل 3 كليات
    probs = model.predict_proba(X)[0] # التنبئ بالمصفوفه
    top3_idx = np.argsort(probs)[-3:][::-1] # ترتيب 
    top3_encoded = model.classes_[top3_idx] #  يقراهاالمودل 
    top3_colleges = le.inverse_transform(top3_encoded) # تحويل لنصوص
# ترجمة الكليات للعربي
    top3_colleges_ar = [college_mapping.get(c, c) for c in top3_colleges]
    # تجهيز النتيجة للعرض
    results = []
    for i in top3_colleges:
          college_ar = college_mapping.get(i, i)
          results.append({
            "college": college_ar,
            "majors": college_majors.get(college_ar, []),
            "slug": {"كلية العلوم الطبية":"medical-sciences","كلية علوم وهندسة الحاسب":"computer-science-engineering","كلية إدارة الأعمال":"business-administration","كلية العلوم":"sciences","كلية الآداب والعلوم الإنسانية":"humanities-arts","كلية القانون":"law","كلية الهندسة":"engineering"}.get(college_ar)
    })

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    for college_ar in top3_colleges_ar:
       cursor.execute(
        "INSERT INTO resulte (resulte_text, date) VALUES (?, DATE('now'))",
        (college_ar,)
    )

    conn.commit()
    conn.close()
    return render_template("result.html", results=results)

if __name__ == "__main__": # انشاء الاتصال 
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1") 


