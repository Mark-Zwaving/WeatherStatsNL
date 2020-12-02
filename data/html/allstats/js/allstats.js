/**
 * Column titles to be sorted for allstats html file
 * @author   M.Zwaving
 * @license  MIT-license
 * @version  0.0.2
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

let col_titles = {
    PLACE:     obj( 'PLACE',    sort_txt,  ascending,   row_nr,   1 ),
    PROVINCE:  obj( 'PROVINCE', sort_txt,  ascending,   row_nr,   2 ),
    TG:        obj( 'TG',       sort_num,  descending,  row_nr,   4 ),
    TX_MAX:    obj( 'TX_MAX',   sort_num,  descending,  row_nr,   5 ),
    TG_MAX:	   obj( 'TG_MAX',   sort_num,  descending,  row_nr,   6 ),
    TN_MAX:    obj( 'TN_MAX',   sort_num,  descending,  row_nr,   7 ),
    TX_MIN:    obj( 'TX_MIN',   sort_num,  descending,  row_nr,   8 ),
    TG_MIN:	   obj( 'TG_MIN',   sort_num,  descending,  row_nr,   9 ),
    TN_MIN:    obj( 'TN_MIN',   sort_num,  descending,  row_nr,  10 ),
    SUN:       obj( 'SUN',      sort_num,  descending,  row_nr,  11 ),
    RAIN:      obj( 'RAIN',     sort_num,  descending,  row_nr,  12 ),

    HEATNDX:   obj( 'HEATNDX',  sort_num,  descending,  row_nr,  13 ),
    TXGE20:    obj( 'TXGE20',   sort_num,  descending,  row_nr,  14 ),
    TXGE25:    obj( 'TXGE25',   sort_num,  descending,  row_nr,  15 ),
    TXGE30:    obj( 'TXGE30',   sort_num,  descending,  row_nr,  16 ),
    TXGE35:    obj( 'TXGE35',   sort_num,  descending,  row_nr,  17 ),
    TXGE40:    obj( 'TXGE40',   sort_num,  descending,  row_nr,  18 ),
    TGGE18:    obj( 'TGGE18',   sort_num,  descending,  row_nr,  19 ),
    TGGE20:    obj( 'TGGE20',   sort_num,  descending,  row_nr,  20 ),
    SQGE10:    obj( 'SQGE10',   sort_num,  descending,  row_nr,  21 ),
    RHGE10:    obj( 'TGGE20',   sort_num,  descending,  row_nr,  22 ),

    HELLMANN:  obj( 'HELLMANN', sort_num,  descending,  row_nr,  23 ),
    IJNSEN:    obj( 'IJNSEN',   sort_num,  descending,  row_nr,  24 ),
    FSUM:      obj( 'FROST_SUM', sort_num,  descending, row_nr,  25 ),
    TXLT0:     obj( 'TXLT0',    sort_num,  descending,  row_nr,  26 ),
    TGLT0:     obj( 'TGLT0',    sort_num,  descending,  row_nr,  27 ),
    TNLT0:     obj( 'TNLT0',    sort_num,  descending,  row_nr,  28 ),
    TNLT_5:    obj( 'TNLT_5',   sort_num,  descending,  row_nr,  29 ),
    TNLT_10:   obj( 'TNLT_10',  sort_num,  descending,  row_nr,  30 ),
    TNLT_15:   obj( 'TNLT_15',  sort_num,  descending,  row_nr,  31 ),
    TNLT_20:   obj( 'TNLT_20',  sort_num,  descending,  row_nr,  32 )
}
