# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    t_list_utils.py                                    :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: mogawa <mogawa@student.42tokyo.jp>         +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/11/11 22:03:39 by mogawa            #+#    #+#              #
#    Updated: 2023/12/13 23:13:22 by mogawa           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import lldb
import optparse
import shlex

def ptlist(debugger, command, result, internal_dict):
    """
    Prints the content of (void *) content of t_list for school 42
    """
    target = debugger.GetSelectedTarget()
    process = target.GetProcess()
    thread = process.GetSelectedThread()
    frame = thread.GetSelectedFrame()

    # Parse the args
    options = parse_ptlist(command)

    # Get the head of the linked list from the parser
    head = frame.FindVariable(options.head)
    if not head.IsValid():
        result.SetError(f'Error: t_list head "{options.head}" is not valid')
        return
    # Define the SBType for t_list
    content_type = target.FindFirstType(options.content).GetPointerType()
    if not content_type.IsValid():
        result.SetError(f'Error: content type "{options.content}" is not valid')
        return

    content_fields = get_content_fields(content_type)

    all_outputs = []
    current = head
    while current.GetValueAsUnsigned() != 0:
        # Cast the content pointer to a pointer
        data = current.GetChildMemberWithName('content').Cast(content_type)
        output = format_content_data(data, content_fields)
        if output:
            all_outputs.append(output)
        current = current.GetChildMemberWithName('next')
        if not current.IsValid():
            break

    for output in all_outputs:
        print(output)

    result.SetStatus(lldb.eReturnStatusSuccessFinishResult)

def parse_ptlist(command):
    """
    Parses command line arguments for the ptlist custom command.
    """
    usage = "usage: %prog [options]"
    description = "Prints contents of t_list"

    parser = optparse.OptionParser(description=description, prog="ptlist", usage=usage)
    parser.add_option('-l', '--list-head', dest='head', help='Name of the t_list head variable. Default value is head.', default='head')
    parser.add_option('-n', '--name', dest='content', help='Name of the structure that (void *) content of t_list is pointing at. Default value is t_content', default='t_content')
    options, args = parser.parse_args(shlex.split(command))
    return (options)

def get_content_fields(content_type):
    """
    Retrieves the field names of a given content type
    """
    fields = []
    pointee_type = content_type.GetPointeeType()
    if not pointee_type.IsValid():
        return (fields)
    for i in range(pointee_type.GetNumberOfFields()):
        field = pointee_type.GetFieldAtIndex(i)
        if field.IsValid():
            fields.append(field.GetName())
    return (fields)

def format_content_data(data, content_fields):
    """
    Formats the content data based on the fields names.
    """
    output = ""
    for field_name in content_fields:
        field_data = data.GetChildMemberWithName(field_name)
        if not field_data.IsValid():
            continue
        field_type = field_data.GetType()
        basic_type = field_type.GetBasicType()
        value = get_field_value(field_data, basic_type)
        output += f'[{field_name}:{value}]'
    return (output.strip())

def get_field_value(field_data, basic_type):
    """Utility function for format_content_data"""
    if basic_type in [lldb.eBasicTypeInt, lldb.eBasicTypeUnsignedInt, lldb.eBasicTypeLong, lldb.eBasicTypeUnsignedLong]:
        value = field_data.GetValueAsSigned()
    elif basic_type in [lldb.eBasicTypeFloat, lldb.eBasicTypeDouble]:
        value_str = field_data.GetValue()
        value = float(value_str) if value_str is not None else None
    elif field_data.TypeIsPointerType():
        value = field_data.GetSummary()
    else:
        value = field_data.GetValue()
    return (value)

# Register the LLDB command
def __lldb_init_module(debugger, internal_dict):
    """
    Registerrs the ptlist command with LLDB.
    """
    debugger.HandleCommand('command script add -f t_list_utils.ptlist ptlist')