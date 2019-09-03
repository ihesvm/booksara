#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import string
import random


def get_file_name(path):
    return os.path.basename(path)


def random_string(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choices(chars) for _ in range(size))


def get_file_name_ext(filepath):
    basename = os.path.basename(filepath)
    name, ext = os.path.splitext(basename)
    return name, ext


def upload_image_path(instance, filenames):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_file_name_ext(filenames)
    final_filenames = f'{new_filename}{ext}'
    return f'static/img/{new_filename}/{final_filenames}'
