class BinaryTree:
    def __init__(self, root_obj):
        self.key = root_obj
        self.left_child = None
        self.right_child = None

    def insert_left(self,new_node):
        if self.left_child is None:
            self.left_child = BinaryTree(new_node)
        else:
            t = BinaryTree(new_node)
            t.left_child = self.left_child
            self.left_child = t

    def insert_right(self, new_node):
        if self.right_child is None:
            self.right_child = BinaryTree(new_node)
        else:
            t = BinaryTree(new_node)
            t.right_child = self.right_child
            self.right_child = t

    def get_right_child(self):
        return self.right_child

    def get_left_child(self):
        return self.left_child

    def set_root_val(self, obj):
        self.key = obj

    def get_root_val(self):
        return self.key

    def convert_from_list(self, other):
        if len(other) == 3:
            self.set_root_val(other[1])
            self.insert_left("")
            self.left_child.convert_from_list(other[0])
            self.insert_right("")
            self.right_child.convert_from_list(other[2])

    def convert_to_list(self):
        result = []
        if self.get_left_child() or self.get_right_child():
            if self.get_left_child():
                result.append(self.get_left_child().convert_to_list())
            else:
                result.append([])
            result.append(self.get_root_val())
            if self.right_child:
                result.append(self.get_right_child().convert_to_list())
            else:
                result.append([])
        else:
            result.append(self.get_root_val())
        return result

    def __eq__(self, other):
        """
        function allows to check if two trees contains same elements
        :param other: BinaryTree
        :return: bool
        """
        try:
            if float(self.get_root_val()) == float(other.get_root_val()):
                return True
        except ValueError:
            pass
        if self.get_root_val() == other.get_root_val():
            if self.get_left_child():
                if not self.get_left_child() == other.get_left_child():
                    return False
            else:
                if other.get_left_child():
                    return False
            if self.get_right_child():
                if not self.get_right_child() == other.get_right_child():
                    return False
            else:
                if other.get_right_child():
                    return False
            return True
        else:
            return False

    def __str__(self, if_main=True):
        """
        function returns BinaryTree print
        :param if_main: help bool used in algorithm
        :return: print representation
        """
        left_child = self.get_left_child()
        right_child = self.get_right_child()
        if if_main:
            if left_child and right_child:
                return [left_child.__str__(False), self.get_root_val(), right_child.__str__(False)].__str__()
            elif left_child:
                return [left_child.__str__(False), self.get_root_val(), []].__str__()
            elif right_child:
                return [[], self.get_root_val(), right_child.__str__(False)].__str__()
            else:
                return [self.get_root_val()].__str__()
        else:
            if left_child and right_child:
                return [left_child.__str__(False), self.get_root_val(), right_child.__str__(False)]
            elif left_child:
                return [left_child.__str__(False), self.get_root_val(), []]
            elif right_child:
                return [[], self.get_root_val(), right_child.__str__(False)]
            else:
                return [self.get_root_val()]

    def __copy__(self):
        """
        function returns copied object
        :return: BinaryTree copy
        """
        result = BinaryTree(self.get_root_val())
        if self.get_left_child():
            result.left_child = self.get_left_child().__copy__()
        if self.get_right_child():
            result.right_child = self.get_right_child().__copy__()
        return result


def program_run(expression):
    """
    main function that maintain whole process
    :param expression: string with math expression
    :return: derivatice of string expression in a string
    """
    expression = expression_main(expression)
    tree = expression_to_tree_main(expression)
    tree_derivative = derivative_main(tree)
    tree_simplified = tree_simplify_main(tree_derivative)
    expression = tree_to_expression_main(tree_simplified)
    return expression


def expression_main(expression):
    """
    main function that maintains operations on input expression. It checks expression's correctness and edits it to form,
        which is acceptable by rest functions in the process
    :param expression: math expression as string
    :return: string
    """
    func_names_normal = ["sin", "cos", "tg", "ctg", "sec", "csc", "sinh", "cosh", "tgh", "ctgh", "sech", "csch", "log", "sqrt", "exp"]
    func_names_arc = ["arc_sin", "arc_cos", "arc_tg", "arc_ctg", "arc_sec", "arc_csc"]
    expression = expression.replace("**", "^")  # ujednolicenie potęgowania

    if expression.count("(") != expression.count(")"):
        raise Exception("Niepoprawnie wprowadzone wyrażenie - nie zgadza się liczba otwieranych oraz zamykanych nawiasów")

    for i in ["arcsin", "arccos", "arcctg", "arcsec", "arccsc"]:  # zamiana arcusów napisanych bez spacji na konwencję
        expression = expression.replace(i, f"arc_{i[-3:]}")
    expression = expression.replace("arctg", "arc_tg")

    expression = expression.replace("(", " (")  # dodawanie spacji przed nawiasami otwierającymi i za zamykającymi
    expression = expression.replace(")", ") ")

    operations = expression.split(" ")  # splitowanie po spacjach
    operations = [i for i in operations if i != ""]  # redukcja wielokrotnych spacji

    expression_check_arc(operations, func_names_normal, func_names_arc)

    index = 0
    while index < len(operations):  # inteligentne dodawanie nawiasów przy funkcjach ARCUSY
        expression_brackets_arc(operations, index, func_names_normal, func_names_arc)
        index += 1

    index = 0
    while index < len(operations):  # inteligentne dodawanie nawiasów przy funkcjach
        expression_brackets_normal(operations, index, func_names_normal, func_names_arc)
        index += 1

    expression = "".join(operations)

    expression = expression.replace("x", "(x)")
    expression = expression.replace("e(x)p", "exp")

    expression = expression_brackets_power(expression)
    expression = expression.replace("(-", "((-1)*")
    if expression[0] == "-":
        expression = "(-1)*" + expression[1:]
    expression = expression_brackets_mul_div(expression)
    return expression


def expression_check_arc(operations, func_names_normal, func_names_arc):
    """
    function finds arc functions and checks their correctness. It also transforms them to needed form
    :param operations: expressions in a list separated by spaces
    :param func_names_normal: just in case of future modifications
    :param func_names_arc: just in case of future modifications
    """
    index = 0
    while index < len(operations):  # arcusy
        if operations[index][-3:] == "arc":  # szuka arcusów oddzielonych spacją i łączy je ze sobą
            if len(operations[index+1]) >= 2 and operations[index + 1][:2] == "tg":  # przypadek z tangensem
                operations[index] = f"{operations[index][:-3]}arc_{operations[index+1][:2]}"
                operations[index+1] = operations[index+1][2:]
            elif len(operations[index+1]) >= 3 and operations[index + 1][:3] in ["sin", "cos", "ctg", "sec", "csc"]:  # reszta przypadków
                operations[index] = f"{operations[index][:-3]}arc_{operations[index+1][:3]}"
                operations[index+1] = operations[index+1][3:]
            else:
                raise Exception(f"Błąd w wyrażeniu {operations[index]} {operations[index+1]}")
        index += 1


def expression_brackets_arc(operations, index, func_names_normal, func_names_arc):
    """
    function inserts needed brackets in arcus functions if user didn't type them
    :param operations: expressions in a list separated by spaces
    :param index: index of operation from operations list that function is supposed to work on
    :param func_names_normal: list with supported function names (without arc)
    :param func_names_arc: list with supported arc function names
    """
    current = operations[index]
    for i in func_names_arc:  # dla każdego arkusa
        counter = current.count(i)  # ilość
        if counter:
            last_index = 0
            while counter > 0:  # dla każdego w rozpatrywanym fragmencie
                current_index = current.find(i, last_index) + len(i)  # szuka arkusa i zapisuje index jego argumentu

                if current_index == len(current):
                    if index + 1 < len(operations):
                        if operations[index+1][0] == "(":
                            expression_brackets_arc(operations, index+1, func_names_normal, func_names_arc)
                            operations[index] = current + operations.pop(index+1)
                            current = operations[index]
                        else:
                            expression_brackets_arc(operations, index+1, func_names_normal, func_names_arc)
                            operations[index] = current + "(" + operations.pop(index+1) + ")"
                            current = operations[index]
                    else:
                        raise Exception(f"Błąd w elemencie {current} w funkcji {i}")

                elif current[current_index] != "(":  # jeśli nie ma nawiasu to go dodaje
                        operations[index] = current[:current_index] + "(" + current[current_index:] + ")"
                        current = operations[index]
                current_index += 1
                last_index = current_index  # żeby szukać od tego momentu
                counter -= 1


