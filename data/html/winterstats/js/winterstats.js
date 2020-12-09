/**
 * Column titles to be sorted for winterstats html file
 * @author   M.Zwaving
 * @license  MIT-license
 * @version  0.0.5
 */

'use strict';

// HTML table init values
let table_tbody      =  'table#stats>tbody',
    table_stats_sel  =  'table#stats>tbody>tr',  // Locations of the tr with data
    // table_popup_sel  =  'table#stats>tbody>tr>td>table.popup', // Popup table
    descending       =  '+',   // Identifier sort direction: large to small
    ascending        =  '-',   // Identifier sort direction: small to high
    sort_num         =  'num', // Identifier sort num-based
    sort_txt         =  'txt', // Identifier sort txt-based
    row_nr           =  2,     // Row tr num for click to sort
    diff_col         =  2,     // hack
    // Reg expression for grepping a float number from a td cell.
    // Result float is used for numeric sorting in a td cell.
    // Update here reg expression for extracting floats in td cell, if needed
    reg_float = /[+-]?[0-9]*[.]?[0-9]+/g;

 // Function returns an object with all the needed values for sorting a column
 // See object col_titles below
let obj = ( name, type, dir, row, col ) =>
{
    return {
         name: name,
         // Make columns clickable for sorting
         // Update here the selector for other tables
         doc: document.querySelector (
                `table#stats>thead>tr:nth-child(${row})>th:nth-child(${col})`
              ),
         type: type, // Sort by num or txt
         dir: dir,   // Start sort direction
         row: row,   // Row of sort column
         col: col    // Number of sort column
    }
}

// Column titles to sort
let col_titles = {
    PLACE:    obj( 'PLACE',    sort_txt,  ascending,   row_nr,   2 ),
    PROVINCE: obj( 'PROVINCE', sort_txt,  ascending,   row_nr,   3 ),
    TG:       obj( 'TG',       sort_num,  descending,  row_nr,   5 ),
    HELLMANN: obj( 'HELLMANN', sort_num,  descending,  row_nr,   6 ),
    IJNSEN:   obj( 'IJNSEN',   sort_num,  descending,  row_nr,   7 ),
    FROSTSUM: obj( 'FROST_SUM', sort_num, descending,  row_nr,   8 ),
    TX_MIN:   obj( 'TX_MIN',   sort_num,  ascending,   row_nr,   9 ),
    TG_MIN:	  obj( 'TG_MIN',   sort_num,  ascending,   row_nr,  10 ),
    TN_MIN:   obj( 'TN_MIN',   sort_num,  ascending,   row_nr,  11 ),
    SUN:      obj( 'SUN',      sort_num,  ascending,   row_nr,  12 ),
    RAIN:     obj( 'RAIN',     sort_num,  ascending,   row_nr,  13 ),
    TXlt0:    obj( 'TXlt0',    sort_num,  descending,  row_nr,  14 ),
    TGlt0:    obj( 'TGlt0',    sort_num,  descending,  row_nr,  15 ),
    TNlt0:    obj( 'TNlt0',    sort_num,  descending,  row_nr,  16 ),
    TNlt_5:   obj( 'TNlt_5',   sort_num,  descending,  row_nr,  17 ),
    TNlt_10:  obj( 'TNlt_10',  sort_num,  descending,  row_nr,  18 ),
    TNlt_15:  obj( 'TNlt_15',  sort_num,  descending,  row_nr,  19 ),
    TNlt_20:  obj( 'TNlt_20',  sort_num,  descending,  row_nr,  20 )
}
