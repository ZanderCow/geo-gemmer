const searchGem = (gem) => {
    var card = document.createElement('div');
    card.className = 'card';
    card.innerHTML = `
    <div class="card-body px-4 py-5 px-md-5" style="padding: 0px;">
        <div class="row">
        <div class="col-md-4 col-lg-6 col-xl-5 col-xxl-6 offset-xl-0 offset-xxl-0 d-md-flex d-xl-flex d-xxl-flex justify-content-md-center align-items-md-center align-items-xl-center align-items-xxl-center">
            <header id="greeting-2" class="bg-primary-gradient" style="background: #ffffff;">
            <div class="text-center">
                <p class="fw-bold text-success mb-2">Gem</p>
                <h3 class="fw-bold" style="padding: 15px;">${gem.name}</h3>
                
            </div>
            </header>
        </div>
        <div class="col-md-8 col-lg-6 col-xl-7 col-xxl-6 offset-xl-0 offset-xxl-0 d-xxl-flex justify-content-xxl-end">
            <img id="gem-image" class="rounded d-xl-flex align-items-xl-center fit-cover w-100" style="min-height: 300px;" src="/static/img/gem-image-placeholder.png" width="659" height="373">
        </div>
        </div>
        <div class="row" style="padding-top: 20px;">
        <div class="col-md-4 offset-xxl-1 d-xxl-flex justify-content-xxl-center align-items-xxl-center">
            <div class="card flex-grow-1 flex-fill">
            <div class="card-body">
                <div class="row">
                <div class="col-md-6 col-xl-6 col-xxl-3 d-lg-flex d-xxl-flex justify-content-lg-center align-items-lg-center justify-content-xxl-center align-items-xxl-center"><svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 24 24" fill="none" class="text-success" style="top: 1rem;center: 1rem;font-size: 35px;">
                    <path fill-rule="evenodd" clip-rule="evenodd" d="M11 17.9C8.71776 17.4367 7 15.419 7 13V7C7 4.23858 9.23858 2 12 2C14.7614 2 17 4.23858 17 7V13C17 15.419 15.2822 17.4367 13 17.9V21C13 21.5523 12.5523 22 12 22C11.4477 22 11 21.5523 11 21V17.9ZM12 4C13.6569 4 15 5.34315 15 7V13C15 14.3062 14.1652 15.4175 13 15.8293V11C13 10.4477 12.5523 10 12 10C11.4477 10 11 10.4477 11 11V15.8293C9.83481 15.4175 9 14.3062 9 13V7C9 5.34315 10.3431 4 12 4Z" fill="currentColor"></path>
                    </svg></div>
                <div class="col-md-12 col-xl-12 col-xxl-9">
                    <h5 class="fw-bold text-center" style="padding-top: 10px;">Type</h5>
                    <p class="text-center text-muted mb-4">${gem.gem_type}</p>
                </div>
                </div>
            </div>
            </div>
        </div>
        <div class="col-md-4 offset-xxl-0 d-xxl-flex justify-content-xxl-center align-items-xxl-center">
            <div class="card flex-grow-1 flex-fill">
            <div class="card-body">
                <div class="row">
                <div class="col-md-6 col-xxl-3 d-lg-flex d-xxl-flex justify-content-sm-center align-items-sm-center justify-content-md-center align-items-md-center justify-content-lg-center align-items-lg-center justify-content-xl-center align-items-xl-center justify-content-xxl-center align-items-xxl-center"><svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 24 24" fill="none" class="text-success" style="top: 1rem;center: 1rem;font-size: 35px;">
                                    <path fill-rule="evenodd" clip-rule="evenodd" d="M12 21C16.9706 21 21 16.9706 21 12C21 7.02944 16.9706 3 12 3C7.02944 3 3 7.02944 3 12C3 16.9706 7.02944 21 12 21ZM14.8055 18.4151C17.1228 17.4003 18.7847 15.1667 18.9806 12.525C18.1577 12.9738 17.12 13.3418 15.9371 13.598C15.7882 15.4676 15.3827 17.1371 14.8055 18.4151ZM9.1945 5.58487C7.24725 6.43766 5.76275 8.15106 5.22208 10.244C5.4537 10.4638 5.84813 10.7341 6.44832 11.0008C6.89715 11.2003 7.42053 11.3798 8.00537 11.5297C8.05853 9.20582 8.50349 7.11489 9.1945 5.58487ZM10.1006 13.9108C10.2573 15.3675 10.5852 16.6202 10.9992 17.5517C11.2932 18.2133 11.5916 18.6248 11.8218 18.8439C11.9037 18.9219 11.9629 18.9634 12 18.9848C12.0371 18.9634 12.0963 18.9219 12.1782 18.8439C12.4084 18.6248 12.7068 18.2133 13.0008 17.5517C13.4148 16.6202 13.7427 15.3675 13.8994 13.9108C13.2871 13.9692 12.6516 14 12 14C11.3484 14 10.7129 13.9692 10.1006 13.9108ZM8.06286 13.598C8.21176 15.4676 8.61729 17.1371 9.1945 18.4151C6.8772 17.4003 5.21525 15.1666 5.01939 12.525C5.84231 12.9738 6.88001 13.3418 8.06286 13.598ZM13.9997 11.8896C13.369 11.9609 12.6993 12 12 12C11.3008 12 10.631 11.9609 10.0003 11.8896C10.0135 9.66408 10.4229 7.74504 10.9992 6.44832C11.2932 5.78673 11.5916 5.37516 11.8218 5.15605C11.9037 5.07812 11.9629 5.03659 12 5.01516C12.0371 5.03659 12.0963 5.07812 12.1782 5.15605C12.4084 5.37516 12.7068 5.78673 13.0008 6.44832C13.5771 7.74504 13.9865 9.66408 13.9997 11.8896ZM15.9946 11.5297C15.9415 9.20582 15.4965 7.11489 14.8055 5.58487C16.7528 6.43766 18.2373 8.15107 18.7779 10.244C18.5463 10.4638 18.1519 10.7341 17.5517 11.0008C17.1029 11.2003 16.5795 11.3798 15.9946 11.5297Z" fill="currentColor"></path>
                                </svg></div>
                            <div class="col-md-12 col-xl-12 col-xxl-9">
                                <h5 class="fw-bold text-center" style="padding-top: 10px;">Distance</h5>
                                <p class="text-center text-muted mb-4">${gem.distance} mi away</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-4 col-xxl-3 offset-xxl-0 d-flex d-md-flex d-xl-flex d-xxl-flex justify-content-center align-items-md-center align-items-xl-center justify-content-xxl-center align-items-xxl-center">
                <button id="view-${gem.gem_id}" class="btn btn-success btn-lg" type="submit"><span style="color: rgb(255, 255, 255);">View</span></button>
        </div>
    </div>

    
    
    `;
    /*
    
    // get primary image from s3 database
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
    .catch(error => {
        
        card.querySelector("#gem-image").src = `data:image/png;base64,${data}`;
    });
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

    card.querySelector(`#view-${gem.gem_id}`).addEventListener('click', function() {
        window.location.href = `/gem/${gem.gem_id}`;
    });
    


    return card;
}
export {searchGem};