def expression_brackets_normal(operations, index, func_names_normal, func_names_arc):
    """
    function inserts needed brackets in functions (without arc) if user didn't type them
    :param operations: expressions in a list separated by spaces
    :param index: index of operation from operations list that function is supposed to work on
    :param func_names_normal: list with supported function names (without arc)
    :param func_names_arc: list with supported arc function names
    """
    current = operations[index]
    for i in func_names_normal:  # dla każdego arkusa
        counter = current.count(i) - current.count(f"arc_{i}") - current.count(f"{i}h")  # ilość
        if counter:
            last_index = 0
            while counter > 0:  # dla każdego w rozpatrywanym fragmencie
                while True:  # żeby uniknąć rozpatrywania arkusów
                    current_index = current.find(i, last_index)  # szuka funkcji i zapisuje jej index
                    if current_index == 0 or current[current_index-1] != "_":
                        current_index = current_index + len(i)  # szuka funkcji i zapisuje index jej argumentu
                        break
                    last_index = current.find(i, last_index) + len(i)  # szuka funkcji i zapisuje index jej argumentu

                if current_index == len(current):
                    if index + 1 < len(operations):
                        if operations[index+1][0] == "(":
                            expression_brackets_normal(operations, index+1, func_names_normal, func_names_arc)
                            operations[index] = current + operations.pop(index+1)
                            current = operations[index]
                        else:
                            expression_brackets_normal(operations, index+1, func_names_normal, func_names_arc)
                            operations[index] = current + "(" + operations.pop(index+1) + ")"
                            current = operations[index]
                    else:
                        raise Exception(f"Błąd w elemencie {current} w funkcji {i}")

                elif current[current_index] != "(":  # jeśli nie ma nawiasu to go dodaje
                    operations[index] = current[:current_index] + "(" + current[current_index:] + ")"
                    current = operations[index]
                last_index = current_index  # żeby szukać od tego momentu
                counter -= 1


def expression_brackets_power(expression):
    """
    function inserts brackets on sides of power arguments if user didn't do so
    :param expression: string
    :return: string
    """
    counter = expression.count("^")
    last_index = 0
    while counter > 0:
        start, end = 0, 0
        current_index = expression.find("^", last_index)
        if current_index == 0:
            raise Exception("Operator potęgowania użyty niepoprawnie (na początku wyrażenia)")

        ### lewa strona od potęgi
        if expression[current_index-1] == ")":  # przypadek że potęga odnosi się do nawiasu
            index_open = bracket_search_opening(expression, current_index-1)
            start = index_open  # początek całego wyrażenia
            if expression[index_open-1].isalpha():
                i = index_open-1
                while expression[i].isalpha():
                    i -= 1
                expression = expression[:i+1] + "(" + expression[i+1:current_index] + ")" + expression[current_index:]
                last_index = current_index + 2  # bo dochodzi nawias  # potrzebne do wyszukiwania ale pycharm zaznacza jako nieużywane
                current_index += 2  # bo dochodzi nawias
                start = i + 1  # początek całego wyrażenia

        elif expression[current_index-1].isalpha():  # przypadek że potęga odnosi się do x
            expression = expression[:current_index-1] + "(" + expression[current_index-1] + ")" + expression[current_index:]
            last_index = current_index + 2  # bo dochodzi nawias  # potrzebne do wyszukiwania ale pycharm zaznacza jako nieużywane
            current_index += 2  # bo dochodzi nawias
            start = current_index - 1  # początek całego wyrażenia

        elif expression[current_index-1].isnumeric():  # przypadek że potęga odnosi się do liczby
            i = current_index - 1
            is_float = False
            is_last_dot = False
            while (expression[i].isnumeric() or expression[i] == ".") and i >= 0:
                if expression[i] == ".":
                    if not is_float:
                        is_float = True
                        is_last_dot = True
                    else:
                        raise Exception(f"Liczbę zmiennoprzecionkową {expression[i:current_index]} podano niepoprawnie")
                elif expression[i].isnumeric():
                    is_last_dot = False
                i -= 1
            if is_last_dot:
                raise Exception(f"Liczbę zmiennoprzecionkową {expression[i:current_index]} podano niepoprawnie")
            expression = expression[:i+1] + "(" + expression[i+1:current_index] + ")" + expression[current_index:]
            last_index = current_index + 2  # bo dochodzi nawias  # potrzebne do wyszukiwania ale pycharm zaznacza jako nieużywane
            current_index += 2  # bo dochodzi nawias
            start = i + 1  # początek całego wyrażenia

        ### prawa strona od potęgi
        if expression[current_index+1] == "(":  # przypadek potęgowania przez wyrażenie w nawiasie
            index_close = bracket_search_closing(expression, current_index+1)
            last_index = current_index  # potrzebne do wyszukiwania ale pycharm zaznacza jako nieużywane
            end = index_close

        elif expression[current_index+1] == "x":  # przypadek że wyrażenie podnosi się do x
            expression = expression[:current_index+1] + "(" + expression[current_index+1] + ")" + expression[current_index+2:]
            last_index = current_index  # potrzebne do wyszukiwania ale pycharm zaznacza jako nieużywane
            end = current_index + 3

        elif expression[current_index+1].isalpha():  # przypadek że wyrażenie podnosi się do funkcji
            index_open = expression.find("(", current_index+1)
            index_close = bracket_search_closing(expression, index_open)
            expression = expression[:current_index+1] + "(" + expression[current_index+1:index_close+1] + ")" + expression[index_close+1:]
            last_index = current_index  # potrzebne do wyszukiwania ale pycharm zaznacza jako nieużywane
            end = index_close + 2

        elif expression[current_index+1].isnumeric():  # przypadek że wyrażenie podnosi się do liczby
            i = current_index + 1
            is_float = False
            is_last_dot = False
            while (expression[i].isnumeric() or expression[i] == ".") and i+1 < len(expression):
                if expression[i] == ".":
                    if not is_float:
                        is_float = True
                        is_last_dot = True
                    else:
                        raise Exception(f"Liczbę zmiennoprzecionkową {expression[current_index:i]} podano niepoprawnie")
                elif expression[i].isnumeric():
                    is_last_dot = False
                i += 1
            if is_last_dot:
                raise Exception(f"Liczbę zmiennoprzecionkową {expression[current_index:i]} podano niepoprawnie")
            expression = expression[:current_index+1] + "(" + expression[current_index+1:i+1] + ")" + expression[i+1:]
            last_index = current_index  # potrzebne do wyszukiwania ale pycharm zaznacza jako nieużywane
            end = i+1

        expression = expression[:start+1] + "(" + expression[start+1:end+1] + ")" + expression[end+1:]  # pakuje całe wyrażenie jeszcze w nawias
        last_index = current_index + 2  # żeby rozpatrywać od indeksu po obecnej potędze
        counter -= 1
    return expression


