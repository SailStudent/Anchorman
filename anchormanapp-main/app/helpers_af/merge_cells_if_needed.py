def merge_cells_if_needed(table, start_row, start_col, end_row, end_col):
    try:
        start_cell = table.cell(start_row, start_col)
        end_cell = table.cell(end_row, end_col)
        start_cell.merge(end_cell)
    except IndexError:
        pass