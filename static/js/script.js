function showhide(toggleID) {
    if (toggleID == 'general_form') {

        document.getElementById('general_form').style.display = 'block'
        document.getElementById('review_form').style.display = 'none'
        document.getElementById('review_form').style.display = 'none'
    } else if (toggleID == 'review_form') {
        document.getElementById('general_form').style.display = 'none'
        document.getElementById('review_form').style.display = 'block'
        document.getElementById('code_form').style.display = 'none'
    } else if (toggleID == 'code_form') {
        document.getElementById('general_form').style.display = 'none'
        document.getElementById('review_form').style.display = 'none'
        document.getElementById('code_form').style.display = 'block'
    }
}
