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

async function upload_config() {
  let files = document.getElementById("config-upload").files;
  if (files.length <= 0) {
    show_error("You have to upload a json file!");
    return;
  } else {
    let data = null;
    try {
      let json_text = await files[0].text();
      let data_parsed = JSON.parse(json_text);
      data = { config_method: "upload", data: data_parsed };
    } catch (err) {
      show_error("The file choosen is not a json file!");
      return;
    }
    request_next(data);
  }
}
