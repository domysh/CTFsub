
function request_next(data = null,ondone = (data)=>{}) {
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
            .then(res => {ondone(res);solve_result(res)})
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

function request_back_raw(){
    fetch("/api/init/back")
        .then((res) => {
            swup.loadPage({ url: res.url })
        })
}

function request_back(data = null) {

    if (data == null) {
        request_back_raw()
    } else {
        fetch("/api/init/save", {
            method: 'POST',
            cache: 'no-cache',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        }).then(res => res.json())
        .then(res => {
            if (res.status){
                request_back_raw()
            }else{
                show_question("Are you sure to go back?",
                `Going back some setting will be lost, so remember to reset this configuration in case you want to go back!
                Error: ${res.msg}`)
                .then( asw => {
                    if (asw){
                        request_back_raw();
                    }
                })
            }
        })
    }
}

function move_init(next,data = null){
    if (next){
        request_next(data)
    }else{
        request_back(data)
    }
}