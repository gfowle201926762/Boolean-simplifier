# solve boolean algebra.
# you can use assertions in python!

from ast import operator
import string

from numpy import insert
from pandas import merge


# RECOGNISED CHARACTERS:
OPEN_BRACKET = '('
CLOSED_BRACKET = ')'
COMPLEMENT = '!'
DISJUNCTION = '+'
CONJUNCTION = '.'
IMPLICATION = '=>'
EQUIVALENCE = '<=>'
TRUE = '1'
FALSE = '0'

# CODED CHARACTERS:
IMPLICATION_CODE = '>'
EQUIVALENCE_CODE = '<'


class BooleanParser():

    def __init__(self):
        self.recognised_characters = [OPEN_BRACKET, CLOSED_BRACKET, COMPLEMENT, DISJUNCTION, CONJUNCTION, IMPLICATION_CODE, EQUIVALENCE_CODE, TRUE, FALSE] + list(string.ascii_lowercase) + list(string.ascii_uppercase)
        self.letters = list(string.ascii_lowercase) + list(string.ascii_uppercase)
        self.complementable = [COMPLEMENT, TRUE, FALSE, OPEN_BRACKET] + list(string.ascii_lowercase) + list(string.ascii_uppercase)
        self.operators = [DISJUNCTION, CONJUNCTION, IMPLICATION_CODE, EQUIVALENCE_CODE]
        self.simple_operators = [DISJUNCTION, CONJUNCTION]
        self.operator_precedence = {CONJUNCTION: 1, DISJUNCTION: 2, IMPLICATION_CODE: 3, EQUIVALENCE_CODE: 4}

    def check_implication(self, my_list):
        for i in range(0, len(my_list) - 1):
            test = my_list[i:i+2]
            if test == list(IMPLICATION):
                my_list[i] = IMPLICATION_CODE
                del my_list[i+1]
        return my_list

    def check_equivalence(self, my_list):
        for i in range(0, len(my_list) - 2):
            test = my_list[i:i+3]
            if test == list(EQUIVALENCE):
                my_list[i] = EQUIVALENCE_CODE
                del my_list[i + 1]
                del my_list[i + 1]
        return my_list

    def delete_unnecessary_chars(self, my_list):
        count = 0
        for char in my_list:
            if char not in self.recognised_characters:
                del my_list[count]
            count += 1
        return my_list

    def check_bracket_count(self, my_list):
        open_bracket_count = 0
        closed_bracket_count = 0
        for char in my_list:
            if char == OPEN_BRACKET:
                open_bracket_count += 1

            if char == CLOSED_BRACKET:
                closed_bracket_count += 1

            if closed_bracket_count > open_bracket_count:
                return 1
        if open_bracket_count != closed_bracket_count:
            return 1
        return 0

    def check_complement(self, my_list):
        #check the complement is infront of a letter or an open bracket, and nothing else.
        count = 0
        for char in my_list:
            if char == COMPLEMENT:
                if count != len(my_list) - 1:
                    next_char = my_list[count + 1]
                    if next_char not in self.complementable:
                        return 1
                else:
                    # complement found as last character, return error.
                    return 1
            count += 1
        return 0

    def check_variable(self, my_list):
        count = 0
        for char in my_list:
            if char in self.letters:
                if count != len(my_list) - 1:
                    if my_list[count + 1] in self.letters:
                        return 1
            count += 1
        return 0



    def deleting_the_brackets(self, my_list, count, i):
        #print(f"\n\nINCOMING COUNT: {count}\nINCOMING LIST: {''.join(my_list)} list length: {len(my_list)}")
        deletions = 0
        total_deletions = 0
        total_difference = 0
        while count - (1*deletions) + 1 < len(my_list) and i - (1*deletions) - 1 >= 0:
            #print(f"count + 1: {count - (1*deletions) + 1}, i - 1: {i - (1*deletions) - 1}")

            if my_list[count - (1*deletions) + 1] == CLOSED_BRACKET and my_list[i - (1*deletions) - 1] == OPEN_BRACKET:
                #print('\nCUNTABLE')
                del my_list[count - (1*deletions) + 1]
                del my_list[i - (1*deletions) - 1]
                deletions += 1
                total_deletions += 1

                original_length = len(my_list)
                my_list = self.delete_unnecessary_complements(my_list)
                difference = original_length - len(my_list)
                #print(f"difference here: {difference}")
                deletions += difference
                total_difference += difference
                #print(f"MODIFIED LIST: {''.join(my_list)} length: {len(my_list)}")
            
            elif i - (1*deletions) - 2 >= 0:
                if my_list[count - (1*deletions) + 1] == CLOSED_BRACKET and my_list[i - (1*deletions) - 1] == COMPLEMENT and my_list[i - (1*deletions) - 2] == OPEN_BRACKET:
                    #print("\nFUCKER")
                    del my_list[count - (1*deletions) + 1]
                    del my_list[i - (1*deletions) - 2]
                    deletions += 1
                    total_deletions += 1

                    #print(f"PRE-COMPLEMENTED MODIFIED LIST: {''.join(my_list)} length: {len(my_list)}")
                    original_length = len(my_list)
                    my_list = self.delete_unnecessary_complements(my_list)
                    difference = original_length - len(my_list)
                    deletions += difference
                    total_difference += difference
                    #print(f"MODIFIED LIST: {''.join(my_list)} length: {len(my_list)}")

                else:
                    return my_list, total_difference, total_deletions

            else:
                return my_list, total_difference, total_deletions

        return my_list, total_difference, total_deletions

    def delete_unnecessary_brackets_multiple(self, my_list):
        #print('\n\n')
        #print(f"MODIFIED LIST: {''.join(my_list)}")
        count = -1
        for char in range(0, len(my_list)):
            count += 1
            #print(f"COUNT: {count}")
            if count < len(my_list): 
                if my_list[count] == CLOSED_BRACKET:
                    #print(f'\nCLOSED BRACKET!! at {count}\nLIST: {"".join(my_list)}')
                    closed_bracket_count = 1
                    open_bracket_count = 0
                    for i in reversed(range(0, count)): # we removed a '- 1' from count.

                        if my_list[i] == CLOSED_BRACKET:
                            closed_bracket_count += 1

                        if my_list[i] == OPEN_BRACKET: # and closed_bracket_count > 1:
                            open_bracket_count += 1

                        if open_bracket_count == closed_bracket_count:
                            my_list, total_difference, deletions = self.deleting_the_brackets(my_list, count, i)
                            #print(f"TOTAL DIFFERENCE: {total_difference}\nDELETIONS: {deletions}")
                            count -= (total_difference + (deletions))
                            break

                        

        if my_list[len(my_list) - 1] == CLOSED_BRACKET and my_list[0] == OPEN_BRACKET:

            open_bracket_count = 0
            closed_bracket_count = 0
            count = 0
            delete_first_last = True
            for char in my_list:
                if char == OPEN_BRACKET:
                    open_bracket_count += 1
                if char == CLOSED_BRACKET:
                    closed_bracket_count += 1
                
                if open_bracket_count - closed_bracket_count == 0 and count < len(my_list) - 1:
                    delete_first_last = False
                    break

                count += 1
            
            if delete_first_last == True:
                del my_list[len(my_list) - 1]
                del my_list[0]

        my_list = self.delete_unnecessary_brackets(my_list)

        #print(f"\nEND OF MY_LIST {''.join(my_list)}\n")
        return my_list

    def delete_unnecessary_brackets(self, my_list):
        count = 0
        changed_single = False
        for char in my_list:
            if char == CLOSED_BRACKET:
                for i in reversed(range(0, count - 1)):
                    if my_list[i] == OPEN_BRACKET:
                        statement = my_list[i+1:count]

                        
                    
                        if len(statement) == 1:
                            changed_single = True
                            del my_list[count]
                            del my_list[i]

                        elif len(statement) == 2:
                            if my_list[i + 1] == COMPLEMENT and my_list[i + 2] in self.letters:
                                del my_list[count]
                                del my_list[i]

                        # what if this then makes a double negative? This must be checked for.
                        my_list = self.delete_unnecessary_complements(my_list)


                        break
            count += 1

        if changed_single == True:
            return self.delete_unnecessary_brackets(my_list)


        return my_list



    def delete_unnecessary_complements(self, my_list):
        count = 0
        for char in my_list:
            if char == COMPLEMENT:
                if count != len(my_list) - 2:
                    if my_list[count + 1] == COMPLEMENT:
                        del my_list[count]
                        del my_list[count]
            count += 1
        return my_list

    def evaluate_complements(self, my_list): # aka retard proofing
        #print(my_list)

        for count in range(0, len(my_list)):
            if count < len(my_list):
                if my_list[count] == COMPLEMENT:
                    if count + 1 < len(my_list):
                        if my_list[count + 1] == TRUE:
                            del my_list[count]
                            my_list[count] = FALSE
                        elif my_list[count + 1] == FALSE:
                            del my_list[count]
                            my_list[count] = TRUE
                    else: # In no circumstances should there be a complement at the end of a statement being evaluated.
                        return '[ERROR] Unexpected complement at end of list in evaluate_complements function'
                count += 1

        return my_list





    def simplify_constants(self, operator, variables):
        if len(variables) != 2:
            return '[ERROR] Unexpected quantity of variables in simplify_constants function'
        if operator == CONJUNCTION:
            if variables[0] == TRUE and variables[1] == TRUE:
                return [TRUE]
            else:
                return [FALSE]

        if operator == DISJUNCTION:
            if variables[0] == TRUE or variables[0] == TRUE:
                return [TRUE]
            else:
                return [FALSE]

        return '[ERROR] Unexpected operator in simplify_constants function'
        
    def identity_rule(self, operator, variables, complemented):
        if len(variables) != 2:
            return '[ERROR] Unexpected quantity of variables in simplify_constants function'

        if len(complemented) > 1:
            return '[ERROR] Unexpected quantity of complements in simplify_constants function'

        constant = None
        var = None
        for variable in variables:
            if variable == TRUE or variable == FALSE:
                constant = variable
            else:
                var = variable

        if len(complemented) == 1:
            var = [COMPLEMENT, var]

        if len(complemented) == 0:
            var = [var]
        
        if operator == CONJUNCTION:
            if constant == TRUE:
                return var
            if constant == FALSE:
                return [FALSE]
        
        if operator == DISJUNCTION:
            if constant == TRUE:
                return [TRUE]
            if constant == FALSE:
                return var

        return '[ERROR] Could not evaluate statement in identity_rule function'

    def idempotence_rule(self, operator, variables, complemented):
        if len(variables) != 2:
            return '[ERROR] Unexpected quantity of variables in idempotence_rule function'

        if variables[0] == variables[1]:

            if len(complemented) == 0:
                return [variables[0]]

            if len(complemented) == 1:
                if operator == DISJUNCTION:
                    return [TRUE]
                if operator == CONJUNCTION:
                    return [FALSE]

            if len(complemented) == 2:
                return [COMPLEMENT, variables[0]]

        return None

    def implication_rule(self, variables, complemented):

        if len(complemented) == 0:
            return [COMPLEMENT, variables[0], DISJUNCTION, variables[1]]

        if len(complemented) == 1:
            if variables[0] == complemented[0]:
                return [variables[0], DISJUNCTION, variables[1]]
            if variables[1] == complemented[0]:
                return [COMPLEMENT, variables[0], DISJUNCTION, COMPLEMENT, variables[1]]

        if len(complemented) == 2:
            return [variables[0], DISJUNCTION, COMPLEMENT, variables[1]]

    def equivalence_rule(self, variables, complemented):
        
        new_list = [OPEN_BRACKET, COMPLEMENT, variables[0], DISJUNCTION, variables[1], CLOSED_BRACKET, CONJUNCTION, OPEN_BRACKET, variables[0], DISJUNCTION, COMPLEMENT, variables[1], CLOSED_BRACKET]

        if len(complemented) == 0:
            return new_list

        if len(complemented) == 1:
            if variables[0] == complemented[0]:
                return [OPEN_BRACKET, variables[0], DISJUNCTION, variables[1], CLOSED_BRACKET, CONJUNCTION, OPEN_BRACKET, COMPLEMENT, variables[0], DISJUNCTION, COMPLEMENT, variables[1], CLOSED_BRACKET]

            if variables[1] == complemented[0]:
                return [OPEN_BRACKET, COMPLEMENT, variables[0], DISJUNCTION, COMPLEMENT, variables[1], CLOSED_BRACKET, CONJUNCTION, OPEN_BRACKET, variables[0], DISJUNCTION, variables[1], CLOSED_BRACKET]

            else:
                return '[ERROR] Unexpected complement in equivalence_rule function'

        if len(complemented) == 2:
            return [OPEN_BRACKET, variables[0], DISJUNCTION, COMPLEMENT, variables[1], CLOSED_BRACKET, CONJUNCTION, OPEN_BRACKET, COMPLEMENT, variables[0], DISJUNCTION, variables[1], CLOSED_BRACKET]

        return '[ERROR] Unexpected number of complements in equivalence_rule function'

    def absorption_rule(self, statement):
        pass

    def rejoin_operators(self, operator_list, statement_list, insert_before, insert_after, insert_within):
        non_bracket_indexes = []
        if insert_before == 1:
            non_bracket_indexes.append(0)
        for index in insert_within:
            non_bracket_indexes.append(index)
        if insert_after == 1:
            non_bracket_indexes.append(len(statement_list) - 1)

        #print(f"non-bracket indexes: {non_bracket_indexes}")
        #print(f"OPERATOR LIST: {operator_list}")

        re_joined_statements = []
        for count in range(0, len(statement_list)):
            if count not in non_bracket_indexes:
                re_joined_statements = re_joined_statements + [OPEN_BRACKET]

            re_joined_statements = re_joined_statements + statement_list[count]

            if count not in non_bracket_indexes:
                re_joined_statements = re_joined_statements + [CLOSED_BRACKET]

            if count < len(operator_list):
                re_joined_statements = re_joined_statements + [operator_list[count]]

        return re_joined_statements



    def evaluate_statement_original(self, statement):
        #print(f"\nSTATEMENT AT TOP OF EVALUATE: {statement}")
        # focus on just 2 variables first.
        variable_count = 0
        operator_count = 0
        complement_count = 0
        bracket_count = 0
        variables = []
        operators = []
        complemented = []

        statement = self.evaluate_complements(statement)

        count = 0
        for char in statement:
            if char in self.letters or char == TRUE or char == FALSE:
                variable_count += 1
                variables.append(char)
            if char in self.operators:
                operator_count += 1
                operators.append(char)
            if char == COMPLEMENT:
                complement_count += 1
                complemented.append(statement[count + 1])
            if char == OPEN_BRACKET or char == CLOSED_BRACKET:
                bracket_count += 1
            count += 1

        if bracket_count % 2 != 0:
            return '[ERROR] Unexpected number of brackets while parsing an inner statement'


        if bracket_count > 1:
            #print("BRACKETS IN THE EVALUATED STATEMENT!")

            #evaluated_statement = self.absorption_rule(statement)


            ev_statement = self.parse_tree(statement)
            if ev_statement != statement:
                ev_statement = self.evaluate_statement(ev_statement)
                #print(f"RETURNING {ev_statement}")
                return ev_statement





        evaluated_statement = None
        if operator_count == 1 and variable_count == 2 and bracket_count == 0:
            # expression with two variables connected with a disjunction or conjunction.

            if operators[0] == IMPLICATION_CODE:
                evaluated_statement = self.implication_rule(variables, complemented)

            elif operators[0] == EQUIVALENCE_CODE:
                evaluated_statement = self.equivalence_rule(variables, complemented)
            
            elif ((variables[0] == TRUE or variables[0] == FALSE) and (variables[1] == TRUE or variables[1] == FALSE)):
                # both variables are in fact constants.
                evaluated_statement = self.simplify_constants(operators[0], variables)

            elif (variables[0] == TRUE or variables[0] == FALSE or variables[1] == TRUE or variables[1] == FALSE):
                # there is one constant and one variable. Solve using identity rule.
                evaluated_statement = self.identity_rule(operators[0], variables, complemented)

            else: #only variables
                evaluated_statement = self.idempotence_rule(operators[0], variables, complemented)

        

        if evaluated_statement != None:
            #print("THERE WAS A CHANGE TO THE EVALUATED STATEMENT!")
            #print(f"RE EVALUATING / RETURNING {''.join(evaluated_statement)}")
            return self.evaluate_statement(evaluated_statement)

        #print(f"RETURNING {''.join(statement)}")
        return statement

    def parse_tree_original(self, my_list):
        # This function splits my_list into seperate lists representing the highest level statements.
        # These highest level statements may or may not contain lower level statements within themselves.
        # UNNECESSARY BRACKETS HAVE ALREADY BEEN REMOVED!

        print(f"\nSTATEMENT AT TOP OF PARSE TREE: {''.join(my_list)}")

        saved_statements = []
        total_statements = []
        saved_operators = []

        count = 0
        bracket_detection_count = 0
        insert_before = 0
        insert_after = 0
        insert_within = []


        saved_open_bracket_index = []
        saved_closed_bracket_index = []

        while count >= 0 and count < len(my_list):
            #print(f"COUNT: {count}")
            delayed_count_addition = 0
            delayed_complement_addition = 0
            if my_list[count] == OPEN_BRACKET:
                closed_bracket_count = 0
                open_bracket_count = 1
                for i in range(count + 1, len(my_list)):
                    if my_list[i] == OPEN_BRACKET:
                        open_bracket_count += 1
                    if my_list[i] == CLOSED_BRACKET:
                        closed_bracket_count += 1
                    if closed_bracket_count == open_bracket_count: # DETECTED A BRACKETED STATEMENT
                        #print("BRACKETED STATEMENT DETECTED!")

                        saved_open_bracket_index.append(count)
                        saved_closed_bracket_index.append(i)
                        
                        if count > 0:
                            if my_list[count-1] == COMPLEMENT: # EVALUATE THE BRACKETED STATEMENT IF IT HAS BEEN COMPLEMENTED (and is not the same as the original)!
                                statement = my_list[count-1:i+1]
                                if statement != my_list:
                                    evaluated_statement = self.evaluate_statement(statement) # RECURSION WARNING
                                    total_statements.append(evaluated_statement)
                                    saved_statements.append(statement)
                                    bracket_detection_count += 1
                                    delayed_count_addition = i - count
                                    delayed_complement_addition = 1
                                    if i+1 < len(my_list):
                                        saved_operators.append(my_list[i+1])
                                if statement == my_list:
                                    special_list = self.parse_tree(statement[2:len(statement)-1])
                                    special_list = ['!', '('] + special_list + [')']
                                    return special_list # this used to just be return my_list to prevent recursion.
                                break

                        statement = my_list[count+1:i] # NON-COMPLEMENTED BRACKETED STATEMENT
                        evaluated_statement = self.evaluate_statement(statement)
                        total_statements.append(evaluated_statement)
                        saved_statements.append(statement)
                        bracket_detection_count += 1
                        delayed_count_addition = i - count
                        if i+1 < len(my_list):
                            saved_operators.append(my_list[i+1])
                        break
                
                if count > 1 and bracket_detection_count == 1: # We have evaluated the first bracketed statement from the left. Check if there is anything else to the left.
                    if my_list[count - 1 - delayed_complement_addition] in self.operators:
                        #print("STATEMENT OUTSIDE OF BRACKETS AT START OF LIST")
                        statement = my_list[0:count-1-delayed_complement_addition]
                        evaluated_statement = self.evaluate_statement(statement)
                        total_statements.insert(0, evaluated_statement) # make sure this is inserted at index 0 of total statements.
                        saved_statements.insert(0, statement)
                        insert_before = 1
                        saved_operators.insert(0, my_list[count-1-delayed_complement_addition])
                    else:
                        return '[ERROR] Expected an operator while parsing string before the first bracketed statement.'

            count += delayed_count_addition
            count += 1
            
        

        for x in reversed(range(0, len(my_list))): # DETECTING UNBRACKETED STATEMENT AT THE END OF LIST
            if my_list[x] == CLOSED_BRACKET:
                if x < len(my_list) - 1: # FIRST closed bracket from the right, and it is not the rightmost character
                    if my_list[x+1] in self.operators:
                        if x + 2 < len(my_list):
                            #print("STATEMENT OUTSIDE OF BRACKETS AT END OF LIST")
                            statement = my_list[x+2:len(my_list)]
                            evaluated_statement = self.evaluate_statement(statement)
                            total_statements.append(evaluated_statement)
                            saved_statements.append(statement)
                            insert_after = 1
                        else:
                            return '[ERROR] Expected more characters while parsing string after the last bracketed statement.'
                    else:
                        return '[ERROR] Expected an operator while parsing string after the last bracketed statement.'
                break # we only need to detect the first closed bracket from the right

            
        count = 0
        for x in range(0, len(saved_closed_bracket_index)): # DETECTING UNBRACKETED STATEMENTS IN THE MIDDLE OF THE LIST
            if x < len(saved_closed_bracket_index) - 1:
                if saved_closed_bracket_index[count] + 3 < saved_open_bracket_index[count + 1]: # There must be a non-bracketed statement here.
                    #print("STATEMENT OUTSIDE OF BRACKETS IN MIDDLE OF LIST")

                    complemented_next_statement = 0
                    if my_list[saved_open_bracket_index[count + 1] - 1] == COMPLEMENT:
                        complemented_next_statement = 1

                    statement = my_list[saved_closed_bracket_index[count]+2:saved_open_bracket_index[count + 1]-1-complemented_next_statement]
                    evaluated_statement = self.evaluate_statement(statement)
                    index = count + insert_before + 1
                    total_statements.insert(index, evaluated_statement)
                    saved_statements.insert(index, statement)
                    insert_within.append(index)

                    if complemented_next_statement == 1:
                        saved_operators.append(my_list[saved_open_bracket_index[count + 1] - 2])
                    else:
                        saved_operators.append(my_list[saved_open_bracket_index[count + 1] - 1])

        if bracket_detection_count == 0: # NO BRACKETS: Must be an irreducible list.
            #print("NO BRACKETS DETECTED")
            evaluated_statement = self.evaluate_statement(my_list)
            return evaluated_statement


        # ABSTRACTING BIG STATEMENTS AS SINGLE VARIABLES, SO IT WILL WORK IN THE EVALUATE STATEMENT FUNCTION
        translated_list = None
        if bracket_detection_count > 0:
            print(f"\nSTATEMENT BEFORE ABSTRACTION: {''.join(my_list)}")
            non_bracket_indexes = []

            if insert_before == 1:
                non_bracket_indexes.append(0)
            for index in insert_within:
                non_bracket_indexes.append(index)
            if insert_after == 1:
                non_bracket_indexes.append(len(total_statements) - 1)

            converted_statements = []
            repeated_statements = []
            saved_equalities = {}
            repeated_count = {}

            for count in range(0, len(total_statements)):
                modified_statement = total_statements[count]
                if len(modified_statement) >= 3 and modified_statement[0] == COMPLEMENT and modified_statement[1] == OPEN_BRACKET and modified_statement[len(modified_statement)-1] == CLOSED_BRACKET:
                    modified_statement = modified_statement[2:len(modified_statement)-1]
                repeated = None
                no_of_repetitions = repeated_statements.count(modified_statement)
                if no_of_repetitions == 0:
                    repeated_statements.append(modified_statement)
                if no_of_repetitions > 0:
                    repeated = repeated_statements.index(modified_statement)
                
                pointer = count
                if repeated == None:
                    repeated_count[pointer] = 0
                if repeated != None:
                    pointer = repeated
                    repeated_count[pointer] += 0
                
                if total_statements[count][0] == COMPLEMENT:
                    bracketed = True # This is referring to brackets outside of what we can see in the total statements.
                    if count in non_bracket_indexes:
                        bracketed = False

                    inner_bracketing = False
                    if len(total_statements[count]) >= 3:
                        if total_statements[count][1] == OPEN_BRACKET and total_statements[count][len(total_statements[count])-1] == CLOSED_BRACKET:
                            inner_bracketing = True

                    if list(string.ascii_lowercase)[pointer] not in list(saved_equalities.keys()):
                        saved_equalities[list(string.ascii_lowercase)[pointer]] = {}

                    if inner_bracketing == True:
                        converted_statements.append([COMPLEMENT] + list(list(string.ascii_lowercase)[pointer]))
                        saved_equalities[list(string.ascii_lowercase)[pointer]][repeated_count[pointer]] = [total_statements[count][2:len(total_statements[count])-1], bracketed, False]


                    if inner_bracketing == False:
                        converted_statements.append(list(list(string.ascii_lowercase)[pointer]))
                        saved_equalities[list(string.ascii_lowercase)[pointer]][repeated_count[pointer]] = [total_statements[count], bracketed, False]



                else:
                    if len(total_statements[count]) == 1:
                        if total_statements[count][0] == TRUE or total_statements[count][0] == FALSE:
                            converted_statements.append(list(total_statements[count][0]))
                        else:
                            converted_statements.append(list(list(string.ascii_lowercase)[pointer]))
                            if list(string.ascii_lowercase)[pointer] not in list(saved_equalities.keys()):
                                saved_equalities[list(string.ascii_lowercase)[pointer]] = {}
                            saved_equalities[list(string.ascii_lowercase)[pointer]][repeated_count[pointer]] = [total_statements[count], False, False]
                    else:
                        converted_statements.append(list(list(string.ascii_lowercase)[pointer]))
                        bracketed = True
                        if count in non_bracket_indexes:
                            bracketed = False
                        if list(string.ascii_lowercase)[pointer] not in list(saved_equalities.keys()):
                            saved_equalities[list(string.ascii_lowercase)[pointer]] = {}
                        saved_equalities[list(string.ascii_lowercase)[pointer]][repeated_count[pointer]] = [total_statements[count], bracketed, False]


            print(f"converted statement, real OG: {(converted_statements)}")
            joined_converted_statements = self.rejoin_operators(saved_operators, converted_statements, insert_before, insert_after, insert_within)
            joined_converted_statements = self.delete_unnecessary_complements(joined_converted_statements)
            joined_converted_statements = self.delete_unnecessary_brackets_multiple(joined_converted_statements)

            print(f"converted statement, original: {''.join(joined_converted_statements)}")
            evaluated_converted_statement = self.evaluate_statement(joined_converted_statements)
            print(f"converted statement, evaluated: {''.join(evaluated_converted_statement)}")


            # PUT THE ABSTRACTED EVALUATED VALUES BACK INTO THIS LEVEL. Bracket it, but only if it was bracketed before.
            translated_list = []
            repeats = {}
            for count in range(0, len(evaluated_converted_statement)):
                if evaluated_converted_statement[count] in list(saved_equalities.keys()): # MUST BE A VARIABLE
                    print(f"\n{evaluated_converted_statement[count]}")
                    if evaluated_converted_statement[count] in list(repeats.keys()):
                        repeats[evaluated_converted_statement[count]] += 1
                    if evaluated_converted_statement[count] not in list(repeats.keys()):
                        repeats[evaluated_converted_statement[count]] = 0

                    print(f"SAVED EQUALITIES: {saved_equalities[evaluated_converted_statement[count]]}")
                    print(f"REPEATS: {repeats[evaluated_converted_statement[count]]}")
                    if saved_equalities[evaluated_converted_statement[count]][repeats[evaluated_converted_statement[count]]][1] == False: # THE STATEMENT WAS NOT BRACKETED
                        translated_list = translated_list + saved_equalities[evaluated_converted_statement[count]][repeats[evaluated_converted_statement[count]]][0]
                    
                    if saved_equalities[evaluated_converted_statement[count]][repeats[evaluated_converted_statement[count]]][1] == True: # THE STATEMENT WAS BRACKETED
                        translated_list = translated_list + [OPEN_BRACKET]
                        translated_list = translated_list + saved_equalities[evaluated_converted_statement[count]][repeats[evaluated_converted_statement[count]]][0]
                        translated_list = translated_list + [CLOSED_BRACKET]
                else: # IS NOT A VARIABLE
                    skip = False
                    if count + 1 < len(evaluated_converted_statement):
                        if evaluated_converted_statement[count + 1] in list(saved_equalities.keys()):
                            if evaluated_converted_statement[count] in list(repeats.keys()):
                                pointer = repeats[evaluated_converted_statement[count]] + 1
                            if evaluated_converted_statement[count] not in list(repeats.keys()):
                                pointer = 0
                            if saved_equalities[evaluated_converted_statement[count + 1]][pointer][2] == True: # DO NOT APPEND A ! IN THIS CASE!... How do we get its pointer though?
                                print("SKIPPING!")
                                skip = True
                    if skip == False:
                        translated_list = translated_list + [evaluated_converted_statement[count]]


            translated_list = self.delete_unnecessary_complements(translated_list)
            translated_list = self.delete_unnecessary_brackets_multiple(translated_list)
            print(f"translated statement: {''.join(translated_list)}")

        

        # RE-JOIN THE OPERATORS:
        if translated_list == None:
            translated_list = self.rejoin_operators(saved_operators, total_statements, insert_before, insert_after, insert_within)
            translated_list = self.delete_unnecessary_complements(translated_list)
            translated_list = self.delete_unnecessary_brackets_multiple(translated_list)

        #print(f"{total_statements}")
        #print(f"{''.join(re_joined_statements)}\n")

        if translated_list == my_list:
            return translated_list

        return self.parse_tree(translated_list)





    def get_statements(self, my_list):
        # This function scans through a list, and returns its highest order statements. These are not stripped.
        # If the statement has no brackets, then it will return the input.

        explicit_statement_start_index = [] # This stores the index in my_list where the detected statements start and end.
        explicit_statement_end_index = []

        total_statements = []
        count = 0
        while count >= 0 and count < len(my_list):
            if my_list[count] == OPEN_BRACKET:
                open_bracket_count = 1
                closed_bracket_count = 0
                for i in range(count+1, len(my_list)):
                    if my_list[i] == OPEN_BRACKET:
                        open_bracket_count += 1
                    if my_list[i] == CLOSED_BRACKET:
                        closed_bracket_count += 1
                    if closed_bracket_count == open_bracket_count:
                        complemented = False
                        if count - 1 >= 0:
                            if my_list[count - 1] == COMPLEMENT: # complemented bracket detected!
                                complemented = True
                                statement = my_list[count-1:i+1]
                                explicit_statement_start_index.append(count-1)
                                explicit_statement_end_index.append(i+1)
                        if complemented == False:
                            statement = my_list[count:i+1]
                            explicit_statement_start_index.append(count)
                            explicit_statement_end_index.append(i+1)
                        total_statements.append(statement)
                        count = i
                        break
            
            else: # DEFINITELY NOT BRACKETED (unless a complement, for which we check...)
                if my_list[count] == COMPLEMENT:
                    bracketed = False
                    if count + 1 < len(my_list):
                        if my_list[count + 1] == OPEN_BRACKET:
                            bracketed = True

                        if bracketed == False:
                            if my_list[count + 1] in self.letters:
                                statement = my_list[count:count+2]
                                total_statements.append(statement)
                                count += 1
                    else:
                        return '[ERROR] Unexpected complement at end of statement'
                
                elif my_list[count] in self.letters or my_list[count] == TRUE or my_list[count] == FALSE: # Not complemented: count has skipped it if it was.
                    statement = my_list[count:count+1]
                    total_statements.append(statement)

                elif my_list[count] in self.operators:
                    statement = my_list[count:count+1]
                    total_statements.append(statement)

            count += 1

        #print(f"TOTAL STATEMENTS: {total_statements}")
        return total_statements

    def abstract_statements(self, total_statements):

        abstracted_statements = []
        seen_statements = []
        count = 0
        for statement in total_statements:
            pointer = count
            if statement in seen_statements:
                pointer = seen_statements.index(statement)

            if statement[-1] == CLOSED_BRACKET and statement[0] == COMPLEMENT:
                if statement[1:] in seen_statements:
                    pointer = seen_statements.index(statement[1:])
            
            if statement[-1] == CLOSED_BRACKET:
                if statement[0] == COMPLEMENT:
                    if statement[1:] not in seen_statements:
                        seen_statements.append(statement[1:])
                    new_statement = [COMPLEMENT, OPEN_BRACKET, list(string.ascii_uppercase)[pointer], CLOSED_BRACKET]
                    abstracted_statements.append(new_statement)

                elif statement[0] == OPEN_BRACKET:
                    if statement not in seen_statements:
                        seen_statements.append(statement)
                    new_statement = [OPEN_BRACKET, list(string.ascii_uppercase)[pointer], CLOSED_BRACKET]
                    abstracted_statements.append(new_statement)

                else:
                    print("[ERROR] Unexpected value while trimming a statement")
                    return '[ERROR] Unexpected value while trimming a statement'   

                count += 1             
            else:
                abstracted_statements.append(statement)
            
        #print(f"ABSTRACTED STATEMENTS: {abstracted_statements}")
        return abstracted_statements

    def trim_statement(self, statement):
        if statement[-1] == CLOSED_BRACKET and statement[0] == OPEN_BRACKET:
            return statement[1:len(statement)-1]
        elif statement[-1] == CLOSED_BRACKET and statement[0] == COMPLEMENT:
            return statement[2:len(statement)-1]
        else:
            return statement

    def binary_matches(self, statement):
        # only find matches if there are NO BRACKETS IN THE TRIMMED STATEMENT

        statement = self.trim_statement(statement)

        for char in statement:
            if char == OPEN_BRACKET:
                return []

        total_statements = self.get_statements(statement)

        operators = []
        for s in total_statements:
            if len(s) == 1:
                if s[0] in self.operators:
                    operators.append(s[0])
        


        binary_matches = []
        # go from right to left (for implication and equivalence precendence), so reverse the operator order.
        for i in reversed(range(0, len(operators))):
            #print(f"i: {i}")
            if i+1 < len(operators) and i-1 >= 0: # operator either side
                if self.operator_precedence[operators[i]] < self.operator_precedence[operators[i-1]] and self.operator_precedence[operators[i]] < self.operator_precedence[operators[i+1]]:
                    match = total_statements[i*2] + total_statements[(i*2)+1] + total_statements[(i*2)+2]
                    binary_matches.append(match)
                elif self.operator_precedence[operators[i]] == self.operator_precedence[operators[i-1]] and self.operator_precedence[operators[i]] < self.operator_precedence[operators[i+1]] and (self.operator_precedence[operators[i]] == 3 or self.operator_precedence[operators[i]] == 4):
                    match = total_statements[i*2] + total_statements[(i*2)+1] + total_statements[(i*2)+2]
                    binary_matches.append(match)
            if i+1 < len(operators) and i-1 < 0: # one operator to the right
                if self.operator_precedence[operators[i]] < self.operator_precedence[operators[i+1]]:
                    match = total_statements[i*2] + total_statements[(i*2)+1] + total_statements[(i*2)+2]
                    binary_matches.append(match)
            if i+1 >= len(operators) and i-1 >= 0: # one operator to the left
                if self.operator_precedence[operators[i]] < self.operator_precedence[operators[i-1]]:
                    match = total_statements[i*2] + total_statements[(i*2)+1] + total_statements[(i*2)+2]
                    binary_matches.append(match)
                elif self.operator_precedence[operators[i]] == self.operator_precedence[operators[i-1]] and (self.operator_precedence[operators[i]] == 3 or self.operator_precedence[operators[i]] == 4):
                    match = total_statements[i*2] + total_statements[(i*2)+1] + total_statements[(i*2)+2]
                    binary_matches.append(match)
            if i+1 >= len(operators) and i-1 < 0: # it is the only operator...
                match = total_statements[i*2] + total_statements[(i*2)+1] + total_statements[(i*2)+2]
                binary_matches.append(match)

        binary_matches = list(reversed(binary_matches))
        #print(f"BINARY MATCHES: {binary_matches}")
        return binary_matches

    def multiple_matches(self, statement):
        # ONLY IF THERE ARE NO BRACKETS IN THE TRIMMED STATEMENT
        
        statement = self.trim_statement(statement)
        #print(f"\nINITIAL STATEMENT: {''.join(statement)}")

        for char in statement:
            if char == OPEN_BRACKET:
                #print('[ERROR] bracket in trimmed statement')
                return []

        total_statements = self.get_statements(statement)

        operators = []
        for s in total_statements:
            if len(s) == 1:
                if s[0] in self.operators:
                    operators.append(s[0])

        #print(f"TOTAL STATEMENTS: {total_statements}")

        multiple_matches = []
        i = 0
        while i >= 0 and i < len(operators):
            #print(f"\ni: {i}, OPERATOR: {operators[i]}")
            if self.operator_precedence[operators[i]] < 3:
                breaking = False
                for x in range(i, len(operators)):
                    if operators[i] != operators[x]:
                        breaking = True
                        break
                #print(f"x: {x}")
                if x-1 >= 0:
                    match = []
                    if self.operator_precedence[operators[x]] > self.operator_precedence[operators[x-1]]: # The next operator after the last in the chain has a lower precedence.
                        for j in range(i*2, (x*2)+1):
                            match = match + total_statements[j]
                        if len(self.get_statements(match)) > 3:
                            #print(f"APPENDING if: {match}")
                            multiple_matches.append(match)
                            i = x
                    
                    elif breaking == False:
                        for j in range(i*2, (x*2)+3):
                            match = match + total_statements[j]
                        if len(self.get_statements(match)) > 3:
                            #print(f"APPENDING elif: {match}")
                            multiple_matches.append(match)
                            i = len(operators)

                    else:
                        for j in range(i*2, (x*2)-1):
                            match = match + total_statements[j]
                        if len(self.get_statements(match)) > 3:
                            #print(f"APPENDING else: {match}")
                            multiple_matches.append(match)
                            i = x-1
            i += 1

        print(f"MULTIPLE MATCHES: {multiple_matches}")
        return multiple_matches

    def evaluate_binary_statement(self, statement):
        #print(f"INCOMING BINARY STATEMENT: {statement}")

        statement = self.evaluate_complements(statement)

        operator = None
        operator_count = 0
        count = 0
        variables = []
        complemented = []
        for char in statement:
            if char in self.operators:
                operator = char
                operator_count += 1
            if char in self.letters or char == TRUE or char == FALSE:
                variables.append(char)
            if char == COMPLEMENT:
                complemented.append(statement[count + 1])
            count += 1

        if operator_count != 1 or operator == None:
            print('[ERROR] Unexpected operator count while evaluating a binary statement')
            return '[ERROR] Unexpected operator count while evaluating a binary statement'

        evaluated_statement = None

        primary_check = False
        if operator == IMPLICATION_CODE:
            evaluated_statement = self.implication_rule(variables, complemented)
            primary_check = True
        if operator == EQUIVALENCE_CODE:
            evaluated_statement = self.equivalence_rule(variables, complemented)
            primary_check = True
        
        if primary_check == False:
            both_constants = False
            if ((variables[0] == TRUE or variables[0] == FALSE) and (variables[1] == TRUE or variables[1] == FALSE)):
                # both variables are in fact constants.
                evaluated_statement = self.simplify_constants(operator, variables)
                both_constants = True

            if (variables[0] == TRUE or variables[0] == FALSE or variables[1] == TRUE or variables[1] == FALSE) and both_constants == False:
                # there is one constant and one variable. Solve using identity rule.
                evaluated_statement = self.identity_rule(operator, variables, complemented)

            if (variables[0] != TRUE and variables[0] != FALSE and variables[1] != TRUE and variables[1] != FALSE): #only variables
                evaluated_statement = self.idempotence_rule(operator, variables, complemented)



        

        if evaluated_statement == None:
            return statement

        evaluated_statement = self.evaluate_complements(evaluated_statement)

        # go straight to the parse tree.


        #print(f"EVALUATED STATEMENT: {''.join(evaluated_statement)}")
        return evaluated_statement

    def unpack_multiple_matches(self, statement):
        # assuming the return (each statement in iteration) of the multiple matches function is being passed into here.
        # all the operators will be the same.
        total_statements = self.get_statements(statement)

        # all possible combinations to be exhausted.
        operator = statement[1]
        possible_combinations = []
        for i in range(0, len(total_statements)):
            if i % 2 == 0:
                for x in range(i+2, len(total_statements)):
                    if x % 2 == 0:
                        match = total_statements[i] + [operator] + total_statements[x]
                        possible_combinations.append(match)

        #print(f"POSSIBLE COMBINATIONS: {possible_combinations}")
        return possible_combinations

    def merge_lists(self, statements):
        merged_list = []
        for statement in statements:
            merged_list = merged_list + statement
        return merged_list

    def all_binary_matches(self, statements): # I DO NOT UNDERSTAND WHY THIS FUNCTION WORKS.
        # if there is a repeated binary match, then surely it will index at the incorrect place?
        # also, why the fuck is the statements list changing DIFFERENTLY to the all evaluated statements list?
            # this is answered - the function calls later do not change the original. But messing with pointers in the same function does change an equivalence.
        # wtf?

        #print(f"\nINCOMING STATEMENTS {statements}")
        # statements coming in in total_statement format.
        binary_matches = self.binary_matches(self.merge_lists(statements))
        #print(f"BINARY MATCHES: {binary_matches}")

        all_evaluated_statements = statements
        for i in range(0, len(binary_matches)):
            evaluated_binary_statement = self.evaluate_binary_statement(binary_matches[i])
            for x in range(0, len(statements)):
                if x < len(statements)-2:
                    possible_link = self.merge_lists(statements[x:x+3])
                    if possible_link == binary_matches[i]:
                        evaluated_link = self.get_statements(evaluated_binary_statement)
                        if len(evaluated_link) == 1:
                            all_evaluated_statements[x] = evaluated_link[0]
                            all_evaluated_statements[x+1] = ['-']
                            all_evaluated_statements[x+2] = ['-']
                        else:
                            all_evaluated_statements[x] = [OPEN_BRACKET] + evaluated_link[0]
                            all_evaluated_statements[x+1] = evaluated_link[1]
                            the_rest = []
                            for k in range(2, len(evaluated_link)):
                                the_rest += evaluated_link[k]
                            all_evaluated_statements[x+2] = the_rest + [CLOSED_BRACKET]
                        break

        #print(f"all evaluated statements up here: {all_evaluated_statements}") # at this point, all_evaluated_statements == statements.
        
        # when putting all_evaluated_statements into a function, the overwriting does not affect the original statements list.
        all_evaluated_statements = self.merge_lists(all_evaluated_statements)
        all_evaluated_statements = self.delete_unnecessary_brackets_multiple(all_evaluated_statements)
        all_evaluated_statements = self.get_statements(all_evaluated_statements)

        # after these function calls, all_evaluated_statements is now different from the original statements list.
        #print(f"ALL EVALUATED STATEMENTS: {all_evaluated_statements}\n")
        #print(f"total statements...: {statements}\n")
        return all_evaluated_statements

    def all_multiple_matches(self, statements):
        pass

    def save_abstraction(self, abstracted_statements, original_statements):
        linked_statements = {}
        for i in range(0, len(abstracted_statements)):
            if len(abstracted_statements[i]) == 1:
                if abstracted_statements[i][0] in list(string.ascii_uppercase):
                    #found an abstracted statement
                    if abstracted_statements[i][0] not in list(linked_statements.keys()):
                        linked_statements[abstracted_statements[i][0]] = original_statements[i]
        return linked_statements
        
    def rejoin_abstraction(self, eval_abstract_statements, linked_statements):
        # the abstracted statement and the original statement would have the same length; statements would have the same index.
        # bu what about after the abstracted statement has been evaluated?
        merged_eval_abstract_statements = self.merge_lists(eval_abstract_statements)
        #print(f"ORIGINAL MERGED STATEMENTS: {merged_eval_abstract_statements}")
        for i in range(0, len(merged_eval_abstract_statements)):
            if merged_eval_abstract_statements[i] in list(string.ascii_uppercase):
                replacement = linked_statements[merged_eval_abstract_statements[i]]
                merged_eval_abstract_statements[i] = [OPEN_BRACKET] + replacement + [CLOSED_BRACKET]
            else:
                merged_eval_abstract_statements[i] = [merged_eval_abstract_statements[i]]

        #print(f"pre-merge: {merged_eval_abstract_statements}")
        merged_eval_statements = self.merge_lists(merged_eval_abstract_statements)
        #print(f"post-merge: {merged_eval_statements}")

        merged_eval_statements = self.delete_unnecessary_brackets_multiple(merged_eval_statements)
        #print(f"post-merge de-bracketed: {merged_eval_statements}")
        rejoined_statements = self.get_statements(merged_eval_statements)
        return rejoined_statements


    def parse_tree(self, my_list):
        #print(f"\nmy_list up here: {(my_list)}")
        # SPLIT INTO STATEMENTS
        total_statements = self.get_statements(my_list) # untrimmed brackets, complements, and operators

        # EVALUATE WITHOUT ABSTRACTION
        eval_total_statements = self.all_binary_matches(total_statements) # finds potential binary matches and replaces them if evaluatable.
        #print(f"FIRST BINARY EVALUATION: {(eval_total_statements)}")

        # ABSTRACT
        abstracted_statements = self.abstract_statements(eval_total_statements) # untrimmed, the inside of bracketed statements abstracted with ascii uppercase
        # Format without unneccessary brackets...
        merged_abstracted_statements = self.merge_lists(abstracted_statements)
        merged_abstracted_statements = self.delete_unnecessary_brackets_multiple(merged_abstracted_statements)
        abstracted_statements = self.get_statements(merged_abstracted_statements)
        #print(f"ABSTRACTED: {(abstracted_statements)}")

        # save abstraction
        linked_statements = self.save_abstraction(abstracted_statements, eval_total_statements)
        #print(f"LINKED STATEMENTS: {(linked_statements)}")
        
        # EVALUATE WITH ABSTRACTION
        eval_abstract_statements = self.all_binary_matches(abstracted_statements)
        #print(f"EVALUATED ABSTRACTED STATEMENTS: {(eval_abstract_statements)}")

        # rejoin abstraction to original statements
        eval_statements = self.rejoin_abstraction(eval_abstract_statements, linked_statements)
        #print(f"EVALUATED ANSWER: {(eval_statements)}")
        #print(f"my_list: {(my_list)}")
        

        if my_list != self.merge_lists(eval_statements):
            return self.parse_tree(self.merge_lists(eval_statements))

        return eval_statements







    def parse_string(self, my_string):
        my_list = list(my_string)
        my_list = self.check_equivalence(my_list)
        my_list = self.check_implication(my_list)
        my_list = self.delete_unnecessary_chars(my_list)

        bracket_check = self.check_bracket_count(my_list)
        if bracket_check == 1:
            print('[ERROR] BRACKET ERROR')
            return '[ERROR] BRACKET ERROR'

        complement_check = self.check_complement(my_list)
        if complement_check == 1:
            print('[ERROR] COMPLEMENT ERROR')
            return '[ERROR] COMPLEMENT ERROR'

        variable_check = self.check_variable(my_list)
        if variable_check == 1:
            print('[ERROR] VARIABLE ERROR')
            return '[ERROR] VARIABLE ERROR'

        my_list = self.delete_unnecessary_complements(my_list)
        my_list = self.delete_unnecessary_brackets_multiple(my_list)

        print(f"\nINITIAL LIST: {''.join(my_list)}")
        my_list = self.merge_lists(self.parse_tree(my_list))
        print(f"MY ANSWER:    {''.join(my_list)}\n")
        #for i in range(0, len(my_list)):
        #    print(''.join(my_list[i]))
        #print('\n')
        
        return my_list







