function general_setting_help() {
    show_message("What these settings do 💡", `
    <h4><b>- Tick time</b></h4>
    <p>
        The tick time is the time during the bots of the gameserver, 
        insert in the services the flag to stole, and verify in the
        meantime the effective function of the same service.
        CTFsub use this information for start attacks in an inteligent way
        going to stole the flags only when the bots have injected once
        ( there is a timer for every team and attack ).
    </p>
    <h4><b>- Timeout</b></h4>
    <p>
        Some time the attack script can go in stange loops, or can waste time
        waiting for a broken connection. Setting a timeout, every attack script
        can be executed for a team maximum for the time specified 
        (It's possible customize the timeout for every "type" of attack, this is the default setting )
    </p>
    <h4><b>- Workers</b></h4>
    <p>
        CTFsub use threads for start the attack, every thread attack
        a team with an attack (Looking for the next attack that is necessary to do).
        These threads are called workers. You can specify how many workers start
        (choose it looking at the computer specifications, remembering also that usually
            threads are busy only for send and receve connection, so you can abound)
    </p>
    `, false);
}

function auto_blacklist_help() {
    show_message("How auto blacklist Works 💡", `
    <h4><b>What is the autoblacklist?</b></h4>
    <p>
        The autoblacklist is a system that allow CTFsub detect which
        teams closed a vulnerability, and automatically exclude them from the attacks
    </p>
    <h4><b>How it works</b></h4>
    <p>
        When CTFsub run an attack, at the end get a status of the attack (Gived by who create the attack),
        When the status of the attack is VULN_CLOSED (that is different from CONN_CLOSED), CTFsub register the failure of the 
        script... If this happen consecutively for a specific number of time (Specified in these configs), CTFsub
        put the attack in a blacklist (Only for that team!).
        Anyway if you want to try to execute the attack while the attack is in the blacklist after sometime, 
        it's also possible set a time range after that the attack will be retried.
        If the attack goes well, the attack will be removed by the blacklist, instead after the same time,
        the attack will be retried.
    </p>
    <h4><b>- Failure times</b></h4>
    <p>
        (This paramether is compulsory if Auto blacklist is enabled)<br>
        Number of attacks failed consecutively needed for enable the blacklist
    </p>
    <h4><b>- Retry times</b></h4>
    <p>
        If you want, you can set this time range when after that, if the attack is blacklisted, will be retried. 
    </p>

    `, false);
}

function auto_blacklist_change(){
    let status = document.getElementById("auto-blacklist").checked;
    let inputs = document.getElementById("auto-backlist-inputs");
    if (status) {
      inputs.style.opacity = "";
    } else {
      inputs.style.opacity = "0.3";
    }
}

function reload_config(){
    fetch("/api/init/state/4")
    .then( res => res.json() )
    .then( res => {
      if(res.status){
        res = res.data
        if (res.attack_tick_time != null){
            document.getElementById("tick-time").value = res.attack_tick_time
        }
        if (res.attack_timeout != null){
            document.getElementById("timeout").value = res.attack_timeout
        }
        if (res.attack_workers != null){
            document.getElementById("workers").value = res.attack_workers
        }
        if (res.autoblacklist){
            document.getElementById("auto-blacklist").checked = true
            document.getElementById("failure-times").value = res.autoblacklist.max_fails
            document.getElementById("retry-after").value = res.autoblacklist.retry_loop_times
            auto_blacklist_change()
        }
      }
    })
}

function send_attack_configs(next){
    let tick_time = document.getElementById("tick-time").value
    let timeout = document.getElementById("timeout").value
    let workers = document.getElementById("workers").value
    let auto_blacklist = document.getElementById("auto-blacklist").checked
    let failure_times = document.getElementById("failure-times").value
    let retry_after = document.getElementById("retry-after").value

    if(tick_time == ""){
        tick_time = null
    }else{
        tick_time = Number(tick_time)
        if (isNaN(tick_time) || !Number.isInteger(tick_time) || tick_time <= 0){
            show_error("Invalid number for 'tick time'")
            return;
        }
    }

    if(timeout == ""){
        timeout = null
    }else{
        timeout = Number(timeout)
        if (isNaN(timeout) || !Number.isInteger(tick_time) || timeout <= 0){
            show_error("Invalid number for 'timeout'")
            return;
        }
    }

    if(workers == ""){
        workers = null
    }else{
        workers = Number(workers)
        if (isNaN(workers) || !Number.isInteger(tick_time) || workers <= 0){
            show_error("Invalid number for 'workers'")
            return;
        }
    }

    if (auto_blacklist){
        if(failure_times == ""){
            show_error("If you enable autoblacklist, you must insert 'Failure Times'")
            return;
        }else{
            failure_times = Number(failure_times)
            if (isNaN(failure_times) || !Number.isInteger(failure_times) || failure_times <= 0){
                show_error("Invalid number for 'Failure times'")
                return;
            }
        }

        if(retry_after == ""){
            retry_after = null;
        }else{
            retry_after = Number(retry_after)
            if (isNaN(retry_after) || !Number.isInteger(retry_after) || retry_after <= 0){
                show_error("Invalid number (greater than 1)) for 'Retry after'")
                return;
            }
        }
        auto_blacklist = {
            "max_fails":failure_times,
            "retry_loop_times": retry_after
        }
    
    }else{
        auto_blacklist = null;
    }

    move_init(next,{
        "attack_tick_time":tick_time,
        "attack_timeout":timeout,
        "attack_workers":workers,
        "autoblacklist":auto_blacklist
    });
}

auto_blacklist_change();
reload_config();