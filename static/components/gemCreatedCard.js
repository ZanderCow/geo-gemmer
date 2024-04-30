const gemCreated = (gem) => {
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
                                        <p class="fw-bold text-success mb-2">Gem</p>
                                        <h4 class="fw-bold">${gem.name}</h4>
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

                        </div>
                        <div class="col-md-6 col-xxl-3 text-start d-sm-flex d-xxl-flex justify-content-sm-center align-items-md-center align-items-lg-center justify-content-xxl-center align-items-xxl-center" style="padding-top:10px;">
                            <div class="row">
                                <div class="col d-flex d-sm-flex d-md-flex d-lg-flex d-xxl-flex justify-content-center justify-content-sm-center justify-content-md-center justify-content-lg-center justify-content-xxl-center">
                                    <button id="view-gem-button" class="btn btn-success btn-lg d-lg-flex align-items-lg-center" data-bss-hover-animate="pulse" type="submit" style="background: rgb(131,178,113);"><span style="color: rgb(255, 255, 255);">View Gem</span>
                                    </button>
                                </div>
                                <div class="col-md-12 d-flex d-sm-flex d-md-flex d-lg-flex d-xxl-flex justify-content-center justify-content-sm-center justify-content-md-center justify-content-lg-center justify-content-xxl-center" style="padding-top:30px;">
                                    <button id="edit-gem-button" class="btn btn-success btn-lg d-lg-flex align-items-lg-center" data-bss-hover-animate="pulse" type="submit" style="background: rgb(68,157,238);"><span style="color: rgb(255, 255, 255);">Edit Gem&nbsp;</span>
                                    </button>
                                </div>
                                <div class="col-md-12 d-flex d-sm-flex d-md-flex d-lg-flex d-xxl-flex justify-content-center justify-content-sm-center justify-content-md-center justify-content-lg-center justify-content-xxl-center" style="padding-top:30px;">
                                    <button id="delete-gem-button" class="btn btn-success btn-lg d-lg-flex align-items-lg-center" data-bss-hover-animate="pulse" type="submit" style="background: rgb(242,93,83);"><span style="color: rgb(255, 255, 255);">Delete&nbsp;</span>
                                    </button>
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

    // Add hover event listeners to buttons for continuous animation
    card.querySelectorAll('button').forEach(button => {
    button.addEventListener('mouseover', () => {
            button.classList.add('animate__animated', 'animate__pulse', 'animate__infinite',"animate__fast");
        });
        button.addEventListener('mouseout', () => {
            button.classList.remove('animate__animated', 'animate__pulse', 'animate__infinite',"animate__fast");
        });
    });
    
    var viewGemButton = card.querySelector('#view-gem-button');
    viewGemButton.addEventListener('click', () => {
        window.location.href = `/gem/${gem.gem_id}`;
    });
    var editReviewButton = card.querySelector('#edit-gem-button');
    editReviewButton.addEventListener('click', () => {
        window.location.href = `/gem/${gem.gem_id}/edit-gem`;
    });
    var deleteReviewButton = card.querySelector('#delete-gem-button');
    deleteReviewButton.addEventListener('click', () => {
        // Add code to delete review
    });

    return card;
}
export { gemCreated} ;