# tests
boolean_parser = BooleanParser()
def test():
    

    # converting implications and equivalences to single character codes
    #test_string = ' <=>=>=>hello,! => there<=> are impl=>ications=><=> '
    #assert boolean_parser.parse_string(test_string) == list('><<hello!<there>areimpl<ications<>')

    # checking the brackets are legal
    test_string = ')('
    assert boolean_parser.check_bracket_count(list(test_string)) == 1

    test_string = '(()))('
    assert boolean_parser.check_bracket_count(list(test_string)) == 1

    test_string = '()()'
    assert boolean_parser.check_bracket_count(list(test_string)) == 0

    test_string = '((h)(v(p(e))))'
    assert boolean_parser.check_bracket_count(list(test_string)) == 0

    #checking complements are in legal positions
    test_string = '!h'
    assert boolean_parser.check_complement(list(test_string)) == 0

    test_string = '!h!'
    assert boolean_parser.check_complement(list(test_string)) == 1

    test_string = '!1+(r + (!e.!s))'
    assert boolean_parser.check_complement(list(test_string)) == 0

    test_string = '!!1+(r + (!!!e.!s))'
    assert boolean_parser.check_complement(list(test_string)) == 0

    test_string = '1!+(r + (!e.!s))'
    assert boolean_parser.check_complement(list(test_string)) == 1

    test_string = '1+(r + (!e.!s)!)!'
    assert boolean_parser.check_complement(list(test_string)) == 1

    #checking variables are not bunched together
    test_string = '!hh'
    assert boolean_parser.check_variable(list(test_string)) == 1

    test_string = '1+(r + (!e.!se)!)!'
    assert boolean_parser.check_complement(list(test_string)) == 1

    test_string = '!1+(r + (!e.!s))'
    assert boolean_parser.check_complement(list(test_string)) == 0

    #removing unnecessary complements
    test_string = '!!!1+(r + (!!e.!s))'
    assert boolean_parser.delete_unnecessary_complements(list(test_string)) == list('!1+(r + (e.!s))')

    test_string = '!!(r.!p)+!!!!!(!!u+!!!p).!(i+!i)'
    assert boolean_parser.delete_unnecessary_complements(list(test_string)) == list('(r.!p)+!(u+!p).!(i+!i)')

    #evaluating complements... aka retard proofing
    test_string = '!0.0.!1+(r + (1.!0))'
    assert boolean_parser.evaluate_complements(list(test_string)) == list('1.0.0+(r + (1.1))')

    #delete unneccessary brackets... phew that was fucking arduous
    test_string = '(v)'
    assert boolean_parser.delete_unnecessary_brackets_multiple(list(test_string)) == list('v')

    test_string = '((v))'
    assert boolean_parser.delete_unnecessary_brackets_multiple(list(test_string)) == list('v')

    test_string = '((h).(v))'
    assert boolean_parser.delete_unnecessary_brackets_multiple(list(test_string)) == list('h.v')

    test_string = '(((h)).((((((v)))))))'
    assert boolean_parser.delete_unnecessary_brackets_multiple(list(test_string)) == list('h.v')

    test_string = '(h.((((v+i)))))'
    assert boolean_parser.check_bracket_count(list(test_string)) == 0
    assert boolean_parser.delete_unnecessary_brackets_multiple(list(test_string)) == list('h.(v+i)')

    test_string = '(((((v+r)))))'
    assert boolean_parser.check_bracket_count(list(test_string)) == 0
    assert boolean_parser.delete_unnecessary_brackets_multiple(list(test_string)) == list('v+r')

    test_string = '(((((((((v))))+(r))))))'
    assert boolean_parser.check_bracket_count(list(test_string)) == 0
    assert boolean_parser.delete_unnecessary_brackets_multiple(list(test_string)) == list('v+r')

    test_string = '(x+(y)).((((e))))+((e.r)+(t))'
    assert boolean_parser.check_bracket_count(list(test_string)) == 0
    assert boolean_parser.delete_unnecessary_brackets_multiple(list(test_string)) == list('(x+y).e+((e.r)+t)')

    test_string = '(x+(((((y)))))).((((e))))+((((((e.r)))+((t)))))'
    assert boolean_parser.check_bracket_count(list(test_string)) == 0
    assert boolean_parser.delete_unnecessary_brackets_multiple(list(test_string)) == list('(x+y).e+((e.r)+t)')

    test_string = '(((1))+((!(!(!(y)))))).((!((!e))))+((((((!e.!r)))+(!(!t)))))'
    assert boolean_parser.check_bracket_count(list(test_string)) == 0
    assert boolean_parser.delete_unnecessary_brackets_multiple(list(test_string)) == list('(1+!y).e+((!e.!r)+t)')

    test_string = '(((1))+((!(!(!(y)))))).((!((!e))))+((((!(!(!e.!r)))+(!(!t)))))'
    assert boolean_parser.check_bracket_count(list(test_string)) == 0
    assert boolean_parser.delete_unnecessary_brackets_multiple(list(test_string)) == list('(1+!y).e+((!e.!r)+t)')

    test_string = '!(!(!e+d))'
    assert boolean_parser.check_bracket_count(list(test_string)) == 0
    assert boolean_parser.delete_unnecessary_brackets_multiple(list(test_string)) == list('!e+d')

    test_string = '(!(!(!e+d))).!((!(v))+0)'
    assert boolean_parser.check_bracket_count(list(test_string)) == 0
    assert boolean_parser.delete_unnecessary_brackets_multiple(list(test_string)) == list('(!e+d).!(!v+0)')

    test_string = '!((!(!(!e+d))).!((!(v))+0))+!v'
    assert boolean_parser.check_bracket_count(list(test_string)) == 0
    assert boolean_parser.delete_unnecessary_brackets_multiple(list(test_string)) == list('!((!e+d).!(!v+0))+!v')

    test_string = '!(!((!(!(!e+d))).!((!(v))+0)))+!v'
    assert boolean_parser.check_bracket_count(list(test_string)) == 0
    assert boolean_parser.delete_unnecessary_brackets_multiple(list(test_string)) == list('((!e+d).!(!v+0))+!v')

    test_string = '!(((v+e).((a+b)+(z.!x)))+((e+f).(e.g)))'
    assert boolean_parser.check_bracket_count(list(test_string)) == 0
    assert boolean_parser.delete_unnecessary_brackets_multiple(list(test_string)) == list('!(((v+e).((a+b)+(z.!x)))+((e+f).(e.g)))')

    test_string = '!!!(((v+e).((a+(!(!(b))))+!(!(z.!x))))+((e+f).!(!(e.g))))'
    assert boolean_parser.check_bracket_count(list(test_string)) == 0
    assert boolean_parser.delete_unnecessary_brackets_multiple(list(test_string)) == list('!(((v+e).((a+b)+(z.!x)))+((e+f).(e.g)))')


