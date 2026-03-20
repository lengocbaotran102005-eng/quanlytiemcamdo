<h1 align="center">🏦 Pawnshop Management System (PMS)</h1>
<h3 align="center">Hệ Thống Quản Lý Tiệm Cầm Đồ Toàn Diện</h3>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Flask-3.0.0-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask"/>
  <img src="https://img.shields.io/badge/MySQL-8.0-4479A1?style=for-the-badge&logo=mysql&logoColor=white" alt="MySQL"/>
  <img src="https://img.shields.io/badge/TailwindCSS-3.4.0-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white" alt="TailwindCSS"/>
</p>

<p align="center">
  <b>PMS</b> là hệ thống quản lý tiệm cầm đồ chuyên nghiệp, chuẩn quy trình, hỗ trợ cầm, chuộc, gia hạn, tính lãi tự động, và báo cáo chi tiết.
</p>

---

## 🌟 Tính năng nổi bật

- **Quản lý giao dịch cầm đồ**: cầm mới, gia hạn, chuộc, đóng lãi, in phiếu.
- **Quản lý khách hàng**: CRUD, tìm kiếm, load lịch sử, xóa mềm.
- **Quản lý vật phẩm**: CRUD, trạng thái, cấu hình giá cầm/giá dự tính.
- **Quản lý người dùng**: phân quyền Admin/Thu ngân, đổi mật khẩu, avatar.
- **Dashboard báo cáo**: doanh thu tháng, hợp đồng mới, công nợ, xuất Excel.
- **Lãi suất tự động**: tính dựa theo kỳ (ngày/tháng), cảnh báo quá hạn.
- **Tích hợp QR**: QR interest / QR redeem cho giao dịch nhanh.

## 🌐 Demo online

- Link: [http://103.56.163.84:5000/](http://103.56.163.84:5000/)

---

## 🛠️ Công nghệ (Tech Stack)

| Layer | Công nghệ |
|---|---|
| Backend | Python 3.11 |
| Web framework | Flask 3.0.0 |
| ORM | Flask-SQLAlchemy |
| Migration | Flask-Migrate (Alembic) |
| Auth | Flask-Login, Flask-Bcrypt |
| DB driver | PyMySQL (MySQL/MariaDB) |
| Frontend | Tailwind CSS 3.4.0 |
| Hình ảnh | Pillow |
| Excel | openpyxl |
| Môi trường | python-dotenv |

---

## 📁 Cấu trúc thư mục

- `app/`
  - `controllers/`: routes (auth, customers, items, transactions, reports, users)
  - `models/`: SQLAlchemy models (User, Customer, Item, Transaction)
  - `services/`: nghiệp vụ (interest, notification, upload, QR)
  - `static/`: css/js/img/uploads
  - `views/`: template Jinja2
  - `extensions.py`: khởi tạo extensions
  - `__init__.py`: app factory
  - `config.py`: cấu hình
- `migrations/`: Alembic migration
- `requirements.txt`
- `package.json`
- `run.py`
- `tests/test_interest.py`

---

## 🚀 Cài đặt nhanh

```bash
# 1) clone
git clone <repo-url> .

# 2) tạo virtualenv
python -m venv venv
venv\Scripts\activate

# 3) cài dependencies
pip install -r requirements.txt
npm install
npm run build:css

# 4) chạy migration
flask db upgrade

# 5) chạy app
python run.py
```

Truy cập: `http://127.0.0.1:5000` hoặc demo: `http://103.56.163.84:5000/`

---

## 🔧 Biến môi trường mẫu

```
FLASK_APP=run.py
FLASK_ENV=development
SQLALCHEMY_DATABASE_URI=mysql+pymysql://USER:PASSWORD@HOST:PORT/DBNAME
SECRET_KEY=your-secret-key
```