def expression_brackets_mul_div(expression):
    """
    function inserts brackets on sides of arguments of multiplication and division if user didn't do so
    :param expression: string
    :return: string
    """
    expression = expression.replace(")(", ")*(")
    index = 0
    last_type = None  # operator, num, bracket_open, bracket_close, alpha(func, x)
    while index < len(expression):  # dodawanie mnożenia w domyśle
        current_element = expression[index]
        current_type = element_check_type(current_element)
        if current_type == "alpha":
            if current_element == "x" and last_type != "alpha_func":
                current_type = "alpha_x"
            else:
                current_type = "alpha_func"

        if last_type in ["alpha_x", "bracket_close"] and current_type not in ["operator", "bracket_close"]:
            expression = expression[:index] + "*" + expression[index:]  # dodawanie znaku mnożenia
            index += 1  # bo dochodzi "*" przed obecnym elementem
        elif last_type == "num" and current_type not in ["operator", "bracket_close", "num"]:
            expression = expression[:index] + "*" + expression[index:]  # dodawanie znaku mnożenia
            index += 1  # bo dochodzi "*" przed obecnym elementem
        elif last_type and last_type not in ["operator", "alpha_func", "bracket_open"] and current_type == "bracket_open":
            expression = expression[:index] + "*" + expression[index:]  # dodawanie znaku mnożenia
            index += 1  # bo dochodzi "*" przed obecnym elementem
        elif last_type == "operator" and current_type == "operator":
            raise Exception("Niepoprawny zapis: operatory działań nie mogą znajdować się obok siebie - należy użyć nawiasu")
        index += 1
        last_type = current_type

    if expression[0] in ["*", "/"] or expression[-1] in ["*", "/"]:
        raise Exception("Niepoprawny zapis: na początku ani na końcu wyrażenia nie może być operatorów działania")
    index = 0
    while index < len(expression):  # separowanie nawiasami
        start, end = 0, 0
        current_element = expression[index]
        if current_element in ["*", "/"]:
            previous_element = expression[index-1]
            next_element = expression[index+1]

            ### lewa strona
            if previous_element == ")":  # zobaczyć czy nawias czy funkcja
                index_opening = bracket_search_opening(expression, index-1)
                if expression[index_opening-1].isalpha() and expression[index_opening-1] != "x":  # przypadek że mnoży się funkcję
                    start = function_search_beginning(expression, index_opening-1)
                    expression = expression[:start] + "(" + expression[start:index] + ")" + expression[index:]
                    index += 2  # bo dodane nawiasy
                else:  # przypadek że mnoży się nawias
                    start = index_opening

            elif previous_element.isnumeric():
                i = index - 1
                is_float = False
                while (expression[i].isnumeric() or expression[i] == ".") and i >= 0:
                    if expression[i] == ".":
                        if not is_float:
                            is_float = True
                        else:
                            raise Exception(f"Liczbę zmiennoprzecionkową {expression[i:index]} podano niepoprawnie")
                    i -= 1

                start = i + 1
                expression = expression[:i+1] + "(" + expression[i+1:index] + ")" + expression[index:]
                index += 2  # bo dodane nawiasy

            ### prawa strona
            if next_element == "(":  # przypadek że mnoży się przez nawias
                index_closing = bracket_search_closing(expression, index+1)
                end = index_closing

            elif next_element.isalpha():  # przypadek że mnoży się przez funkcję
                index_closing = bracket_search_closing(expression, expression.find("(", index+1))
                expression = expression[:index+1] + "(" + expression[index+1:index_closing+1] + ")" + expression[index_closing+1:]
                end = index_closing + 2

            elif next_element.isnumeric():  # przypadek że mnoży się przez liczbę
                i = index + 1
                is_float = False
                is_last_dot = False
                while (expression[i].isnumeric() or expression[i] == ".") and i < len(expression):
                    if expression[i] == ".":
                        if not is_float:
                            is_float = True
                            is_last_dot = True
                        else:
                            raise Exception(
                                f"Liczbę zmiennoprzecionkową {expression[index+1:i]} podano niepoprawnie")
                    elif expression[i].isnumeric():
                        is_last_dot = False
                    i += 1
                if is_last_dot:
                    raise Exception(f"Liczbę zmiennoprzecionkową {expression[index+1:i]} podano niepoprawnie")

                end = i
                expression = expression[:index+1] + "(" + expression[index+1:i] + ")" + expression[i:]
                index += 2  # bo dodane nawiasy

            expression = expression[:start] + "(" + expression[start:end+1] + ")" + expression[end+1:]
            index += 1
        index += 1
    return expression


def element_check_type(element):
    """
    function used just in expression_brackets_mul_div func to recognise type of element in order to add multiplication
        operator in a smart way
    :param element: string element (len(param) = 1)
    :return: string
    """
    if element.isnumeric() or element == ".":
        return "num"
    elif element.isalpha() or element == "_":
        return "alpha"
    elif element in ["+", "-", "*", "/", "^"]:
        return "operator"
    elif element == "(":
        return "bracket_open"
    elif element == ")":
        return "bracket_close"
    else:
        raise Exception(f"Podano niepoprawny element {element}")


def function_search_beginning(expression, index):  # nie myli funckji z x-ami bo x-y są jako (x)
    """
    function search for beginning of a string (a string must be a function). used in expression_brackets_mul_div
    :param expression: string
    :param index: last index of string
    :return: int
    """
    while (expression[index].isalpha() or expression[index] == "_") and index >= 0:
        index -= 1
    return index + 1


def bracket_search_opening(expression, index_closing):
    """
    function searches index of opening bracket to the bracket with index given
    :param expression: string
    :param index_closing: index
    :return: int
    """
    stack = [index_closing]
    i = index_closing - 1
    while i >= 0:
        if expression[i] == ")":
            stack.append(i)
        elif expression[i] == "(":
            stack.pop()
        if not stack:
            return i
        i -= 1
    raise Exception(f"Niepoprawne ułożenie nawiasów w podanym wyrażeniu: {expression}")


def bracket_search_closing(expression, index_opening):
    """
    function searches index of closing bracket to the bracket with index given
    :param expression: string
    :param index_opening: index
    :return: int
    """
    stack = [index_opening]
    i = index_opening + 1
    while i < len(expression):
        if expression[i] == "(":
            stack.append(i)
        elif expression[i] == ")":
            stack.pop()
        if not stack:
            return i
        i += 1
    raise Exception(f"Niepoprawne ułożenie nawiasów w podanym wyrażeniu: {expression}")


def expression_to_tree_main(expression):  # główna funckja przekształcająca wyrażenie w drzewo
    """
    main function that maintains converting expression to a BinaryTree
    :param expression: string
    :return: BinaryTree
    """
    tree = BinaryTree(expression)
    tree_separate(tree)
    return tree


def tree_separate(tree):  # rekurencyjny proces wpisywania wyrażenia do drzewa
    """
    function expands BinaryTree object to create correct BinaryTree of expression. Works recursive
    :param tree: BinaryTree
    """
    expression = tree.get_root_val()
    main_bracket_open = expression.find("(")
    if main_bracket_open != -1:
        main_bracket_close = bracket_search_closing(expression, main_bracket_open)

        if main_bracket_open == 0 and main_bracket_close == len(expression)-1:  # przypadek że całe wyrażenie jest w jednym nawiasie
            tree.set_root_val(expression[1:-1])
            tree_separate(tree)

        else:  # trzeba sprawdzić czy całe wyrażenie jest funkcją czy są jakieś inne operatory
            mode = None
            if main_bracket_close == len(expression) - 1 and expression[main_bracket_open - 1].isalpha():
                i = main_bracket_open - 1
                while i >= 0:
                    if not (expression[i] == "_" or expression[i].isalpha()):
                        mode = "operator"
                        break
                    else:
                        mode = "func"
                    i -= 1
            else:
                mode = "operator"

            if mode == "operator":  # rozpatrujemy wyrażenie względem najogólniejszego operatora
                sign = expression_search_main_operator(expression)
                if sign is not None:
                    tree.set_root_val(expression[sign])
                    tree.insert_left(expression[:sign])
                    tree.insert_right(expression[sign+1:])
                    tree_separate(tree.get_left_child())
                    tree_separate(tree.get_right_child())
            elif mode == "func":  # przypadek że całe wyrażenie jest w funkcji
                tree.set_root_val(expression[:main_bracket_open])
                tree.insert_right(expression[main_bracket_open:])
                tree_separate(tree.get_right_child())

    else:  # przypadek że nie ma nawiasów więc szukamy operatorów
        sign = expression_search_main_operator(expression)
        if sign is not None and sign != 0:
            tree.set_root_val(expression[sign])
            tree.insert_left(expression[:sign])
            tree.insert_right(expression[sign+1:])
            tree_separate(tree.get_left_child())
            tree_separate(tree.get_right_child())


