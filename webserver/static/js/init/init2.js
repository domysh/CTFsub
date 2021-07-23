function how_ip_range_works() {
  show_message(
    "How IP range works 💡",
    `
<b>With ip range you can generate the teams' ip list easily and fast.</b>
<br>
<p>
    For generate the list of ip you can insert in every field the number,
    or a range of numbers like: '1-20'. You can insert at maximum 2 range in the ip. The real IP list
    will be generated automaticaly. If this method is not efficent for your race, you should
    not chose this method and upload a teams' ip list.<br>
    <span style="color: var(--third);">Remember to insert your team's IP as the IP to exclude for avoid to attack yourserlf!</span>
</p>
For instance:
<br>
<div class="ip-writer col-10">
    <div id="ip-byte-1"><input type="text" class="ip-byte-text form-control" value="10" readonly/></div>
    <span class="ip-dot">.</span>
    <div id="ip-byte-2"><input type="text" class="ip-byte-text form-control" value="1" readonly/></div>
    <span class="ip-dot">.</span>
    <div id="ip-byte-3"><input type="text" class="ip-byte-text form-control" value="1" readonly/></div>
    <span class="ip-dot">.</span>
    <div id="ip-byte-4"><input type="text" class="ip-byte-text form-control" value="1-10" readonly/></div>
</div>
will generate this list of IPs:<br>
<pre><code class="language-json">[ "10.1.1.1", "10.1.1.2", "10.1.1.3", "10.1.1.4", 
"10.1.1.5", "10.1.1.6", "10.1.1.7", "10.1.1.8", 
"10.1.1.9", "10.1.1.10" ]</code></pre>
<br>
OR
<br>
<div class="ip-writer col-10">
    <div id="ip-byte-1"><input type="text" class="ip-byte-text form-control" value="10" readonly/></div>
    <span class="ip-dot">.</span>
    <div id="ip-byte-2"><input type="text" class="ip-byte-text form-control" value="1" readonly/></div>
    <span class="ip-dot">.</span>
    <div id="ip-byte-3"><input type="text" class="ip-byte-text form-control" value="1-3" readonly/></div>
    <span class="ip-dot">.</span>
    <div id="ip-byte-4"><input type="text" class="ip-byte-text form-control" value="1-2" readonly/></div>
</div>
will generate this list of IPs:<br>
<pre><code class="language-json">[ "10.1.1.1", "10.1.1.2", "10.1.2.1", 
"10.1.2.2", "10.1.3.1", "10.1.3.2" ]</code></pre>
<br>
OR
<br>
<div class="ip-writer col-10">
    <div id="ip-byte-1"><input type="text" class="ip-byte-text form-control" value="10" readonly/></div>
    <span class="ip-dot">.</span>
    <div id="ip-byte-2"><input type="text" class="ip-byte-text form-control" value="1" readonly/></div>
    <span class="ip-dot">.</span>
    <div id="ip-byte-3"><input type="text" class="ip-byte-text form-control" value="1" readonly/></div>
    <span class="ip-dot">.</span>
    <div id="ip-byte-4"><input type="text" class="ip-byte-text form-control" value="1" readonly/></div>
</div>
will generate this list of IPs:<br>
<pre><code class="language-json">[ "10.1.1.1" ]</code></pre>
<br>
`,
    false
  );
}

document
  .getElementById("config-upload")
  .addEventListener("change", function () {
    const fileChosen = document.getElementById("upload-btn");
    if (this.files.length <= 0) {
      fileChosen.textContent = "Choose file";
      fileChosen.style = "";
    } else {
      fileChosen.textContent = this.files[0].name;
      fileChosen.style["font-weight"] = "bold";
      fileChosen.style.color = "var(--done)";
    }
  });

function ip_composed_ctrl(n) {
  let input_to_check = document.querySelector(`#ip-byte-${n} input`);
  let text = input_to_check.value;
  let new_text = "";
  let pass_to_next = null;
  let line_count = 0;
  for (let i = 0; i < text.length; i++) {
    if (is_numeric(text[i])) {
      new_text += text[i];
    } else if (text[i] == "-") {
      if (line_count == 0) {
        line_count++;
        new_text += "-";
      }
    } else if (text[i] == ".") {
      pass_to_next = i;
      break;
    }
  }
  input_to_check.value = new_text;
  if (pass_to_next != null && n != 4) {
    let next_input = document.querySelector(`#ip-byte-${n + 1} input`);
    next_input.focus();
    if (pass_to_next < text.length) {
      next_input.value =
        text.substring(pass_to_next + 1, text.length) + next_input.value;
    }
    ip_composed_ctrl(n + 1);
  }
}

function ip_ctrl() {
  let input_to_check = document.getElementById("team-ip");
  let new_text = "";
  let text = input_to_check.value;
  let dot_counter = 0;
  for (let i = 0; i < text.length; i++) {
    if (is_numeric(text[i])) {
      new_text += text[i];
    } else if (text[i] == "." && dot_counter < 3) {
      new_text += text[i];
      dot_counter++;
    }
  }
  input_to_check.value = new_text;
}

