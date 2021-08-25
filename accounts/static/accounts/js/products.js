//Tools
function getProductId() {
    const url = new URL(window.location.href)
    args = url.pathname.split('/', 3)
    return args[args.length - 1]
}


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


//Comments tools
function insertComment(user, comment) {
    element = document.querySelector('#insert_comments')
    template = document.getElementById('comment_template').innerHTML
    template = template
    .replace('\{comment_id\}', comment['id'])
    .replace('\{comment_username\}', comment['account'])
    .replace('\{comment_desc\}', comment['comment'])

    element.insertAdjacentHTML('beforebegin', template)

    if (user['user'] == comment['account']) {
        control_template = document.getElementById('comment_control_template').innerHTML
        .replaceAll('\{comment_id\}', comment['id'])

        element = document.querySelector('#comment' + comment['id'])

        element.insertAdjacentHTML('beforeend', control_template)
    }
}


function deleteComment(commentId) {
    token = document.querySelector('input[name="csrfmiddlewaretoken"]').getAttribute('value')

    fetch('http://localhost/api/comments/' + commentId, {
        credentials: 'include',
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': token
        }
    })
    .then(response => {
        if (!response.ok) {
            throw Error(`Couldn\'t delete comment with id: ${commentId}\n` + response.statusText)
        }
        document.querySelector('#comment' + commentId).remove()
    })
}


function createComment1() {
    text = document.querySelector('#id_comment').value

    if (text.length == 0 || gUser == undefined) {
        return
    }

    token = document.querySelector('input[name="csrfmiddlewaretoken"]').getAttribute('value')

    comment = {
        'product': 'http://localhost/api/products/' + getProductId() + '/',
        'comment': text
    }

    fetch('http://localhost/api/comments/', {
        credentials: 'include',
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': token
        },
        body: JSON.stringify(comment)
    })
    .then(response => {
        if (!response.ok) {
            throw Error('Couldn\'t POST comment!\n' + response.statusText)
        }
        return response.json()
    })
    .then(json => {
        insertComment(gUser, json)
        document.querySelector('#id_comment').value = ''
    })
    .catch(error => {
        console.log(error)
    })
}


//Product tools
function insertProduct(user, product) {
    document.querySelector('#product_name').insertAdjacentHTML('beforeend', product['name'])
    document.querySelector('#product_author').insertAdjacentHTML('beforeend', product['author'])
    document.querySelector('#product_description').insertAdjacentHTML('beforeend', product['description'])
}


//Fetching
//User
function fetchUser() {
    fetch('http://localhost/api/accounts/')
    .then(response => {
        if (!response.ok) {
            throw Error('Couldn\'t fetch user!')
        }
        return response.json()
    })
    .then(json => {
        userFetched(json)
    })
    .catch(error => {
        console.log(error)
    })
}


//Comments
function fetchComments(user, productId) {
    fetch('http://localhost/api/comments/?product=' + productId)
    .then(response => {
        if (!response.ok) {
            throw Error('Couldn\'t fetch product!')
        }
        return response.json()
    })
    .then(json => {
        for (comment of json.results) {
            insertComment(user, comment)
        }
    })
    .catch(error => {
        console.log(error)
    })
}


//Product
function fetchProduct(user, productId) {
    fetch('http://localhost/api/products/' + productId + '/')
    .then(response => {
        if (!response.ok) {
            throw Error('Couldn\'t fetch comments!')
        }
        return response.json()
    })
    .then(json => {
        insertProduct(user, json)
    })
    .catch(error => {
        console.log(error)
    })
}


//Fetch stuff & Execution
function userFetched(user) {
    gUser = user

    productId = getProductId()

    fetchComments(user, productId)
    fetchProduct(user, productId)
}


var gUser = undefined
fetchUser()