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
    $('#confirm-action-modal').modal('toggle');
    $('#confirm-action-modal').find('.btn-primary').attr('href', $(button).data('url'));
}
