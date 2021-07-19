window.history.pushState(null, null, window.location.href);
window.onpopstate = function() {
    window.history.go(1);
};

if (typeof Array.isArray === 'undefined') {
    Array.isArray = function(obj) {
      return Object.prototype.toString.call(obj) === '[object Array]';
    }
  };
function isDict(v) {
    return typeof v==='object' && v!==null && !(v instanceof Array) && !(v instanceof Date);
}

function validIPaddress(ipaddress) {  
    if (/^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/.test(ipaddress)) {  
      return true 
    }    
    return false  
  }  

function on_new_page(){
    hljs.highlightAll()
    load_tooltips()
}

function is_numeric(str){
    return /^\d+$/.test(str);
}

window.addEventListener("load", (e) => {
    const swup = new Swup({
        plugins: [new SwupScriptsPlugin({
            head: false,
            body: true
        })],
        cache: false,
        containers: ["#swup-container"]
    });
    window.swup = swup
    on_new_page()

    swup.on("contentReplaced", () => {
        on_new_page()
    })
})

function load_tooltips() {
    window.tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    window.tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    })
}

function create_modal() {
    if (document.getElementById("occasional_html_code") == null) {
        var myDiv = document.createElement("div");
        myDiv.id = 'occasional_html_code';
        document.body.appendChild(myDiv);
    }
}

function modify_modal(htmlCode) {
    let code = document.getElementById('occasional_html_code')
    code.innerHTML = htmlCode
}

function show_message(title, text, html_escape = true) {
    create_modal()
    modify_modal(`
    <div class="modal fade" id="modal_message" tabindex="-1" aria-labelledby="modal_title" aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="modal_title">Modal title</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body" id="modal_text">
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
        </div>
      </div>
    </div>
  </div>
    `)

    let code = document.getElementById('modal_text')
    if (html_escape)
        code.innerText = text
    else
        code.innerHTML = text

    code = document.getElementById('modal_title')
    if (html_escape)
        code.innerText = title
    else
        code.innerHTML = title

    if (!html_escape)
        hljs.highlightAll()


    var myModal = new bootstrap.Modal(document.getElementById('modal_message'))
    myModal.show()
}