def expression_search_main_operator(expression):  # funkcja zwraca indeks operatora najbardziej ogólnego działania
    """
    function used in tree_separate func. Returns index of the most general operator
    :param expression: string
    :return: int
    """
    main_bracket_open = [expression.find("(")]
    main_bracket_close = [-1]
    if main_bracket_open[0] == -1:
        for i in ["+", "-"]:
            a = expression.find(i)
            if a != -1:
                return a
        return None
    else:
        while main_bracket_open[-1] != -1:
            main_bracket_close.append(bracket_search_closing(expression, main_bracket_open[-1]))
            main_bracket_open.append(expression.find("(", main_bracket_close[-1]))
        main_bracket_open.pop(-1)
        main_bracket_open.append(len(expression))

        for i in range(len(main_bracket_close)):
            temp_expression = expression[main_bracket_close[i]+1:main_bracket_open[i]]
            for k in ["+", "-"]:
                a = temp_expression.find(k)
                if a != -1:
                    return a + main_bracket_close[i] + 1

        for i in range(len(main_bracket_close)):
            temp_expression = expression[main_bracket_close[i]+1:main_bracket_open[i]]
            for k in ["*", "/"]:
                a = temp_expression.find(k)
                if a != -1:
                    return a + main_bracket_close[i] + 1

        for i in range(len(main_bracket_close)):
            temp_expression = expression[main_bracket_close[i]+1:main_bracket_open[i]]
            a = temp_expression.find("^")
            if a != -1:
                return a + main_bracket_close[i] + 1
        return None


def derivative_main(tree):
    """
    main function that maintains derivation of expression in a BinaryTree process
    :param tree: BinaryTree
    :return: BinaryTree
    """
    tree = tree.__copy__()
    tree = derivative_recursive(tree)
    return tree