def test2(): #test was getting too long...

    #identity rule
    operator = CONJUNCTION
    variables = ['x', FALSE]
    complements = []
    assert boolean_parser.identity_rule(operator, variables, complements) == [FALSE]

    operator = CONJUNCTION
    variables = ['x', TRUE]
    complements = []
    assert boolean_parser.identity_rule(operator, variables, complements) == ['x']

    operator = CONJUNCTION
    variables = ['x', TRUE]
    complements = ['x']
    assert boolean_parser.identity_rule(operator, variables, complements) == [COMPLEMENT, 'x']

    operator = DISJUNCTION
    variables = [FALSE, 'a']
    complements = []
    assert boolean_parser.identity_rule(operator, variables, complements) == ['a']

    operator = DISJUNCTION
    variables = [FALSE, 'a']
    complements = ['a']
    assert boolean_parser.identity_rule(operator, variables, complements) == [COMPLEMENT, 'a']

    operator = DISJUNCTION
    variables = [TRUE, 'a']
    complements = []
    assert boolean_parser.identity_rule(operator, variables, complements) == [TRUE]


    #more retard proofing:
    operator = CONJUNCTION
    variables = [FALSE, FALSE]
    assert boolean_parser.simplify_constants(operator, variables) == [FALSE]

    operator = CONJUNCTION
    variables = [TRUE, TRUE]
    assert boolean_parser.simplify_constants(operator, variables) == [TRUE]

    operator = DISJUNCTION
    variables = [FALSE, FALSE]
    assert boolean_parser.simplify_constants(operator, variables) == [FALSE]

    operator = DISJUNCTION
    variables = [TRUE, FALSE]
    assert boolean_parser.simplify_constants(operator, variables) == [TRUE]

    #idempotence
    operator = DISJUNCTION
    variables = ['x', 'x']
    complements = []
    assert boolean_parser.idempotence_rule(operator, variables, complements) == ['x']

    operator = DISJUNCTION
    variables = ['x', 'y']
    complements = []
    assert boolean_parser.idempotence_rule(operator, variables, complements) == None

    operator = DISJUNCTION
    variables = ['x', 'x']
    complements = ['x']
    assert boolean_parser.idempotence_rule(operator, variables, complements) == [TRUE]

    operator = DISJUNCTION
    variables = ['x', 'x']
    complements = ['x', 'x']
    assert boolean_parser.idempotence_rule(operator, variables, complements) == [COMPLEMENT, 'x']

    operator = CONJUNCTION
    variables = ['x', 'x']
    complements = ['x']
    assert boolean_parser.idempotence_rule(operator, variables, complements) == [FALSE]

    operator = CONJUNCTION
    variables = ['x', 'y']
    complements = ['x', 'y']
    assert boolean_parser.idempotence_rule(operator, variables, complements) == None

    #implication rules
    variables = ['x', 'y']
    complements = ['x', 'y']
    assert boolean_parser.implication_rule(variables, complements) == ['x', DISJUNCTION, COMPLEMENT, 'y']

    variables = ['x', 'y']
    complements = []
    assert boolean_parser.implication_rule(variables, complements) == [COMPLEMENT, 'x', DISJUNCTION, 'y']

    variables = ['x', 'y']
    complements = ['y']
    assert boolean_parser.implication_rule(variables, complements) == [COMPLEMENT, 'x', DISJUNCTION, COMPLEMENT, 'y']

    #equivalence rules
    variables = ['x', 'y']
    complements = []
    assert boolean_parser.equivalence_rule(variables, complements) == [OPEN_BRACKET, COMPLEMENT, 'x', DISJUNCTION, 'y', CLOSED_BRACKET, CONJUNCTION, OPEN_BRACKET, 'x', DISJUNCTION, COMPLEMENT, 'y', CLOSED_BRACKET]

    variables = ['x', 'y']
    complements = ['y']
    assert boolean_parser.equivalence_rule(variables, complements) == [OPEN_BRACKET, COMPLEMENT, 'x', DISJUNCTION, COMPLEMENT, 'y', CLOSED_BRACKET, CONJUNCTION, OPEN_BRACKET, 'x', DISJUNCTION, 'y', CLOSED_BRACKET]

    variables = ['x', 'y']
    complements = ['x']
    assert boolean_parser.equivalence_rule(variables, complements) == [OPEN_BRACKET, 'x', DISJUNCTION, 'y', CLOSED_BRACKET, CONJUNCTION, OPEN_BRACKET, COMPLEMENT, 'x', DISJUNCTION, COMPLEMENT, 'y', CLOSED_BRACKET]

    variables = ['x', 'y']
    complements = ['x', 'y']
    assert boolean_parser.equivalence_rule(variables, complements) == [OPEN_BRACKET, 'x', DISJUNCTION, COMPLEMENT, 'y', CLOSED_BRACKET, CONJUNCTION, OPEN_BRACKET, COMPLEMENT, 'x', DISJUNCTION, 'y', CLOSED_BRACKET]


