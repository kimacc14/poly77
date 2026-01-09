# 🚀 Railway Custom Domain - Quick Start Guide

## สรุปแบบเข้าใจง่าย

### ขั้นตอนที่ 1: ซื้อ Domain (5 นาที)

**เลือกที่ซื้อ:**

#### Namecheap (แนะนำ - ถูกที่สุด $8-12/year)
1. ไปที่: https://www.namecheap.com
2. ค้นหาชื่อ domain ที่ต้องการ (เช่น `poly-market.com`)
3. กด "Add to Cart" → "View Cart" → "Confirm Order"
4. สมัครบัญชี (หรือ login)
5. ชำระเงิน (Visa/Mastercard/PayPal/PromptPay)

**ตัวอย่างชื่อ domain ที่ดี:**
- `poly-market-ai.com`
- `prediction-analyzer.com`
- `market-sentiment.ai`
- `crypto-prediction-ai.com`

**ค้นหาชื่อว่าง:** https://www.namecheap.com/domains/domain-name-search/

---

### ขั้นตอนที่ 2: Upgrade Railway เป็น Hobby Plan ($5/month)

**ทำไมต้อง upgrade?**
- Railway Free tier **ไม่รองรับ custom domain**
- ต้อง Hobby Plan ($5/month) ขึ้นไป

**วิธี upgrade:**

1. ไปที่: https://railway.com/account/billing
2. คลิก **"Upgrade to Hobby"**
3. ใส่ข้อมูลบัตรเครดิต
4. Confirm ($5/month)

**ลิงก์ตรง:** https://railway.com/account/billing

---

### ขั้นตอนที่ 3: เพิ่ม Domain ใน Railway (2 นาที)

**ทาง 1: ผ่าน Railway CLI**

```bash
# เพิ่ม domain หลัก
railway domain add yourdomain.com

# เพิ่ม www subdomain
railway domain add www.yourdomain.com
```

**ทาง 2: ผ่าน Dashboard**

1. ไปที่ project: https://railway.com/project/77950b06-1505-4ce4-9198-d48dd25291a9
2. คลิก service: **poly77-ai-market-analyzer**
3. ไปที่แท็บ **"Settings"**
4. เลื่อนลงหา **"Domains"**
5. คลิก **"+ Custom Domain"**
6. ใส่ชื่อ domain: `yourdomain.com`
7. คลิก **"Add"**

Railway จะให้ CNAME record ที่ต้องตั้งค่า:
```
CNAME: poly77-ai-market-analyzer-production.up.railway.app
```

**ลิงก์ตรง:** https://railway.com/project/77950b06-1505-4ce4-9198-d48dd25291a9

---

### ขั้นตอนที่ 4: ตั้งค่า DNS ที่ผู้ให้บริการ Domain (5 นาที)

#### ถ้าซื้อจาก Namecheap:

1. Login: https://www.namecheap.com
2. ไป **"Domain List"** → คลิก **"Manage"** ที่ domain ของคุณ
3. เลือกแท็บ **"Advanced DNS"**
4. คลิก **"Add New Record"**

**เพิ่ม 2 records:**

**Record 1 (Root domain):**
```
Type: CNAME Record
Host: @
Value: poly77-ai-market-analyzer-production.up.railway.app
TTL: Automatic
```

**Record 2 (WWW subdomain):**
```
Type: CNAME Record
Host: www
Value: poly77-ai-market-analyzer-production.up.railway.app
TTL: Automatic
```

5. คลิก **"Save All Changes"**

**ลิงก์ตรง Namecheap DNS:** https://www.namecheap.com/myaccount/domain-list/

---

#### ถ้าซื้อจาก Cloudflare:

1. Login: https://dash.cloudflare.com
2. เลือก domain ของคุณ
3. ไปที่ **DNS** → **Records**
4. คลิก **"Add record"**

**เพิ่ม 2 records:**

```
Type: CNAME
Name: @
Target: poly77-ai-market-analyzer-production.up.railway.app
Proxy status: DNS only (gray cloud ☁️)
TTL: Auto
```

