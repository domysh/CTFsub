function how_flag_regex_works() {
  show_message("How Flag Regex Works 💡", `HELP TEXT`, false);
}

function how_temporised_flag_submit_works() {
  show_message("How temporised flag submit works 💡", `HELP TEXT`, false);
}

function temporised_submit_change() {
  let status = document.getElementById("temporised-flags").checked;
  let inputs = document.getElementById("temporised-flags-detail-inputs");
  if (status) {
    inputs.style.opacity = "";
  } else {
    inputs.style.opacity = "0.3";
  }
  console.log("NOT IMPLEMENTED");
}

function get_default_text() {
  let def = `"""
Insert here the code for submit the flag
in this code there is just defined the FLAG variable that contain the flag to submit.
[ if you enable multiple flag submit, FLAG variable will contain an array of flags ]

Manage also the status of the submit with the variable STATUS (assigned to SUCCESS by default)
Possible states to assign: SUCCESS, FAILED, INVALID
"""
#Example of implementation:
import requests
try:
    status = requests.post("https://gameserver.com/api/flag_submit", 
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

init_monaco_editor();
temporised_submit_change();
