#!/usr/bin/env python3

import os
import platform

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

program_path = os.path.abspath("program.py")

if platform.system() == "Windows":
    script_extension = ".bat"
    script_content = f'@echo off\npython "{program_path}"'
else:
    script_extension = ".sh"
    script_content = f'#!/bin/bash\npython3 "{program_path}"\n'


script_file = f"run_program{script_extension}"

with open(script_file, "w") as script:
    script.write(script_content)