function openNav() {
    //opens side navbar by 70 percent
    document.getElementById("mySidenav").style.width = "20%" 

   //opens overlay display
    document.getElementById('backdrop').style.display = "block" 
}

function closeNav() {
    //closes side navbar totally
    document.getElementById("mySidenav").style.width = "0"

    //removes overlay display
    document.getElementById('backdrop').style.display = "none"
}