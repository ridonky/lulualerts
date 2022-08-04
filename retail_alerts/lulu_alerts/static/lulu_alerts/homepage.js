document.addEventListener('DOMContentLoaded', function() {

    window.onscroll = () => {   
        if (window.scrollY >= (window.innerHeight)/3) {

            // If div is not already there, make it appear slowly
            if (document.querySelector('#homepageinfo').style.opacity == 0) {
                
                // suspend the event listener so it stops skipping
                window._onscrollupholder = window.onscroll
                window.onscroll = null;

                let id = null;
                let opaque = 0;
                clearInterval(id);
    
                // Every 30ms, execute appear
                id = setInterval(appear, 50);
                
                function appear() {
                    // If opacity=1, stop 
                    if (opaque == 10) {
                        document.querySelector('#homepageinfo').style.opacity = 1;                       
                        clearInterval(id);

                        // add back the event listener
                        window.onscroll = window._onscrollupholder;
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


        // if (window.scrollY + window.innerHeight >= document.body.offsetHeight) {
        //     const default_borderWidth = document.querySelector('#bottomcta').style.borderWidth;
        //     const default_borderColor = document.querySelector('#bottomcta').style.borderColor;
            
        //     document.querySelector('#bottomcta').style.borderWidth = "10px";
        //     document.querySelector('#bottomcta').style.borderColor = "yellow";
        //     let id2 = null;
        //     let counter = 0;

        //     clearInterval(id2);
        //     setInterval(timer,500);

        //     function timer() {
        //         if (counter = 1)
        //         {
        //             document.querySelector('#bottomcta').style.borderWidth = default_borderWidth;
        //             document.querySelector('#bottomcta').style.borderColor = default_borderColor;
        //             clearInterval(id2);
        //         }
        //         else {
        //             counter++;
        //         }
        //     }
        // }

        // else {
        //     document.querySelector('#bottomcta').style.borderWidth = default_borderWidth;
        //     document.querySelector('#bottomcta').style.borderColor = default_borderColor;
        // }

    
    };

});