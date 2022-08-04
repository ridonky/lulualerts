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

    document.querySelector('#product_url').onpaste = () => {
        if (document.querySelector('#id_productquery').value.length > 0) {
            document.querySelector('#url_submit').disabled = false;
        }
        else {
            document.querySelector('#url_submit').disabled = true;
        }
    }

    // // show a way to follow url if there is a URL filled in in the form
    // if (document.querySelector('#product_url').value != ''){
    //     pass
    // }

    // show spinner on product url form submit
    document.querySelector('#product_url').onsubmit = () =>{
        // find what the user just submitted
        const url = document.querySelector('#product_url').value;

        // start the spinner
        document.querySelector('.yes-spinner').style.display = 'flex';
        document.querySelector('.no-spinner').style.display='none';

        // clear out input field - NO DON"T - just keep for now.
        // document.querySelector('#product_url').value = '';

        // disable the submit button again:
        document.querySelector('#url_submit').disabled = true;
        };
});