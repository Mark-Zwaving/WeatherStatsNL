/**
 * Menu for possible
 * @author   M.Zwaving
 * @license  MIT-license
 * @version  0.0.3
 */
'use strict';

// See row 154 for the stations list
let activate_menu = true,  // Gloabal setter any menu Set: true for 'yess'  false for 'no'
    activate_menu_dropdown = true, // Dropdown menu (slow)
    activate_menu_form = true,  // Form menu
    menu_links_max = 10,  // How many links in one block
    path_to_root = './' , // ->  {}/wmo/yyyy/mm/
    jan=1, febr=2, march=3, april=4, mai=5, june=6,
    july=7, aug=8, sept=9, oct=10, nov=11, dec=12,
    id_menu = 'dayvalues_menu',
    months = [ 'januari', 'februari', 'march', 'april', 'mai', 'june',
               'july', 'august', 'september', 'october', 'november',
               'december' ],

    menu_font_size = '0.7rem',
    id_iframe = 'dayvalues_page',
    date_act  = '19900704',
    wmo_act   = '280';

// Helper fn
let docid = ( id ) => document.getElementById(id);
let show  = ( id ) => docid(id).style.display = 'inline-block';
let hide  = ( id ) => docid(id).style.display = 'none';
let add_zero  = ( i ) => i < 10 ? `0${i}` : `${i}`;
let is_leap_year = ( y ) => y % 100 === 0 ? y % 400 === 0 : y % 4 === 0;
let open_url_in_iframe = ( url ) => docid(id_iframe).src = url
let get_day_in_month = ( y, m ) => [ 31, is_leap_year(y) ? 29 : 28,
                                     31, 30, 31, 30, 31, 31, 30, 31, 30, 31
                                    ][m-1];

let get_yyyymmdd_now = () =>
{
    let d  = new Date(),
        yy = d.getFullYear(),
        mm = d.getMonth(),
        dd = d.getDate();

    return `${yy}${mm}${dd}`;
}

let split_date = ( d ) =>
{
    let yy = d.slice(0, 4),
        mm = d.slice(4, 6),
        dd = d.slice(6, 8);

    return [ yy, mm, dd ];
}

let get_day_before = ( d ) =>
{
    let    l  = split_date( d ),
          yy  = parseInt( l[0], 10 ),
          mm  = parseInt( l[1], 10 ),
          dd  = parseInt( l[2], 10 ) - 1;

    if ( dd == 0 )
    {
        mm -= 1;  // Last month
        if ( mm == 0 )
        {
            mm = 12
            yy -= 1
        }
        dd = get_day_in_month(yy, mm);
    }

    let edate = `${yy}${add_zero(mm)}${add_zero(dd)}`;
    return edate;
}

let get_day_next = ( d ) =>
{
    let    l  = split_date( d ),
          yy  = parseInt(l[0], 10 ),
          mm  = parseInt(l[1], 10 ),
          dd  = parseInt(l[2], 10 ) + 1,  // Next
          max = get_day_in_month(yy, mm);

    switch ( mm )
    {
        case jan:
            if ( dd > max )
                dd = 1, mm = febr;
            break;
        case febr:
            if ( dd > max )
                dd = 1, mm = march;
            break;
        case march:
            if ( dd > max )
                dd = 1, mm = april;
            break;
        case april:
            if ( dd > max )
                dd = 1, mm = mai;
            break;
        case mai:
           if ( dd > max )
                dd = 1, mm = june;
           break;
        case june:
            if ( dd > max )
                dd = 1, mm = july;
            break;
        case july:
            if ( dd > max )
                dd = 1, mm = aug;
            break;
        case aug:
            if ( dd > max )
                dd = 1, mm = sept;
            break;
        case sept:
            if ( dd > max )
                dd = 1, mm = oct;
            break;
        case oct:
            if ( dd > max )
                dd = 1, mm = sept;
            break;
        case nov:
            if ( dd > max )
                dd = 1, mm = dec;
            break;
        case dec:
            if ( dd > max )
                dd = 1, mm = jan, yy += 1;
            break;
    }

    let edate = `${yy}${add_zero(mm)}${add_zero(dd)}`;
    return edate;
}

/**
 * Station object
 */
class Station
{
    constructor( wmo, name, sdate )
    {
        this.wmo = wmo;
        this.name = name;
        this.sdate = sdate;             // Start date of data
        this.edate = get_day_before(get_yyyymmdd_now()); // Max date of data
        this.base_url = `${path_to_root}${wmo}`;
        this.base_file = `dayvalues-${wmo}`;
    }
}

