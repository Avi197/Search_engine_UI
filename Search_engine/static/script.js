$("#inpt_search").on('focus', function () {
	$(this).parent('label').addClass('active');
});

$("#inpt_search").on('blur', function () {
	if($(this).val().length == 0)
		$(this).parent('label').removeClass('active');
});

function submitForm() {
   // Get the first form with the name
   // Usually the form name is not repeated
   // but duplicate names are possible in HTML
   // Therefore to work around the issue, enforce the correct index
   var frm = document.getElementsByName('contact-form')[0];
   frm.submit(); // Submit the form
   frm.reset();  // Reset all form data
   return false; // Prevent page refresh
}


$("#in_search").on('focus', function () {
	$(this).parent('label').addClass('active');
});

$("#in_search").on('blur', function () {
	if($(this).val().length == 0)
		$(this).parent('label').removeClass('active');
});

//function submitForm() {
//   // Get the first form with the name
//   // Usually the form name is not repeated
//   // but duplicate names are possible in HTML
//   // Therefore to work around the issue, enforce the correct index
//   var frm = document.getElementsByName('contact-form')[0];
//   frm.submit(); // Submit the form
//   frm.reset();  // Reset all form data
//   return false; // Prevent page refresh
//}