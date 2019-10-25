$(function() {

	// jQuery selection for the 2 select boxes
	var dropdown = {
		state: $('#select_state'),
		county: $('#select_county')
	};
	// console.log(dropdown)
	// dropdown.state.empty();
	// dropdown.county.empty();
	// call to update on load
	updateCounties();

	// function to call XHR and update county dropdown
	function updateCounties() {
		var send = {
			state: dropdown.state.val()
		};
		// console.log(send)
		dropdown.county.attr('disabled', 'disabled');
		dropdown.county.empty();
		$.getJSON("{{ url_for('main._get_counties') }}", send, function(data) {
			data.forEach(function(item) {
				dropdown.county.append(
					$('<option>', {
						value: item[0],
						text: item[1]
					})
				);
			});
			dropdown.county.removeAttr('disabled');
		});
	}

	// event listener to state dropdown change
	dropdown.state.on('change', function() {
		updateCounties();
	});

});