$(document).ready(function() {
    $('.table').DataTable({
      language: {
        //customize pagination prev and next buttons: use arrows instead of words
        'paginate': {
          'previous': '<span class="fa fa-chevron-left"></span>',
          'next': '<span class="fa fa-chevron-right"></span>'
        },
        //customize number of elements to be displayed
        "lengthMenu": 'Display <select class="form-control input-sm">'+
        '<option value="10">10</option>'+
        '<option value="50">50</option>'+
        '<option value="100">100</option>'+
        '<option value="-1">All</option>'+
        '</select> results'
      }
    })
} );