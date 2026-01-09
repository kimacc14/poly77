# 🚀 เชื่อม Domain จาก Hostinger กับ Railway

## สรุปขั้นตอน

1. ✅ ซื้อ domain จาก Hostinger
2. ✅ Upgrade Railway เป็น Hobby Plan ($5/month)
3. ✅ ตั้งค่า DNS ใน Hostinger
4. ✅ รอ DNS propagation (30 นาที - 2 ชั่วโมง)

---

## ขั้นตอนที่ 1: ซื้อ Domain จาก Hostinger

### ลิงก์ Hostinger:
- **Domain Search:** https://www.hostinger.com/domain-name-search
- **Hostinger Homepage:** https://www.hostinger.com

### ราคา:
- Domain `.com`: ประมาณ ฿100-300/year (ปีแรกมักลดราคา)
- ถูกกว่า Namecheap ถ้ามี promotion

### วิธีซื้อ:
1. ไปที่: https://www.hostinger.com/domain-name-search
2. ค้นหาชื่อ domain (เช่น `poly-market.com`)
3. Add to Cart → Checkout
4. สมัครบัญชี (หรือ login)
5. ชำระเงิน (บัตรเครดิต/PromptPay)

**แนะนำชื่อ domain:**
- `poly-market-ai.com`
- `prediction-analyzer.com`
- `market-mindshare.com`
- `crypto-prediction.ai`

---

## ขั้นตอนที่ 2: Upgrade Railway เป็น Hobby Plan

### ทำไมต้อง upgrade?
Railway Free tier **ไม่รองรับ custom domain**

### ลิงก์ตรง:
https://railway.com/account/billing

### วิธี upgrade:
1. ไปที่: https://railway.com/account/billing
2. คลิก **"Upgrade to Hobby"**
3. ใส่บัตรเครดิต
4. Confirm ($5/month)

**ค่าใช้จ่าย:**
- $5/month (ประมาณ ฿175/เดือน)

---

## ขั้นตอนที่ 3: เพิ่ม Domain ใน Railway

### ทาง 1: ผ่าน Railway Dashboard

1. ไปที่ project: https://railway.com/project/77950b06-1505-4ce4-9198-d48dd25291a9

2. คลิก service: **poly77-ai-market-analyzer**

3. ไปที่แท็บ **"Settings"**

4. เลื่อนลงหา **"Domains"** section

5. คลิก **"+ Custom Domain"**

6. ใส่ชื่อ domain ที่ซื้อจาก Hostinger:
   ```
   yourdomain.com
   ```

7. คลิก **"Add"**

Railway จะแสดง CNAME record ที่ต้องตั้งค่า:
```
CNAME Target: poly77-ai-market-analyzer-production.up.railway.app
```

**จดค่านี้ไว้** - จะใช้ตั้งค่าใน Hostinger

---

### ทาง 2: ผ่าน Railway CLI

```bash
# เพิ่ม domain หลัก
railway domain add yourdomain.com

# เพิ่ม www subdomain
railway domain add www.yourdomain.com
```

---

## ขั้นตอนที่ 4: ตั้งค่า DNS ใน Hostinger (สำคัญที่สุด!)

### 4.1 เข้าสู่ DNS Management

1. Login Hostinger: https://hpanel.hostinger.com

2. ไปที่ **"Domains"** (เมนูด้านซ้าย)

3. คลิก domain ที่ซื้อมา

4. คลิก **"DNS / Name Servers"** หรือ **"Manage DNS"**

---

### 4.2 ลบ Records เก่า (ถ้ามี)

ก่อนเพิ่ม CNAME ใหม่ ต้องลบ A records เก่าที่ชี้ไปที่ Hostinger parking page:

**ลบ records เหล่านี้ (ถ้ามี):**
- `A` record ที่ Host = `@` หรือว่าง
- `A` record ที่ Host = `www`

---

### 4.3 เพิ่ม CNAME Records สำหรับ Railway

คลิก **"Add Record"** และเพิ่ม 2 records:

#### Record 1: Root Domain (@)

⚠️ **หมายเหตุสำคัญ:** Hostinger อาจไม่รองรับ CNAME สำหรับ root domain (@)

**ถ้ารองรับ CNAME (ลองก่อน):**
```
Type: CNAME
Name: @
Target: poly77-ai-market-analyzer-production.up.railway.app
TTL: 3600 (หรือ Auto)
```

**ถ้าไม่รองรับ CNAME (ใช้ A record แทน):**

ต้อง resolve Railway domain เป็น IP ก่อน:
```bash
dig poly77-ai-market-analyzer-production.up.railway.app A +short
```

แล้วเพิ่ม A record:
```
Type: A
Name: @
Points to: [IP address จาก dig command]
TTL: 3600
```

#### Record 2: WWW Subdomain

```
Type: CNAME
Name: www
Target: poly77-ai-market-analyzer-production.up.railway.app
TTL: 3600 (หรือ Auto)
```

---

### 4.4 Save Changes

1. คลิก **"Save"** หรือ **"Add Record"**
2. ตรวจสอบว่า records ถูกบันทึก
3. อาจถาม confirmation - คลิก **"Confirm"**

---

## ขั้นตอนที่ 5: รอ DNS Propagation

DNS ต้องใช้เวลาแพร่กระจาย:
- **เร็วสุด:** 10-30 นาที
- **ปกติ:** 1-2 ชั่วโมง
- **สูงสุด:** 24-48 ชั่วโมง (หายาก)

### ตรวจสอบ DNS Status

**วิธีที่ 1: Command Line**
```bash
# ตรวจสอบ CNAME record
dig www.yourdomain.com CNAME +short

# ควรแสดง:
# poly77-ai-market-analyzer-production.up.railway.app

# ตรวจสอบ IP
dig yourdomain.com A +short
```

