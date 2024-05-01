const gemPinned = (gem) => {
    var card = document.createElement('div');
    card.className = 'card';
    card.innerHTML = `
    <div class="card-body px-4 py-5 px-md-5">
        <div class="row gy-4 row-cols-1 row-cols-md-2 row-cols-xl-3 d-md-flex d-lg-flex justify-content-md-center align-items-md-center justify-content-lg-center">
            <div class="col-md-9 col-lg-10 col-xxl-3 d-sm-flex d-xxl-flex justify-content-sm-center justify-content-xxl-center align-items-xxl-center">
                <img id="gem-image" class="rounded fit-cover" src="/static/img/gem-image-placeholder-jpg" width="314" height="193">
            </div>
            <div class="col-md-9 col-lg-10 col-xxl-9 d-xxl-flex flex-fill align-items-xxl-center">
                <div class="container">
                    <div class="row d-xxl-flex justify-content-xxl-center">
                        <div class="col-md-6">
                            <div class="row">
                                <div class="col-md-12">
                                    <div class="text-center">
                                        <p class="fw-bold text-success mb-2">Gem </p>
                                        <h4 class="fw-bold">${gem.gem_name}</h4>
                                    </div>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-md-12">
                                    <div class="card flex-grow-1 flex-fill">
                                        <div class="card-body"><svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="currentColor" viewBox="0 0 16 16" class="bi bi-grid-1x2-fill text-success" style="top:1rem;center:1rem;position:absolute;font-size:35px;">
                                                <path d="M0 1a1 1 0 0 1 1-1h5a1 1 0 0 1 1 1v14a1 1 0 0 1-1 1H1a1 1 0 0 1-1-1zm9 0a1 1 0 0 1 1-1h5a1 1 0 0 1 1 1v5a1 1 0 0 1-1 1h-5a1 1 0 0 1-1-1zm0 9a1 1 0 0 1 1-1h5a1 1 0 0 1 1 1v5a1 1 0 0 1-1 1h-5a1 1 0 0 1-1-1z"></path>
                                            </svg>
                                            <h5 class="fw-bold text-center card-title" style="padding-top:10px;">Type</h5>
                                            <p class="text-center text-muted card-text">${gem.gem_type}</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-md-12">
                                    <div class="card flex-grow-1 flex-fill">
                                        <div class="card-body"><svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="currentColor" viewBox="0 0 16 16" class="bi bi-calendar-date-fill text-success" style="top:1rem;center:1rem;position:absolute;font-size:35px;">
                                                <path d="M4 .5a.5.5 0 0 0-1 0V1H2a2 2 0 0 0-2 2v1h16V3a2 2 0 0 0-2-2h-1V.5a.5.5 0 0 0-1 0V1H4zm5.402 9.746c.625 0 1.184-.484 1.184-1.18 0-.832-.527-1.23-1.16-1.23-.586 0-1.168.387-1.168 1.21 0 .817.543 1.2 1.144 1.2z"></path>
                                                <path d="M16 14V5H0v9a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2m-6.664-1.21c-1.11 0-1.656-.767-1.703-1.407h.683c.043.37.387.82 1.051.82.844 0 1.301-.848 1.305-2.164h-.027c-.153.414-.637.79-1.383.79-.852 0-1.676-.61-1.676-1.77 0-1.137.871-1.809 1.797-1.809 1.172 0 1.953.734 1.953 2.668 0 1.805-.742 2.871-2 2.871zm-2.89-5.435v5.332H5.77V8.079h-.012c-.29.156-.883.52-1.258.777V8.16a12.6 12.6 0 0 1 1.313-.805h.632z"></path>
                                            </svg>
                                            <h5 class="fw-bold text-center card-title" style="padding-top:10px;">Date Visited</h5>
                                            <p class="text-center text-muted d-flex justify-content-center card-text">${gem.date_pinned}</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-6 col-xxl-3 text-start d-sm-flex d-xxl-flex justify-content-sm-center align-items-md-center align-items-lg-center justify-content-xxl-center align-items-xxl-center" style="padding-top:10px;">
                            <div class="row">
                                <div class="col d-flex d-sm-flex d-md-flex d-lg-flex d-xxl-flex justify-content-center justify-content-sm-center justify-content-md-center justify-content-lg-center justify-content-xxl-center">
                                    <button id="get-gem-${gem.gem_id}" class="btn btn-success btn-lg d-lg-flex align-items-lg-center" type="submit" style="background: rgb(131,178,113);" on><span style="color: rgb(255, 255, 255);">View Gem</span></button>
                                </div>
                                <div class="col-md-12 d-flex d-sm-flex d-md-flex d-lg-flex d-xxl-flex justify-content-center justify-content-sm-center justify-content-md-center justify-content-lg-center justify-content-xxl-center" style="padding-top:30px;">
                                    <button id="delete-gem-${gem.gem_id}"class="btn btn-success btn-lg d-lg-flex align-items-lg-center" data-bss-hover-animate="pulse" type="submit" style="background: rgb(242,93,83);"><span style="color: rgb(255, 255, 255);">Delete&nbsp;</span></button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="row gy-4 row-cols-1 row-cols-md-2 row-cols-xl-3 d-md-flex d-lg-flex justify-content-md-center justify-content-lg-center"><div class="w-100"></div></div>
    </div>
    
    `;
    /*
    fetch(`/gem/${gem.gem_id}/get-primary-gem-image`, {
        method: 'GET',
        credentials: 'include'  // Necessary to include cookies with requests
    })
    .then((response) => {
        if (response.ok) {
            return response.json();
        } 
        else {
            return response.text().then(text => {
                throw new Error(text);
            });
        }
    })

    .then(data => { 
        card.querySelector("#gem-image").src = `data:image/png;base64,${data}`;
    })
    
    */
    // Add hover event listeners to buttons for continuous animation
    card.querySelectorAll('button').forEach(button => {
    button.addEventListener('mouseover', () => {
        button.classList.add('animate__animated', 'animate__pulse', 'animate__infinite',"animate__fast");
        });
    button.addEventListener('mouseout', () => {
        button.classList.remove('animate__animated', 'animate__pulse', 'animate__infinite',"animate__fast");
        });
    });

    var viewButton = card.querySelector(`#get-gem-${gem.gem_id}`);
    viewButton.addEventListener('click', () => {
        window.location.href = `/gem/${gem.gem_id}`; // Modify the URL according to your routing logic
    });

    var viewButton = card.querySelector(`#delete-gem-${gem.gem_id}`);
    viewButton.addEventListener('click', () => {

        // Get the CSRF token from the cookie
        let csrf_token = document.cookie.split('; ')  
        .find(row => row.startsWith("csrf_access_token" + '=')) 
        ?.split('=')[1];  

        fetch(`/user/delete-gem/${gem.gem_id}`, {
            method: 'DELETE',
            headers: {
                 'X-CSRF-Token': csrf_token // The CSRF token you retrieved from your cookie or elsewhere
                 }, // Setting the Content-Type as application/json
            credentials: 'include'  // Necessary to include cookies with requests
        })
        
        .then((response) => {
            if (response.ok) {
                return response.json();
            } 
            else {
                return response.text().then(text => {
                    throw new Error(text);
                });
            }
        })

        .then(data => { 
            card.remove();
        })
    });


    return card;
}
export  { gemPinned };