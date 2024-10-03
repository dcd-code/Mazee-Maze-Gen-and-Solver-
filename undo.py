def undo_action(undo_stack, grid_state, start_node, end_node, setting_start_node):
    message = ""
    if not undo_stack:
        return message, grid_state, start_node, end_node, setting_start_node
    last_action = undo_stack.pop()
    action_type, action_data = last_action
    if action_type == "start":
        y, x = action_data
        grid_state[y][x] = 1
        start_node = None
        setting_start_node = True
    elif action_type == "end":
        y, x = action_data
        grid_state[y][x] = 1
        end_node = None
        setting_start_node = False
    elif action_type == "wall":
        y, x = action_data
        grid_state[y][x] = 1
    elif action_type == "empty":
        y, x = action_data
        grid_state[y][x] = 0
    elif action_type == "clear":
        grid_state = action_data["grid_state"]
        start_node = action_data["start_node"]
        end_node = action_data["end_node"]
        setting_start_node = start_node is None


    return message, grid_state, start_node, end_node, setting_start_node
