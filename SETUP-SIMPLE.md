# 🚨 LỖI CONNECTION - HƯỚNG DẪN SỬA LỖI

## 🔍 **VẤN ĐỀ HIỆN TẠI:**
- ❌ Browser hiển thị "Disconnected" 
- ❌ WebSocket server có thể chưa chạy đúng
- ❌ Fusion 360 add-in chưa kết nối

## 🛠️ **CÁCH SỬA TỪNG BƯỚC:**

### **Bước 1: Khởi động WebSocket Server**
```cmd
# Double-click file này để start server:
debug-start-server.bat

# Hoặc manual command:
.venv\Scripts\python.exe remote_server_simple.py
```

**✅ Server chạy đúng khi thấy:**
```
🚀 Starting Fusion 360 Remote Server...
✅ Server running on ws://localhost:8765
💡 Open remote-control-browser.html to start controlling!
```

### **Bước 2: Test Browser Connection**
```
1. Mở remote-control-browser.html
2. URL field: ws://localhost:8765
3. Click CONNECT
4. Status: "Connected" (green dot) ✅
```

### **Bước 3: Khởi động Fusion 360 Add-in**
```
1. Mở Fusion 360
2. Scripts & Add-ins → HTLM
3. Click "Stop" (nếu đang chạy)
4. Click "Run"
5. Popup hiện: "🌐 Remote Control Connected!"
```

### **Bước 4: Test Commands**
```
1. Browser: Click "Create Box"
2. Fusion 360: Box xuất hiện ✅
3. Browser: Click "Save Document"
4. Fusion 360: Document được save ✅
```

## 🐛 **TROUBLESHOOTING:**

### **Lỗi: "Connection closed"**
- ❌ Nguyên nhân: Server chưa chạy
- ✅ Giải pháp: Chạy `debug-start-server.bat`

### **Lỗi: "Commands not working"**
- ❌ Nguyên nhân: Add-in chưa kết nối WebSocket
- ✅ Giải pháp: Restart add-in trong Fusion 360

### **Lỗi: "Port 8765 in use"**
- ❌ Nguyên nhân: Server khác đang dùng port
- ✅ Giải pháp: Tắt process khác hoặc restart máy

## 🎯 **MANUAL STARTUP:**

```cmd
# Terminal 1: Start Server
cd "C:\Users\Admin\AppData\Roaming\Autodesk\Autodesk Fusion 360\API\AddIns\HTLM"
.venv\Scripts\python.exe remote_server_simple.py

# Browser: Open Interface
File: remote-control-browser.html
URL: ws://localhost:8765
Action: Click CONNECT

# Fusion 360: Restart Add-in
Scripts & Add-ins → HTLM → Stop → Run
Expected: "🌐 Remote Control Connected!" popup
```

## ✅ **SUCCESS INDICATORS:**

**Server Console:**
```
✅ Server running on ws://localhost:8765
📱 New client connected
🎯 Fusion 360 client registered  
🚀 Command forwarded: create_box
```

**Browser:**
```
✅ Status: Connected (green dot)
✅ Logs: "Command sent: create_box"
✅ Real-time response
```

**Fusion 360:**
```
✅ Objects appear instantly
✅ Commands execute immediately
✅ No errors in console
```

---

## � **KHI NÀO HỆ THỐNG HOẠT ĐỘNG:**
- **Server:** Running on port 8765 ✅
- **Browser:** Connected with green status ✅  
- **Fusion 360:** Add-in connected via WebSocket ✅
- **Commands:** Real-time execution ✅

**➡️ Làm theo từng bước trên để sửa lỗi connection!**
   HOẶC
2. Sửa trong `entry.py`:
   ```python
   PALETTE_URL = 'https://YOUR-USERNAME.github.io/fusion360-control-panel/online-index.html'
   ```

## ⚡ SCRIPT TỰ ĐỘNG:
- Chạy `setup-github-pages.bat` để tự động upload và cấu hình
- Chỉ cần nhập username GitHub

## 🚨 LƯU Ý:
- Repository PHẢI là PUBLIC
- Đợi 1-2 phút để GitHub deploy
- Thay YOUR-USERNAME bằng username GitHub thật của bạn