def derivative_recursive(element):
    result = BinaryTree("")
    if element.get_root_val() == "+":
        result.set_root_val("+")

        result.left_child = derivative_recursive(element.left_child.__copy__())
        result.right_child = derivative_recursive(element.right_child.__copy__())

    elif element.get_root_val() == "-":
        result.set_root_val("-")

        result.left_child = derivative_recursive(element.left_child.__copy__())
        result.right_child = derivative_recursive(element.right_child.__copy__())

    elif element.get_root_val() == "*":
        result.set_root_val("+")

        left = BinaryTree("*")
        left.left_child = derivative_recursive(element.left_child.__copy__())
        left.right_child = element.right_child.__copy__()

        right = BinaryTree("*")
        right.left_child = element.left_child.__copy__()
        right.right_child = derivative_recursive(element.right_child.__copy__())

        result.left_child = left
        result.right_child = right

    elif element.get_root_val() == "/":
        result.set_root_val("/")

        left = BinaryTree("-")

        left_left = BinaryTree("*")
        left_left.left_child = derivative_recursive(element.left_child.__copy__())
        left_left.right_child = element.right_child.__copy__()

        left_right = BinaryTree("*")
        left_right.left_child = element.left_child.__copy__()
        left_right.right_child = derivative_recursive(element.right_child.__copy__())

        left.left_child = left_left
        left.right_child = left_right

        right = BinaryTree("^")
        right.left_child = element.right_child.__copy__()
        right.right_child = BinaryTree("2")

        result.left_child = left
        result.right_child = right

    elif element.get_root_val() == "^":
        result.set_root_val("*")

        left = BinaryTree("*")

        left_left = element.right_child.__copy__()
        left_right = derivative_recursive(element.left_child.__copy__())

        right = BinaryTree("^")

        right_left = element.left_child.__copy__()
        right_right = BinaryTree("-")

        right_right_left = element.right_child.__copy__()
        right_right_right = BinaryTree("1")

        right_right.left_child = right_right_left
        right_right.right_child = right_right_right

        left.left_child = left_left
        left.right_child = left_right

        right.left_child = right_left
        right.right_child = right_right

        result.left_child = left
        result.right_child = right


    elif element.get_root_val() == "exp":
        result.set_root_val("*")

        left = derivative_recursive(element.right_child.__copy__())

        right = BinaryTree("exp")

        right_right = element.right_child.__copy__()

        right.right_child = right_right

        result.left_child = left
        result.right_child = right

    elif element.get_root_val() == "sin":
        result.set_root_val("*")

        left = derivative_recursive(element.right_child.__copy__())

        right = BinaryTree("cos")

        right_right = element.right_child.__copy__()

        right.right_child = right_right

        result.left_child = left
        result.right_child = right

    elif element.get_root_val() == "cos":
        result.set_root_val("*")

        left = BinaryTree("*")

        left_left = BinaryTree("-1")

        left_right = derivative_recursive(element.right_child.__copy__())

        right = BinaryTree("sin")

        right_right = element.right_child.__copy__()

        left.left_child = left_left
        left.right_child = left_right

        right.right_child = right_right

        result.left_child = left
        result.right_child = right

    elif element.get_root_val() == "tg":
        result.set_root_val("/")

        left = derivative_recursive(element.right_child.__copy__())

        right = BinaryTree("^")

        right_left = BinaryTree("cos")
        right_right = BinaryTree("2")

        right_left_right = element.right_child.__copy__()

        right_left.right_child = right_left_right

        right.left_child = right_left
        right.right_child = right_right

        result.left_child = left
        result.right_child = right

    elif element.get_root_val() == "ctg":
        result.set_root_val("/")

        left = BinaryTree("*")
        left_left = BinaryTree("-1")
        left_right = derivative_recursive(element.right_child.__copy__())

        right = BinaryTree("^")

        right_left = BinaryTree("sin")
        right_right = BinaryTree("2")

        right_left_right = element.right_child.__copy__()

        right_left.right_child = right_left_right

        left.left_child = left_left
        left.right_child = left_right

        right.left_child = right_left
        right.right_child = right_right

        result.left_child = left
        result.right_child = right

    elif element.get_root_val() == "sec":
        result.set_root_val("*")

        left = derivative_recursive(element.right_child.__copy__())

        right = BinaryTree("*")

        right_left = BinaryTree("tg")
        right_right = BinaryTree("sec")

        right_left_right = element.right_child.__copy__()
        right_right_right = element.right_child.__copy__()

        right_left.right_child = right_left_right
        right_right.right_child = right_right_right

        right.left_child = right_left
        right.right_child = right_right

        result.left_child = left
        result.right_child = right

    elif element.get_root_val() == "csc":
        result.set_root_val("*")

        left = BinaryTree("*")
        right = BinaryTree("*")

        left_left = BinaryTree("-1")
        left_right = derivative_recursive(element.right_child.__copy__())

        right_left = BinaryTree("ctg")
        right_right = BinaryTree("csc")

        right_left_right = element.right_child.__copy__()
        right_right_right = element.right_child.__copy__()

        right_left.right_child = right_left_right
        right_right.right_child = right_right_right

        left.left_child = left_left
        left.right_child = left_right

        right.left_child = right_left
        right.right_child = right_right

        result.left_child = left
        result.right_child = right

    elif element.get_root_val() == "arc_sin":
        result.set_root_val("/")

        left = derivative_recursive(element.right_child.__copy__())

        right = BinaryTree("^")

        right_left = BinaryTree("-")
        right_right = BinaryTree("1/2")

        right_left_left = BinaryTree("1")
        right_left_right = BinaryTree("^")

        right_left_right_left = element.right_child.__copy__()
        right_left_right_right = BinaryTree("2")

        right_left_right.left_child = right_left_right_left
        right_left_right.right_child = right_left_right_right

        right_left.left_child = right_left_left
        right_left.right_child = right_left_right

        right.left_child = right_left
        right.right_child = right_right

        result.left_child = left
        result.right_child = right

    elif element.get_root_val() == "arc_cos":
        result.set_root_val("/")

        left = BinaryTree("*")

        right = BinaryTree("^")

        left_left = BinaryTree("-1")
        left_right = derivative_recursive(element.right_child.__copy__())

        right_left = BinaryTree("-")
        right_right = BinaryTree("1/2")

        right_left_left = BinaryTree("1")
        right_left_right = BinaryTree("^")

        right_left_right_left = element.right_child.__copy__()
        right_left_right_right = BinaryTree("2")

        right_left_right.left_child = right_left_right_left
        right_left_right.right_child = right_left_right_right

        right_left.left_child = right_left_left
        right_left.right_child = right_left_right

        right.left_child = right_left
        right.right_child = right_right

        left.left_child = left_left
        left.right_child = left_right

        result.left_child = left
        result.right_child = right

    elif element.get_root_val() == "arc_tg":
        result.set_root_val("/")

        left = derivative_recursive(element.right_child.__copy__())

        right = BinaryTree("+")

        right_left = BinaryTree("1")
        right_right = BinaryTree("^")

        right_right_left = element.right_child.__copy__()
        right_right_right = BinaryTree("2")

        right_right.left_child = right_right_left
        right_right.right_child = right_right_right

        right.left_child = right_left
        right.right_child = right_right

        result.left_child = left
        result.right_child = right

    elif element.get_root_val() == "arc_ctg":
        result.set_root_val("/")

        left = BinaryTree("*")

        left_left = BinaryTree("-1")
        left_right = derivative_recursive(element.right_child.__copy__())

        right = BinaryTree("+")

        right_left = BinaryTree("1")
        right_right = BinaryTree("^")

        right_right_left = element.right_child.__copy__()
        right_right_right = BinaryTree("2")

        right_right.left_child = right_right_left
        right_right.right_child = right_right_right

        right.left_child = right_left
        right.right_child = right_right

        left.left_child = left_left
        left.right_child = left_right

        result.left_child = left
        result.right_child = right

    elif element.get_root_val() == "arc_sec":
        result.set_root_val("/")

        left = derivative_recursive(element.right_child.__copy__())

        right = BinaryTree("*")

        right_left = BinaryTree("^")
        right_right = BinaryTree("^")

        right_left_left = element.right_child.__copy__()
        right_left_right = BinaryTree("2")

        right_right_left = BinaryTree("-")
        right_right_right = BinaryTree("1/2")

        right_right_left_left = BinaryTree("1")
        right_right_left_right = BinaryTree("/")

        right_right_left_right_left = BinaryTree("1")
        right_right_left_right_right = BinaryTree("^")

        right_right_left_right_right_left = element.right_child.__copy__()
        right_right_left_right_right_right = BinaryTree("2")

        right_right_left_right_right.left_child = right_right_left_right_right_left
        right_right_left_right_right.right_child = right_right_left_right_right_right

        right_right_left_right.left_child = right_right_left_right_left
        right_right_left_right.right_child = right_right_left_right_right

        right_right_left.left_child = right_right_left_left
        right_right_left.right_child = right_right_left_right

        right_right.left_child = right_right_left
        right_right.right_child = right_right_right

        right_left.left_child = right_left_left
        right_left.right_child = right_left_right

        right.left_child = right_left
        right.right_child = right_right

        result.left_child = left
        result.right_child = right

    elif element.get_root_val() == "arc_csc":
        result.set_root_val("/")

        left = BinaryTree("*")

        left_left = BinaryTree("-1")
        left_right = derivative_recursive(element.right_child.__copy__())

        right = BinaryTree("*")

        right_left = BinaryTree("^")
        right_right = BinaryTree("^")

        right_left_left = element.right_child.__copy__()
        right_left_right = BinaryTree("2")

        right_right_left = BinaryTree("-")
        right_right_right = BinaryTree("1/2")

        right_right_left_left = BinaryTree("1")
        right_right_left_right = BinaryTree("/")

        right_right_left_right_left = BinaryTree("1")
        right_right_left_right_right = BinaryTree("^")

        right_right_left_right_right_left = element.right_child.__copy__()
        right_right_left_right_right_right = BinaryTree("2")

        right_right_left_right_right.left_child = right_right_left_right_right_left
        right_right_left_right_right.right_child = right_right_left_right_right_right

        right_right_left_right.left_child = right_right_left_right_left
        right_right_left_right.right_child = right_right_left_right_right

        right_right_left.left_child = right_right_left_left
        right_right_left.right_child = right_right_left_right

        right_right.left_child = right_right_left
        right_right.right_child = right_right_right

        right_left.left_child = right_left_left
        right_left.right_child = right_left_right

        right.left_child = right_left
        right.right_child = right_right

        left.left_child = left_left
        left.right_child = left_right

        result.left_child = left
        result.right_child = right

    elif element.get_root_val() == "sinh":
        result.set_root_val("*")

        left = derivative_recursive(element.right_child.__copy__())

        right = BinaryTree("cosh")

        right_right = element.right_child.__copy__()

        right.right_child = right_right

        result.left_child = left
        result.right_child = right

    elif element.get_root_val() == "cosh":
        result.set_root_val("*")

        left = derivative_recursive(element.right_child.__copy__())

        right = BinaryTree("sinh")

        right_right = element.right_child.__copy__()

        right.right_child = right_right

        result.left_child = left
        result.right_child = right

    elif element.get_root_val() == "tgh":
        result.set_root_val("/")

        left = derivative_recursive(element.right_child.__copy__())

        right = BinaryTree("^")

        right_left = BinaryTree("cosh")
        right_right = BinaryTree("2")

        right_left_right = element.right_child.__copy__()

        right_left.right_child = right_left_right

        right.left_child = right_left
        right.right_child = right_right

        result.left_child = left
        result.right_child = right

    elif element.get_root_val() == "ctgh":
        result.set_root_val("/")

        left = BinaryTree("*")

        left_left = BinaryTree("-1")
        left_right = derivative_recursive(element.right_child.__copy__())

        right = BinaryTree("^")

        right_left = BinaryTree("sinh")
        right_right = BinaryTree("2")

        right_left_right = element.right_child.__copy__()

        right_left.right_child = right_left_right

        right.left_child = right_left
        right.right_child = right_right

        left.left_child = left_left
        left.right_child = left_right

        result.left_child = left
        result.right_child = right

    elif element.get_root_val() == "sech":
        result.set_root_val("*")

        left = BinaryTree("*")
        right = BinaryTree("*")

        left_left = BinaryTree("-1")
        left_right = derivative_recursive(element.right_child.__copy__())

        right_left = BinaryTree("tgh")
        right_right = BinaryTree("sech")

        right_left_right = element.right_child.__copy__()
        right_right_right = element.right_child.__copy__()

        right_left.right_child = right_left_right
        right_right.right_child = right_right_right

        left.left_child = left_left
        left.right_child = left_right

        right.left_child = right_left
        right.right_child = right_right

        result.left_child = left
        result.right_child = right

    elif element.get_root_val() == "csch":
        result.set_root_val("*")

        left = BinaryTree("*")
        right = BinaryTree("*")

        left_left = BinaryTree("-1")
        left_right = derivative_recursive(element.right_child.__copy__())

        right_left = BinaryTree("ctgh")
        right_right = BinaryTree("csch")

        right_left_right = element.right_child.__copy__()
        right_right_right = element.right_child.__copy__()

        right_left.right_child = right_left_right
        right_right.right_child = right_right_right

        left.left_child = left_left
        left.right_child = left_right

        right.left_child = right_left
        right.right_child = right_right

        result.left_child = left
        result.right_child = right

    elif element.get_root_val() == "log":
        result.set_root_val("/")

        left = derivative_recursive(element.right_child.__copy__())
        right = element.right_child.__copy__()

        result.left_child = left
        result.right_child = right

    elif element.get_root_val() == "sqrt":
        result.set_root_val("/")

        left = BinaryTree("*")
        right = BinaryTree("sqrt")

        left_left = BinaryTree("/")
        left_right = derivative_recursive(element.right_child.__copy__())

        right_right = element.right_child.__copy__()

        left_left_left = BinaryTree("1")
        left_left_right = BinaryTree("2")

        left_left.left_child = left_left_left
        left_left.right_child = left_left_right

        left.left_child = left_left
        left.right_child = left_right

        right.right_child = right_right

        result.left_child = left
        result.right_child = right

    elif element.get_root_val() == "x":
        result = BinaryTree("1")

    elif check_numeric(element.get_root_val()):
        result = BinaryTree("0")

    return result


def tree_simplify_main(tree):
    """
    main function that maintains simplifying of expression in a BinaryTree process
    :param tree: BinaryTree
    :return: BinaryTree
    """
    last = tree.__copy__()
    while True:
        current = tree_simplify_recursive(last)
        if last == current:
            break
        else:
            last = current
    return current