def test3():
    # PARSE THE STRING!!!
    statement = list('a=>0')
    assert boolean_parser.parse_string(statement) == list('!a')

    statement = list('x<=>0')
    assert boolean_parser.parse_string(statement) == list('!x')

    statement = list('(a<=>0)+!1')
    assert boolean_parser.parse_string(statement) == list('!a')

    statement = list('((a<=>0)+!1).!b')
    assert boolean_parser.parse_string(statement) == list('!a.!b')

    statement = list('((!a.0).b)')
    assert boolean_parser.parse_string(statement) == list('0')

    statement = list('(a+b).1')
    assert boolean_parser.parse_string(statement) == list('a+b')

    statement = list('(x+y).((a+b).p.(d.b))')
    assert boolean_parser.parse_string(statement) == list('(x+y).((a+b).p.(d.b))')

    statement = list('(x+y).((a+b).p.!(d.b))')
    assert boolean_parser.parse_string(statement) == list('(x+y).((a+b).p.!(d.b))')

    statement = list('(x+y).1+((!w+1).(!w+1))')
    assert boolean_parser.parse_string(statement) == list('x+y')

    statement = list('((x+y).1+((!w+1).(!w+1)))+((x+y).1+((!w+1).(!w+1)))')
    assert boolean_parser.parse_string(statement) == list('x+y')

    statement = list('!((x+y).1+((!w+1).(!w+1)))')
    assert boolean_parser.parse_string(statement) == list('!(x+y)')

    statement = list('(x+y)+!(x+y)')
    assert boolean_parser.parse_string(statement) == list('1')

    statement = list('((x+y).1+((!w+1).(!w+1)))+!((x+y).1+((!w+1).(!w+1)))')
    assert boolean_parser.parse_string(statement) == list('1')

    statement = list('z=>(z.!y)')
    assert boolean_parser.parse_string(statement) == list('!z+(z.!y)')

    statement = list('z=>((z.!y)+(z.!y))')
    assert boolean_parser.parse_string(statement) == list('!z+(z.!y)')

    statement = list('z=>(!(z.!y)+!(z.!y))')
    assert boolean_parser.parse_string(statement) == list('!z+!(z.!y)')

    statement = list('(z=>(!(z.!y)+!(z.!y)))=>v')
    assert boolean_parser.parse_string(statement) == list('!(!z+!(z.!y))+v')

    statement = list('!(z=>(!(z.!y)+!(z.!y)))=>v')
    assert boolean_parser.parse_string(statement) == list('(!z+!(z.!y))+v')

    statement = list('((z=>(!(z.!y)+!(z.!y)))=>v).h+h')
    assert boolean_parser.parse_string(statement) == list('(!(!z+!(z.!y))+v).h')

    statement = list('(((((x+y).1+((!w+1).(!w+1)))+!((x+y).1+((!w+1).(!w+1)))=>(!(z.!y)+!(z.!y)))=>v).h+h)=>p')
    assert boolean_parser.parse_string(statement) == list('!((!(!z+!(z.!y))+v).h)+p')

    
