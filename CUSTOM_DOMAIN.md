# 🌐 Custom Domain Setup - Railway

## เลือกซื้อ Domain

### ที่แนะนำ (ราคาถูก):

| Provider | ราคา/ปี | Link |
|----------|---------|------|
| **Namecheap** | ~$9-12 (.com) | [namecheap.com](https://www.namecheap.com) |
| **Cloudflare** | ~$10-11 (.com) | [cloudflare.com/domains](https://www.cloudflare.com/products/registrar/) |
| **Porkbun** | ~$10 (.com) | [porkbun.com](https://porkbun.com) |
| **GoDaddy** | ~$15-20 (.com) | [godaddy.com](https://www.godaddy.com) |

**แนะนำ**: Namecheap หรือ Cloudflare (ราคาดี, จัดการง่าย)

---

## ขั้นตอนการเชื่อม Custom Domain

### 1️⃣ Upgrade Railway Plan

1. ไปที่ Railway dashboard
2. Settings → Billing
3. Upgrade เป็น **Developer Plan** ($5/เดือน)
   - Unlimited hours
   - Custom domains
   - 8 GB RAM
   - Priority support

---

### 2️⃣ เพิ่ม Custom Domain ใน Railway

1. ไปที่ project ของคุณ
2. เลือก service (web service)
3. Settings → Domains
4. กด **+ Custom Domain**
5. ใส่ domain เช่น: `aimarket.com` หรือ `www.aimarket.com`
6. Railway จะให้ข้อมูล DNS records:

```
Type: CNAME
Name: www (หรือ @)
Value: xxxx.up.railway.app
```

---

### 3️⃣ ตั้งค่า DNS ที่ Domain Provider

#### ตัวอย่าง: Namecheap

1. Login → Domain List → Manage
2. Advanced DNS
3. เพิ่ม record ใหม่:

**สำหรับ www.aimarket.com**:
```
Type: CNAME Record
Host: www
Value: xxxx.up.railway.app
TTL: Automatic
```

**สำหรับ aimarket.com (root domain)**:
```
Type: ALIAS Record (หรือ CNAME Flattening)
Host: @
Value: xxxx.up.railway.app
TTL: Automatic
```

**หมายเหตุ**: ถ้า provider ไม่รองรับ ALIAS record สำหรับ root domain:
- ใช้แค่ `www.aimarket.com`
- หรือใช้ Cloudflare (รองรับ CNAME flattening)

---

### 4️⃣ รอ DNS Propagation

- ใช้เวลา **15 นาที - 48 ชั่วโมง**
- ปกติ ~1-2 ชั่วโมง ก็ใช้งานได้แล้ว

เช็คสถานะ:
- เปิด https://dnschecker.org
- ใส่ domain ของคุณ
- ดูว่า propagate ไปทั่วโลกแล้วหรือยัง

---

### 5️⃣ SSL Certificate (HTTPS)

Railway จัดการให้อัตโนมัติ:
- ✅ Free SSL certificate จาก Let's Encrypt
- ✅ Auto-renewal
- ✅ Forced HTTPS redirect

**ไม่ต้องทำอะไรเพิ่ม** - Railway setup ให้หมด

---

## 💡 ทางเลือกอื่น: ใช้ Cloudflare (แนะนำ)

### ทำไมควรใช้ Cloudflare

1. **ฟรี CDN** - เว็บเร็วขึ้น
2. **DDoS Protection** - ป้องกันการโจมตี
3. **Analytics** - ดูสถิติผู้เข้าชม
4. **CNAME Flattening** - รองรับ root domain
5. **Cache** - ลด load บน server

### Setup กับ Cloudflare

#### 1. เพิ่ม Site ใน Cloudflare
1. ไปที่ [cloudflare.com](https://www.cloudflare.com)
2. Add a Site → ใส่ domain ของคุณ
3. เลือก Free Plan
4. Cloudflare จะ scan DNS records

#### 2. เปลี่ยน Nameservers
ที่ domain provider (Namecheap/GoDaddy):
1. Domain Settings → Nameservers
2. Custom Nameservers
3. ใส่ที่ Cloudflare ให้มา:
   ```
   ns1.cloudflare.com
   ns2.cloudflare.com
   ```

#### 3. เพิ่ม DNS Records ใน Cloudflare
```
Type: CNAME
Name: @
Target: xxxx.up.railway.app
Proxy: Enabled (orange cloud)

Type: CNAME
Name: www
Target: xxxx.up.railway.app
Proxy: Enabled (orange cloud)
```

#### 4. SSL/TLS Settings
- SSL/TLS → Full (Strict)
- Always Use HTTPS → On
- Automatic HTTPS Rewrites → On

---

## 📊 ต้นทุนรวม

### ตัวเลือก 1: Railway + Free Subdomain
```
Railway Free Tier: $0/เดือน (500 ชม.)
Domain: ฟรี (.up.railway.app)
SSL: ฟรี

รวม: $0/เดือน
```

### ตัวเลือก 2: Railway + Custom Domain
```
Railway Developer: $5/เดือน
Domain (Namecheap): ~$1/เดือน ($12/ปี)
SSL: ฟรี (Let's Encrypt)
Cloudflare (Optional): ฟรี

รวม: ~$6/เดือน
```

---

## 🎯 คำแนะนำ

### เริ่มต้น (ทดสอบ):
✅ ใช้ **Railway Free + Subdomain ฟรี**
- ไม่ต้องจ่ายเงิน
- ได้ URL ใช้งานได้เลย: `https://poly77.up.railway.app`
- ทดสอบ features ได้เต็มที่

### จริงจัง (Production):
✅ **Railway Developer + Custom Domain + Cloudflare**
- ดูโปรมากกว่า
- SEO ดีกว่า
- Performance ดีขึ้น (CDN)
- ค่าใช้จ่าย ~$6/เดือน

---

## ⚠️ Tips

1. **ชื่อ Domain**:
   - สั้น, จำง่าย
   - เกี่ยวกับ AI/Markets
   - ตัวอย่าง: `aimarkets.io`, `predictai.app`, `marketmind.ai`

2. **ชื่อ Extension**:
   - `.com` - ดีที่สุด แต่แพง
   - `.io` - เหมาะกับ tech startup
   - `.app` - ทันสมัย, secure (HTTPS required)
   - `.ai` - เกี่ยวกับ AI แต่แพงมาก (~$80/ปี)

3. **Cloudflare ฟรี**:
   - ควรใช้เสมอ
   - CDN global ฟรี
   - ไม่มีค่าใช้จ่ายเพิ่ม

---

## 🔍 ตรวจสอบ Domain ว่าว่างหรือไม่

เช็คได้ที่:
- [namecheap.com](https://www.namecheap.com)
- [name.com](https://www.name.com)
- [instant-domain-search.com](https://instantdomainsearch.com)

พิมพ์ชื่อที่ต้องการ → ดูราคาและความพร้อม

---

## 📞 Support

ถ้ามีปัญหา:
1. Railway Discord: [discord.gg/railway](https://discord.gg/railway)
2. Cloudflare Community: [community.cloudflare.com](https://community.cloudflare.com)
3. ดู DNS propagation: [dnschecker.org](https://dnschecker.org)

---

## ✅ Checklist

- [ ] Deploy บน Railway สำเร็จ (ได้ subdomain ฟรี)
- [ ] ทดสอบว่าเว็บทำงานถูกต้อง
- [ ] (Optional) ซื้อ custom domain
- [ ] (Optional) Upgrade Railway เป็น $5/เดือน
- [ ] (Optional) เชื่อม custom domain
- [ ] (Optional) Setup Cloudflare
- [ ] ตรวจสอบ SSL ใช้งานได้ (HTTPS)
- [ ] แชร์ link ให้เพื่อนทดสอบ!

---

**เริ่มจาก Free Subdomain ก่อนก็ได้ครับ!** 🚀