let station_list = [
    new Station('391', 'Arcen', '19900704'),
    // new Station('249', 'Berkhout', '19510101'),
    // new Station('348', 'Cabauw Mast', '19510101'),
    new Station('260', 'De Bilt', '19010101'),
    new Station('235', 'De Kooy', '19060101'),
    // new Station('275', 'Deelen', '19010101'),
    new Station('280', 'Eelde', '19060301'),
    // new Station('370', 'Eindhoven', '19010101'),
    // new Station('377', 'Ell', '19010101'),
    // new Station('350', 'Gilze-Rijen', '19010101'),
    // new Station('278', 'Heino', '19010101'),
    // new Station('356', 'Herwijnen', '19010101'),
    // new Station('330', 'Hoek van Holland', '19010101'),
    // new Station('279', 'Hoogeveen', '19010101'),
    // new Station('251', 'Hoorn Terschelling', '19010101'),
    // new Station('283', 'Hupsel', '19010101'),
    // new Station('277', 'Lauwersoog', '19010101'),
    // new Station('270', 'Leeuwarden', '19010101'),
    // new Station('269', 'Lelystad', '19010101'),
    new Station('380', 'Maastricht', '19060101'),
    // new Station('273', 'Marknesse', '19010101'),
    new Station('286', 'Nieuw Beerta', '19900219'),
    // new Station('344', 'Rotterdam', '19010101'),
    // new Station('240', 'Schiphol', '19010101'),
    // new Station('267', 'Stavoren', '19010101'),
    // new Station('290', 'Twenthe', '19010101'),
    // new Station('242', 'Vlieland', '19010101'),
    new Station('310', 'Vlissingen', '19060101')
    // new Station('375', 'Volkel', '19010101'),
    // new Station('215', 'Voorschoten', '19010101'),
    // new Station('319', 'Westdorpe', '19010101'),
    // new Station('257', 'Wijk aan Zee', '19010101'),
    // new Station('323', 'Wilhelminadorp', '19010101')
];

let html_menu_dropdown = () =>
{
      let html = '';

      station_list.forEach( ( station ) =>
      {
          html += `<ul class="navbar-nav">
                   <li class="nav-item dropdown">
                   <a class="nav-link dropdown-toggle" href="#" id="navbarDropdownMenuLink"
                      data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"> ${station.name} </a>
                   <ul class="dropdown-menu" aria-labelledby="navbarDropdownMenuLink">`;

          let l_s = split_date(station.sdate),
              i_y = parseInt( l_s[0], 10 ),
              l_e = split_date(station.edate),
              i_e = parseInt( l_e[0], 10 ),
              i_date_e = parseInt(station.edate, 10);

          while ( i_y <= i_e )
          {
              // All Months
              html += `<li class="dropdown-submenu">
                         <a class="dropdown-item dropdown-toggle" href="#"
                            style="font-size:${menu_font_size};"> ${i_y} </a>
                         <ul class="dropdown-menu">`;
              // Months
              let i_m = 1;
              while ( i_m <= 12 )
              {
                  // Days
                  html += `<li class="dropdown-submenu">
                             <a class="dropdown-item dropdown-toggle" href="#"
                                style="font-size:${menu_font_size};"> ${months[i_m-1]} </a>
                                <ul class="dropdown-menu">`;
                  let i_d   = 1,
                      i_max = get_day_in_month(i_y, i_m),
                      mm = add_zero(i_m);

                  while ( i_d <= i_max )
                  {
                      let dd = add_zero(i_d),
                          ymd = `${i_y}${mm}${dd}`;

                      html += `<li><a class="dropdown-item" href="#"
                                      onclick="onclick_dropdown_menu('${station.wmo}','${ymd}'); return false;"
                                      style="font-size:${menu_font_size};"> ${dd} </a>
                                      </li>`;

                      let i_date_s = parseInt(get_day_next(ymd), 10);
                      if ( i_date_s > i_date_e )
                      {   // Set all to max
                          i_y = i_e;
                          i_d = i_max;
                          i_m = 12
                      }
                      ++i_d;
                  }
                  html += '</ul></li>'; // dd
                  ++i_m;
              }
              html += '</ul></li>';  // mm
              ++i_y;
          }
          html += '</ul></li></ul>';  // stations
      } );

      return html;
}

let get_station_from_list_by_wmo = ( wmo ) =>
{
    let ndx = 0, station = false;
    while ( ndx < station_list.length )
    {
        station = station_list[ndx];
        if ( station.wmo == wmo )
            break;
        ndx++;
    }
    return station;
}

let make_url = (wmo, date) =>
{
    let       l = split_date( date ),
             yy = l[0], mm = l[1], dd = l[2],
        station = get_station_from_list_by_wmo(wmo),
           name = `${station.base_file}-${yy}-${mm}-${dd}.html`,
           url  = `${station.base_url}/${yy}/${mm}/${name}`;

    return url
}

