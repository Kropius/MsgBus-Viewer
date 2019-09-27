$(document).ready(function () {
    $('button#btnGet').click(function () {

            $.ajax({
                url: "http://127.0.0.1:5001/print_pids/",
                type: "POST",
                success: function (resp) {
                    $('div#pids').append(resp.data);
                }
            });
        }
    );
});
var file_created = 0, reg_create_key = 0, library_load = 0, file_directory_create = 0, file_read = 0,
    file_change_basic_attributes = 0, file_datetime_change = 0, file_write = 0;
String.prototype.replaceAll = function (search, replacement) {
    var target = this;
    return target.split(search).join(replacement);
};

function  color_the_panel(myPanel,flag){
    if (flag == 1) {
        $(myPanel).parent().parent().parent().parent().parent().css({
            "background-color": "#5bc0de",
            "border-color": "#46b8da"
        });
    }
    else{
        $(myPanel).parent().parent().parent().parent().parent().css({
            "background-color": "",
            "border-color": ""
        });
    }
}
function modifyAttribute(toBeChanged,myAttributesParsed,flag){
    switch (myAttributesParsed['event_name']) {
                case "file_create":
                    if (flag == 1){
                         file_created++;
                    }
                    else {
                        file_created--;
                    }
                    toBeChanged.innerHTML = "file_created: " + file_created;
                    break;
                case "reg_create_key":
                     if (flag == 1){
                          reg_create_key++;
                    }
                    else {
                         reg_create_key--;
                    }
                    console.log("ba sunt in reg");
                    toBeChanged.innerHTML = "reg_create_key: " + reg_create_key;
                    break;
                case "library_load":
                      if (flag == 1){
                          library_load++;
                    }
                    else {
                         library_load--;
                    }
                    toBeChanged.innerHTML = "library_load: " + library_load;
                    break;
                case "file_directory_create":
                       if (flag == 1){
                          file_directory_create++;
                    }
                    else {
                         file_directory_create--;
                    }
                    toBeChanged.innerHTML = "file_directory_create: " + file_directory_create;
                    break;
                case "file_read":
                    if (flag == 1){
                          file_read++;
                    }
                    else {
                        file_read--;
                    }
                    toBeChanged.innerHTML = "file_read: " + file_read;
                    break;
                case "file_change_basic_attributes":
                    if (flag == 1){
                           file_change_basic_attributes++;
                    }
                    else {
                          file_change_basic_attributes--;
                    }
                    toBeChanged.innerHTML = "file_change_basic_attributes: " + file_change_basic_attributes;
                    break;
                case "file_datetime_change":
                    if (flag == 1){
                           file_datetime_change++;
                    }
                    else {
                          file_datetime_change--;
                    }
                    toBeChanged.innerHTML = "file_datetime_change: " + file_datetime_change;
                    break;
                case "file_write":
                     if (flag == 1){
                           file_write++;
                    }
                    else {
                          file_write--;
                    }
                    toBeChanged.innerHTML = "file_write: " + file_write;
                    break;
            }

}

function do_the_stuff(button){
    var myAttributes = (button.attr('value'));
    var myAttributesParsed = JSON.parse(String(myAttributes).replaceAll('\'','\"'));
    var toBeChanged = document.getElementById(myAttributesParsed['event_name']);
    var color = button.parent().parent().parent().parent().parent().css('background-color');
    console.log(button.name);
    if (color == 'rgb(255, 255, 255)' && button.attr('name') == 'select_event'){
        console.log("dsdsds")
        modifyAttribute(toBeChanged,myAttributesParsed,1);
          $.ajax({
            url: "http://127.0.0.1:5001/get_events",
            type: "POST",
            data: myAttributes,
            contentType: 'application/json',
            success: function (data) {
                console.log('success!')
            }
        });
    }
    else if (color == 'rgb(91, 192, 222)' && button.attr('name') != 'select_event'){
          console.log(color)
            modifyAttribute(toBeChanged,myAttributesParsed,0);
          $.ajax({
            url: "http://127.0.0.1:5001/delete_event",
            type: "POST",
            data: myAttributes,
            contentType: 'application/json',
            success: function (data) {
                console.log('success!')
            }
        });
    }
}

$(document).ready(function () {
    $('button.btn-success').click(function () {
        console.log('button pressed');
            do_the_stuff($(this));
            color_the_panel($(this),1);
    });
    $('button.btn-danger').click(function () {
        do_the_stuff($(this),0);
                    color_the_panel($(this),0);


    })
});
