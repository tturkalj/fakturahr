/**
 * Created by tomislav on 10.04.17..
 */
$(document).ready(function(){
    $('[data-toggle="tooltip"]').tooltip();
    window.setTimeout(function() {
        $(".alert-dismissable").slideUp(3000).alert('close');
    }, 5000);

    // $('#confirm-action-modal').on('show.bs.modal', function (event) {
    //   var button = $(event.relatedTarget); // Button that triggered the modal
    //   var url = button.data('url'); // Extract info from data-* attributes
    //   // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
    //   // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
    //   var modal = $(this);
    //   modal.find('.btn-primary').attr('href', url);
    // })
});

function toggleModal(button){
    var url =  $(button).data('url');
    $('#confirm-action-modal').find('.btn-primary').attr('href', $(button).data('url'));
    $('#confirm-action-modal').modal('toggle');
}

function initDatepicker(date_field){
    date_field.datepicker({
        dateFormat: 'dd.mm.yy.',
        changeMonth: true,
        changeYear: true,
        showOtherMonths: true,
        weekStart: 1,
        firstDay: 1,
        autoclose: true,
        constrainInput: true,
        monthNamesShort: [ "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
        dayNamesMin: ['S', 'M', 'T', 'W', 'T', 'F', 'S']
    });
};