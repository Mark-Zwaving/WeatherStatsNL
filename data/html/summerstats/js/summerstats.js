/**
 * Column titles to be sorted for summerstats html file
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
        doc: document.querySelector(
               `table#stats>thead>tr:nth-child(${row})>th:nth-child(${col})`
             ),
        type: type, // Sort by num or txt
        dir: dir,   // Start sort direction
        row: row,   // Row of sort column
        col: col    // Number of sort column
    }
}

let col_titles = {
    PLACE:    obj( 'PLACE',    sort_txt, ascending,  row_nr,  1 ),
    PROVINCE: obj( 'PROVINCE', sort_txt, ascending,  row_nr,  2 ),
    TG:       obj( 'TG',       sort_num, descending, row_nr,  4 ),
    HEATNDX:  obj( 'HEATNDX',  sort_num, descending,  row_nr,  5 ),
    TX_MAX:   obj( 'TX_MAX',   sort_num, descending,  row_nr,  6 ),
    TG_MAX:	  obj( 'TG_MAX',   sort_num, descending,  row_nr,  7 ),
    TN_MAX:   obj( 'TN_MAX',   sort_num, descending,  row_nr,  8 ),
    TXGTE20:  obj( 'TXGTE20',  sort_num, descending,  row_nr,  9 ),
    TXGTE25:  obj( 'TXGTE25',  sort_num, descending,  row_nr, 10 ),
    TXGTE30:  obj( 'TXGTE30',  sort_num, descending,  row_nr, 11 ),
    TXGTE35:  obj( 'TXGTE35',  sort_num, descending,  row_nr, 12 ),
    TXGTE40:  obj( 'TXGTE40',  sort_num, descending,  row_nr, 13 ),
    TGGE18:   obj( 'TGGE18',   sort_num, descending,  row_nr, 14 ),
    TGGE20:   obj( 'TGGE20',   sort_num, descending,  row_nr, 15 ),
    SUN:      obj( 'SUN',      sort_num, descending, row_nr, 16 ),
    SQGE10:   obj( 'SQGE10',   sort_num, descending,  row_nr, 17 ),
    RAIN:     obj( 'RAIN',     sort_num, descending, row_nr, 18 ),
    RHGE10:   obj( 'TGGE20',   sort_num, descending,  row_nr, 19 )
}
