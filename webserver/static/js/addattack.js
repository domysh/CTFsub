function how_flag_regex_works() {
    show_message("How Flag Regex Works 💡", `
      <h5>Regexes can help you to better filter the flags:</h5>
      Infact setting a flag regex, whatever is the output of your attack script, this will be
      selected with the regex. <b>If in some service the format of the flag is different or 
      doesn't exists, don't worry, you will be able to choose a custom regex for every attack you start.</b>
      If you wnat to disable the regex filter, leave the text input blank.
    `, false);
  }
  
  function get_default_text() {
    let def = ``;
    return def;
  }
  function init_monaco_editor() {
    require.config({
      paths: {
        vs: "https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.25.2/min/vs",
      },
    });
    require(["vs/editor/editor.main"], async function () {
      window.editor = monaco.editor.create(
        document.getElementById("code-editor"),
        {
          value: get_text_editor(),
          language: "python",
          automaticLayout: true,
          minimap: {
            enabled: false,
          },
        }
      );
      fetch("/static/monaco-themes/Monokai.json")
        .then((data) => data.json())
        .then((data) => {
          monaco.editor.defineTheme("monokai", data);
          monaco.editor.setTheme("monokai");
        });
    });
  }
  
  function reset_text() {
    window.editor.setValue(get_default_text());
  }
  
  function reload_text() {
    if (window.attack_code == undefined){
      window.attack_code = get_default_text()
    }
    if (window.editor != undefined){
      window.editor.setValue(window.attack_code);
    }
  }
  
  function get_text_editor(){
    if (window.attack_code == undefined){
      window.attack_code = get_default_text()
    }
    return window.attack_code
  }
  
  function useless_function() {
    show_message('▶️ WTF❓',`<a href='https://www.youtube.com/watch?v=dQw4w9WgXcQ' target='_blanck' >https://www.youtube.com/watch?v=dQw4w9WgXcQ</a>`,false)
  }
  
  function submit_flag_settings(next){
  }
  
  function reload_config(){
    window.attack_code = get_default_text()
  }
  
  function set_run_code_attack_init(){
    modify_modal(`
      <div class="modal fade" id="try-to-run" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="try-to-runLabel" aria-hidden="true">
        <div class="modal-dialog modal-xl">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="try-to-runLabel">Try to execute the attack 🔥</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body" id="try-to-run-body">
  
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
              <button type="button" class="btn btn-success" id="try-to-run-btn" onclick="run_code_script()"><i class="fas fa-play"></i></button>
            </div>
          </div>
        </div>
      </div>
    `)
    document.getElementById("try-to-run-btn").style.display = "";
    document.getElementById("try-to-run-body").innerHTML = `
    <div class="alert alert-success" role="alert">
      TODO!
    </div>
    <div class="input-group">
      <span class="input-group-text">Target ip</span>
      <input type="text" class="form-control" id="run-input"></input>
    </div>
    `
  
    var myModal = new bootstrap.Modal(document.getElementById('try-to-run'))
    myModal.show()
  }
  
  function set_run_code_attack_error(text){
    document.getElementById("try-to-run-btn").style.display = "none";
    document.getElementById("try-to-run-body").innerHTML = `
    <h3><u>An error occurred during the submit</u></h3>
    <h5>Message:</h5>
    <div class="alert alert-danger" id="try-to-run-inner-alert" role="alert">
      
    </div>
    `
    document.getElementById("try-to-run-inner-alert").innerText = text
  }
  function set_run_code_attack_success(status, output){
    document.getElementById("try-to-run-btn").style.display = "none";
    let additional_html = ""
    if (status == "FAILED"){
      additional_html = `
      <div class="alert alert-warning"role="alert">
        In a real situation the flag will be sended next possible time 
      </div>
      `
    }else if (status == "INVALID"){
      additional_html = `
      <div class="alert alert-warning"role="alert">
        In a real situation the flag won't be sended
      </div>
      `
    }
    document.getElementById("try-to-run-body").innerHTML = `
    <h2 id="status-try-to-run"></h2>
    ${additional_html}
    <h4>Generated output</h4>
    <pre class="alert alert-primary" id="try-to-run-inner-alert" role="alert">
    </pre>
  `
  document.getElementById("status-try-to-run").innerText = `Flag status: ${status}`
  document.getElementById("try-to-run-inner-alert").innerText = output
}

  init_monaco_editor();
  reload_config();
  