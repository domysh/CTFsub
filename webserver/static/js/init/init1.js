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
    let modal = loading_modal();
    request_next(data,(data)=>{
      modal.hide()
      if ("msg" in data){
        show_error(data.msg)
      }
    });    
  }
}

function loading_modal(){
  modify_modal(`
  <div class="modal fade" id="loading_modal" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="loading_modalLabel" aria-hidden="true">
  <div class="modal-dialog modal-xl">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="loading_modalLabel">Loading configurations ⌛</h5>
      </div>
      <div class="modal-body" id="loading_modal-body">
        <div class="d-flex justify-content-center align-items-center" style="min-height:300px">
          <div class="spinner-border" role="status"></div>
          <span style="margin-left:10px">Loading...</span>
        </div>
      </div>
    </div>
  </div>
</div>
  `)

  var myModal = new bootstrap.Modal(document.getElementById('loading_modal'))
    myModal.show()
  return myModal
}
