function unload() {
    $.ajax({
        url: "chat/",
        type: "POST",
        data: {},
        success: function (request) {
            request.session.clear();
        },
        error: function (error) {
            print(error);
        }
    })
}
