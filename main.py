

def sql_to_phi(query):
    '''
        queries is an array of the lines of sql
        
    '''
    print('----------------------')
    print(query)

    proj_columns = None
    num_grouping_variables = None
    grouping_attributes = None
    f_vect = None
    pred_list = None
    having = None

    print('00000000000000000000000')
    print("LINE")

    for line in query:
        line_words = line.split(' ')
        print("LINE: " + line)
        print(line_words)
        if line_words[0].lower() == 'select':
            print('this is a select')
            args_str = line[7:]
            print("args_str:", args_str)
            args = args_str.split(',')
            if args:
                proj_columns = []
            for arg in args:
                proj_columns.append(arg.strip())
            print("PROJ COLUMNS")
            print(proj_columns)
            pass
        elif line_words[0].lower() == 'from':
            # not in phi
            pass
        elif line_words[0].lower() == 'where':
            # not in phi
            pass
        elif line_words[0].lower() == 'group':
            print('this is a group by')
            args_str = line[9:]
            print("args_str:", args_str)
            args_str = args_str.replace(';', ':')
            # uses colon instead of semicolon
            args = args_str.split(':')

            print('abc')
            # getting grouping attributes
            grouping_attrs_str = args[0]
            grouping_attrs = grouping_attrs_str.strip().split(',')
            print('def')
            print(grouping_attrs)
            if grouping_attrs:
                grouping_attributes = []
            for attr in grouping_attrs:
                grouping_attributes.append(attr.strip())
            print('sdfsdf')
            # counting number of grouping variables
            grouping_vars_str = args[1]
            grouping_vars = grouping_vars_str.strip().split(',')
            num_grouping_variables = len(grouping_vars)

            print('end of gb')
            # group by
        elif line_words[0].lower() == 'such':
            print('this is a such that')
            # such that
        elif line_words[0].lower() == 'having':
            print('this is a having')
        else:
            print('AAAAAAAA')
    print('----------------------')
    # Return variables proj, num, etc. as dictionary (phi)
    return {'S': proj_columns, 'n': num_grouping_variables, 'V': grouping_attributes}


if __name__ == '__main__':
    '''
    Step 1. Get the file for query (ex. q1.txt) in first line.
    Step 2. Read from the file the lines of SQL. Put each line as a value in the text array query_as_text_arr
    Step 3. Pass this into the sql to phi function.
    '''
    file = open('q1.txt')
    query_as_text_arr = []
    lines = file.readlines()
    for line in lines:
        line = line.strip('\n')
        query_as_text_arr.append(line)

    phi = sql_to_phi(query_as_text_arr)
    print('PHI')
    print(phi)