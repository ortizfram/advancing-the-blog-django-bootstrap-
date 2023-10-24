// Maintaining Player Height
player = document.getElementById('player')

document.onreadystatechange = function() {
    if(document.readystate == 'interactive'){
        maintainRatio()
    }
}

function maintainRatio(){
    var w =player.clientWidth
    var h =(w*9)/16
    console.log({w, h})
    player.height = h
}

window.onresize = maintainRatio