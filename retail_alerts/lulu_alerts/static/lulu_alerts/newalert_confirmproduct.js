document.addEventListener('DOMContentLoaded', function(){

    // when user confirms the product details look good, let them access alert settings
    document.querySelector('#product-is-good-button').onclick = ()=> {

        // hide the buttons, unhide the alert settings, switch the page~!
        document.querySelector('#product-detail-buttons').style.display = 'none';
        document.querySelector('#alert-settings-div').style.display='';
        document.querySelector('#menu-page-3').setAttribute('class','sidebar-menu-item-selected px-3')
        document.querySelector('#menu-page-2').setAttribute('class','sidebar-menu-item px-3')
    }

    // if item is 2, dont also allow #3
    if (document.querySelector('#menu-page-2') == document.querySelector('.sidebar-menu-item-selected px-3')) {
        document.querySelector('#menu-page-3').setAttribute('class','sidebar-menu-item px-3')
        document.querySelector('#menu-page-1').setAttribute('class','sidebar-menu-item px-3')
    }
})

// Require the custom price input if the custom price field is checked, otherwise its chill
function requirecustom() {
    const current_price = document.querySelector('#current_price')
    const customize_price = document.querySelector('#customize_price')
    const custom_price = document.querySelector('#custom_price')

    if (current_price.checked) {
        custom_price.removeAttribute('required')
    }
    else if (customize_price.checked) {
        custom_price.setAttribute('required','')
    }
}