def test4():

    statement = list('a')
    assert boolean_parser.get_statements(statement) == [list('a')]

    statement = list('!a')
    assert boolean_parser.get_statements(statement) == [list('!a')]

    statement = list('a.0')
    assert boolean_parser.get_statements(statement) == [list('a'), list('.'), list('0')]

    statement = list('(a.0)')
    assert boolean_parser.get_statements(statement) == [list('(a.0)')]

    statement = list('!(a.0)')
    assert boolean_parser.get_statements(statement) == [list('!(a.0)')]

    statement = list('!(!a.!0)')
    assert boolean_parser.get_statements(statement) == [list('!(!a.!0)')]

    statement = list('!(!a.!0).p+q')
    assert boolean_parser.get_statements(statement) == [list('!(!a.!0)'), list('.'), list('p'), list('+'), list('q')]

    statement = list('!(!a.!0).!p+!q')
    assert boolean_parser.get_statements(statement) == [list('!(!a.!0)'), list('.'), list('!p'), list('+'), list('!q')]

    statement = list('(!(!a.!0).!p+!q)>!(!x.!m)')
    assert boolean_parser.get_statements(statement) == [list('(!(!a.!0).!p+!q)'), list('>'), list('!(!x.!m)')]

    statement = list('a.b.c.(!(!a.!0).!p+!q)>!(!x.!m)')
    assert boolean_parser.get_statements(statement) == [list('a'), list('.'), list('b'), list('.'), list('c'), list('.'), list('(!(!a.!0).!p+!q)'), list('>'), list('!(!x.!m)')]

    statement = list('!a.!b.!c.(!(!a.!0).!p+!q)>!(!x.!m)')
    assert boolean_parser.get_statements(statement) == [list('!a'), list('.'), list('!b'), list('.'), list('!c'), list('.'), list('(!(!a.!0).!p+!q)'), list('>'), list('!(!x.!m)')]



    # ABSTRACTING STATEMENTS:
    statement = [list('a')]
    assert boolean_parser.abstract_statements(statement) == [list('a')]

    statement = [list('!a')]
    assert boolean_parser.abstract_statements(statement) == [list('!a')]

    statement = [list('!a'), list('.'), list('b')]
    assert boolean_parser.abstract_statements(statement) == [list('!a'), list('.'), list('b')]

    statement = [list('!(a.b)'), list('.'), list('b')]
    assert boolean_parser.abstract_statements(statement) == [list('!(A)'), list('.'), list('b')]

    statement = [list('!(!a.!b)'), list('.'), list('b'), list('+'), list('((!(a.b)+c)>d)')]
    assert boolean_parser.abstract_statements(statement) == [list('!(A)'), list('.'), list('b'), list('+'), list('(B)')]

    statement = [list('!b'), list('.'), list('!(!a.!b)'), list('.'), list('b'), list('+'), list('((!(a.b)+c)>d)'), list('+'), list('!(c.!x)')]
    assert boolean_parser.abstract_statements(statement) == [list('!b'), list('.'), list('!(A)'), list('.'), list('b'), list('+'), list('(B)'), list('+'), list('!(C)')]

    statement = [list('!b'), list('.'), list('!((!(a.b)+c)>d)'), list('.'), list('b'), list('+'), list('((!(a.b)+c)>d)'), list('+'), list('!((!(a.b)+c)>d)')]
    assert boolean_parser.abstract_statements(statement) == [list('!b'), list('.'), list('!(A)'), list('.'), list('b'), list('+'), list('(A)'), list('+'), list('!(A)')]

    statement = [list('!b'), list('.'), list('((!(a.b)+c)>d)'), list('.'), list('b'), list('+'), list('((!(a.b)+c)>d)'), list('+'), list('!((!(a.b)+c)>d)')]
    assert boolean_parser.abstract_statements(statement) == [list('!b'), list('.'), list('(A)'), list('.'), list('b'), list('+'), list('(A)'), list('+'), list('!(A)')]




    #binary matches:
    statement = list('!a.b')
    assert boolean_parser.binary_matches(statement) == [list('!a.b')]

    statement = list('!a.b+r')
    assert boolean_parser.binary_matches(statement) == [list('!a.b')]

    statement = list('x<y>!a+b.r')
    assert boolean_parser.binary_matches(statement) == [list('b.r')]

    statement = list('!(!x<y>!a+b.r)')
    assert boolean_parser.binary_matches(statement) == [list('b.r')]

    statement = list('(x<y>!a+b.r)')
    assert boolean_parser.binary_matches(statement) == [list('b.r')]

    statement = list('(x<y>(!a+b).r)')
    assert boolean_parser.binary_matches(statement) == []

    statement = list('(x<y>!a.b.r)')
    assert boolean_parser.binary_matches(statement) == []

    statement = list('a.b.c+r.f.d')
    assert boolean_parser.binary_matches(statement) == []

    statement = list('a+b.c+r.f.d')
    assert boolean_parser.binary_matches(statement) == [list('b.c')]

    statement = list('a.b+c+r.f.d')
    assert boolean_parser.binary_matches(statement) == [list('a.b')]

    statement = list('a>b>c>d>e>f')
    assert boolean_parser.binary_matches(statement) == [list('e>f')]

    statement = list('a>b>c>d>e>f.c')
    assert boolean_parser.binary_matches(statement) == [list('f.c')]

    statement = list('a>b>c>d>e>f.c')
    assert boolean_parser.binary_matches(statement) == [list('f.c')]

    statement = list('a>b>c>d>e>f<c')
    assert boolean_parser.binary_matches(statement) == [list('e>f')]

    statement = list('a.b>c>d>e>f<c')
    assert boolean_parser.binary_matches(statement) == [list('a.b'), list('e>f')]

    statement = list('a>b<c<d>e>f<c')
    assert boolean_parser.binary_matches(statement) == [list('a>b'), list('e>f')]


    # MULTIPLE MATCHES
    statement = list('a.b.c<d>e>f<c')
    assert boolean_parser.multiple_matches(statement) == [list('a.b.c')]

    statement = list('a.b')
    assert boolean_parser.multiple_matches(statement) == []

    statement = list('!(a.b.c<d>(e>f)<c)')
    assert boolean_parser.multiple_matches(statement) == []

    statement = list('!(a.b.c+d+e+f+c.r)')
    assert boolean_parser.multiple_matches(statement) == [list('a.b.c'), list('d+e+f')]

    statement = list('!(a.b.c+d+e+f+c.r<!a.s.z)')
    assert boolean_parser.multiple_matches(statement) == [list('a.b.c'), list('d+e+f'), list('!a.s.z')]

    statement = list('a.b.c+z.e.f')
    assert boolean_parser.multiple_matches(statement) == [list('a.b.c'), list('z.e.f')]

    statement = list('!a.!b.!c+z.e.f<g<s<t<m>w>e>q>t.q')
    assert boolean_parser.multiple_matches(statement) == [list('!a.!b.!c'), list('z.e.f')]

    statement = list('!a.!b.!c+z.e.f<!g<!s<t<!m>!w>!e>q>!t.!q.!l')
    assert boolean_parser.multiple_matches(statement) == [list('!a.!b.!c'), list('z.e.f'), list('!t.!q.!l')]

    statement = list('q>t.q.!l')
    assert boolean_parser.multiple_matches(statement) == [list('t.q.!l')]


