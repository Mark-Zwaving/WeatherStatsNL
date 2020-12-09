/**
 * Column titles to be sorted for search4days html file
 * @author   M.Zwaving
 * @license  MIT-license
 * @version  0.0.3
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
     diff_col         =  1,     // hack
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
    PLACE: obj('PLACE', sort_txt, ascending,  row_nr,  2),
    STATE: obj('STATE', sort_txt, ascending,  row_nr,  3),
    DATE:  obj('DATE',  sort_num, descending, row_nr,  5),
    TX:    obj('TX',    sort_num, descending, row_nr,  6),
    TG:	   obj('TG',    sort_num, descending, row_nr,  7),
    TN:    obj('TN',    sort_num, descending, row_nr,  8),
    T10N:  obj('T10N',  sort_num, descending, row_nr,  9),
    SQ:    obj('SQ',    sort_num, descending, row_nr, 10),
    SP:    obj('SP',    sort_num, descending, row_nr, 11),
    RH:    obj('RH',    sort_num, descending, row_nr, 12),
    RHX:   obj('RHX',   sort_num, descending, row_nr, 13),
    DR:    obj('DR',    sort_num, descending, row_nr, 14),
    PG:    obj('PG',    sort_num, descending, row_nr, 15),
    PX:    obj('PX',    sort_num, descending, row_nr, 16),
    PN:    obj('PN',    sort_num, descending, row_nr, 17),
    UG:    obj('UG',    sort_num, descending, row_nr, 18),
    UX:    obj('UX',    sort_num, descending, row_nr, 19),
    UN:    obj('UN',    sort_num, descending, row_nr, 20),
    NG:    obj('NG',    sort_num, descending, row_nr, 21),
    DDVEC: obj('DDVEC', sort_num, ascending,  row_nr, 22),
    FHVEC: obj('FHVEC', sort_num, descending, row_nr, 23),
    FG:    obj('FG',    sort_num, descending, row_nr, 24),
    FHX:   obj('FHX',   sort_num, descending, row_nr, 25),
    FHN:   obj('FHN',   sort_num, descending, row_nr, 26),
    FXX:   obj('FXX',   sort_num, descending, row_nr, 27),
    VVX:   obj('VVX',   sort_num, descending, row_nr, 28),
    VVN:   obj('VVN',   sort_num, descending, row_nr, 29),
    Q:     obj('Q',     sort_num, descending, row_nr, 30),
}
