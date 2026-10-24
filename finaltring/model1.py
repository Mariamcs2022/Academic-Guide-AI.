import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, top_k_accuracy_score
import joblib

# تحميل البيانات النظيفة
df = pd.read_csv(r"genaraldatatDONE4.csv")

# تجهيز بيانات التدريب
X = df.drop(columns=["major", "Major_Group"])
y = df["Major_Group"]

# ترميز الهدف
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# تقسيم البيانات
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42
)

# تدريب الموديل
RandomForestmodel = RandomForestClassifier( max_depth=10 ,  random_state=42) #  تدريب اي اسم  وتخزين الخورزاميه بمتغير واستدعائه بالتدريب
RandomForestmodel.fit(X_train, y_train)   #  تدريب المودل المتغير اسمه مودل  #فت هو متغير التدريب 


y_pred = RandomForestmodel.predict(X_test) # التنبو
proba = RandomForestmodel.predict_proba(X_test)

top1_acc = accuracy_score(y_test, y_pred)
top2_acc = top_k_accuracy_score(y_test, proba, k=2)
top3_acc = top_k_accuracy_score(y_test, proba, k=3)

print(f" Top-1 Accuracy: {top1_acc:.4f}")
print(f" Top-2 Accuracy: {top2_acc:.4f}")
print(f" Top-3 Accuracy: {top3_acc:.4f}")


joblib.dump(RandomForestmodel, "college1_model.pkl")
joblib.dump(le, "label1_encoder.pkl")
print("Done Save")