let onclick_dropdown_menu = ( wmo, date ) =>
{
    let url = make_url(wmo, date);
    console.log(url);

    // Update globals
    date_act = date;
    wmo_act  = wmo;

    // console.log( 'Station is: ' + wmo );
    // console.log( 'Date is: ' + date );
    // console.log( 'Url is: ' + url);
    open_url_in_iframe(url);  // Open the url
}

let onclick_go_btn = ( ) =>
{
    let wmo  = document.getElementById('station_form_id').value,
        date = document.getElementById('date_form_id').value,
           l = date.split('-'),
         ymd = `${l[0]}${l[1]}${l[2]}`,
        url  = make_url( wmo, ymd );

    console.log(document.getElementById('station_form_id').value);
    console.log(document.getElementById('date_form_id').value);
    console.log(ymd);
    console.log(url);

    // Update globals
    date_act = ymd;
    wmo_act  = wmo;

    // console.log( 'Station is: ' + wmo );
    // console.log( 'Date is: ' + date );
    // console.log( 'Url is: ' + url);
    open_url_in_iframe(url);  // Open the url
}

let onclick_next = () =>
{
    date_act = get_day_next( date_act );
    let url = make_url(wmo_act, date_act);
    console.log(url);
    open_url_in_iframe(url);  // Open the url
}

let onclick_back = () =>
{
    date_act = get_day_before( date_act );
    let url = make_url(wmo_act, date_act);
    console.log(url);
    open_url_in_iframe(url);  // Open the url
}

let html_menu_form = () =>
{
    let html = `<form class="form-inline" style="font-size:${menu_font_size};">
      <div class="form-group mr-2">
        <button type="submit" class="btn btn-info btn-sm" style="font-size:${menu_font_size};"
                onclick="onclick_back(); return false;"> <i class="fas fa-chevron-circle-left"></i> </button>
      </div>
      <div class="form-group mr-5">
        <button type="submit" class="btn btn-info btn-sm" style="font-size:${menu_font_size};"
                onclick="onclick_next(); return false;"> <i class="fas fa-chevron-circle-right"></i> </button>
      </div>

      <div class="form-group mr-2">
        <select id="station_form_id" class="form-control custom-select" style="font-size:${menu_font_size};">
        <option selected>Select a station</option>`;

    station_list.forEach( (item) => {
        html += `<option value="${item.wmo}"> ${item.wmo} ${item.name} </option>`;
    } );

    html += `</select></div>
        <div class="form-group mr-2">
          <label for="validationServerUsername"></label>
          <div class="input-group">
            <div class="input-group-prepend">
              <span class="input-group-text" id="inputGroupPrepend3">
                <i class="fa fa-calendar fa-xs" aria-hidden="true"></i>
              </span>
            </div>
            <input type="date" id="date_form_id" class="form-control form-control-sm"
                   aria-describedby="inputGroupPrepend3" style="font-size:${menu_font_size};" required>
          </div>
        </div>
        <div class="form-group">
          <button type="submit" class="btn btn-success btn-sm" style="font-size:${menu_font_size};"
                  onclick="onclick_go_btn(); return false;"> GO </button>
        </div>
      </div>
    </form>`;

    return html;
}

let add_menus_to_page = () =>
{
    console.log('The html page has loaded');
    if ( activate_menu )
    {
        console.log('Activate menu');
        let html = `
                <nav class="navbar navbar-expand-md navbar-light bg-light" style="font-size:${menu_font_size};" >
                <button class="navbar-toggler" type="button" data-toggle="collapse"
                        data-target="#navbarNavDropdown" aria-controls="navbarNavDropdown"
                        aria-expanded="false" aria-label="Toggle navigation">
                      <span class="navbar-toggler-icon"></span></button>`;

        if (activate_menu_dropdown)
        {
            console.log('Start make dropdown menu');
            html += `<div class="collapse navbar-collapse" id="navbarNavDropdown">`
            html += html_menu_dropdown();
            html += `</div>`
            console.log('End make dropdown menu');
        }
        if (activate_menu_dropdown && activate_menu_form)
            html += '<div class="h-divider"> </div>';

        if (activate_menu_form)
        {
            console.log('Start make form menu');
            html += html_menu_form();
            console.log('End make form menu');
        }

        html +=  '</div></nav>';

        console.log('Start putting menu on screen');
        docid(id_menu).innerHTML = html //.replace( /\s+/g, ' ' );
        console.log('End putting menu on screen');
    }
};

// Start main fn
add_menus_to_page();
