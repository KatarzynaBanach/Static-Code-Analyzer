import re
import argparse
from pathlib import Path
import os
import ast
import checks


def get_from_command_line():
    parser = argparse.ArgumentParser()
    parser.add_argument('dir_or_file')
    args = parser.parse_args()
    return args.dir_or_file


def print_errors(files_with_errors):
    for f in files_with_errors:
        for l in files_with_errors[f]:
            for e in files_with_errors[f][l]:
                print(f'{f}: Line {l}: {e} {files_with_errors[f][l][e]}')


def get_files_from_dir(directory):
    py_files = []
    entries = Path(directory)
    for entry in entries.iterdir():
        if entry.is_file() and entry.name.endswith('.py'):
            py_files.append(str(entry))

    return py_files


def files_to_check(file_or_dir):
    files_list = []
    if os.path.isfile(file_or_dir):
        files_list.append(str(Path(file_or_dir)))
    elif os.path.isdir(file_or_dir):
        files_list.extend(get_files_from_dir(file_or_dir))
    else:
        print('Wrong path')
    return files_list


def main():
    file_or_dir = get_from_command_line()
    files_list = files_to_check(file_or_dir)

    files_with_errors = {}
    for file in files_list:
        with open(file, 'r') as f:
            code = f.readlines()

        code_to_tree = ''.join(code)
        errors = {}

        for i, c in enumerate(code):
            errors = checks.check_s001(c, i, errors)
            if i >= 3:
                errors = checks.check_s006(code, i, errors)
            errors = checks.check_s002(c, i, errors)
            errors = checks.check_s004(c, i, errors)
            errors = checks.check_s005(c, i, errors)
            errors = checks.check_s003(c, i, errors)
            if re.match(r'class|def', c.strip()):
                errors = checks.check_s007(c, i, errors)
                errors = checks.check_s008(c, i, errors)
                errors = checks.check_s009(c, i, errors)

        tree = ast.parse(code_to_tree)
        errors = checks.check_ast_10_11_12(tree, errors)
        errors = {k: dict(sorted(v.items())) for k, v in errors.items()}
        files_with_errors[file] = errors

    print_errors(files_with_errors)

if __name__ == '__main__':
    main()
