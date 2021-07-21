function how_flag_regex_works() {
  show_message("How Flag Regex Works 💡", `
    <h5>Regexes can help you to better filter the flags:</h5>
    Infact setting a flag regex, whatever is the output of your attack script, this will be
    selected with the regex. <b>If in some service the format of the flag is different or 
    doesn't exists, don't worry, you will be able to choose a custom regex for every attack you start.</b>
    If you wnat to disable the regex filter, leave the text input blank.
  `, false);
}

function how_temporised_flag_submit_works() {
  show_message("How temporised flag submit works 💡", `
    In some A/D CTFs, the game server can receve limited connection for the flag submit (usually for avoid DoS),
    for this reason, in these cases it's important send as many submit as the game server can accept.<br<br>
    Set a time range for submit a flag, after this set how many request are accepted in that range.
    For instance, if the game server accept 5 request every minute, you could set the time range to 5*60 seconds and
    ask to send 5 request in every range. 
  `, false);
}

function how_multiple_flag_submit_works() {
  show_message("How multiple flag submit works 💡", `
  If your game server allow to send multiple flag, enable this option and specify the maximum number of flag that can be submitted in each request.
  When you enable this option, the FLAG variable gived in the submit script will become a list of str (so a list of flags)!
  `, false);
}

function how_flag_expire_works() {
  show_message("How flag expire works 💡", `
  Usually in A/D competitions, the flags generated have a limited validity in the time: Consequently setting an expire time for the flags can avoid to send 
  too old flags and allow to reduce the number of requests. Infact since the flag is stored in the database, it have a limited time for being submitted,
  and after this, the flag is automatically considered invalid, enabling this option.
  `, false);
}

function temporised_submit_change() {
  let status = document.getElementById("temporised-flags").checked;
  let inputs = document.getElementById("temporised-flags-detail-inputs");
  if (status) {
    inputs.style.opacity = "";
  } else {
    inputs.style.opacity = "0.3";
  }
}

function multiple_submit_change() {
  let status = document.getElementById("multiple-flags").checked;
  let inputs = document.getElementById("multiple-flag-detail-inputs");
  if (status) {
    inputs.style.opacity = "";
  } else {
    inputs.style.opacity = "0.3";
  }
}

function flag_expire_change(){
  let status = document.getElementById("flag-expire").checked;
  let inputs = document.getElementById("flag-expire-detail-inputs");
  if (status) {
    inputs.style.opacity = "";
  } else {
    inputs.style.opacity = "0.3";
  }
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

async function get_setted_text() {
  let res = get_default_text();
  await fetch("/api/flag-submit-code/get")
    .then((r) => r.json())
    .then((r) => {
      if (r.status) {
        res = r.data;
      }
    });
  return res;
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
        value: await get_setted_text(),
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

async function reload_text() {
  window.editor.setValue(await get_setted_text());
}

function useless_function() {
  show_message("Useless", "I'm useless!");
}

function submit_flag_settings(){
  show_error("Not valid json sended! Read the instruction about the possible configurations of the json file");
  request_next();
}

init_monaco_editor();
temporised_submit_change();
multiple_submit_change();
flag_expire_change();


/*TODO
Verify (and/or complete) /api/flag-submit-code/get backend

Full HELP texts in help show functions

Build next button function with backend data collect and frontend check paramethers
- Valid numbers
- Valid regex
- valid python code for flag submit (syntax (In the backend))

{
    "libs":
}


*/