from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from setting.config import settings

# 1. Khởi tạo Engine (Tương đương với DataSource trong Spring)
# engine là cỗ máy chịu trách nhiệm giao tiếp trực tiếp với Postgres qua DATABASE_URL.
# echo=settings.APP_DEBUG: Nếu là True, nó sẽ in mọi câu lệnh SQL ra terminal (giống show-sql: true trong Spring).
engine = create_engine(settings.DATABASE_URL, echo=settings.APP_DEBUG)

# 2. Tạo SessionLocal (Tương đương với SessionFactory trong Hibernate)
# Mỗi instance của SessionLocal sẽ là một phiên làm việc (session) với database.
# autocommit=False: Không tự động lưu, bạn phải gọi db.commit() để xác nhận giao dịch.
# autoflush=False: Không tự động đẩy dữ liệu xuống DB trước khi query trừ khi bạn yêu cầu.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. Tạo Base Class (Tương đương với việc đánh dấu @Entity)
# Mọi Model (Bảng) sau này bạn viết sẽ kế thừa từ Base này để SQLAlchemy nhận diện.
Base = declarative_base()

# 4. Hàm get_db (Tương đương với cơ chế Dependency Injection / @Transactional)
# Đây là một "Generator function" dùng để quản lý vòng đời của kết nối.
def get_db():
    # Mở một phiên kết nối mới
    db = SessionLocal()
    try:
        # yield trả về session cho Controller sử dụng và tạm dừng hàm ở đây.
        yield db
    finally:
        # Sau khi Request hoàn tất, hàm chạy tiếp vào đây để đóng kết nối.
        # Giúp tránh lỗi "Too many connections" (Tràn kết nối).
        db.close()