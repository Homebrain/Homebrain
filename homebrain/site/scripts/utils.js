
function toggleHidden(elementid){
    element = document.getElementById(elementid);
    if (element.style.display == "")
        element.style.display = "none";
    else
        element.style.display = "";
}
