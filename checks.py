import re
import ast


def add_error(errors, i, code, message):
    errors.setdefault(i+1, {})
    errors[i+1].setdefault(code, message)
    return errors


def check_s001(line, i, errors):
    code = 'S001'
    message = 'Too long'
    if len(line.strip()) > 79:
        errors = add_error(errors, i, code, message)
    return errors


def check_s002(line, i, errors):
    code = 'S002'
    message = 'Indentation is not a multiple of four'
    x = re.search(r'\S', line)
    if x is not None:
        if x.start() % 4 != 0:
            errors = add_error(errors, i, code, message)
    return errors


def check_s003(line, i, errors):
    code = 'S003'
    message = 'Unnecessary semicolon after a statement'
    x = re.search(r';\s*#', line)
    y = re.search(r';$', line)
    z = re.search(r'#[\S ]*;', line)
    if x is not None or (y is not None and z is None):
        errors = add_error(errors, i, code, message)
    return errors


def check_s004(line, i, errors):
    code = 'S004'
    message = 'Less than two spaces before inline comments'
    x = re.search(r'\S\s*#', line)
    if x is not None:
        if (x.end() - x.start() - 2) != 2:
            errors = add_error(errors, i, code, message)
    return errors


def check_s005(line, i, errors):
    code = 'S005'
    message = 'TODO found'
    x = re.search(r'#[\S ]*[tT][oO][dD][oO]', line)
    if x is not None:
        errors = add_error(errors, i, code, message)
    return errors


def check_s006(line, i, errors):
    code = 'S006'
    message = 'More than two blank lines preceding a code line'
    if all([len(l.strip()) == 0 for l in line[i-3:i]]) and len(line[i]) > 0:
        errors = add_error(errors, i, code, message)
    return errors


def check_s007(line, i, errors):
    code = 'S007'
    class_or_def = re.search(r'class|def', line.strip()).group()
    message = f'Too many spaces after \'{class_or_def}\''
    if not(re.match(r'(class|def)\s\S', line.strip())):
        errors = add_error(errors, i, code, message)
    return errors


def check_s008(line, i, errors):
    if 'class' in line:
        code = 'S008'
        class_name = re.search(r'class\s+(\S+):', line).group(1)
        message = f'Class name \'{class_name}\' should use CamelCase'
        if not(class_name[0].isupper()) or '_' in class_name:
            errors = add_error(errors, i, code, message)
    return errors


def check_s009(line, i, errors):
    if 'def' in line:
        code = 'S009'
        func_name = re.search(r'def\s+(\S+)', line).group(1)
        message = f'Function name \'{func_name}\' should use snake_case'
        if not(func_name[0].islower()) and not(func_name[0] in ['_', '__']):
            errors = add_error(errors, i, code, message)
    return errors


def check_s010(node, errors):
    for a in node.args.args:
        arg_name = a.arg
        if not(arg_name[0].islower()) and not(arg_name[0] == '_'):
            i = a.lineno - 1
            code = 'S010'
            message = f'Argument name \'{arg_name}\' should be snake_case'
            errors = add_error(errors, i, code, message)
    return errors


def check_s011(node, errors):
    for a in node.body:
        if isinstance(a, ast.Assign):
            try:
                var_name = a.targets[0].id
                if not(var_name[0].islower()) and not(var_name[0] == '_'):
                    i = a.lineno - 1
                    code = 'S011'
                    message = f'Variable \'{var_name}\' in function should be snake_case'
                    errors = add_error(errors, i, code, message)
            except AttributeError:
                pass
    return errors


def check_s012(node, errors):
    for d in node.args.defaults:
        if isinstance(d, ast.List) or isinstance(d, ast.Dict) or isinstance(d, ast.Set):
            i = d.lineno - 1
            code = 'S012'
            message = 'Default argument value is mutable'
            errors = add_error(errors, i, code, message)


def check_ast_10_11_12(tree, errors):
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            check_s010(node, errors)
            check_s011(node, errors)
            check_s012(node, errors)
    return errors


if __name__ == '__main__':
    main()
