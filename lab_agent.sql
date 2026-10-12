-- ========================================
-- 实验室智能预约系统数据库初始化脚本
-- ========================================

-- 创建数据库
CREATE DATABASE IF NOT EXISTS lab_agent
    DEFAULT CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE lab_agent;

-- ========================================
-- 1. 用户信息表
-- ========================================
DROP TABLE IF EXISTS reservations;
DROP TABLE IF EXISTS equipments;
DROP TABLE IF EXISTS labs;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    username VARCHAR(50) NOT NULL COMMENT '账号',
    password VARCHAR(255) NOT NULL COMMENT '密码（bcrypt加密）',
    name VARCHAR(50) NOT NULL COMMENT '姓名',
    role VARCHAR(50) NOT NULL COMMENT '角色：student-学生，admin-管理员',
    email VARCHAR(50) DEFAULT NULL COMMENT '邮箱',
    phone VARCHAR(50) DEFAULT NULL COMMENT '手机号',
    avatar VARCHAR(50) DEFAULT NULL COMMENT '头像',
    status INT DEFAULT 1 COMMENT '状态：0-禁用，1-正常',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户信息表';

-- ========================================
-- 2. 实验室信息表
-- ========================================
CREATE TABLE labs (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    name VARCHAR(50) NOT NULL COMMENT '实验室名称',
    location VARCHAR(100) DEFAULT NULL COMMENT '位置',
    capacity INT DEFAULT 0 COMMENT '容纳人数',
    open_time VARCHAR(20) DEFAULT NULL COMMENT '开放开始时间',
    close_time VARCHAR(20) DEFAULT NULL COMMENT '开放结束时间',
    description VARCHAR(500) DEFAULT NULL COMMENT '简介',
    img VARCHAR(200) DEFAULT NULL COMMENT '封面图',
    status INT DEFAULT 1 COMMENT '状态：0-关闭，1-开放',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='实验室信息表';

-- ========================================
-- 3. 实验室设备表
-- ========================================
CREATE TABLE equipments (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    lab_id INT NOT NULL COMMENT '所属实验室ID',
    name VARCHAR(50) NOT NULL COMMENT '设备名称',
    description VARCHAR(500) DEFAULT NULL COMMENT '说明',
    img VARCHAR(200) DEFAULT NULL COMMENT '图片',
    spec VARCHAR(100) DEFAULT NULL COMMENT '型号规格',
    quantity INT DEFAULT 1 COMMENT '数量',
    status INT DEFAULT 1 COMMENT '状态：0-维修，1-正常',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (lab_id) REFERENCES labs(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='实验室设备表';

-- ========================================
-- 4. 预约信息表
-- ========================================
CREATE TABLE reservations (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    user_id INT NOT NULL COMMENT '预约人ID',
    lab_id INT NOT NULL COMMENT '实验室ID',
    equipment_id INT DEFAULT NULL COMMENT '设备ID（空表示预约实验室）',
    date VARCHAR(20) NOT NULL COMMENT '预约日期',
    start_time VARCHAR(20) NOT NULL COMMENT '开始时间',
    end_time VARCHAR(20) NOT NULL COMMENT '结束时间',
    remark VARCHAR(255) DEFAULT NULL COMMENT '备注',
    status INT DEFAULT 0 COMMENT '预约状态：0-待审核，1-已通过，2-已拒绝，3-已取消',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (lab_id) REFERENCES labs(id) ON DELETE CASCADE,
    FOREIGN KEY (equipment_id) REFERENCES equipments(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='预约信息表';

-- ========================================
-- 5. 初始化测试数据
-- ========================================

-- 插入测试用户（密码使用bcrypt加密）
-- 管理员账号：admin / admin123
-- 学生账号：student / student123
INSERT INTO users (username, password, name, role, email, phone, status) VALUES
('admin', '$2b$12$jUCaK081ZMM6Xezn.onyRO8rK7toVvNKnGT44SlWA6tMeMFLUr8ne', '系统管理员', 'admin', 'admin@example.com', '13800000001', 1),
('student', '$2b$12$0HP/5938eBBTvmgOdeC1Q.0QpnQnamInSyMc7nvhWFuuaZYg.LhQK', '测试学生', 'student', 'student@example.com', '13800000002', 1);

-- 插入测试实验室
INSERT INTO labs (name, location, capacity, open_time, close_time, description, img, status) VALUES
('人工智能实验室', '教学楼A-301', 30, '08:00', '22:00', '配备高性能计算设备，用于AI模型训练和深度学习研究', '/uploads/lab_ai.jpg', 1),
('物联网实验室', '教学楼A-302', 25, '08:30', '21:30', '配备各类传感器和开发板，支持IoT项目开发', '/uploads/lab_iot.jpg', 1),
('数据分析实验室', '教学楼B-201', 40, '09:00', '21:00', '配备大数据处理平台，用于数据挖掘和分析', '/uploads/lab_data.jpg', 1),
('网络安全实验室', '教学楼B-202', 20, '08:00', '20:00', '配备网络安全测试工具，用于安全研究和渗透测试', '/uploads/lab_security.jpg', 1);

-- 插入测试设备
INSERT INTO equipments (lab_id, name, description, spec, quantity, status) VALUES
(1, 'GPU服务器', 'NVIDIA A100 GPU，用于深度学习训练', 'NVIDIA A100 80GB', 4, 1),
(1, '高性能工作站', '配备RTX 4090显卡', 'i9-13900K/64GB/RTX4090', 10, 1),
(2, '树莓派开发板', 'Raspberry Pi 4 Model B', '8GB版本', 20, 1),
(2, 'Arduino套件', 'Arduino Mega 2560开发套件', 'Mega 2560', 15, 1),
(3, '数据服务器', '大数据处理服务器', 'Xeon Silver/128GB/10TB', 2, 1),
(3, '客户端电脑', '数据分析终端', 'i7-13700/32GB/512GB SSD', 30, 1),
(4, '网络交换机', '可管理交换机', 'Cisco Catalyst 9200', 5, 1),
(4, '安全测试电脑', '网络安全测试专用', 'i7-13700/32GB/Kali Linux', 10, 1);

-- 插入测试预约记录
INSERT INTO reservations (user_id, lab_id, equipment_id, date, start_time, end_time, remark, status) VALUES
(2, 1, 1, '2026-10-15', '14:00', '18:00', '需要使用GPU服务器训练模型', 0),
(2, 2, 3, '2026-10-16', '09:00', '12:00', '物联网课程项目实验', 1),
(2, 3, NULL, '2026-10-14', '13:00', '17:00', '数据分析项目讨论', 2);

-- ========================================
-- 6. 创建索引（优化查询性能）
-- ========================================
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_labs_status ON labs(status);
CREATE INDEX idx_equipments_lab_id ON equipments(lab_id);
CREATE INDEX idx_reservations_user_id ON reservations(user_id);
CREATE INDEX idx_reservations_lab_id ON reservations(lab_id);
CREATE INDEX idx_reservations_date ON reservations(date);
CREATE INDEX idx_reservations_status ON reservations(status);

-- ========================================
-- 完成提示
-- ========================================
SELECT '数据库初始化成功！' AS message;
SELECT COUNT(*) AS '用户数量' FROM users;
SELECT COUNT(*) AS '实验室数量' FROM labs;
SELECT COUNT(*) AS '设备数量' FROM equipments;
SELECT COUNT(*) AS '预约记录数量' FROM reservations;
