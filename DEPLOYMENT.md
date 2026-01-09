# 🚀 Deployment Guide - Railway.app

## ทำไมเลือก Railway?

✅ **ง่ายที่สุด** - Push code แล้วจบ, ไม่ต้อง config เยอะ
✅ **ฟรี 500 ชั่วโมง/เดือน** - พอสำหรับ side project
✅ **ไม่มี Cold Start** - รันตลอด 24/7
✅ **รองรับ AI Model** - Memory 8GB (ฟรี tier 1GB แต่พอใช้)
✅ **Auto Deploy** - เชื่อม GitHub แล้ว deploy อัตโนมัติ

---

## 📋 ขั้นตอนการ Deploy (5 นาที)

### 1️⃣ สร้าง Reddit API Credentials (ถ้ายังไม่มี)

1. ไปที่ https://www.reddit.com/prefs/apps
2. กด **"create another app..."**
3. เลือก **"script"**
4. ตั้งชื่อ: `AI-Mindshare-Analyzer`
5. Redirect URI: `http://localhost:8080`
6. กด **Create app**
7. เก็บ:
   - `client_id` (ข้างล่างชื่อ app)
   - `client_secret` (ข้อความที่เห็น secret)

---

### 2️⃣ Push Code ไปที่ GitHub

```bash
# ใน terminal ที่ /Users/mac/Documents/claude/poly77

# เพิ่มไฟล์ทั้งหมด
git add .

# Commit
git commit -m "Deploy to Railway"

# สร้าง repo ใหม่บน GitHub แล้ว push
git remote add origin https://github.com/<your-username>/<repo-name>.git
git branch -M main
git push -u origin main
```

---

### 3️⃣ Deploy บน Railway

1. **Sign up/Login**: ไปที่ [railway.app](https://railway.app)
   - Login ด้วย GitHub account

2. **New Project**:
   - กด **"New Project"**
   - เลือก **"Deploy from GitHub repo"**
   - เลือก repository ที่เพิ่ง push

3. **Auto Detection**:
   - Railway จะอ่าน `Procfile` และ `requirements.txt` อัตโนมัติ
   - เริ่ม build (ใช้เวลา 5-10 นาที ครั้งแรก เพราะต้องดาวน์โหลด AI model)

4. **Set Environment Variables**:
   - ไปที่ **Variables** tab
   - เพิ่ม:
     ```
     REDDIT_CLIENT_ID=<your_client_id>
     REDDIT_CLIENT_SECRET=<your_client_secret>
     REDDIT_USER_AGENT=AI-Mindshare-Analyzer/1.0
     ```

5. **Generate Domain**:
   - ไปที่ **Settings** tab
   - กด **Generate Domain**
   - จะได้ URL เช่น `https://poly77.up.railway.app`

6. **เสร็จแล้ว!** 🎉
   - เปิด URL ที่ได้
   - ระบบจะรัน Frontend + Backend ในที่เดียว

---

## 🔧 Config ที่สำคัญ

### ไฟล์ที่ Railway ใช้:

1. **`requirements.txt`** - Python dependencies
2. **`Procfile`** - คำสั่งรัน app
   ```
   web: cd backend && uvicorn production_server:app --host 0.0.0.0 --port $PORT
   ```
3. **`railway.json`** - Railway config (optional)
4. **`runtime.txt`** - Python version
   ```
   python-3.12.4
   ```

---

## 📊 Free Tier Limits

| Resource | Free Tier | หมายเหตุ |
|----------|-----------|----------|
| **Hours** | 500 ชม./เดือน | ~16 ชม./วัน |
| **Memory** | 1 GB | พอสำหรับ RoBERTa model |
| **CPU** | Shared | เร็วพอ |
| **Storage** | 100 GB | เหลือเฟือ |
| **Bandwidth** | 100 GB | เหลือเฟือ |

**Tips**:
- ถ้าใช้เกิน 500 ชม. → Upgrade เป็น $5/เดือน (ไม่จำกัด)
- ถ้า Memory ไม่พอ → ลดขนาด model หรือ upgrade

---

## ⚙️ Environment Variables ที่ต้องตั้ง

```bash
# Required
REDDIT_CLIENT_ID=your_client_id_here
REDDIT_CLIENT_SECRET=your_secret_here
REDDIT_USER_AGENT=AI-Mindshare-Analyzer/1.0

# Optional
KALSHI_API_KEY=                    # ไม่ใส่ก็ได้
PORT=8002                          # Railway จะ set ให้เอง
```

---

## 🐛 Troubleshooting

### ❌ Build Failed

**ปัญหา**: `requirements.txt not found`
- **แก้**: ตรวจสอบว่า `requirements.txt` อยู่ที่ root folder

**ปัญหา**: `torch installation failed`
- **แก้**: ใช้เวลานาน (~5 นาที) รอให้จบ

### ❌ App Crashed

**ปัญหา**: `Memory limit exceeded`
- **แก้**: Upgrade Railway plan หรือลดขนาด model

**ปัญหา**: `Module not found`
- **แก้**: ตรวจสอบ import paths ใน `production_server.py`

### ✅ Check Logs

ใน Railway dashboard:
- ไปที่ **Deployments** tab
- กด deployment ล่าสุด
- ดู **Build Logs** และ **Deploy Logs**

---

## 🔄 Auto Deploy

หลัง setup เสร็จ:
- Push code ใหม่ไปที่ GitHub → Railway deploy อัตโนมัติ
- ไม่ต้องทำอะไรเพิ่ม

```bash
git add .
git commit -m "Update features"
git push
# Railway จะ deploy ให้อัตโนมัติ
```

---

## 📱 Access Your App

หลัง deploy เสร็จ:
1. เปิด URL ที่ Railway ให้มา (เช่น `https://poly77.up.railway.app`)
2. Frontend และ Backend รันในที่เดียว
3. ไม่ต้อง config CORS เพิ่ม

---

## 💡 Tips

1. **ตั้งชื่อ Service**: ใน Settings → Rename service เป็นชื่อที่จำง่าย
2. **Monitor Usage**: ตรวจสอบ Hours ที่ใช้ไปที่ **Metrics** tab
3. **Custom Domain**: Upgrade plan ถ้าต้องการใช้ domain ของตัวเอง
4. **Database**: Railway มี PostgreSQL, Redis ถ้าต้องการในอนาคต

---

## 🆚 Alternative: Render.com

ถ้า Railway ไม่เวิร์ค ลอง **Render.com** (ฟรีเหมือนกัน):

1. ไปที่ [render.com](https://render.com)
2. New → Web Service → Connect GitHub
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `cd backend && uvicorn production_server:app --host 0.0.0.0 --port $PORT`

**ข้อแตกต่าง**:
- ❌ มี Cold Start (sleep หลัง 15 นาที ไม่ใช้งาน)
- ✅ ฟรีไม่มีขอบเขตเวลา
- ⚡ ตื่นใช้เวลา ~1 นาที

---

## 📞 Support

ถ้ามีปัญหา:
1. เช็ค Logs ใน Railway dashboard
2. ดู troubleshooting ข้างบน
3. Open issue บน GitHub

---

## ✨ เสร็จแล้ว!

Deploy แล้วได้ URL:
```
https://your-app.up.railway.app
```

แชร์ให้เพื่อนใช้ได้เลยครับ! 🚀
