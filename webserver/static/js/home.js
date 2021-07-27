function ctfsub_help(){
    show_message('▶️ WTF❓',`<a href='https://www.youtube.com/watch?v=dQw4w9WgXcQ' target='_blanck' >https://www.youtube.com/watch?v=dQw4w9WgXcQ</a>`,false)
}

function back_to_config(){
    show_question("Change configuration of CTFsub ⚙️",`
    For change the configurations of CTFsub, the web server will come back to configuration mode.
    
    After you changed the configuration of CTFsub, click the start button and at that moment the engine will update the configurations.
    Clicking "OK", CTFsub will switch to configuration mode.
    <br><b>Nothing will be lost and the attacks will keep running during the re-configuration!</b>
    `,false).then( ans => { if (ans) { fetch("/api/back_to_configuration") } })
}