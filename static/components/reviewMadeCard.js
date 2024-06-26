const reviewMade = (review) =>{
    var card = document.createElement('div');
    card.className = 'card';

    function generateStars(rating) {
        let starsHTML = '';
        for (let i = 1; i <= 5; i++) {
            if (i <= rating) {
                // Black star
                starsHTML += `<svg xmlns="http://www.w3.org/2000/svg" width="24px" height="24px" fill="currentColor" viewBox="0 0 16 16" class="bi bi-star-fill fs-1"><path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"></path></svg>`;
            } else {
                // White star
                starsHTML += `<svg xmlns="http://www.w3.org/2000/svg" width="24px" height="24px" fill="currentColor" viewBox="0 0 16 16" class="bi bi-star" style="font-size: 39px;"><path d="M2.866 14.85c-.078.444.36.791.746.593l4.39-2.256 4.389 2.256c.386.198.824-.149.746-.592l-.83-4.73 3.522-3.356c.33-.314.16-.888-.282-.95l-4.898-.696L8.465.792a.513.513 0 0 0-.927 0L5.354 5.12l-4.898.696c-.441.062-.612.636-.283.95l3.523 3.356-.83 4.73zm4.905-2.767-3.686 1.894.694-3.957a.565.565 0 0 0-.163-.505L1.71 6.745l4.052-.576a.525.525 0 0 0 .393-.288L8 2.223l1.847 3.658a.525.525 0 0 0 .393.288l4.052.575-2.906 2.77a.565.565 0 0 0-.163.506l.694 3.957-3.686-1.894a.503.503 0 0 0-.461 0z"></path></svg>`;
            }
        }
        return starsHTML;
    }

    card.innerHTML = `
    <div class="card-body px-4 py-5 px-md-5">
        <div class="row gy-4 row-cols-1 row-cols-md-2 row-cols-xl-3 d-md-flex d-lg-flex justify-content-md-center align-items-md-center justify-content-lg-center">
            <div class="col-md-9 col-lg-10 col-xxl-9 d-xxl-flex flex-fill align-items-xxl-center">
                <div class="container">
                    <div class="row d-xxl-flex justify-content-xxl-center">
                        <div class="col-md-6">
                            <div class="row">
                                <div class="col-md-12">
                                    <div class="text-center">
                                        <a href="/gem/${review.gem_id}" class="hidden-link">
                                            <p class="fw-bold text-success mb-2">Review </p>
                                            <h4 class="fw-bold">${review.gem_name}</h4>
                                            <div id="stars">
                                                ${generateStars(review.rating)}
                                            </div>
                                        </a>
                                    </div>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-md-12">
                                    <div class="card flex-grow-1 flex-fill">
                                        <div class="card-body">
                                            <p class="text-center text-muted d-flex justify-content-center card-text">${review.review}&nbsp;</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-6 col-xxl-3 text-start d-sm-flex d-xxl-flex justify-content-sm-center align-items-md-center align-items-lg-center justify-content-xxl-center align-items-xxl-center" style="padding-top:10px;">
                            <div class="row">
                                <div class="col-md-12 d-flex d-sm-flex d-md-flex d-lg-flex d-xxl-flex justify-content-center justify-content-sm-center justify-content-md-center justify-content-lg-center justify-content-xxl-center" style="padding-top:30px;">
                                    <button id="edit-review-${review.review_id}" class="btn btn-success btn-lg d-lg-flex align-items-lg-center" data-bss-hover-animate="pulse" type="submit" style="background: rgb(68,157,238);"><span style="color: rgb(255, 255, 255);">Edit Review&nbsp;</span>
                                    </button>
                                </div>
                                <div class="col-md-12 d-flex d-sm-flex d-md-flex d-lg-flex d-xxl-flex justify-content-center justify-content-sm-center justify-content-md-center justify-content-lg-center justify-content-xxl-center" style="padding-top:30px;">
                                    <button id="delete-review-${review.review_id}" class="btn btn-success btn-lg d-lg-flex align-items-lg-center" data-bss-hover-animate="pulse" type="submit" style="background: rgb(242,93,83);"><span style="color: rgb(255, 255, 255);">Delete&nbsp;</span>
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    `;

    // Add hover event listeners to buttons for continuous animation
    card.querySelectorAll('button').forEach(button => {
        button.addEventListener('mouseover', () => {
            button.classList.add('animate__animated', 'animate__pulse', 'animate__infinite',"animate__fast");
        });
        button.addEventListener('mouseout', () => {
            button.classList.remove('animate__animated', 'animate__pulse', 'animate__infinite',"animate__fast");
        });
    });

    var viewButton = card.querySelector(`#edit-review-${review.review_id}`);
    viewButton.addEventListener('click', () => {
        window.location.href = `/review/${review.review_id}/edit-review`; // Modify the URL according to your routing logic
    });

    var viewButton = card.querySelector(`#delete-review-${review.review_id}`);
    viewButton.addEventListener('click', () => {

        // Get the CSRF token from the cookie
        let csrf_token = document.cookie.split('; ')  
        .find(row => row.startsWith("csrf_access_token" + '=')) 
        ?.split('=')[1];  

        fetch(`/review/${review.review_id}/delete-review`, {
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
export  { reviewMade };