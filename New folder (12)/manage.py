#!/usr/bin/env python
"""
REJA - Shaxsiy ish rejalashtirish sayti boshqaruv skripti.
"""
import os
import sys

def asosiy():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reja.soz')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as xato:
        raise ImportError("Django topilmadi. O'rnatilganini tekshiring.") from xato
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    asosiy()
