# 🤖 Buddy AI — Hệ Sinh Thái Trợ Lý AI Đồng Hành, Điều Khiển Thiết Bị & Lập Trình

> **Sản phẩm dự thi Cuộc thi Hackathon SGU 2026 – 2027**  
> **Chủ đề:** Trợ lý AI Đa phương thức (Voice · Vision · Desktop Control · Agentic Coding) tối ưu cho Sinh viên & Lập trình viên trên Windows.

---

## 📌 1. Tổng Quan Dự Án (Overview)

**Buddy AI** là hệ sinh thái trợ lý trí tuệ nhân tạo kết hợp không gian học tập/làm việc trên Web với Robot đồng hành trên Desktop Windows và phân hệ lập trình tự động **Buddy Coder**. Hệ thống được thiết kế theo hướng **Local-First & Modular Gateway**, giúp người dùng:
- **Tương tác Đa phương thức:** Trò chuyện tiếng Việt theo lượt (PhoWhisper STT → Qwen3-VL / Devstral → Piper TTS) và nhận diện tín hiệu hiện diện/an toàn qua Camera (MoveNet Multipose).
- **Điều khiển Thiết bị Có Kiểm soát:** Thực thi các tác vụ mở ứng dụng, tìm kiếm thông tin, quản lý tệp và thư mục được cấp quyền trên Windows.
- **Không gian Lập trình Tự hành (Buddy Coder):** Duyệt mã nguồn, xem trước bản vá với **Inline Diff**, kiểm tra lỗi và hỗ trợ phiên làm việc tương tác qua cổng Gateway cục bộ.
- **Bảo mật & An toàn Chủ động:** Tích hợp bộ phân tích lừa đảo (`scam-inspector`), tương quan bảo mật (`security-correlation`), và xử lý an toàn cá nhân (`person-safety-worker`).

---

## 📂 2. Cấu Trúc Kho Mã Nguồn (Repository Structure)

```text
Buddy_agent/
├── buddy-app/                        # Mã nguồn chính của nền tảng Buddy AI & Control UI
│   ├── src/                          # Lõi điều phối Gateway, CLI, Agents, Channels & Tools
│   ├── ui/                           # Giao diện điều khiển trung tâm (SolidJS + TypeScript)
│   │   ├── buddy-src/                # Các phân hệ đặc thù của Buddy (Coder, Inline Diff, Security, Person Safety)
│   │   ├── src/pages/buddy/          # Định tuyến & trang không gian làm việc Buddy Workspace
│   │   └── public/assets/            # Tài nguyên mô hình thị giác (MoveNet Multipose) & giao diện
│   ├── packages/                     # Các gói thư viện nội bộ & hợp đồng giao thức (Session/Gateway)
│   ├── extensions/                   # Hệ thống 플러그인/tiện ích mở rộng đa kênh
│   ├── skills/                       # Bộ kỹ năng tự động hóa cho Agent
│   └── Start-Buddy-Coder.cmd         # Script khởi động nhanh không gian lập trình Buddy Coder
├── buddy-runtime/                    # Gói thực thi cục bộ (Prebuilt Local Gateway & UI) trên Windows
│   ├── control-ui/                   # Bản dựng giao diện tối ưu hóa sẵn sàng phục vụ qua Gateway
│   ├── package.json                  # Cấu hình phụ thuộc runtime cục bộ
│   └── Start-Buddy.cmd               # Script 1-click khởi chạy đồng thời Buddy Gateway (18789) & Coder (4096)
├── output/                           # Tài liệu báo cáo & Bộ Slide thuyết trình đồ án
│   ├── Buddy_AI_Tech_Presentation_13_Slides.pptx   # Bộ Slide 13 trang chuẩn AI Tech
│   ├── Buddy_Tom_tat_san_pham.docx                 # Tài liệu tóm tắt sản phẩm Buddy
│   └── ppt_assets/                                 # Hình nền HUD công nghệ của bộ Slide
├── create_buddy_ai_presentation.py   # Script Python tự động thiết kế & xuất bộ Slide 13 trang
└── create_buddy_summary.py           # Script Python xuất tài liệu tóm tắt sản phẩm (.docx)
```

---

## 🚀 3. Hướng Dẫn Khởi Chạy Nhanh (Quick Start)

### Yêu cầu hệ thống
- Hệ điều hành: **Windows 10 / 11 (64-bit)**
- Môi trường: **Node.js 24+** (`node -v`) và **pnpm** (nếu build từ mã nguồn `buddy-app`)

### Cách 1: Chạy trực tiếp bản Runtime đóng gói sẵn (`buddy-runtime`)
Chỉ cần chạy tệp lệnh trong thư mục `buddy-runtime`:
```cmd
cd buddy-runtime
Start-Buddy.cmd
```
Script sẽ tự động:
1. Kiểm tra môi trường Node.js 24 và khởi tạo khóa phiên cục bộ an toàn trong `buddy-runtime/state/` (không lưu lên Git).
2. Khởi chạy dịch vụ **Buddy Coder** tại `http://127.0.0.1:4096`.
3. Khởi chạy **Buddy Gateway** tại `http://127.0.0.1:18789` và mở trực tiếp giao diện **Buddy Workspace** trên trình duyệt.

### Cách 2: Phát triển và kiểm thử từ mã nguồn (`buddy-app`)
```powershell
cd buddy-app
pnpm install
pnpm ui:build
pnpm test
```

---

## 🧠 4. Điểm Nhấn Thuật Toán & Tối Ưu Hóa

1. **Xử lý Ngôn ngữ Tự nhiên & Giọng nói Tiếng Việt (SLU/NLU & ASR):**
   - Kết hợp phân loại ý định **LinearSVC** với **Conditional Random Fields (Context-CRF)** và giải mã **Constrained Viterbi** theo lược đồ BIO/BILOU (đạt **95.54% Intent** và **70.04% Full Command** trên CPU trong 15 giây / 1.345 câu kiểm thử).
   - Tinh chỉnh **Audio-Tower LoRA** (96 tensors) trên mô hình nhận dạng tiếng nói kèm tập dữ liệu FLEURS Replay chống quên kiến thức.
2. **Không gian Lập trình Tự sửa lỗi (Buddy Coder & Inline Diff):**
   - Thuật toán so khớp và hiển thị khác biệt mã nguồn trực tiếp (`coder-inline-diff.ts`), rút gọn các vùng không thay đổi và bảo vệ toàn vẹn tệp bằng mã băm.
3. **Thị giác Máy tính & Bảo vệ Người dùng (Vision & Security Correlation):**
   - Xử lý tư thế người dùng cục bộ qua Web Worker (`person-safety-worker.ts` + `movenet-multipose`) giúp không làm nghẽn luồng giao diện chính.
   - Phân tích đa chiều các dấu hiệu lừa đảo (`scam-inspector.ts`) và tương quan sự kiện bảo mật (`security-correlation.ts`).

---

## 📊 5. Tài Liệu Thuyết Trình (Presentation Deck)

Bộ slide thuyết trình **13 trang** báo cáo chi tiết về **Giới thiệu · Chức năng · Thuật toán · Hiệu suất · Cách tối ưu** được lưu tại:
- 📊 [`output/Buddy_AI_Tech_Presentation_13_Slides.pptx`](output/Buddy_AI_Tech_Presentation_13_Slides.pptx)