def tree_simplify_recursive(tree):
    """
    function that runs suitable function in order to simplify expression in BinaryTree
    :param tree: BinaryTree
    :return: BinaryTree
    """
    tree = tree.__copy__()  # żeby nie zmienić niczego w orginalnym drzewie

    if tree.get_root_val() == "+":
        tree_simplify_add(tree)

    elif tree.get_root_val() == "-":
        tree_simplify_sub(tree)

    elif tree.get_root_val() == "*":
        tree_simplify_mul(tree)

    elif tree.get_root_val() == "^":
        tree_simplify_pow(tree)

    elif tree.get_root_val() == "/":
        tree_simplify_div(tree)

    if tree.left_child:
        tree.left_child = tree_simplify_recursive(tree.left_child)
    if tree.right_child:
        tree.right_child = tree_simplify_recursive(tree.right_child)

    return tree


def tree_simplify_add(tree):
    """
    function simplifies BinaryTree, when root value is +
    :param tree: BinaryTree
    """
    left = tree.left_child
    right = tree.right_child
    if left:
        left = left.__copy__()
    if right:
        right = right.__copy__()

    if left.get_root_val() in ["0", "0.0", "-0", "-0.0"]:  # lewe jest 0
        tree.set_root_val(right.get_root_val())
        tree.left_child = right.left_child
        tree.right_child = right.right_child

    elif right.get_root_val() in ["0", "0.0", "-0", "-0.0"]:  # prawe jest 0
        tree.set_root_val(left.get_root_val())
        tree.left_child = left.left_child
        tree.right_child = left.right_child

    elif check_numeric(left.get_root_val()) and check_numeric(right.get_root_val()):  # lewe i prawe to liczby
        tree.set_root_val(str(float(left.get_root_val()) + float(right.get_root_val())))
        tree.left_child = None
        tree.right_child = None

    elif left == right:
        tree.set_root_val("*")
        tree.left_child = BinaryTree("2")
        tree.right_child = left

    elif left.get_root_val() == "*" and right.get_root_val() == "*":  # przypadek 2x+4x albo 10sin(x)+7sin(x)
        if check_numeric(left.left_child.get_root_val()):
            if check_numeric(right.left_child.get_root_val()):
                if left.right_child == right.right_child:
                    amount = float(right.left_child.get_root_val()) + float(left.left_child.get_root_val())

                    tree.set_root_val("*")
                    tree.left_child = BinaryTree(str(amount))
                    tree.right_child = left.right_child

            elif check_numeric(right.right_child.get_root_val()):
                if left.right_child == right.left_child:
                    amount = float(right.right_child.get_root_val()) + float(left.left_child.get_root_val())

                    tree.set_root_val("*")
                    tree.left_child = BinaryTree(str(amount))
                    tree.right_child = left.right_child

        elif check_numeric(left.right_child.get_root_val()):
            if check_numeric(right.left_child.get_root_val()):
                if left.left_child == right.right_child:
                    amount = float(right.left_child.get_root_val()) + float(left.right_child.get_root_val())

                    tree.set_root_val("*")
                    tree.left_child = BinaryTree(str(amount))
                    tree.right_child = left.left_child

            elif check_numeric(right.right_child.get_root_val()):
                if left.left_child == right.left_child:
                    amount = float(right.right_child.get_root_val()) + float(left.right_child.get_root_val())

                    tree.set_root_val("*")
                    tree.left_child = BinaryTree(str(amount))
                    tree.right_child = left.left_child

    elif left.get_root_val() == "*":
        if check_numeric(left.left_child.get_root_val()):
            if left.right_child == right:
                tree.set_root_val("*")
                tree.left_child = BinaryTree(str(float(left.left_child.get_root_val()) + 1))
                tree.right_child = left.right_child

        elif check_numeric(left.right_child.get_root_val()):
            if left.left_child == right:
                tree.set_root_val("*")
                tree.left_child = BinaryTree(str(float(left.right_child.get_root_val()) + 1))
                tree.right_child = left.left_child

    elif right.get_root_val() == "*":
        if check_numeric(right.left_child.get_root_val()):
            if right.right_child == left:
                tree.set_root_val("*")
                tree.left_child = BinaryTree(str(float(right.left_child.get_root_val()) + 1))
                tree.right_child = right.right_child

        elif check_numeric(right.right_child.get_root_val()):
            if right.left_child == left:
                tree.set_root_val("*")
                tree.left_child = BinaryTree(str(float(right.right_child.get_root_val()) + 1))
                tree.right_child = right.left_child


def tree_simplify_sub(tree):
    """
    function simplifies BinaryTree, when root value is -
    :param tree: BinaryTree
    """
    left = tree.left_child
    right = tree.right_child
    if left:
        left = left.__copy__()
    if right:
        right = right.__copy__()

    if left.get_root_val() in ["0", "0.0", "-0", "-0.0"]:  # lewe jest 0
        tree.set_root_val("*")
        tree.left_child = BinaryTree("-1")
        tree.right_child = right

    elif right.get_root_val() in ["0", "0.0", "-0", "-0.0"]:  # prawe jest 0
        tree.set_root_val(left.get_root_val())
        tree.left_child = left.left_child
        tree.right_child = left.right_child


    elif check_numeric(left.get_root_val()) and check_numeric(right.get_root_val()):  # lewe i prawe to liczby
        tree.set_root_val(str(float(left.get_root_val()) - float(right.get_root_val())))
        tree.left_child = None
        tree.right_child = None

    elif left == right:
        tree.set_root_val("0")
        tree.left_child = None
        tree.right_child = None

    elif left.get_root_val() == "*" and right.get_root_val() == "*":  # przypadek 2x+4x albo 10sin(x)+7sin(x)
        if check_numeric(left.left_child.get_root_val()):
            if check_numeric(right.left_child.get_root_val()):
                if left.right_child == right.right_child:
                    amount = float(left.left_child.get_root_val()) - float(right.left_child.get_root_val())

                    tree.set_root_val("*")
                    tree.left_child = BinaryTree(str(amount))
                    tree.right_child = left.right_child

            elif check_numeric(right.right_child.get_root_val()):
                if left.right_child == right.left_child:
                    amount = float(left.left_child.get_root_val()) - float(right.right_child.get_root_val())

                    tree.set_root_val("*")
                    tree.left_child = BinaryTree(str(amount))
                    tree.right_child = left.right_child

        elif check_numeric(left.right_child.get_root_val()):
            if check_numeric(right.left_child.get_root_val()):
                if left.left_child == right.right_child:
                    amount = float(left.right_child.get_root_val()) - float(right.left_child.get_root_val())

                    tree.set_root_val("*")
                    tree.left_child = BinaryTree(str(amount))
                    tree.right_child = left.left_child

            elif check_numeric(right.right_child.get_root_val()):
                if left.left_child == right.left_child:
                    amount =  float(left.right_child.get_root_val()) - float(right.right_child.get_root_val())

                    tree.set_root_val("*")
                    tree.left_child = BinaryTree(str(amount))
                    tree.right_child = left.left_child

    elif left.get_root_val() == "*":
        if check_numeric(left.left_child.get_root_val()):
            if left.right_child == right:
                tree.set_root_val("*")
                tree.left_child = BinaryTree(str(float(left.left_child.get_root_val()) - 1))
                tree.right_child = left.right_child

        elif check_numeric(left.right_child.get_root_val()):
            if left.left_child == right:
                tree.set_root_val("*")
                tree.left_child = BinaryTree(str(float(left.right_child.get_root_val()) - 1))
                tree.right_child = left.left_child

    elif right.get_root_val() == "*":
        if check_numeric(right.left_child.get_root_val()):
            if right.right_child == left:
                tree.set_root_val("*")
                tree.left_child = BinaryTree(str(float(right.left_child.get_root_val()) - 1))
                tree.right_child = right.right_child

        elif check_numeric(right.right_child.get_root_val()):
            if right.left_child == left:
                tree.set_root_val("*")
                tree.left_child = BinaryTree(str(float(right.right_child.get_root_val()) - 1))
                tree.right_child = right.left_child


