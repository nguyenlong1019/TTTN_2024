# import mysql.connector

# # Hàm kết nối với MySQL
# def connect_to_mysql():
#     return mysql.connector.connect(
#         host="nhatkydientu.vn",
#         user="Admin01",
#         password="admin@abc",
#         database="thong_tin_tau_ca",
#         port=3306
#     )

# # Tắt ràng buộc khóa ngoại
# def disable_foreign_key_checks():
#     conn = connect_to_mysql()
#     cursor = conn.cursor()
#     cursor.execute("SET FOREIGN_KEY_CHECKS=0")
#     conn.commit()
#     conn.close()

# # Bật ràng buộc khóa ngoại
# def enable_foreign_key_checks():
#     conn = connect_to_mysql()
#     cursor = conn.cursor()
#     cursor.execute("SET FOREIGN_KEY_CHECKS=1")
#     conn.commit()
#     conn.close()

# # Xóa tất cả các bảng
# def drop_all_tables():
#     disable_foreign_key_checks() # Tắt ràng buộc khóa ngoại
#     conn = connect_to_mysql()
#     cursor = conn.cursor()
#     cursor.execute("SHOW TABLES")

#     for table in cursor.fetchall():
#         table_name = table[0]
#         drop_query = f"DROP TABLE {table_name}"
#         cursor.execute(drop_query)
    
#     conn.commit()
#     conn.close()
#     print("Đã xóa tất cả các bảng trong database!!")
#     enable_foreign_key_checks() # Bật lại ràng buộc khóa ngoại

# drop_all_tables()
# print("Thành công!!")
