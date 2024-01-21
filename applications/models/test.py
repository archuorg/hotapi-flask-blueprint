# from applications.extensions import db
from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
# 导入 Student 模型
# from applications.models import Student

# class Attendance(db.Model):
#     __tablename__ = 'admin_attendance'
#     id = db.Column(db.Integer, primary_key=True, comment="考勤记录ID")
#     student_id = db.Column(db.Integer, db.ForeignKey('admin_student.id'), comment="学生ID")
#     student = db.relationship('Student', back_populates='attendance_records')
#     month = db.Column(db.String(7), comment="考勤月份 (YYYY-MM)")
#     hours_present = db.Column(db.Float, comment="出勤时长 (小时)")
#
# # 添加一个 back_populates 属性，以建立 Student 和 Attendance 之间的关联
# Student.attendance_records = db.relationship('Attendance', back_populates='student')