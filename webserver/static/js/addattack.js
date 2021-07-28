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
    let def = `"""
  Insert here the code for submit the flag
  in this code there is just defined the FLAG variable that contain the flag to submit.
  [ if you enable multiple flag submit, FLAG variable will contain an array of flags ]
  
  Manage also the status of the submit with the variable STATUS (assigned to FAILED by default)
  Possible states to assign: SUCCESS, FAILED, INVALID
  """
  #Example of implementation:
  import requests
  try:
      status = requests.post("https://gameserver.example.com/api/flag_submit", 
                      data={
                          "flag":FLAG,
                          "team_id":"this_is_a_team_id"
                      }, timeout=3
      ).status_code
      if status != 200:
          if status == 429:
              STATUS = FAILED #Too many requests to game server
          elif status == 400:
              STATUS = INVALID #The flag submitted is not a valid flag
      else:
          STATUS = SUCCESS #Flag submited successfully!
      
  except requests.exceptions.Timeout: #Probably the gameserver isn't up
      STATUS = FAILED
  `;
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
    if (window.flag_submit_code == undefined){
      window.flag_submit_code = get_default_text()
    }
    if (window.editor != undefined){
      window.editor.setValue(window.flag_submit_code);
    }
  }
  
  function get_text_editor(){
    if (window.flag_submit_code == undefined){
      window.flag_submit_code = get_default_text()
    }
    return window.flag_submit_code
  }
  
  function useless_function() {
    show_message('▶️ WTF❓',`<a href='https://www.youtube.com/watch?v=dQw4w9WgXcQ' target='_blanck' >https://www.youtube.com/watch?v=dQw4w9WgXcQ</a>`,false)
  }
  
  function submit_flag_settings(next){
  }
  
  function reload_config(){
    window.flag_submit_code = get_default_text()
  }
  
  init_monaco_editor();
  temporised_submit_change();
  multiple_submit_change();
  flag_expire_change();
  
  reload_config();
  