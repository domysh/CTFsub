function request_next(data = null) {

    if (data == null) {
        fetch("/api/init/next")
            .then(res => res.json())
            .then(res => solve_result(res))
    } else {
        fetch("/api/init/next", {
                method: 'POST',
                cache: 'no-cache',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            }).then(res => res.json())
            .then(res => solve_result(res))
    }
}

function solve_result(res) {
    if (res.status) {
        swup.loadPage({ url: res.redirect })
    } else {
        show_error(res.msg)
    }

}

function show_error(text) {
    show_message("Ops... there is an error! ⚠️", text)
}

function request_back() {
    fetch("/api/init/back")
        .then((res) => {
            swup.loadPage({ url: res.url })
        })
}