**วิธีที่ 2: Online Tools**
- DNS Checker: https://dnschecker.org
- What's My DNS: https://www.whatsmydns.net

---

## ขั้นตอนที่ 6: ตรวจสอบว่าใช้งานได้

### ทดสอบด้วย Browser:

1. เปิด: `https://yourdomain.com`
2. ควรเห็น UI ของ AI Market Analyzer
3. ตรวจสอบ SSL certificate (🔒 สีเขียว)

### ทดสอบด้วย Command:

```bash
# Test HTTP response
curl -I https://yourdomain.com

# ควรได้ HTTP 200 OK

# Test API endpoint
curl https://yourdomain.com/health
```

---

## 🐛 Troubleshooting

### ปัญหา 1: "CNAME record ไม่รองรับ root domain (@)"

**วิธีแก้:**

1. หา IP address ของ Railway:
   ```bash
   dig poly77-ai-market-analyzer-production.up.railway.app A +short
   ```

2. ใช้ A record แทน CNAME:
   ```
   Type: A
   Name: @
   Points to: [IP address]
   ```

**หรือใช้ Cloudflare CNAME Flattening:**
1. Transfer nameservers ไป Cloudflare
2. Cloudflare รองรับ CNAME สำหรับ root domain

---

### ปัญหา 2: "Domain ไม่ทำงาน"

**เช็คว่า:**
- ✅ Railway upgrade เป็น Hobby Plan แล้ว
- ✅ DNS records ตั้งค่าถูกต้อง (ไม่มี typo)
- ✅ รอ DNS propagation ไปแล้ว 30+ นาที
- ✅ Clear browser cache (Ctrl+Shift+Del)

---

### ปัญหา 3: "SSL Certificate Error"

**สาเหตุ:**
Railway ใช้เวลา 5-10 นาที สร้าง SSL certificate หลัง DNS propagation

**วิธีแก้:**
- รอ 10-15 นาที
- ลอง hard refresh (Ctrl+Shift+R)
- ตรวจสอบใน Railway dashboard ว่า domain verified

---

### ปัญหา 4: "ชี้ไปที่ Hostinger Parking Page"

**สาเหตุ:**
ยังมี A record เก่าชี้ไปที่ Hostinger

**วิธีแก้:**
1. กลับไปที่ Hostinger DNS Management
2. ลบ A records ทั้งหมดที่ชี้ไปที่ Hostinger IP
3. เหลือแค่ CNAME records ที่ชี้ไปที่ Railway

---

## 📋 สรุป DNS Records ที่ต้องตั้งค่า

### ตาราง DNS Records:

| Type | Name | Target/Value | TTL |
|------|------|--------------|-----|
| A | @ | [Railway IP] | 3600 |
| CNAME | www | poly77-ai-market-analyzer-production.up.railway.app | 3600 |

**หรือ (ถ้า Hostinger รองรับ CNAME root):**

| Type | Name | Target/Value | TTL |
|------|------|--------------|-----|
| CNAME | @ | poly77-ai-market-analyzer-production.up.railway.app | 3600 |
| CNAME | www | poly77-ai-market-analyzer-production.up.railway.app | 3600 |

---

## 💰 ค่าใช้จ่ายรวม

### Hostinger:
- **Domain:** ~฿100-300/year (ปีแรก)
- **Renewal:** ~฿400-600/year

### Railway:
- **Hobby Plan:** $5/month (~฿175/month)

### รวมต่อเดือน:
- ประมาณ **฿200-250/month**

---

## 🔗 ลิงก์สำคัญ

### Hostinger:
- **Login/Dashboard:** https://hpanel.hostinger.com
- **Domain Search:** https://www.hostinger.com/domain-name-search

### Railway:
- **Billing/Upgrade:** https://railway.com/account/billing
- **Your Project:** https://railway.com/project/77950b06-1505-4ce4-9198-d48dd25291a9

### DNS Tools:
- **DNS Checker:** https://dnschecker.org
- **What's My DNS:** https://www.whatsmydns.net

---

## ✅ Checklist

หลังซื้อ domain จาก Hostinger แล้ว:

- [ ] 1. ซื้อ domain สำเร็จ (เช็ค email confirmation)
- [ ] 2. Upgrade Railway เป็น Hobby Plan
- [ ] 3. เพิ่ม custom domain ใน Railway dashboard
- [ ] 4. Login Hostinger → Domains → DNS Management
- [ ] 5. ลบ A records เก่าที่ชี้ไปที่ Hostinger
- [ ] 6. เพิ่ม CNAME/A record สำหรับ `@` (root)
- [ ] 7. เพิ่ม CNAME record สำหรับ `www`
- [ ] 8. Save changes ใน Hostinger
- [ ] 9. รอ DNS propagation (30 นาที - 2 ชั่วโมง)
- [ ] 10. ทดสอบ: `https://yourdomain.com`
- [ ] 11. เช็ค SSL certificate (🔒)
- [ ] 12. ทดสอบ API endpoints

---

## 🎉 หลังสำเร็จ

App จะเข้าถึงได้ผ่าน:
- ✅ `https://yourdomain.com` (domain ใหม่ของคุณ)
- ✅ `https://www.yourdomain.com` (www subdomain)
- ✅ `https://poly77-ai-market-analyzer-production.up.railway.app` (Railway URL เดิม - ยังใช้ได้)

---

**ถ้าติดปัญหาตรงไหน บอกได้เลยครับ จะช่วยแก้ให้! 🚀**

---

**Created:** January 9, 2026
**For:** poly77-ai-market-analyzer on Railway + Hostinger Domain
