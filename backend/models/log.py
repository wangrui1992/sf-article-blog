# -*- coding: utf-8 -*-
"""
操作日志模型

用于记录用户操作历史，支持审计追踪

Author: wangrui1992
Date: 2026-05-18
"""

from models.database import db
from datetime import datetime
from sqlalchemy import Index


class OperationLog(db.Model):
    """操作日志"""
    __tablename__ = 'operation_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    operation = db.Column(db.String(50), nullable=False, index=True)  # login, create, update, delete
    resource_type = db.Column(db.String(50))  # article, user, tag
    resource_id = db.Column(db.Integer)
    details = db.Column(db.Text)
    ip_address = db.Column(db.String(45))  # 支持 IPv6
    user_agent = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    __table_args__ = (
        Index('idx_log_user_time', 'user_id', 'created_at'),
        Index('idx_log_resource', 'resource_type', 'resource_id'),
        {'mysql_engine': 'InnoDB'}
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'operation': self.operation,
            'resource_type': self.resource_type,
            'resource_id': self.resource_id,
            'details': self.details,
            'ip_address': self.ip_address,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class LoginLog(db.Model):
    """登录日志"""
    __tablename__ = 'login_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    username = db.Column(db.String(80), index=True)
    status = db.Column(db.String(20))  # success, failed
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(500))
    fail_reason = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    __table_args__ = (
        Index('idx_login_user_time', 'user_id', 'created_at'),
    )
