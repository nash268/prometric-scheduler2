# usage examples of sanitised_input():
# age = sanitised_input("Enter your age: ", int, 1, 101)
# answer = sanitised_input("Enter your answer: ", str.lower, range_=('a', 'b', 'c', 'd'))
# options = sanitised_input("Select toppings for pizza(separated by space): ", str.lower, subsetof_=('tomato', 'onion', 'kabab'))
def sanitised_input(prompt, type_=None, min_=None, max_=None, range_=None, length_=None, subsetof_=None):
    if min_ is not None and max_ is not None and max_ < min_:
        raise ValueError("min_ must be less than or equal to max_.")
    while True:
        ui = input(prompt)
        if type_ is not None:
            try:
                ui = type_(ui)
            except ValueError:
                print("Input type must be {0}.".format(type_.__name__))
                continue
        if max_ is not None and ui > max_:
            print("Input must be less than or equal to {0}.".format(max_))
        elif min_ is not None and ui < min_:
            print("Input must be greater than or equal to {0}.".format(min_))
        elif length_ is not None and len(ui) != length_:
            print("Input must have Length of {0} characters.".format(length_))
        elif range_ is not None and ui not in range_:
            if isinstance(range_, range):
                template = "Input must be between {0.start} and {0.stop}."
                print(template.format(range_))
            else:
                template = "Input must be {0}."
                if len(range_) == 1:
                    print(template.format(*range_))
                else:
                    expected = " or ".join((
                        ", ".join(str(x) for x in range_[:-1]),
                        str(range_[-1])
                    ))
                    print(template.format(expected))
        elif (subsetof_ is not None) and (not(set(ui.split(' ')) <= set(subsetof_))):
            print(f"Input must be a subset of {subsetof_}")
        else:
            return ui