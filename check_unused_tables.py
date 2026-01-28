#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
检查数据库中未使用的表
"""
import os
import sys
import django

# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base_settings')
sys.path.insert(0, os.path.dirname(__file__))

django.setup()

from django.db import connection
from django.apps import apps
from django.db.models import Q


def get_all_db_tables():
    """获取数据库中所有的表"""
    with connection.cursor() as cursor:
        cursor.execute("SHOW TABLES")
        tables = [row[0] for row in cursor.fetchall()]
    return tables


def get_all_model_tables():
    """获取所有 Django 模型对应的表名"""
    model_tables = set()
    for model in apps.get_models():
        model_tables.add(model._meta.db_table)
    return model_tables


def get_table_record_count(table_name):
    """获取表的记录数"""
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT COUNT(*) FROM `{table_name}`")
            count = cursor.fetchone()[0]
        return count
    except Exception as e:
        print(f"  错误: {e}")
        return None


def main():
    print("=" * 80)
    print("数据库未使用表检查工具")
    print("=" * 80)
    print()

    # 获取所有数据库表
    db_tables = get_all_db_tables()
    print(f"数据库中共有 {len(db_tables)} 张表")
    print()

    # 获取所有模型表
    model_tables = get_all_model_tables()
    print(f"Django 模型中共有 {len(model_tables)} 张表")
    print()

    # 找出未使用的表
    unused_tables = set(db_tables) - model_tables

    if unused_tables:
        print(f"发现 {len(unused_tables)} 张未使用的表:")
        print("-" * 80)
        
        for table in sorted(unused_tables):
            print(f"\n表名: {table}")
            count = get_table_record_count(table)
            if count is not None:
                print(f"  记录数: {count}")
                if count == 0:
                    print(f"  状态: 空表，可以安全删除")
                else:
                    print(f"  状态: 有数据，请谨慎处理")
        print()
    else:
        print("没有发现未使用的表")
        print()

    # 找出模型中定义但数据库中不存在的表
    missing_tables = model_tables - set(db_tables)
    if missing_tables:
        print(f"发现 {len(missing_tables)} 张模型定义但数据库中不存在的表:")
        print("-" * 80)
        for table in sorted(missing_tables):
            print(f"  {table}")
        print()

    # 显示所有模型表及其记录数
    print("=" * 80)
    print("所有 Django 模型表及其记录数:")
    print("-" * 80)
    for table in sorted(model_tables):
        count = get_table_record_count(table)
        if count is not None:
            print(f"  {table}: {count} 条记录")
    print()

    # 生成删除建议
    if unused_tables:
        print("=" * 80)
        print("删除建议:")
        print("-" * 80)
        print("以下 SQL 语句可以删除未使用的空表:")
        for table in sorted(unused_tables):
            count = get_table_record_count(table)
            if count == 0:
                print(f"  DROP TABLE `{table}`;")
        print()
        print("注意: 执行删除操作前请先备份数据库！")
        print()


if __name__ == '__main__':
    main()
