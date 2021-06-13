import re
from functools import reduce
########################################################
def arithmetic_arranger(problems, ANSWERS = False):
    
    validated_probs = validate(problems_parser(problems))
    arranged_probs = arrange(validated_probs, ANSWERS)

    return '\n'.join(arranged_probs)
########################################################

def problems_parser(probs, answers):
    """
    Splits each problem string into a list with the first number, operator, 
    and second number as individual strings, then transposes so that we have
    three lists, a list of the first numbers, the operators, and the second
    numbers.
    """
    parsed = list(
        map(list, 
            zip(*map(
                lambda prob: prob.split(), 
                probs))) 
    )
    if answers:

    return parsed

def validate(parsed_probs):
    # Error messages
    ERR_TOO_MANY = "Error: Too many problems."
    ERR_OPERATOR = "Error: Operator must be '+' or '-'."
    ERR_DIGITS = "Error: Numbers must only contain digits." 
    ERR_TOO_BIG = "Error: Numbers cannot be more than four digits."

    # used to concatenate the numbers for a simpler regex scan
    def sum_up(list):
        return reduce(lambda a, b: a + b, list)

    # Is anything not a digit?
    def check_nums(digits):
        non_digits=re.compile(r"\D")
        return non_digits.search(sum_up(digits)) != None
 
    # Any numbers too long?
    def check_num_lengths(num_list):
        return False in map(lambda s: len(s) <= 4, num_list)

    ########################################################
    # Are there too many problems?
    if len(parsed_probs[0]) > 5:
        return ERR_TOO_MANY

    # 
    if '*' in parsed_probs[1] or '/' in parsed_probs[1]:
        return ERR_OPERATOR

    if check_nums(parsed_probs[0] + parsed_probs[2]):
        return ERR_DIGITS

    if check_num_lengths(parsed_probs[0] + parsed_probs[2]):
        return ERR_TOO_BIG

    return parsed_probs

def get_problem_widths(parsed_probs):
    return list(
        map(max, 
            zip(map(len, parsed_probs[0]), 
                map(len, parsed_probs[2]))))

def build_format_strings(widths, ops, answers):
    first = ''.join(list(
        map(lambda w: "{{:>{}}}    ".format(w + 2) , widths)
    ))
    second = ''.join(list(
        map(lambda w, op: "{} ".format(op) + "{{:>{}}}    ".format(w) , widths, ops)
    ))
    line = ''.join(list(
        map(lambda w: "{{0:->{}s}}    ".format(w + 2) , widths)
    ))
 
    return (first, second, line) if answers == 3 else (first, second, line, first)

def arrange(probs,answers):
    pwidths = get_problem_widths(probs)
    fstrs = build_format_strings(pwidths, probs[1], len(probs))
    if answers:
        return (   
            fstrs[0].format(*probs[0]),
            fstrs[1].format(*probs[2]),
            fstrs[2].format(''),
            fstrs[3].format(*probs[3])
        )
    else: 
        return (
            fstrs[0].format(*probs[0]),
            fstrs[1].format(*probs[2]),
            fstrs[2].format('')
        )
    

print(arithmetic_arranger(["32 + 8", "1 - 3801", "9999 + 9999", "523 - 49"], True))