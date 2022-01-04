function create_comment(profile_id, post_id) {
    const comment_input = document.getElementById(`comment-box-${post_id}`)
    const comment_holder = document.getElementById(`comment-holder-${post_id}`);


    let headers = new Headers();
    headers.append('Accept', 'Application/JSON');
    headers.append('Content-Type', 'Application/JSON');
    headers.append('Authorization', getCookie("access_token"));

    let req = new Request(`/api/v1/comments`, {
        method: 'POST',
        mode: 'cors',
        headers,
        body: JSON.stringify({
            content: comment_input.value,
            profile_id: profile_id,
            post_id: post_id,
        })
    });

    fetch(req)
        .then((res) => res.json())
        .then((data) => {
            let commentElement = update_comment_card(data);
            comment_holder.insertBefore(
                commentElement,
                comment_holder.children[comment_holder.children.length]
            );
            comment_input.value = ""
        })
        .catch((e) => {
            console.error(e);
        });
}

function delete_comment(id) {
    let headers = new Headers();
    headers.append('Accept', 'Application/JSON');
    headers.append('Content-Type', 'Application/JSON');
    headers.append('Authorization', getCookie("access_token"));
    let req = new Request(`/api/v1/comments/${id}`, {
        method: 'DELETE',
        mode: 'cors',
        headers,
    });
    fetch(req)
        .then((res) => res.json())
        .then((data) => {
           let comment_card = document.getElementById(`card-comment-${id}`);
           comment_card.remove()
        })
        .catch((e) => {
            console.error(e);
        });
}
function update_comment_card(data) {
    const innerHTML = `
    <div class="vr"></div>
    <div class="mt-2">
    <div class="d-flex justify-content-between">
        <div class="d-flex align-items-center">
            <img src="${ "http://" + window.location.host + "/static" + data.profile.profile_photo}"
                class="comment-img-post">
            <div class="ms-2">
                <div class="fw-bold my-0" style="font-size: 0.9rem;">
                    ${data.profile.first_name} ${data.profile.last_name}
                </div>
                <div class="text-muted my-0" style="font-size: 0.7rem;">
                    1 sec ago
                </div>
            </div>
        </div>
        <div class="align-self-center">
            <div class="btn-group dropstart">
                <button type="button" style="border: 0; background: none;" data-bs-toggle="dropdown"
                    aria-expanded="false">
                    <i class="fas fa-ellipsis-h"></i>
                </button>
                <ul class="dropdown-menu">
                    <li>
                        <a class="dropdown-item dropdown-edit" href="#">
                            <i class="fas fa-pen-nib"></i> Edit comment
                        </a>
                    </li>
                    <li>
                        <button class="dropdown-item dropdown-delete" onclick="delete_comment(${ data.id })">
                            <i class="fas fa-trash-alt"></i> Delete comment
                        </button>
                    </li>
                </ul>
            </div>
        </div>
        </div>
        <p class="mb-0">${data.content}</p>
    </div>
    <div class="ms-5">
        <div class="vr"></div>
        <div class="d-flex align-items-center mb-2">
            <img src="${ "http://" + window.location.host + "/static" + data.profile.profile_photo}"
                class="reply-img-post">
            <div class="d-flex w-100 px-2">
                <input type="text" name="comment" id="comment-box" class="form-control input-box me-2"
                    style="border-radius: 35px; font-size: 0.8rem;" placeholder="Write a reply..." />
                <button class="btn btn-sm btn-light px-3" type="submit"><i
                        class="fas fa-paper-plane"></i></button>
            </div>
        </div>
    </div>
    `;

    let div = document.createElement("div");
    div.id = `card-comment-${data.id}`
    div.innerHTML = innerHTML;

    return div;
}
