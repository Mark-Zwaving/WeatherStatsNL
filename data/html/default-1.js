
// Short functions
docid   = (id) => document.getElementById(id);
show_id = (id) => docid(id).style.display = 'block';
hide_id = (id) => docid(id).style.display = 'none';

// Functions for navigation
show_page = ( page ) =>
{
    if ( page === '--' )
    {
        if ( LINK_ACT > 1 )
        {
            LINK_ACT -= 1;
        }
    }
    else if ( page === '++' )
    {
        if ( LINK_ACT < LINKS_ON_PAGE )
        {
            LINK_ACT += 1;
        }
    }
    else
    {
        LINK_ACT = page;
    }

    let pages_max_shown = LINK_ACT * MAX_ROW_PER_PAGE,
        pages_min_shown = pages_max_shown - MAX_ROW_PER_PAGE;

    // Show or hide rows
    for ( let p = 1; p <= ALL_ROW_COUNT; p++ )
    {
        if ( p > pages_min_shown &&
             p <= pages_max_shown )
        {
            $(`#show_${p}`).show();
        }
        else
        {
            $(`#show_${p}`).hide();
        }
    }

    // Update navigation
    for ( let p = 1; p <= LINKS_ON_PAGE; p++ )
    {
        $(`#li_${p}`).removeClass('active');
    }
    
    $(`#li_${LINK_ACT}`).addClass('active');
}

// Pagination html
pagination = ( ) =>
{
    let nav = ''
    if ( LINKS_ON_PAGE > 1 )
    {
        nav += `
        <nav aria-label="Page navigation example mt-3">
          <ul class="pagination justify-content-center">
              <li class="page-item">
                <a class="page-link" href="#" aria-label="Previous"
                   onclick="show_page('--'); return false;">
                  <span aria-hidden="true">&laquo;</span>
                  <span class="sr-only">Previous</span>
                </a>
              </li>
        `;

        let page_active = '',
            page = 1;
        while ( page <= LINKS_ON_PAGE )
        {
            page_active = page === LINK_ACT ? 'active' : '';
            nav += `
              <li id="li_${page}" class="page-item ${page_active}">
                <a id="a_${page}" class="page-link" href="#"
                   onclick="show_page(${page}); return false;">
                  ${page}
                </a>
              </li>
            `;
            page++;
        }

        nav += `
            <li class="page-item">
              <a class="page-link" href="#" aria-label="Next"
                 onclick="show_page('++'); return false;">
                <span aria-hidden="true">&raquo;</span>
                <span class="sr-only">Next</span>
              </a>
            </li>
          </ul>
        </nav>
        `;

        document.write(nav);

        // Update nav
        show_page( LINK_ACT )
    }
}

show_hide_password = ( id_input, id_icon ) =>
{
    // Get objects
    let input = docid(id_input),
        icon = docid(id_icon);
    // Change show or hidden
    input.type = input.type === 'text' ? 'password' : 'text';
    // Change id_icon open or closed
    icon.className = input.type === 'text' ? 'fa fa-unlock-alt' : 'fa fa-lock' ;
}

edit_yn_all_log = ( id_num ) =>
{
    let btn_save  =  $(`#btn_save_${id_num}`),
        btn_del   =  $(`#btn_delete_${id_num}`),
        btn_date  =  $(`#date_${id_num}`),
        inp_ts    =  $(`#time_start_${id_num}`),
        inp_te    =  $(`#time_end_${id_num}`),
        inp_titl  =  $(`#title_${id_num}`),
        are_txt   =  $(`#text_${id_num}`),
        are_suc   =  $(`#succes_${id_num}`),
        are_fail  =  $(`#setback_${id_num}`),
        are_refl  =  $(`#reflect_${id_num}`),
        l         =  [ btn_save, btn_del, btn_date, inp_ts, inp_te,
                       inp_titl, are_txt, are_suc, are_fail, are_refl ];

    // Start is disabled
    l.forEach( el =>
    {
        el.toggleClass('disabled');
        el.attr('aria-disabled', el.attr('aria-disabled') == 'true' ? 'false' : 'true' );
        el.prop("disabled", el.prop("disabled") == true ? false : true);
    } );
}

edit_yn_all_plan = ( id_num ) =>
{
    let btn_save  =  $(`#btn_save_${id_num}`),
        /*btn_show  =  $(`#btn_show_${id_num}`),*/
        btn_del   =  $(`#btn_delete_${id_num}`),
        btn_date  =  $(`#date_${id_num}`),
        inp_ts    =  $(`#time_start_${id_num}`),
        inp_te    =  $(`#time_end_${id_num}`),
        inp_titl  =  $(`#title_${id_num}`),
        are_txt   =  $(`#text_${id_num}`),
        l         =  [ btn_save, /*btn_show,*/ btn_del, btn_date,
                       inp_ts, inp_te, inp_titl, are_txt ];

    // Start is disabled
    l.forEach( el =>
    {
        el.toggleClass( 'disabled' );
        el.attr( 'aria-disabled', el.attr('aria-disabled') == 'true' ? 'false' : 'true' );
        el.prop( 'disabled', el.prop('disabled') == true ? false : true );
    } );
}

// Unique global identifier. Only needed for visual representations
let ID_NUM = 0;

// Function to read and write template from html page
add_template = (t_id) =>
{
    // Init vars
    let t_new = docid('templates').innerHTML,
        t_old = docid('id_main').innerHTML;

    // Replace all template demo id's in a template with a new id
    while ( t_new.indexOf(t_id) != -1 )
        t_new = t_new.replace( t_id, ID_NUM );

    // Place template in document
    docid('id_main').innerHTML = `${t_old} ${t_new}`;

    // Next id num
    --ID_NUM;
}

// Function to delete an added template
delete_template = (id) =>
{
    let yn = confirm( `
        Are you sure you want to remove this logging section from screen ? \n
        Note that this log is not deleted from the database, if it's already saved.\n
        Press the OK button to remove the log from the screen.
      ` );

    if ( yn )
        docid(id).innerHTML = ''
}
