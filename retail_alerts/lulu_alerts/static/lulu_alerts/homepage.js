document.addEventListener('DOMContentLoaded', function() {

    window.onscroll = () => {   
        if (window.scrollY >= (window.innerHeight)/3) {

            // If div is not already there, make it appear slowly
            if (document.querySelector('#homepageinfo').style.opacity == 0) {
                
                // suspend the event listener so it stops skipping
                // window._onscrollupholder = window.onscroll
                // window.onscroll = null;

                let id = null;
                let opaque = 0;
                clearInterval(id);
    
                // Every 50ms, execute appear
                id = setInterval(appear, 50);
                
                function appear() {
                    // If opacity=1, stop 
                    if (opaque == 10) {
                        document.querySelector('#homepageinfo').style.opacity = 1;                       
                        clearInterval(id);

                        // add back the event listener
                        // window.onscroll = window._onscrollupholder;
                    }

                    // Increase opacity by .1
                    else {
                        opaque++;
                        document.querySelector('#homepageinfo').style.opacity = opaque/10;
                    }
                };
            }
        }
        // otherwise, opacity = 0
        else {
            document.querySelector('#homepageinfo').style.opacity = 0;
        };
    };
});