import re
from functools import reduce

########################################################
def arithmetic_arranger(problems, ANSWERS = False):

    # Transpose the rows of problems into columns of their parts
    parsed_probs = parse(problems)

    # Validate before we eval to provide answers if needed.
    try:
        validate(parsed_probs)
    except ValueError as err:
        return str(err)

    # Append the answer string 
    if ANSWERS:
        parsed_probs += (tuple(map(
            lambda p: str(eval(p)), problems
            )),) 

    arranged_probs = arrange(parsed_probs, ANSWERS)

    return '\n'.join(arranged_probs) 

########################################################
def parse(probs):
    """
    Splits each problem string into a list with the first number, operator, 
    and second number as individual strings, then transposes so that we have
    three tuples, a tuple of the first numbers, the operators, and the second
    numbers.
    """
    return tuple(map(tuple, 
        zip(*map(
            lambda prob: prob.split(), 
            probs))) 
    )

def validate(probs):
    # Error messages
    ERR_TOO_MANY = "Error: Too many problems."
    ERR_OPERATOR = "Error: Operator must be '+' or '-'."
    ERR_DIGITS = "Error: Numbers must only contain digits." 
    ERR_TOO_BIG = "Error: Numbers cannot be more than four digits."

    # used to concatenate the number strings for a simpler regex scan
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

    if len(probs[0]) > 5:
        raise ValueError(ERR_TOO_MANY)

    if '*' in probs[1] or '/' in probs[1]:
        raise ValueError(ERR_OPERATOR)

    if check_nums(probs[0] + probs[2]):
        raise ValueError(ERR_DIGITS)

    if check_num_lengths(probs[0] + probs[2]):
        raise ValueError(ERR_TOO_BIG)

def arrange(probs, answers):

    def get_problem_widths(probs):
        return tuple(
            map(max, 
                zip(map(len, probs[0]), 
                    map(len, probs[2]))))

    def build_format_strings(widths, ops, answers):
        first = ''.join(tuple(
            map(lambda w: "{{:>{}}}    ".format(w + 2) , widths)
        )).strip()

        second = ''.join(tuple(
            map(lambda w, op: "{} ".format(op) + "{{:>{}}}    ".format(w) , widths, ops)
        )).strip()

        line = ''.join(tuple(
            map(lambda w: "{{0:->{}s}}    ".format(w + 2) , widths)
        )).strip()

        # The answer line can use the same format string as the first line.    
        return (first, second, line, first) if answers else (first, second, line)

    pwidths = get_problem_widths(probs)
    fstrs = build_format_strings(pwidths, probs[1], answers)

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


    