```
Type: CNAME
Name: www
Target: poly77-ai-market-analyzer-production.up.railway.app
Proxy status: DNS only (gray cloud ☁️)
TTL: Auto
```

**ลิงก์ตรง Cloudflare DNS:** https://dash.cloudflare.com

---

### ขั้นตอนที่ 5: รอ DNS Propagation (30 นาที - 2 ชั่วโมง)

DNS ต้องใช้เวลาแพร่กระจายไปทั่วโลก:
- **เร็วสุด:** 5-10 นาที
- **ปกติ:** 30 นาที - 2 ชั่วโมง
- **สูงสุด:** 24 ชั่วโมง (หายาก)

**เช็ค DNS status:**
```bash
# ตรวจสอบ DNS
dig yourdomain.com CNAME +short

# ควรจะแสดง:
# poly77-ai-market-analyzer-production.up.railway.app
```

**ออนไลน์:** https://dnschecker.org

---

### ขั้นตอนที่ 6: ตรวจสอบว่าทำงาน ✅

**ทดสอบ:**
```bash
# 1. Test domain resolves
curl -I https://yourdomain.com

# 2. Test in browser
open https://yourdomain.com
```

**ควรเห็น:**
- ✅ หน้า UI โหลดปกติ
- ✅ Markets data แสดงผล
- ✅ SSL certificate (🔒 สีเขียว)
- ✅ ไม่มี warning

---

## 💰 ค่าใช้จ่ายทั้งหมด

### รายเดือน:
- **Railway Hobby Plan:** $5/month

### รายปี:
- **Domain (.com):** $8-12/year (~$1/month)

**รวม:** ประมาณ **$6-7/month**

---

## 🎯 สรุปแบบเร็ว (Checklist)

- [ ] 1. ซื้อ domain จาก Namecheap/Cloudflare (~$10/year)
- [ ] 2. Upgrade Railway เป็น Hobby Plan ($5/month)
- [ ] 3. เพิ่ม custom domain ใน Railway dashboard
- [ ] 4. ตั้งค่า CNAME records ที่ผู้ให้บริการ domain:
  - [ ] `@` → `poly77-ai-market-analyzer-production.up.railway.app`
  - [ ] `www` → `poly77-ai-market-analyzer-production.up.railway.app`
- [ ] 5. รอ DNS propagation (30 นาที - 2 ชั่วโมง)
- [ ] 6. ทดสอบ: เปิด `https://yourdomain.com`
- [ ] 7. เช็ค SSL certificate (ควรเป็น 🔒 สีเขียว)

---

## 🔗 ลิงก์สำคัญ

### ซื้อ Domain:
- Namecheap: https://www.namecheap.com
- Cloudflare: https://www.cloudflare.com/products/registrar/

### Railway:
- Billing/Upgrade: https://railway.com/account/billing
- Your Project: https://railway.com/project/77950b06-1505-4ce4-9198-d48dd25291a9

### ตรวจสอบ DNS:
- DNS Checker: https://dnschecker.org
- What's My DNS: https://www.whatsmydns.net

---

## 🆘 ปัญหาที่พบบ่อย

### "Domain ไม่ทำงาน"
- รอ DNS propagation อีก 30-60 นาที
- ตรวจสอบ CNAME records ว่าตั้งค่าถูกต้อง
- ลอง clear browser cache (Ctrl+Shift+Del)

### "SSL Certificate Error"
- Railway ใช้เวลา 5-10 นาที สร้าง SSL certificate
- รอแล้วลองใหม่

### "Railway บอกว่าต้อง upgrade"
- Free tier ไม่รองรับ custom domain
- ต้อง upgrade เป็น Hobby Plan ($5/month)

---

## ✅ หลังสำเร็จแล้ว

App ของคุณจะเข้าถึงได้ที่:
- ✅ `https://yourdomain.com`
- ✅ `https://www.yourdomain.com`
- ✅ `https://poly77-ai-market-analyzer-production.up.railway.app` (ยังใช้ได้)

**ทั้ง 3 URLs จะชี้ไปที่ app เดียวกัน**

---

**Created:** January 9, 2026
**For:** poly77-ai-market-analyzer on Railway
