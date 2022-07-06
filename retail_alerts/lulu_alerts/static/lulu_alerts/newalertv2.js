document.addEventListener('DOMContentLoaded', function() {

    // validate url submit button for non-empty state
    document.querySelector('#url_submit').disabled = true;

    document.querySelector('#product_url').onkeyup = () => {
        if (document.querySelector('#id_productquery').value.length > 0) {
            document.querySelector('#url_submit').disabled = false;
        }
        else {
            document.querySelector('#url_submit').disabled = true;
        }
    }


    // show spinner on product url form submit
    document.querySelector('#product_url').onsubmit = () =>{
        // find what the user just submitted
        const url = document.querySelector('#product_url').value;

        // start the spinner
        document.querySelector('.yes-spinner').style.display = 'flex';
        document.querySelector('.no-spinner').style.display='none';

        // clear out input field:
        document.querySelector('#product_url').value = '';

        // disable the submit button again:
        document.querySelector('#url_submit').disabled = true;
        };
});