function saveComment(id, input) {
    var comment = input.value;
    var data = {id: id, comment : comment};

    $.post("/comments", data)
        .done(function() {
            input.style.background = "#3CC900";
            console.log('success for ', id);
        })
        .fail(function () {
            input.style.background = "#A80000";
            console.log('Failed saving comment');
        });

}