async function upload_config() {
  let files = document.getElementById("config-upload").files;
  if (files.length <= 0) {
    show_error("You have to upload a json file!");
    return;
  } else {
    let data = null;
    try {
      let json_text = await files[0].text();
      data = JSON.parse(json_text);
    } catch (err) {
      show_error("The file choosen is not a json file!");
      return;
    }
    let res = {};
    if (Array.isArray(data)) {
      if (data.length <= 0) {
        show_error("Insert at least 1 IP in the list!");
        return;
      }
      for (let i = 0; i < data.length; i++) {
        if (isDict(data[i])) {
          try {
            if (!validIPaddress(data[i].ip)) {
              show_error(
                "Not valid format sended! (Found an invalid IP) Read the instruction about the possible configurations of the json file"
              );
              return;
            } else {
              while (true) {
                if (data[i].name in res) {
                  data[i].name += "_";
                } else {
                  res[data[i].name] = data[i].ip;
                  break;
                }
              }
            }
          } catch (err) {
            show_error(
              "Not valid format sended! (Found an invalid syntax) Read the instruction about the possible configurations of the json file"
            );
            return;
          }
        } else {
          if (!validIPaddress(data[i])) {
            show_error(
              "Not valid format sended! (Found an invalid IP) Read the instruction about the possible configurations of the json file"
            );
            return;
          } else {
            let name = `team_${i + 1}`;
            while (true) {
              if (name in res) {
                name += "_";
              } else {
                res[name] = data[i];
                break;
              }
            }
          }
        }
      }
    } else if (isDict(data)) {
      var keys = Object.keys(data);
      for (let i = 0; i < keys.length; i++) {
        if (!validIPaddress(data[keys[i]])) {
          show_error(
            "Not valid format sended! (Found an invalid IP) Read the instruction about the possible configurations of the json file"
          );
          return;
        }
      }
      res = data;
    } else {
      show_error(
        "Not valid json sended! Read the instruction about the possible configurations of the json file"
      );
      return;
    }
    request_next(res);
  }
}
function send_team_list(next) {
  if (window.init2_old_status != null && document.getElementById("keep-old").checked){
    move_init(next,window.init2_old_status);
    return
  }
  let ip_bytes = ["", "", "", ""];
  ip_bytes[0] = document.querySelector("#ip-byte-1 input").value;
  ip_bytes[1] = document.querySelector("#ip-byte-2 input").value;
  ip_bytes[2] = document.querySelector("#ip-byte-3 input").value;
  ip_bytes[3] = document.querySelector("#ip-byte-4 input").value;

  let ip_to_skip = document.getElementById("team-ip").value.replace(" ", "");

  let range_counter = 0;
  for (let i = 0; i < ip_bytes.length; i++) {
    if (ip_bytes[i] == "") {
      if (!next){
        request_back()
        return;
      }
      show_error(
        "For go to next step, you have to select a range or upload a list of IP"
      );
      return;
    }
    if (ip_bytes[i].includes("-")) {
      let range = ip_bytes[i].replace(" ", "").split("-");
      if (range.length != 2) {
        show_error(
          "Invalid IP range (A range have to be written in this way: '[from]-[to]', example: '30-72')"
        );
        return;
      }
      if (isNaN(parseInt(range[0])) || isNaN(parseInt(range[1]))) {
        show_error(
          "Invalid IP range (A range have to be written in this way: '[from]-[to]', example: '30-72')"
        );
        return;
      }
      range[0] = parseInt(range[0]);
      range[1] = parseInt(range[1]);
      if (range[0] >= range[1]) {
        show_error(
          "Invalid IP range (A range have to be written in this way: '[from]-[to]', example: '30-72') P.S. [from] have to be < of [to]"
        );
        return;
      }

      if (range[0] < 0 || range[0] > 255 || range[1] < 0 || range[1] > 255) {
        show_error(
          "Invalid IP range (A range have to be written in this way: '[from]-[to]', example: '30-72') P.S. [from] and [to] have to be >= 0 and <= 255"
        );
        return;
      }
      ip_bytes[i] = range;
      range_counter++;
    } else {
      if (!isNaN(parseInt(ip_bytes[i]))) {
        ip_bytes[i] = parseInt(ip_bytes[i]);
        if (ip_bytes[i] < 0 || ip_bytes[i] > 255) {
          show_error(
            "Invalid IP range (You can insert only numbers valid for an IPv4 [0 <= byte <= 255])"
          );
          return;
        }
      } else {
        show_error(
          "Invalid IP range (You can insert only numbers or ranges in text fields!)"
        );
        return;
      }
    }
  }
  if (range_counter > 2) {
    show_error("Invalid IP range (You can use at maximum 2 ranges)");
    return;
  }
  if (ip_to_skip != "" && !validIPaddress(ip_to_skip)) {
    show_error("Insert a valid ip to skip (You team IP)");
    return;
  }

  let ret = {};
  let counter = 0;

  function generate_ips(pref, ip_b) {
    if (ip_b.length <= 0) {
      pref = pref.substring(0, pref.length - 1);

      if (validIPaddress(pref) && pref != ip_to_skip) {
        ret[`team_${counter}`] = pref;
        counter++;
      }
      return;
    }
    if (typeof ip_b[0] == "number") {
      generate_ips(`${pref}${ip_b[0]}.`, ip_b.slice(1));
    } else {
      for (let i = ip_b[0][0]; i <= ip_b[0][1]; i++) {
        generate_ips(`${pref}${i}.`, ip_b.slice(1));
      }
    }
  }
  generate_ips("", ip_bytes);
  move_init(next,ret);
}

function reload_config(){
  fetch("/api/init/state/2")
    .then( res => res.json() )
    .then( res => {
      if(res.status){
        window.init2_old_status = res.data
        document.getElementById("old-settings").style.display = ""
      }else{
        window.init2_old_status = null
      }
    })
}

function show_old_config(){
  if (window.init2_old_status != null){
    show_message(
      "Setted configurations:",
      `<pre><code class="language-json">${escapeHtml(JSON.stringify(window.init2_old_status,null,4))}</code></pre>`,
      false
    )
  }
}

reload_config()