def tree_simplify_mul(tree):
    """
    function simplifies BinaryTree, when root value is *
    :param tree: BinaryTree
    """
    left = tree.left_child
    right = tree.right_child
    if left:
        left = left.__copy__()
    if right:
        right = right.__copy__()

    if left.get_root_val() in ["0", "0.0", "-0", "-0.0"] or right.get_root_val() in ["0", "0.0", "-0", "-0.0"]:  # mnożenie przez 0
        tree.set_root_val("0")
        tree.left_child = None
        tree.right_child = None

    elif left.get_root_val() in ["1", "1.0"]:  # 1*2x
        tree.set_root_val(right.get_root_val())
        tree.left_child = right.left_child
        tree.right_child = right.right_child

    elif right.get_root_val() in ["1", "1.0"]:  # 2x*1
        tree.set_root_val(left.get_root_val())
        tree.left_child = left.left_child
        tree.right_child = left.right_child

    elif check_numeric(left.get_root_val()) and check_numeric(right.get_root_val()):  # 2*4
        tree.set_root_val(str(float(left.get_root_val())*float(right.get_root_val())))
        tree.left_child = None
        tree.right_child = None

    elif (right.left_child and right.right_child) and check_numeric(left.get_root_val()) and check_numeric(right.left_child.get_root_val()) and right.get_root_val() == "*":  # 2*4x
        tree.left_child.set_root_val(str(float(left.get_root_val())*float(right.left_child.get_root_val())))
        tree.right_child = right.right_child

        tree.left_child.left_child = None
        tree.left_child.right_child = None

    elif (right.left_child and right.right_child) and check_numeric(left.get_root_val()) and check_numeric(right.right_child.get_root_val()) and right.get_root_val() == "*":  # 2*x4
        tree.left_child.set_root_val(str(float(left.get_root_val())*float(right.right_child.get_root_val())))
        tree.right_child = right.left_child

        tree.left_child.left_child = None
        tree.left_child.right_child = None

    elif (left.left_child and left.right_child) and check_numeric(right.get_root_val()) and check_numeric(left.left_child.get_root_val()) and left.get_root_val() == "*":  # 4x*2
        tree.left_child.set_root_val(str(float(right.get_root_val())*float(left.left_child.get_root_val())))
        tree.right_child = left.right_child

        tree.left_child.left_child = None
        tree.left_child.right_child = None

    elif (left.left_child and left.right_child) and check_numeric(right.get_root_val()) and check_numeric(left.right_child.get_root_val()) and left.get_root_val() == "*":  # x4*2
        tree.left_child.set_root_val(str(float(right.get_root_val())*float(left.right_child.get_root_val())))
        tree.right_child = left.left_child

        tree.left_child.left_child = None
        tree.left_child.right_child = None

    elif left == right:  # sin(x)*sin(x)
        tree.set_root_val("^")
        tree.left_child = left
        tree.right_child = BinaryTree("2")

    elif left.get_root_val() == "^" and left.left_child == right:  # ((4x)^2)*4x
        tree.set_root_val("^")
        tree.left_child = left.left_child

        tree.right_child = BinaryTree("+")
        tree.right_child.left_child = left.right_child
        tree.right_child.right_child = BinaryTree("1")

    elif right.get_root_val() == "^" and right.left_child == left:  # x*((x)^2)
        tree.set_root_val("^")
        tree.left_child = right.left_child

        tree.right_child = BinaryTree("+")
        tree.right_child.left_child = right.right_child
        tree.right_child.right_child = BinaryTree("1")

    elif left.get_root_val() == "exp" and right.get_root_val() == "exp":
        tree.set_root_val("exp")
        tree.left_child = None
        tree.right_child = BinaryTree("+")

        right_left = left.right_child
        right_right = right.right_child

        tree.right_child.left_child = right_left
        tree.right_child.right_child = right_right

    elif left.get_root_val() == "*" and left.left_child.get_root_val() == "exp" and right.get_root_val() == "exp":
        tree.left_child = left.right_child
        tree.right_child = BinaryTree("exp")
        tree.right_child.right_child = BinaryTree("+")

        tree.right_child.right_child.left_child = left.left_child.right_child
        tree.right_child.right_child.right_child = right.right_child

    elif left.get_root_val() == "*" and left.right_child.get_root_val() == "exp" and right.get_root_val() == "exp":
        tree.left_child = left.left_child
        tree.right_child = BinaryTree("exp")
        tree.right_child.right_child = BinaryTree("+")

        tree.right_child.right_child.left_child = left.right_child.right_child
        tree.right_child.right_child.right_child = right.right_child

    elif left.get_root_val() == "/":  # (x/2)*x
        left = tree.left_child.__copy__()
        right = tree.right_child.__copy__()

        tree.set_root_val("/")

        tree.left_child.set_root_val("*")
        tree.left_child.left_child = left.left_child
        tree.left_child.right_child = right

        tree.right_child = left.right_child

    elif right.get_root_val() == "/":  # x*(x/2)
        left = tree.left_child.__copy__()
        right = tree.right_child.__copy__()

        tree.set_root_val("/")

        tree.left_child.set_root_val("*")
        tree.left_child.left_child = left
        tree.left_child.right_child = right.left_child

        tree.right_child = right.right_child


def tree_simplify_div(tree):
    """
    function simplifies BinaryTree, when root value is /
    :param tree: BinaryTree
    """
    left = tree.left_child
    right = tree.right_child
    if left:
        left = left.__copy__()
    if right:
        right = right.__copy__()

    if right.get_root_val() in ["0", "0.0", "-0", "-0.0"]:  # mianownik 0
        raise Exception("Błąd dzielenia przez 0 w podanym wyrażeniu")

    elif left.get_root_val() in ["0", "0.0", "-0", "-0.0"]:  # licznik to 0
        tree.set_root_val("0")
        tree.left_child = None
        tree.right_child = None

    elif right.get_root_val() in ["1", "1.0"]:  # mianownik to 1
        tree.set_root_val(left.get_root_val())
        tree.left_child = left.left_child
        tree.right_child = left.right_child

    elif left == right:  # licznik == mianownik
        tree.set_root_val("1")
        tree.left_child = None
        tree.right_child = None

    elif right.get_root_val() == "*" and left == right.left_child:  # licznik == mianownik
        tree.left_child = BinaryTree("1")
        tree.right_child = right.right_child

    elif right.get_root_val() == "*" and left == right.right_child:  # licznik == mianownik
        tree.left_child = BinaryTree("1")
        tree.right_child = right.left_child

    elif left.get_root_val() == "*" and left.left_child == right:  # licznik == mianownik
        tree.set_root_val(left.right_child.get_root_val())
        tree.left_child = left.right_child.left_child
        tree.right_child = left.right_child.right_child

    elif left.get_root_val() == "*" and left.right_child == right:  # licznik == mianownik
        tree.set_root_val(left.left_child.get_root_val())
        tree.left_child = left.left_child.left_child
        tree.right_child = left.left_child.right_child

    elif left.get_root_val() == "*" and right.get_root_val() == "*" and left.left_child == right.left_child:  # licznik == mianownik
        tree.left_child = left.right_child
        tree.right_child = right.right_child

    elif left.get_root_val() == "*" and right.get_root_val() == "*" and left.left_child == right.right_child:  # licznik == mianownik
        tree.left_child = left.right_child
        tree.right_child = right.left_child

    elif left.get_root_val() == "*" and right.get_root_val() == "*" and left.right_child == right.left_child:  # licznik == mianownik
        tree.left_child = left.left_child
        tree.right_child = right.right_child

    elif left.get_root_val() == "*" and right.get_root_val() == "*" and left.right_child == right.right_child:  # licznik == mianownik
        tree.left_child = left.left_child
        tree.right_child = right.left_child

    elif left.get_root_val() == "^" and left.left_child == right:  # licznik == mianownik
        tree.left_child.right_child = BinaryTree("-")
        tree.left_child.right_child.left_child = left.right_child
        tree.left_child.right_child.right_child = BinaryTree("1")
        tree.right_child = BinaryTree("1")

    elif left.get_root_val() == "^" and right.get_root_val() == "^" and left.left_child == right.left_child:  # licznik == mianownik
        tree.left_child.right_child = BinaryTree("-")
        tree.left_child.right_child.left_child = left.right_child
        tree.left_child.right_child.right_child = right.right_child
        tree.right_child = BinaryTree("1")