def test5():

    # EVALUATE BINARY STATEMENTS:
    statement = list('a>b')
    assert boolean_parser.evaluate_binary_statement(statement) == list('!a+b')

    statement = list('1>b')
    assert boolean_parser.evaluate_binary_statement(statement) == list('0+b')

    statement = list('1>0')
    assert boolean_parser.evaluate_binary_statement(statement) == list('0+0')

    statement = list('1.0')
    assert boolean_parser.evaluate_binary_statement(statement) == list('0')

    statement = list('1+0')
    assert boolean_parser.evaluate_binary_statement(statement) == list('1')

    statement = list('a+0')
    assert boolean_parser.evaluate_binary_statement(statement) == list('a')

    statement = list('a+1')
    assert boolean_parser.evaluate_binary_statement(statement) == list('1')

    statement = list('a.1')
    assert boolean_parser.evaluate_binary_statement(statement) == list('a')

    statement = list('a<b')
    assert boolean_parser.evaluate_binary_statement(statement) == list('(!a+b).(a+!b)')

    statement = list('1<b')
    assert boolean_parser.evaluate_binary_statement(statement) == list('(0+b).(1+!b)')

    statement = list('a<a')
    assert boolean_parser.evaluate_binary_statement(statement) == list('(!a+a).(a+!a)')

    statement = list('a+a')
    assert boolean_parser.evaluate_binary_statement(statement) == list('a')

    statement = list('a.a')
    assert boolean_parser.evaluate_binary_statement(statement) == list('a')

    statement = list('!a.a')
    assert boolean_parser.evaluate_binary_statement(statement) == list('0')

    statement = list('!a+a')
    assert boolean_parser.evaluate_binary_statement(statement) == list('1')


    # UNPACK MULTIPLE MATCHES
    statement = list('a.b.c.d')
    assert boolean_parser.unpack_multiple_matches(statement) == [list('a.b'), list('a.c'), list('a.d'), list('b.c'), list('b.d'), list('c.d')]


    # evaluate multiple binary statements and rejoin them
    statement = boolean_parser.get_statements(list('a>b>c'))
    assert boolean_parser.all_binary_matches(statement) == [list('a'), list('>'), list('(!b+c)')]

    statement = boolean_parser.get_statements(list('a>b>c.e'))
    assert boolean_parser.all_binary_matches(statement) == [list('a'), list('>'), list('b'), list('>'), list('(c.e)')]

    statement = boolean_parser.get_statements(list('a>b>1.e'))
    assert boolean_parser.all_binary_matches(statement) == [list('a'), list('>'), list('b'), list('>'), list('e')]

    statement = boolean_parser.get_statements(list('a>b>1+e'))
    assert boolean_parser.all_binary_matches(statement) == [list('a'), list('>'), list('b'), list('>'), list('1')]

    statement = boolean_parser.get_statements(list('a<b'))
    assert boolean_parser.all_binary_matches(statement) == [list('(!a+b)'), list('.'), list('(a+!b)')]

    statement = boolean_parser.get_statements(list('(a<b).e'))
    assert boolean_parser.all_binary_matches(statement) == [list('(a<b)'), list('.'), list('e')]

    statement = boolean_parser.get_statements(list('a<b.e'))
    assert boolean_parser.all_binary_matches(statement) == [list('a'), list('<'), list('(b.e)')]

    statement = boolean_parser.get_statements(list('1.e+1.e+1.e+1.e')) # the and statements have already been evaluated (.1).
    assert boolean_parser.all_binary_matches(statement) == [list('e'), list('+'), list('e'), list('+'), list('e'), list('+'), list('e')]

    statement = boolean_parser.get_statements(list('1.!e+1.e+f+1.e+1.!e+o>f>g'))
    assert boolean_parser.all_binary_matches(statement) == [list('!e'), list('+'), list('e'), list('+'), list('f'), list('+'), list('e'), list('+'), list('!e'), list('+'), list('o'), list('>'), list('(!f+g)')]


def test6():
    statement = '(a+b).(a+b)'
    assert boolean_parser.parse_string(statement) == list('a+b')

    statement = '((a+b).(a+b))+((a+b).(a+b))'
    assert boolean_parser.parse_string(statement) == list('a+b')

    statement = '((a+b).(a+b))>((a+b).(a+b))'
    assert boolean_parser.parse_string(statement) == list('1')

    statement = list('z=>(z.!y)')
    assert boolean_parser.parse_string(statement) == list('!z+(z.!y)')

statement = list('((z=>(!(z.!y)+!(z.!y)))=>v).h+h')
assert boolean_parser.parse_string(statement) == list('((!(!z+!(z.!y))+v).h)+h')


# (!(!z+!(z.!y))+v).h =? (((z>(!(z.!y)+!(z.!y)))>v).h)+h

# ( (z => !(z.!y)) => v).h
# (!z + !(z.!y)) => v
# (!(!z + !(z.!y)) + v).h





#test()
#test2()
#test3()
#test4()
#test5()
#test6()