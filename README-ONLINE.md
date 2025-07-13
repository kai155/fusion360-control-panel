# Fusion 360 HTML Control Panel - Online Hosting Guide

## 🌐 Cách Host Giao Diện Online

### Phương án 1: GitHub Pages (Miễn phí, Dễ nhất)

1. **Tạo GitHub Repository thủ công:**
   - Vào https://github.com/new
   - Repository name: `fusion360-control-panel`
   - ✅ Public (BẮT BUỘC)
   - ❌ KHÔNG tick "Add a README file"
   - Click "Create repository"

2. **Upload file:**
   - Click "uploading an existing file"
   - Kéo thả file `online-index.html` vào
   - Commit message: "Add Fusion 360 control panel"
   - Click "Commit changes"

3. **Bật GitHub Pages:**
   - Vào Settings > Pages
   - Source: Deploy from a branch
   - Branch: main / (root)
   - Save

4. **URL sẽ là:** `https://your-username.github.io/fusion360-control-panel/online-index.html`

### Phương án 2: Netlify (Miễn phí, Tự động deploy)

1. **Kéo thả folder vào netlify.com**
2. **URL tự động:** `https://random-name-12345.netlify.app/`
3. **Custom domain:** Có thể đổi tên miễn phí

### Phương án 3: Vercel (Miễn phí, Nhanh)

1. **Kết nối GitHub repo với vercel.com**
2. **Auto deploy:** Mỗi lần push code
3. **URL:** `https://your-project.vercel.app/`

### Phương án 4: Web Server riêng

- Apache/Nginx
- Shared hosting
- VPS/Cloud server

## 🔧 Cập nhật URL trong Code

Sau khi host, cập nhật URL trong file `entry.py`:

```python
# Configuration for online/local mode
USE_ONLINE_VERSION = True

if USE_ONLINE_VERSION:
    PALETTE_URL = 'https://your-actual-domain.com/online-index.html'
```

## 📁 Files cần upload:

- `online-index.html` (file chính - có tất cả CSS/JS inline)
- `index.html` (file gốc - backup)

## 🚀 Lợi ích của Online Version:

1. **Truy cập từ bất kỳ đâu**
2. **Cập nhật tập trung** - sửa 1 lần, áp dụng mọi nơi
3. **Chia sẻ dễ dàng** - gửi link cho người khác
4. **Backup tự động** - code lưu trên cloud
5. **CDN tốc độ cao** - tải nhanh hơn

## 🔒 Bảo mật:

- Chỉ hoạt động khi được load trong Fusion 360
- Không thể truy cập trực tiếp từ browser thường
- API calls chỉ work trong context của add-in

## 🔄 Auto-update:

- Mỗi lần sửa code và push lên GitHub
- Netlify/Vercel tự động deploy
- Fusion 360 sẽ load version mới nhất

## 📱 Responsive Design:

- Giao diện tự động thích ứng màn hình
- Hoạt động tốt trên tablet/mobile (nếu cần)
- Touch-friendly buttons

## 🎯 Demo Mode:

- Khi không kết nối với Fusion 360
- Vẫn hiển thị giao diện để demo
- Hiển thị thông báo "Demo mode"

## 🛠 Troubleshooting:

1. **Nếu không load:** Kiểm tra URL đúng chưa
2. **CORS errors:** Đảm bảo HTTPS (GitHub Pages tự động có)
3. **Slow loading:** Dùng CDN hoặc optimize images
4. **Connection issues:** Check add-in đang chạy chưa

## 🔧 Advanced Features:

- **Custom domain:** Setup domain riêng
- **Analytics:** Theo dõi usage
- **Multiple versions:** Dev/Staging/Production
- **API integration:** Kết nối với external services