def tree_simplify_pow(tree):
    """
    function simplifies BinaryTree, when root value is ^
    :param tree: BinaryTree
    """
    left = tree.left_child
    right = tree.right_child
    if left:
        left = left.__copy__()
    if right:
        right = right.__copy__()

    if right.get_root_val() in ["0", "0.0", "-0", "-0.0"]:  # podnoszenie do potęgi 0
        tree.set_root_val("1")
        tree.left_child = None
        tree.right_child = None

    elif right.get_root_val() in ["1", "1.0"]:  # podnoszenie do potęgi 1
        tree.set_root_val(left.get_root_val())
        tree.left_child = left.left_child
        tree.right_child = left.right_child

    elif check_numeric(right.get_root_val()) and check_numeric(left.get_root_val()):  # podnoszenie liczby do potęgi liczby
        result = str(float(left.get_root_val()) ** float(right.get_root_val()))

        tree.set_root_val(result)
        tree.left_child = None
        tree.right_child = None

    elif check_numeric(right.get_root_val()) and left.get_root_val() == "*" and check_numeric(left.left_child.get_root_val()):  # podnoszenie mnożenia przez liczbę (lewo) do potęgi liczby
        result = str(float(left.left_child.get_root_val()) ** float(right.get_root_val()))

        tree.set_root_val("*")
        tree.left_child = BinaryTree(result)
        tree.right_child = BinaryTree("^")

        tree.right_child.left_child = left.right_child
        tree.right_child.right_child = right

    elif check_numeric(right.get_root_val()) and left.get_root_val() == "*" and check_numeric(left.right_child.get_root_val()):  # podnoszenie mnożenia przez liczbę (prawo) do potęgi liczby
        result = str(float(left.right_child.get_root_val()) ** float(right.get_root_val()))

        tree.set_root_val("*")
        tree.left_child = BinaryTree(result)
        tree.right_child = BinaryTree("^")

        tree.right_child.left_child = left.left_child
        tree.right_child.right_child = right


def check_numeric(element):
    """
    function checks if a string can be interpreted as a number
    :param element: string
    :return: bool
    """
    if not element:
        return False

    dot = False
    i = 0
    if element[0] == ".":
        raise Exception(f"Błędnie zapisana liczba {element}")
    while i < len(element):
        if element[i].isnumeric():
            pass
        elif element[i] == ".":
            if dot:
                raise Exception(f"Błędnie zapisana liczba {element}")
            else:
                dot = True
        elif element[i] == "-":
            if i != 0:
                raise Exception(f"Błędnie zapisana liczba {element}")
            elif i == len(element) - 1:
                return False
        else:
            return False
        i += 1
    return True


def tree_to_expression_main(tree):
    """
    main function that maintains converting BinaryTree of math expression to string process
    :param tree: BinaryTree
    :return: string
    """
    expression = tree_to_expression_recursive(tree)
    if expression and expression[0] == " ":
        expression = expression[1:]
    if expression and expression[-1] == " ":
        expression = expression[:-1]
    return expression


def tree_to_expression_recursive(tree):
    """
    function converts BinaryTree to string. Runs recursive
    :param tree: BinaryTree
    :return: string
    """
    left = tree.left_child
    right = tree.right_child

    if left:
        if left.left_child:
            left_expression = "(" + tree_to_expression_recursive(left) + ")"
        else:
            left_expression = tree_to_expression_recursive(left)
    else:
        left_expression = ""

    root_expression = tree.get_root_val()

    if right:
        if right.left_child:
            right_expression = "(" + tree_to_expression_recursive(right) + ")"
        else:
            right_expression = tree_to_expression_recursive(right)
    else:
        right_expression = ""

    if right and not left and right_expression[0] != "(":
        expression = root_expression + "(" + right_expression + ")"
    else:
        expression = left_expression + root_expression + right_expression
    return expression


if __name__ == "__main__":
    text = None
    text = "(cos(20.5x)+(3sin(x)))-((4exp(3x))/exp(x))"
#    text = "arc sin(2)      x"
#    text = "(x-1)(2x-2)"
#    text = "(cos(2x)+(3sin(x)))-(4exp(3x)/exp(x))"
#    text = "((100x)+(cossinexp2x+x))"
#    text = "(((100x)+(cos(sin(exp(2x)))+x)))"
#    text = "(x+x*x)^3"
#    text = "-(-2x+3x)^(3 + sin(2))"
#    text = "2exp2x"
#    text = "2log2x"
#    text = "2cschx2"
#    text = "2sechx2"
#    text = "2ctghx2"
#    text = "2tghx2"
#    text = "2coshx2"
#    text = "2sinhx2"
#    text = "2arccscx2"
#    text = "2arcsecx2"
#    text = "2arcctgx2"
#    text = "2arctg2x"
#    text = "2arccos2x"
#    text = "2arcsin2x"
#    text = "2csc2x"
#    text = "2x + 2x"
#    text = "4xctg2x"
#    text = "sin2x"
#    text = "(100x)+(cos(exp(2x))+x)"
#    text = "cos2x"
#    text = "sin2x - sinx"
#    text = "-sin-x/x"
#    text = "-sin-x/x + sinx / (-x) + x / 12 + 3-x/(x3) + (-x)/sin2x"
#    text = "12 + 33^2x + sin2x"
#    text = "2x + exp1 + exparccossin2x + 1"
#    text = "2x + exp1 + exparccossin2x+1"
#    text = "2x + 1 + arccos(arcsin2x)+1"
#    text = "2x + 1 + cos(sin2x)+1"
#    text = "sin 2x + 1 + sin 2x+1"
#    text = None
    if text is None:
        text = input("Podaj wyrażenie:\n")
    print(program_run(text))

# zostawiłem przykładowe funkcje po swoich testach dla ułatwienia :)



# Program wykonuje w pełni wszystkie wymagane funkcjonalności. Oprócz rzeczy wymaganych wspierane jest:
#
# - podawanie wyrażenia niekoniecznie w zapisie dwuargumentowym np. 2+x+3+x+4+x
#
# - podawanie wyrażenia matematycznego z pominięciem znaku mnożenia w sytuacjach "oczywistych" np. 2x, 2sin(2x), (x-1)(x-2)
#
# - podawanie wyrażenia matematycznego z pominięciem nawiasów oddzielające kolejność działań. Program inteligentnie
# wykrywa kolejność wykonywania operacji np. x+2*x^2
#
# - podawanie wyrażenia matematycznego z pominięciem nawiasów obejmujących argumenty funkcji
# np. sincosarcsintg2x -> sin(cos(arc_sin(tg(2*x)))), sin2x -> sin(2*x), sin 2x -> sin(2*x), sin 2 x -> sin(2)*x.

# Konwencja: nie ma znaczenia czy podana zostanie spacja po nazwie funkcji czy nie, jest to kwestia wygody użytkownika;
# jeśli nie ma nawiasów to za argument funkcji uznaje się wszystko do pierwszej spacji (pomijając spację po nazwie funkcji opisaną wcześniej);
# na tej samej zasadzie działa tworzenie funkcji złożonych (patrz przykład wyżej)
#
# - funkcje arcusowe można podawać w konwencji arcsin, lub arc_sin (domyślnie program pracuje na arc_sin, ale można
# napisać ciągiem jeśli jest tak wygodniej. Spacja nie jest dopuszczalna)
#
# - wspierane funkcje to: "sin", "cos", "tg", "ctg", "sec", "csc", "sinh", "cosh", "tgh", "ctgh", "sech", "csch", "log",
# "sqrt", "exp", "arc_sin", "arc_cos", "arc_tg", "arc_ctg", "arc_sec", "arc_csc"
#
# - program ma funkcjonalność skracania ostatecznego wyrażenia. Zdążyłem zaimplementować sporo rozwiązań od prosteg
# pomijania dodawania gdy jeden ze składników wynosi 0 do rozpoznawania dodawania wyrażeń podobnych pomnożonych przez
# różne stałe. W schemacie tego upraszczania mogą znajdować się nadal drobne błędy przy bardziej egzotycznych równaniach,
# których nie zdążyłem przetestować (przez brak czasu albo brak pomysłów). Jednak wszystkie wymagane w zadaniu funkcje
# powinny działać, a błędy powinny być nieliczne







