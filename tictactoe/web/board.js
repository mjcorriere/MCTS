
var board_width = 7;
var board_height = 6;

$board = $(".board");

for (var i = 0; i < board_width; i++) {
	$board.append("<col>");
}

for (var i = 0; i < board_height; i++) {
	var $newRow = $("<tr>");
	$board.append($newRow);
	for (var j = 0; j < board_width; j++) {
		$newRow.append( $("<td>").addClass("empty") );
	}
}

$(".board").delegate("td", "mouseover mouseleave", function(event) {
	var index = $(this).index();
	if (event.type == "mouseover") {
		var bg = "#EEE";
	} else if (event.type == "mouseleave") {
		var bg = "#FFF";
	}
	
	$("col").eq(index).css("background-color", bg);

});