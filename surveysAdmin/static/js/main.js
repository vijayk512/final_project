$(document).ready(function() {

    $('#type').change(function(){
    if($(this).val() == 'checkbox' || $(this).val() == 'radio' && $('#option_val').val() != 0 ){
          data = '<div class="form-group">'+
          '<input type="text" class="form-control form-control-user" name="options[]"></div>'+
          '<div class="form-group">'+
          '<input type="text" class="form-control form-control-user" name="options[]"></div>'+
          '<div class="form-group">'+
          '<input type="text" class="form-control form-control-user" name="options[]"></div>'+
          '<div class="form-group">'+
          '<input type="text" class="form-control form-control-user" name="options[]"></div>'+
          '<div class="form-group">'+
          '<input type="text" class="form-control form-control-user" name="options[]"></div>'+
          '<input type="hidden" id="option_val" value="0">';
          $('#options').append(data).show();
         }else if($(this).val() == 'text'){
          $('#options').empty().hide();
         }
    });

});