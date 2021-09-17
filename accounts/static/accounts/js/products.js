//Tools
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


// New OOP code

class User {
    constructor() { }

    async fetch(user) {
        let user = await fetch('http://localhost/api/accounts/')
        .then(response => {
            if (!response.ok) {
                throw Error('Couldn\'t fetch user!')
            }
            return response.json()
        })
        .catch(error => {
            console.log(error)
        })

        this.id = user['id']
        this.name = user['user']
    }

    logUser() {
        console.log(this.id)
        console.log(this.name)
    }
}

class Product {
    constructor(user) {
        this.productId = this.getProductId()
        this.user = user
    }

    async fetch() {
        let product = await fetch('http://localhost/api/products/' + this.productId + '/')
        .then(response => {
            if (!response.ok) {
                throw Error('Couldn\'t fetch comments!')
            }
            return response.json()
        })
        .catch(error => {
            console.log(error)
        })

        this.name = product['name']
        this.author = product['author']
        this.desc = product['description']

        this.insertProduct()
    }

    insertProduct() {
        document.querySelector('#product_name').insertAdjacentHTML('beforeend', this.name)
        document.querySelector('#product_author').insertAdjacentHTML('beforeend', this.author)
        document.querySelector('#product_description').insertAdjacentHTML('beforeend', this.desc)

        if (this.author == this.user.name) {
            let element = document.getElementById('product' + this.productId)
            let template = document.getElementById('product_control_template').innerHTML
            
            element.insertAdjacentHTML('beforeend', template)
        }
    }

    getProductId() {
        if(this.productId) {
            return this.productId
        }

        const url = new URL(window.location.href)
        const args = url.pathname.split('/', 3)
        return args[args.length - 1]
    }

    delete() {
        const token = document.querySelector('input[name="csrfmiddlewaretoken"]').getAttribute('value')

        fetch('http://localhost/api/products/' + this.productId, {
            credentials: 'include',
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': token
            }
        })
        .then(response => {
            if (!response.ok) {
                throw Error(`Couldn\'t delete product with id: ${this.productId}\n` + response.statusText)
            }
            const redirect = document.querySelector('#product_delete_redirect').value
            document.location.href = redirect
        })
    }
}

class Comments {
    constructor(user, productId) {
        this.user = user
        this.productId = productId
    }

    async fetch() {
        const json = await fetch('http://localhost/api/comments/?product=' + this.productId)
        .then(response => {
            if (!response.ok) {
                throw Error('Couldn\'t fetch product!')
            }
            return response.json()
        })
        .catch(error => {
            console.log(error)
        })

        this.comments = json.results
        for (const comment of this.comments) {
            this.insertComment(comment)
        }
    }

    insertComment(comment) {
        let element = document.querySelector('#insert_comments')
        let template = document.getElementById('comment_template').innerHTML
        template = template
        .replaceAll('\{comment_id\}', comment.id)
        .replaceAll('\{comment_username\}', comment.account)
        .replaceAll('\{comment_desc\}', comment.comment)

        element.insertAdjacentHTML('beforebegin', template)

        document.getElementById('comment_text' + comment.id).style.display = 'none'

        if (this.user.name == comment.account) {
            let control_template = document.getElementById('comment_control_template').innerHTML
            .replaceAll('\{comment_id\}', comment.id)

            element = document.querySelector('#comment' + comment.id)

            element.insertAdjacentHTML('beforeend', control_template)

            document.getElementById('comment_cancel' + comment.id).style.display = 'none'
            document.getElementById('comment_apply' + comment.id).style.display = 'none'
        }
    }

    delete(commentId) {
        const token = document.querySelector('input[name="csrfmiddlewaretoken"]').getAttribute('value')

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

    create() {
        const text = document.querySelector('#id_comment').value
    
        if (!text.length) {
            return
        }
    
        const token = document.querySelector('input[name="csrfmiddlewaretoken"]').getAttribute('value')
    
        const comment = {
            'product': 'http://localhost/api/products/' + this.productId + '/',
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
            this.insertComment(json)
            document.querySelector('#id_comment').value = ''
        })
        .catch(error => {
            console.log(error)
        })
    }

    edit(commentId) {
        //Change HTML View
        document.getElementById('comment_text' + commentId).style.display = ''
        document.getElementById('comment_delete' + commentId).style.display = 'none'
        document.getElementById('comment_update' + commentId).style.display = 'none'
        document.getElementById('comment_cancel' + commentId).style.display = ''
        document.getElementById('comment_apply' + commentId).style.display = ''
        document.getElementById('comment_desc' + commentId).style.display = 'none'
        //Put text before
        let commentIndex = this.findComment(commentId)
        let comment = this.comments[commentIndex]
        document.getElementById('comment_text' + commentId).value = comment.comment
    }

    cancelEdit(commentId) {
        //Set previous Text
        let commentIndex = this.findComment(commentId)
        let comment = this.comments[commentIndex]
        document.getElementById('comment_desc' + commentId).innerHTML = comment.comment
        //Change HTML View Back
        document.getElementById('comment_text' + commentId).style.display = 'none'
        document.getElementById('comment_delete' + commentId).style.display = ''
        document.getElementById('comment_update' + commentId).style.display = ''
        document.getElementById('comment_cancel' + commentId).style.display = 'none'
        document.getElementById('comment_apply' + commentId).style.display = 'none'
        document.getElementById('comment_desc' + commentId).style.display = ''
    }

    update(commentId) {
        //Get New Text
        let text = document.getElementById('comment_text' + commentId).value
        if (!text.length) {
            return
        }
        //Update Comment (query and this.comments)
        const token = document.querySelector('input[name="csrfmiddlewaretoken"]').getAttribute('value')
    
        const comment = {
            'comment': text,
            'product': 'http://localhost/api/products/' + this.productId + '/'
        }
    
        fetch('http://localhost/api/comments/' + commentId + '/', {
            credentials: 'include',
            method: 'PUT',
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
            document.querySelector('#id_comment').value = ''

            let commentIndex = this.findComment(commentId)
            this.comments[commentIndex].comment = text
            this.cancelEdit(commentId)
        })
        .catch(error => {
            console.log(error)
        })
    }

    findComment(commentId) {
        let index = 0

        for (let comment of this.comments) {
            if (comment.id == commentId) {
                return index
            }
            index += 1
        }
        return undefined
    }
}


var user = new User()
var product = new Product(user)
var comments = new Comments(user, product.getProductId())

async function loadPage() {
    await user.fetch()

    product.fetch()

    comments.fetch()
}

loadPage()